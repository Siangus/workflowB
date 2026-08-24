"""Extract EPUB chapter content into auditable Markdown source packs."""
from __future__ import annotations

import argparse
import html
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


class TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)


def clean_html(raw: str) -> str:
    parser = TextParser()
    parser.feed(raw)
    lines: list[str] = []
    for value in parser.parts:
        value = html.unescape(value).replace("\u00a0", " ")
        value = re.sub(r"[ \t]+", " ", value).strip()
        if value:
            lines.append(value)
    return "\n".join(lines)


def chapter_number(href: str) -> int | None:
    match = re.search(r"(?:ch|chapter)(\d+)", href, re.IGNORECASE)
    return int(match.group(1)) if match else None


def ncx_chapters(raw: bytes) -> list[tuple[int, str, str]]:
    root = ElementTree.fromstring(raw)
    chapters: list[tuple[int, str, str]] = []
    for point in root.iter():
        label_node = next((child for child in point if child.tag.endswith("navLabel")), None)
        label = "".join(label_node.itertext()) if label_node is not None else None
        content = next((child.attrib.get("src", "") for child in point if child.tag.endswith("content")), "")
        match = re.search(r"Chapter\s+(\d+):?\s*(.*)", label or "", re.IGNORECASE)
        if match and content:
            chapters.append((int(match.group(1)), (match.group(2) or "").strip(), content.split("#", 1)[0]))
    return chapters


def extract(epub: Path, output_dir: Path, book_id: str, title: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(epub) as archive:
        names = set(archive.namelist())
        opf_name = "EPUB/content.opf" if "EPUB/content.opf" in names else next(name for name in names if name.endswith(".opf"))
        opf = ElementTree.fromstring(archive.read(opf_name))
        namespaces = {"opf": "http://www.idpf.org/2007/opf"}
        manifest = {item.attrib["id"]: item.attrib["href"] for item in opf.findall("opf:manifest/opf:item", namespaces)}
        spine = [item.attrib["idref"] for item in opf.findall("opf:spine/opf:itemref", namespaces)]

        grouped: dict[int, list[str]] = {}
        chapter_titles: dict[int, str] = {}
        for idref in spine:
            href = manifest.get(idref, "")
            number = chapter_number(href)
            if number is None:
                continue
            matching = next((name for name in names if name.endswith(href.replace("../", ""))), None)
            if matching:
                grouped.setdefault(number, []).append(matching)

        if not grouped:
            ncx_name = next((name for name in names if name.endswith(".ncx")), None)
            if ncx_name:
                for number, chapter_title, href in ncx_chapters(archive.read(ncx_name)):
                    matching = next((name for name in names if name.endswith(href.replace("../", ""))), None)
                    if matching:
                        grouped[number] = [matching]
                        chapter_titles[number] = chapter_title

        output_lines = [f"# {title}", "", f"- **book_id:** `{book_id}`", f"- **source_epub:** `{epub}`", "", "## Source Map", ""]
        source_map: list[dict[str, object]] = []
        for number in sorted(grouped):
            chapter_start = len(output_lines) + 1
            chapter_files = grouped[number]
            chapter_title = f"Chapter {number}: {chapter_titles.get(number, '')}".rstrip(": ")
            chapter_texts: list[str] = []
            for filename in chapter_files:
                text = clean_html(archive.read(filename).decode("utf-8", "replace"))
                chapter_texts.append(text)
                title_match = re.search(rf"(?:Chapter|CHAPTER)\s+{number}\.?(.*?)(?:\n|$)", text, re.IGNORECASE)
                if title_match and title_match.group(1).strip():
                    chapter_title = f"Chapter {number}: {title_match.group(1).strip()}"
            output_lines.extend([f"## {chapter_title}", "", f"<!-- source files: {', '.join(chapter_files)} -->", ""])
            for text in chapter_texts:
                output_lines.extend(text.splitlines())
                output_lines.append("")
            chapter_end = len(output_lines)
            source_map.append({"chapter": number, "title": chapter_title, "files": chapter_files, "start_line": chapter_start, "end_line": chapter_end})

        output_lines.extend(["## Extracted Source Map", "", "| Chapter | Title | Lines | Original EPUB entries |", "|---:|---|---:|---|"])
        for item in source_map:
            output_lines.append(f"| {item['chapter']} | {item['title']} | {item['start_line']}-{item['end_line']} | {', '.join(item['files'])} |")
        destination = output_dir / "extracted-book.md"
        destination.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
        (output_dir / "epub-source-map.json").write_text(__import__("json").dumps({"book_id": book_id, "title": title, "source_epub": str(epub), "chapters": source_map}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epub", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--book-id", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    extract(Path(args.epub), Path(args.output_dir), args.book_id, args.title)


if __name__ == "__main__":
    main()
