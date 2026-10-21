"""Versjonert registervedlikehold. Ingen år tilbakeprojiseres fra 2027-grunnlaget."""

import hashlib
import json
from bisect import bisect_right
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from .maintenance_store import (
    Diagnostic,
    ImportResult,
    export_basis,
    imported,
    reading,
    reject_large_file,
    save_import,
    writing,
)
from .observations import Organization, encode, identity
from .organization_register import ARTIFACT_SHA256, ENTRIES
from .workfiles import FileLimitError, read_file, write_file

HEADERS = (
    "radtype",
    "eksport_id",
    "forventet_base",
    "nummer",
    "navn",
    "forkortelse",
    "kildenavn",
    "kategori",
    "kapittel",
    "fdep",
    "gdep",
    "gruppenavn",
    "post",
    "fra_ar",
    "til_ar",
    "presisjon",
    "kilde",
    "referanse",
    "begrunnelse",
)


@dataclass(frozen=True)
class DepartmentEntry:
    number: str
    name: str
    abbreviation: str
    source_name: str
    category: str
    valid_from: int
    valid_to: int
    source: str
    reference: str
    reason: str
    precision: str = "år"

    def to_row(self) -> dict[str, str | int]:
        return {
            "nummer": self.number,
            "navn": self.name,
            "forkortelse": self.abbreviation,
            "kildenavn": self.source_name,
            "kategori": self.category,
            **period_row(self),
        }


@dataclass(frozen=True)
class ChapterEntry:
    chapter: str
    department: str
    gdep: str
    group_name: str
    valid_from: int
    valid_to: int
    source: str
    reference: str
    reason: str
    precision: str = "år"

    def to_row(self) -> dict[str, str | int]:
        return {
            "kapittel": self.chapter,
            "fdep": self.department,
            "gdep": self.gdep,
            "gruppenavn": self.group_name,
            **period_row(self),
        }


@dataclass(frozen=True)
class PostEntry:
    chapter: str
    post: str
    valid_from: int
    valid_to: int
    source: str
    reference: str
    reason: str
    precision: str = "år"

    def to_row(self) -> dict[str, str | int]:
        return {"kapittel": self.chapter, "post": self.post, **period_row(self)}


type Entry = DepartmentEntry | ChapterEntry | PostEntry


def period_row(entry: Entry) -> dict[str, str | int]:
    return {
        "fra_ar": entry.valid_from,
        "til_ar": entry.valid_to,
        "presisjon": entry.precision,
        "kilde": entry.source,
        "referanse": entry.reference,
        "begrunnelse": entry.reason,
    }


@dataclass(frozen=True)
class RegisterSnapshot:
    departments: tuple[DepartmentEntry, ...]
    chapters: tuple[ChapterEntry, ...]
    posts: tuple[PostEntry, ...] = ()

    @property
    def id(self) -> str:
        return identity(
            "register-v1",
            *(
                sorted(encode(asdict(e)) for e in group)
                for group in (self.departments, self.chapters, self.posts)
            ),
        )

    def lookup(self, chapter: str | None, year: int | None) -> Organization:
        entry = next(
            (
                e
                for e in self.chapters
                if e.chapter == chapter and year is not None and e.valid_from <= year <= e.valid_to
            ),
            None,
        )
        if entry is None:
            return Organization(null_reason="Ingen eksplisitt kapittelkobling for året")
        dept = next(
            e
            for e in self.departments
            if e.number == entry.department
            and e.valid_from <= entry.valid_from
            and e.valid_to >= entry.valid_to
        )
        special = dept.category == "særkategori"
        return Organization(
            fdep_nr=dept.number,
            gdep_nr=entry.gdep or None,
            gdep_name=entry.group_name,
            mapped_department_code=None if special else dept.number,
            mapped_department_name=None if special else dept.name,
            register_source=f"{entry.source}; {entry.reference}; {entry.reason}",
            register_version=f"register-v1:{self.id}",
            valid_from=str(entry.valid_from),
            valid_to=str(entry.valid_to),
            validity_precision=entry.precision,
            null_reason="Særkategori; ikke ordinært departement"
            if special
            else "Gul bok-gruppe uavklart"
            if not entry.gdep
            else "Kilde-Dep, område og kategori ikke oppgitt",
        )

    def catalogued(self, chapter: str | None, post: str | None, year: int | None) -> bool:
        return any(
            e.chapter == chapter
            and e.post == post
            and year is not None
            and e.valid_from <= year <= e.valid_to
            for e in self.posts
        )


