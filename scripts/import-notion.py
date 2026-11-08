#!/usr/bin/env python3
"""
Importe un export Notion (Markdown & CSV, "Include subpages") dans
src/content/docs d'un projet Astro Starlight.

- Retire les ID hex que Notion ajoute aux noms de fichiers/dossiers
- Slugifie (minuscules, tirets, sans accents)
- Ajoute un frontmatter Starlight minimal si absent
- Copie les images/fichiers joints référencés et réécrit les liens

Usage :
    python3 scripts/import-notion.py "<dossier export Notion>" "<dossier cible docs>"

Exemple :
    python3 scripts/import-notion.py ~/Downloads/"Notion GEII" src/content/docs
"""
from __future__ import annotations

import re
import shutil
import sys
import unicodedata
from pathlib import Path

NOTION_ID_RE = re.compile(r"\s+[0-9a-fA-F]{32}$")  # "Mon TP 1a2b3c...32hex"
NOTION_ID_PARENS_RE = re.compile(r"\s*\([0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\)$")
IMG_LINK_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def strip_notion_id(name: str) -> str:
    stem_no_ext = name
    ext = ""
    if "." in name and not name.endswith("."):
        stem_no_ext, dot, extpart = name.rpartition(".")
        ext = "." + extpart
    stem_no_ext = NOTION_ID_RE.sub("", stem_no_ext)
    stem_no_ext = NOTION_ID_PARENS_RE.sub("", stem_no_ext)
    return stem_no_ext.strip() + ext


def slugify(name: str) -> str:
    name = strip_notion_id(name)
    stem = name
    ext = ""
    if "." in name and not name.endswith("."):
        stem, _, extpart = name.rpartition(".")
        ext = "." + extpart
    nfkd = unicodedata.normalize("NFKD", stem)
    ascii_only = nfkd.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only).strip("-").lower()
    return (slug or "page") + ext.lower()


def make_frontmatter(title: str) -> str:
    safe_title = title.replace('"', "'")
    return f'---\ntitle: "{safe_title}"\nstatut: a-relire\n---\n\n'


def has_frontmatter(text: str) -> bool:
    return text.lstrip().startswith("---")


def display_title(stem: str) -> str:
    return stem.replace("-", " ").strip().capitalize()


def process_tree(src_root: Path, dst_root: Path) -> tuple[int, int]:
    md_count = 0
    asset_count = 0
    dst_root.mkdir(parents=True, exist_ok=True)

    # 1. Construit la correspondance ancien nom -> nouveau slug pour tout le sous-arbre,
    #    pour pouvoir réécrire les liens relatifs ensuite.
    rename_map: dict[Path, Path] = {}
    for path in src_root.rglob("*"):
        rel = path.relative_to(src_root)
        new_parts = [slugify(p) if path.is_dir() or path == path else p for p in rel.parts]
        new_rel = Path(*[slugify(p) for p in rel.parts])
        rename_map[rel] = new_rel

    # 2. Copie les fichiers non-markdown (images, PDF, etc.) tels quels sous leur nouveau nom
    for path in src_root.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(src_root)
        new_rel = rename_map[rel]
        dst_path = dst_root / new_rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() == ".md":
            continue  # traité séparément ci-dessous
        shutil.copy2(path, dst_path)
        asset_count += 1

    # 3. Traite les fichiers Markdown : ajoute frontmatter, réécrit les liens d'images
    for path in src_root.rglob("*.md"):
        rel = path.relative_to(src_root)
        new_rel = rename_map[rel]
        dst_path = dst_root / new_rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        text = path.read_text(encoding="utf-8", errors="ignore")

        def rewrite_link(m: re.Match) -> str:
            alt, link = m.group(1), m.group(2)
            if link.startswith(("http://", "https://")):
                return m.group(0)
            link_path = Path(link.split("#")[0])
            new_link = slugify(link_path.name)
            return f"![{alt}]({new_link})"

        text = IMG_LINK_RE.sub(rewrite_link, text)

        if not has_frontmatter(text):
            title = display_title(new_rel.stem)
            text = make_frontmatter(title) + text

        dst_path.write_text(text, encoding="utf-8")
        md_count += 1

    return md_count, asset_count


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    src = Path(sys.argv[1]).expanduser().resolve()
    dst = Path(sys.argv[2]).expanduser().resolve()

    if not src.is_dir():
        print(f"Dossier source introuvable : {src}")
        sys.exit(1)

    md_count, asset_count = process_tree(src, dst)
    print(f"Terminé : {md_count} pages Markdown et {asset_count} fichiers copiés vers {dst}")
    print("Vérifie ensuite : npm run build")


if __name__ == "__main__":
    main()
