"""Avgrenset immutable 2027-oppslag; ingen intervall- eller +3000-kobling."""

import hashlib
import json
from dataclasses import dataclass

from .observations import Organization

ARTIFACT_SHA256 = "952757a9964f92a7e2cb1972fcfb6b82b426d4973de641a29fef5ea66d6c1adb"
REGISTER_VERSION = "gul-bok-2027-dokumenterte-oppslag-v1"


@dataclass(frozen=True)
class Entry:
    chapter: str
    fdep: str
    department: str
    gdep: str
    group: str
    row: int


ENTRIES = (
    Entry("1", "15", "Digitaliserings- og forvaltningsdepartementet", "91", "Det kongelige hus", 2),
    Entry("41", "16", "Finansdepartementet", "93", "Stortinget og eksterne organer", 8),
    Entry("2309", "23", "Ymse", "23", "Ymse", 1077),
    Entry("2410", "2", "Kunnskapsdepartementet", "24", "Statsbankene", 1078),
    Entry(
        "2445",
        "15",
        "Digitaliserings- og forvaltningsdepartementet",
        "26",
        "Statens forvaltningsbedrifter",
        1106,
    ),
    Entry("2650", "6", "Arbeids- og inkluderingsdepartementet", "27", "Folketrygden", 1129),
    Entry("5309", "23", "Ymse", "60", "Inntekter under departementene", 1453),
    Entry("5501", "16", "Finansdepartementet", "30", "Skatter og avgifter", 1478),
    Entry("5700", "16", "Finansdepartementet", "57", "Folketrygden", 1584),
)
_snapshot = json.dumps(
    [
        REGISTER_VERSION,
        ARTIFACT_SHA256,
        "2027",
        [(e.chapter, e.fdep, e.department, e.gdep, e.group, e.row) for e in ENTRIES],
    ],
    ensure_ascii=False,
    separators=(",", ":"),
)
REGISTER_SNAPSHOT = hashlib.sha256(_snapshot.encode("utf-8")).hexdigest()


def classify_chapter(chapter: str | None) -> str:
    if chapter is not None and chapter.isascii() and chapter.isdigit():
        number = int(chapter)
        if 1 <= number <= 2999:
            return "utgift"
        if 3000 <= number <= 5999:
            return "inntekt"
        if 6000 <= number <= 9999:
            return "kapitalregnskap"
    return "uavklart"


def lookup(chapter: str | None, year: int | None) -> Organization:
    entry = next((e for e in ENTRIES if e.chapter == chapter), None) if year == 2027 else None
    if entry is None:
        return Organization(
            null_reason="Ingen eksplisitt kapittelkobling med gyldighet for budsjettåret"
        )
    return Organization(
        fdep_nr=entry.fdep,
        gdep_nr=entry.gdep,
        gdep_name=entry.group,
        mapped_department_code=None if entry.fdep == "23" else entry.fdep,
        mapped_department_name=None if entry.fdep == "23" else entry.department,
        register_source=(
            f"docs/departementsregister.md; artefakt SHA-256 {ARTIFACT_SHA256}; "
            f"Data!rad {entry.row}; dokumentert oppslag, originalfil ikke nykontrollert"
        ),
        register_version=f"{REGISTER_VERSION}:{REGISTER_SNAPSHOT}",
        valid_from="2027",
        valid_to="2027",
        validity_precision="år",
        null_reason="Særkategori Ymse; ikke ordinært departement"
        if entry.fdep == "23"
        else "Kilde-Dep, område og kategori ikke oppgitt",
    )