def _decode(data: dict[str, Any]) -> RegisterSnapshot:
    return RegisterSnapshot(
        tuple(DepartmentEntry(**e) for e in data["departments"]),
        tuple(ChapterEntry(**e) for e in data["chapters"]),
        tuple(PostEntry(**e) for e in data["posts"]),
    )


def read_register(database: Path, snapshot_id: str | None) -> RegisterSnapshot:
    with reading(database) as connection:
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE name='register_snapshots'"
        ).fetchone()
        row = (
            connection.execute(
                "SELECT content FROM register_snapshots WHERE id=?", (snapshot_id,)
            ).fetchone()
            if exists
            else None
        )
    if row is None:
        raise ValueError("Ukjent registersnapshot")
    result = _decode(json.loads(row[0]))
    if result.id != snapshot_id:
        raise ValueError("Registerets innholdshash stemmer ikke")
    return result


def read_current_register(database: Path) -> RegisterSnapshot:
    with reading(database) as connection:
        row = connection.execute(
            "SELECT snapshot_id FROM register_heads WHERE singleton=1"
        ).fetchone()
    if row is None:
        raise ValueError("Registeret er ikke initialisert")
    return read_register(database, row[0])


def seed_register(database: Path) -> RegisterSnapshot:
    names = (
        ("1", "Utenriksdepartementet", "UD"),
        ("2", "Kunnskapsdepartementet", "KD"),
        ("3", "Kulturdepartementet", "KUD"),
        ("4", "Justis- og beredskapsdepartementet", "JD"),
        ("5", "Kommunal- og distriktsdepartementet", "KDD"),
        ("6", "Arbeids- og inkluderingsdepartementet", "AID"),
        ("7", "Helse- og omsorgsdepartementet", "HOD"),
        ("8", "Barne- og familiedepartementet", "BFD"),
        ("9", "Nærings- og fiskeridepartementet", "NFD"),
        ("11", "Landbruks- og matdepartementet", "LMD"),
        ("13", "Samferdselsdepartementet", "SD"),
        ("14", "Klima- og miljødepartementet", "KLD"),
        ("15", "Digitaliserings- og forvaltningsdepartementet", "DFD"),
        ("16", "Finansdepartementet", "FIN"),
        ("17", "Forsvarsdepartementet", "FD"),
        ("18", "Energidepartementet", "ED"),
        ("23", "Ymse", "Ymse"),
    )
    snapshot = RegisterSnapshot(
        tuple(
            DepartmentEntry(
                number,
                name,
                short,
                "Kultur- og likestillingsdepartementet" if number == "3" else name,
                "særkategori" if number == "23" else "ordinær",
                2027,
                2027,
                "Brukerens oppsett; docs/departementsregister.md"
                if number != "23"
                else f"Dokumentert filkontroll SHA-256 {ARTIFACT_SHA256}",
                "Navnetabell" if number != "23" else "Data!rad 1077",
                "Startgrunnlag; bare 2027, ingen ny filkontroll",
            )
            for number, name, short in names
        ),
        tuple(
            ChapterEntry(
                e.chapter,
                e.fdep,
                e.gdep,
                e.group,
                2027,
                2027,
                f"Dokumentert filkontroll SHA-256 {ARTIFACT_SHA256}",
                f"Data!rad {e.row}",
                "Tidligere filkontroll; original ikke gjenfunnet",
            )
            for e in ENTRIES
        ),
    )
    with writing(database) as connection:
        connection.execute(
            "INSERT OR IGNORE INTO register_snapshots VALUES (?,?)",
            (snapshot.id, encode(asdict(snapshot))),
        )
        connection.execute("INSERT OR IGNORE INTO register_heads VALUES (1,?)", (snapshot.id,))
    return snapshot


