"""Reproduce the PDF's complete embedded-image inventory without network access."""

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path

from pypdf import PdfReader

PACK = Path(__file__).resolve().parent
ROOT = PACK.parents[2]


def inventory(output_images=None):
    raw = gzip.decompress((PACK / "originals/prop108-full-pdf-a1.hop0.gz").read_bytes())
    reader = PdfReader(io.BytesIO(raw))
    rows = []
    if output_images is not None:
        output_images.mkdir(parents=True, exist_ok=True)
    for page_number, page in enumerate(reader.pages, 1):
        for index, image in enumerate(page.images):
            data = image.data
            filename = f"page-{page_number:03d}-{index}.jpg"
            if output_images is not None:
                (output_images / filename).write_bytes(data)
            rows.append(
                {
                    "pdf_page_1based": page_number,
                    "image_index": index,
                    "image_name": image.name,
                    "image_bytes": len(data),
                    "image_sha256": hashlib.sha256(data).hexdigest(),
                    "derived_filename": filename,
                    "appendix": 1 if page_number < 76 else 2,
                    "figure_ordinal": page_number - (10 if page_number < 76 else 76),
                }
            )
    return {
        "schema": "c06-embedded-image-inventory-1",
        "source": "originals/prop108-full-pdf-a1.hop0.gz",
        "pdf_sha256": hashlib.sha256(raw).hexdigest(),
        "pdf_pages": len(reader.pages),
        "extraction": (
            "pypdf 6.10.0 page.images[].data; derived JPEGs are reproducible from the full PDF. "
            "These are not additional HTTP observations or a claim of HTML-JPEG byte identity."
        ),
        "images": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", type=Path)
    parser.add_argument("--write-inventory", action="store_true")
    args = parser.parse_args()
    result = inventory(args.images)
    if args.write_inventory:
        (PACK / "appendix-image-inventory.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    print(json.dumps({"pdf_pages": result["pdf_pages"], "embedded_images": len(result["images"])}))


if __name__ == "__main__":
    main()
