"""Stable data contracts for the Markdown/PDF delivery pipeline."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class DeliveryStatus(str, Enum):
    """The canonical delivery status values from the Research Pack model."""

    MD_READY = "md_ready"
    PDF_READY = "pdf_ready"
    PDF_FAILED = "pdf_failed"
    NOT_RUN = "not_run"


def sha256_file(path: Path | None) -> str | None:
    """Return a file hash without turning missing artifacts into a crash."""

    if path is None or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass
class DeliveryResult:
    """Machine-readable outcome shared by CLI, tests, and audit consumers."""

    input_path: Path
    delivery_status: DeliveryStatus = DeliveryStatus.NOT_RUN
    markdown_status: DeliveryStatus = DeliveryStatus.NOT_RUN
    html_path: Path | None = None
    pdf_path: Path | None = None
    html_sha256: str | None = None
    pdf_sha256: str | None = None
    pdf_size_bytes: int | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    kept_html: bool = False

    @property
    def ok(self) -> bool:
        return not self.errors and self.delivery_status in {
            DeliveryStatus.MD_READY,
            DeliveryStatus.PDF_READY,
        }

    def to_dict(self) -> dict[str, object]:
        """Serialize paths and statuses without exposing non-JSON objects."""

        return {
            "input_path": str(self.input_path),
            "delivery_status": self.delivery_status.value,
            "markdown_status": self.markdown_status.value,
            "html_path": str(self.html_path) if self.html_path else None,
            "pdf_path": str(self.pdf_path) if self.pdf_path else None,
            "html_sha256": self.html_sha256,
            "pdf_sha256": self.pdf_sha256,
            "pdf_size_bytes": self.pdf_size_bytes,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "kept_html": self.kept_html,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