def export_register(database: Path, snapshot_id: str, output: Path) -> str:
    snapshot = read_register(database, snapshot_id)
    identifier = str(uuid4())
    rows = [{"radtype": "grunnlag", "eksport_id": identifier, "forventet_base": snapshot.id}]
    for kind, entries in (
        ("departement", snapshot.departments),
        ("kapittel", snapshot.chapters),
        ("post", snapshot.posts),
    ):
        rows.extend(
            {"radtype": kind, **{k: str(v) for k, v in e.to_row().items()}} for e in entries
        )
    with writing(database) as connection:
        connection.execute(
            "INSERT INTO maintenance_exports VALUES (?,?,?)",
            (identifier, "register", encode({"base": snapshot.id})),
        )
    write_file(
        database,
        output,
        "Register",
        HEADERS,
        rows,
        frozenset(HEADERS) - {"eksport_id", "forventet_base"},
    )
    return identifier


def _code(value: str, maximum: int) -> bool:
    return (
        value.isascii()
        and value.isdigit()
        and str(int(value)) == value
        and 1 <= int(value) <= maximum
    )


def _validate(rows: list[dict[str, str]]) -> tuple[RegisterSnapshot, list[Diagnostic]]:
    errors: list[Diagnostic] = []
    departments: list[DepartmentEntry] = []
    chapters: list[ChapterEntry] = []
    posts: list[PostEntry] = []
    indexed: list[tuple[int, Entry]] = []
    for n, row in enumerate(rows, 3):
        n = int(row.get("__row__", n))

        def fail(field: str, message: str, row_number: int = n) -> None:
            errors.append(Diagnostic("Register", row_number, field, message))

        for field in ("kilde", "referanse", "begrunnelse"):
            if not row[field].strip():
                fail(field, "Må være oppgitt")
        try:
            start, end = int(row["fra_ar"]), int(row["til_ar"])
            if not 1000 <= start <= end <= 9999 or row["presisjon"] != "år":
                raise ValueError
        except ValueError:
            fail("fra_ar/til_ar/presisjon", "Krever fra ≤ til og eksplisitt årspresisjon")
            continue
        common = (start, end, row["kilde"], row["referanse"], row["begrunnelse"], row["presisjon"])
        kind = row["radtype"]
        entry: Entry
        if kind == "departement":
            if not _code(row["nummer"], 999):
                fail("nummer", "Krever positivt normalisert departementsnummer")
            if not all(row[k].strip() for k in ("navn", "forkortelse", "kildenavn")):
                fail("navn/forkortelse/kildenavn", "Krever separate navn og forkortelse")
            if row["kategori"] not in {"ordinær", "særkategori"}:
                fail("kategori", "Velg ordinær eller særkategori")
            if row["nummer"] == "23" and row["kategori"] != "særkategori":
                fail("kategori", "23 Ymse er særkategori")
            entry = DepartmentEntry(
                row["nummer"],
                row["navn"],
                row["forkortelse"],
                row["kildenavn"],
                row["kategori"],
                *common,
            )
            departments.append(entry)
        elif kind == "kapittel":
            if not _code(row["kapittel"], 9999) or not _code(row["fdep"], 999):
                fail("kapittel/fdep", "Krever normaliserte kapittel- og departementskoder")
            if (row["gdep"] and not _code(row["gdep"], 999)) or not row["gruppenavn"].strip():
                fail("gdep/gruppenavn", "Oppgi gruppe eller skriv uavklart uten gruppekode")
            entry = ChapterEntry(
                row["kapittel"], row["fdep"], row["gdep"], row["gruppenavn"], *common
            )
            chapters.append(entry)
        elif kind == "post":
            if not _code(row["kapittel"], 9999) or not _code(row["post"], 99):
                fail("kapittel/post", "Krever normalisert kapittel og post 1–99")
            entry = PostEntry(row["kapittel"], row["post"], *common)
            posts.append(entry)
        else:
            fail("radtype", "Ukjent radtype")
            continue
        indexed.append((n, entry))
    by_department: dict[str, list[DepartmentEntry]] = defaultdict(list)
    for department in departments:
        by_department[department.number].append(department)
    for values in by_department.values():
        values.sort(key=lambda d: d.valid_from)
    starts = {number: [d.valid_from for d in values] for number, values in by_department.items()}
    periods: dict[tuple[str, ...], list[tuple[int, Entry]]] = defaultdict(list)
    for n, entry in indexed:
        if isinstance(entry, ChapterEntry):
            candidates = by_department.get(entry.department, [])
            position = bisect_right(starts.get(entry.department, []), entry.valid_from) - 1
            if position < 0 or candidates[position].valid_to < entry.valid_to:
                errors.append(
                    Diagnostic(
                        "Register", n, "fdep", "Departementet dekker ikke hele kapittelperioden"
                    )
                )

        key = (
            ("departement", entry.number)
            if isinstance(entry, DepartmentEntry)
            else ("post", entry.chapter, entry.post)
            if isinstance(entry, PostEntry)
            else ("kapittel", entry.chapter)
        )
        periods[key].append((n, entry))
    for entries in periods.values():
        previous_end, previous_row = 0, 0
        for n, entry in sorted(entries, key=lambda pair: pair[1].valid_from):
            if entry.valid_from <= previous_end:
                errors.append(
                    Diagnostic("Register", n, "fra_ar/til_ar", f"Overlapp med rad {previous_row}")
                )
            if entry.valid_to > previous_end:
                previous_end, previous_row = entry.valid_to, n
    return RegisterSnapshot(tuple(departments), tuple(chapters), tuple(posts)), errors


