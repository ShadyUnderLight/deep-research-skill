"""Composable Markdown/PDF delivery primitives."""

from .models import DeliveryResult, DeliveryStatus


def run_delivery(*args, **kwargs):
    """Lazily import the pipeline to keep the Markdown facade acyclic."""

    from .pipeline import run_delivery as _run_delivery

    return _run_delivery(*args, **kwargs)

__all__ = ["DeliveryResult", "DeliveryStatus", "run_delivery"]
