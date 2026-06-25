#!/usr/bin/env python3
"""Convert Markdown travel itineraries to PDF with CJK support.

Usage:
  python3 md2pdf.py examples/tokyo-7days-zh.md
  python3 md2pdf.py examples/          # convert all .md in directory

Requires: pip3 install fpdf2
"""

from fpdf import FPDF
import re
import os
import sys

FONT_SIZE = 9.5
LINE_HEIGHT = 5.5

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "C:\\Windows\\Fonts\\msyh.ttc",
]


def find_font() -> str:
    for path in FONT_CANDIDATES:
        if os.path.isfile(path):
            return path
    raise SystemExit("No CJK font found. Install Noto Sans CJK or use macOS/Windows system fonts.")


class MD2PDF(FPDF):
    def __init__(self, title="", font_path=""):
        super().__init__("P", "mm", "A4")
        self.add_font("C", "", font_path)
        self.add_font("C", "B", font_path)
        self.set_auto_page_break(True, 20)
        self.doc_title = title

    def header(self):
        if self.page_no() > 1:
            self.set_font("C", "", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 5, self.doc_title, align="C")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("C", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"- {self.page_no()} -", align="C")

    def render(self, text):
        lines = text.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]

            if re.match(r"^---+$", line.strip()):
                y = self.get_y()
                self.set_draw_color(200, 200, 200)
                self.line(15, y, 195, y)
                self.ln(6)
                i += 1
                continue

            if line.strip().startswith("```"):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                i += 1
                self._code(code_lines)
                continue

            if "|" in line and line.strip().startswith("|"):
                table_lines = []
                while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                    table_lines.append(lines[i])
                    i += 1
                self._table(table_lines)
                continue

            h = re.match(r"^(#{1,6})\s+(.+)$", line)
            if h:
                level = len(h.group(1))
                title = h.group(2).strip()
                sizes = {1: 20, 2: 15, 3: 12, 4: 10.5, 5: 10, 6: 10}
                self.set_font("C", "B", sizes.get(level, 10))
                self.set_text_color(30, 30, 30)
                if level <= 2:
                    self.ln(3)
                self.multi_cell(0, 6.5, title)
                self.ln(2)
                if level == 1:
                    self.set_draw_color(60, 60, 60)
                    self.line(15, self.get_y(), 195, self.get_y())
                    self.ln(4)
                i += 1
                continue

            if line.strip().startswith(">"):
                self.set_font("C", "", 9)
                self.set_text_color(100, 100, 100)
                self.set_x(20)
                self.multi_cell(170, 5, line.strip().lstrip("> "))
                self.ln(1)
                i += 1
                continue

            li = re.match(r"^(\s*)[-*]\s+(.+)$", line)
            num_li = re.match(r"^(\s*)\d+[.)]\s+(.+)$", line)
            if li or num_li:
                content = li.group(2) if li else num_li.group(2)
                self.set_font("C", "", 9)
                self.set_text_color(50, 50, 50)
                self.set_x(20)
                bullet = chr(8226) if li else chr(8212)
                self.cell(5, 5, bullet)
                self.multi_cell(165, 5, self._clean(content))
                i += 1
                continue

            if not line.strip():
                self.ln(3)
                i += 1
                continue

            self.set_font("C", "", FONT_SIZE)
            self.set_text_color(40, 40, 40)
            self.multi_cell(0, LINE_HEIGHT, self._clean(line))
            i += 1

    def _code(self, lines):
        self.ln(2)
        self.set_fill_color(245, 245, 245)
        self.set_font("C", "", 8)
        self.set_text_color(80, 80, 80)
        for cl in lines:
            self.set_x(17)
            self.cell(176, 4.5, cl[:120], fill=True)
            self.ln()
        self.ln(3)

    def _table(self, lines):
        self.ln(2)
        rows = []
        for l in lines:
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if not re.match(r"^[\s\-:]+$", "".join(cells)):
                rows.append(cells)
        if not rows:
            return

        cols = len(rows[0])
        col_w = 176 / cols
        self.set_font("C", "", 7.5)

        for ri, row in enumerate(rows):
            if ri == 0:
                self.set_fill_color(50, 50, 50)
                self.set_text_color(255, 255, 255)
                self.set_font("C", "B", 7.5)
            else:
                shade = 245 if ri % 2 == 0 else 255
                self.set_fill_color(shade, shade, shade)
                self.set_text_color(40, 40, 40)
                self.set_font("C", "", 7.5)

            for ci, cell in enumerate(row[:cols]):
                self.set_x(17 + ci * col_w)
                self.cell(col_w - 1, 5.5, cell[:45], fill=True)
            self.ln()
        self.set_text_color(40, 40, 40)
        self.ln(4)

    def _clean(self, text):
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"`([^`]+)`", r"\1", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"<[^>]+>", "", text)
        return re.sub(r"\s+", " ", text).strip()


def convert_file(path: str, font_path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    title = os.path.splitext(os.path.basename(path))[0]
    pdf = MD2PDF(title=title, font_path=font_path)
    pdf.add_page()
    pdf.render(content)
    out = path.replace(".md", ".pdf")
    pdf.output(out)
    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 md2pdf.py <file.md|directory>")
        sys.exit(1)

    target = sys.argv[1]
    font_path = find_font()

    if os.path.isfile(target):
        if not target.endswith(".md"):
            raise SystemExit("Input must be a .md file")
        out = convert_file(target, font_path)
        size = os.path.getsize(out) / 1024
        print(f"OK  {target}  ->  {out}  ({size:.0f} KB)")
        return

    if not os.path.isdir(target):
        raise SystemExit(f"Not found: {target}")

    files = sorted(f for f in os.listdir(target) if f.endswith(".md"))
    if not files:
        print(f"No .md files in {target}")
        return

    for f in files:
        path = os.path.join(target, f)
        out = convert_file(path, font_path)
        size = os.path.getsize(out) / 1024
        print(f"OK  {f}  ->  {os.path.basename(out)}  ({size:.0f} KB)")
    print(f"Done. {len(files)} file(s) converted.")


if __name__ == "__main__":
    main()