def import_register(database: Path, path: Path) -> ImportResult:
    try:
        raw, rows, errors = read_file(path, HEADERS, "Register")
    except FileLimitError:
        return reject_large_file(database, path, "register", "Register")
    sha = hashlib.sha256(raw).hexdigest()
    identifier = identity("registerimport-v1", sha)
    with writing(database) as connection:
        previous = imported(connection, identifier)
        if previous:
            return previous
        snapshot: RegisterSnapshot | None = None
        if not errors:
            try:
                if not rows or rows[0]["radtype"] != "grunnlag":
                    raise ValueError("Første datarad må være eksportert grunnlag")
                base = export_basis(connection, rows[0]["eksport_id"], "register")["base"]
                head = connection.execute(
                    "SELECT snapshot_id FROM register_heads WHERE singleton=1"
                ).fetchone()
                if rows[0]["forventet_base"] != base or not head or head[0] != base:
                    raise ValueError(
                        "Forventet base er endret; eksporter gjeldende register på nytt"
                    )
                snapshot, errors = _validate(rows[1:])
            except ValueError as error:
                errors.append(Diagnostic("Register", 2, "forventet_base", str(error)))
        new: tuple[str, ...] = ()
        reused: tuple[str, ...] = ()
        if not errors and snapshot:
            exists = connection.execute(
                "SELECT 1 FROM register_snapshots WHERE id=?", (snapshot.id,)
            ).fetchone()
            reused, new = ((snapshot.id,), ()) if exists else ((), (snapshot.id,))
            connection.execute(
                "INSERT OR IGNORE INTO register_snapshots VALUES (?,?)",
                (snapshot.id, encode(asdict(snapshot))),
            )
            connection.execute(
                "UPDATE register_heads SET snapshot_id=? WHERE singleton=1", (snapshot.id,)
            )
        result = ImportResult(
            identifier,
            "register",
            new,
            reused,
            tuple(errors),
            snapshot.id if snapshot and not errors else None,
        )
        save_import(connection, result, path, raw, sha)
        return result
