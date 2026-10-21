"""Ny, atomisk JSON-fil. Databasens kilde-/kontrollgrunnlag overskrives aldri."""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from innlesning.workfiles import safe_output


def publish_text(database: Path, output: Path, text: str) -> None:
    safe_output(database, output)
    if output.exists():
        raise ValueError("Rapport krever ny fil; eksisterende mål overskrives ikke")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with NamedTemporaryFile(dir=output.parent, suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(text.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        if os.name == "nt":
            os.rename(temporary, output)
        else:
            os.link(temporary, output)
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)
