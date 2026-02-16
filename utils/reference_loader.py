"""Load built-in guide references and combine with uploaded references."""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict

from .file_extraction import extract_text_from_path


def load_builtin_guides(base_dir: Path) -> List[Dict[str, str]]:
    guides = []
    guide_dir = base_dir / "assets" / "guides"
    for filename in ["conversation_guide.pdf", "clinician_guide.pdf"]:
        guide_path = guide_dir / filename
        if guide_path.exists():
            try:
                text = extract_text_from_path(guide_path)
                guides.append(
                    {
                        "id": f"builtin-{filename}",
                        "title": filename,
                        "text": text,
                        "length": len(text),
                    }
                )
            except Exception:
                continue
    return guides


def merge_references(builtin: List[Dict[str, str]], uploaded: List[Dict[str, str]]) -> str:
    texts = [ref["text"] for ref in builtin] + [ref["text"] for ref in uploaded]
    # Simple truncation to keep prompt size reasonable
    return "\n\n".join(texts)[:6000]
