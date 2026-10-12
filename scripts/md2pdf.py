#!/usr/bin/env python3
"""Render Markdown itineraries with wrapped tables, CJK and visible diet labels."""
import argparse
import importlib.metadata
import os
from pathlib import Path
import re
import sys

FONT_CANDIDATES = ['/System/Library/Fonts/Supplemental/Arial Unicode.ttf', '/System/Library/Fonts/PingFang.ttc', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc', 'C:\\Windows\\Fonts\\msyh.ttc']
SYMBOLS = {'🟢': '[符合已知限制]', '🟡': '[需调整并确认]', '🔴': '[含受限成分]', '⚠': '[注意]', '⭐': '★', '✈': '[交通]', '🌤': '[天气]', '🛂': '[签证]', '🎯': '[定位]', '🕐': '[时区]', '🍜': '[美食]', '🏨': '[住宿]', '💰': '[预算]', '📍': '[地点]', '📅': '[日期]', '💱': '[汇率]'}

try:
    if tuple(int(n) for n in importlib.metadata.version('fpdf2').split('.')[:3]) < (2, 8, 4):
        raise ImportError('fpdf2 >= 2.8.4 required')
    from fpdf import FPDF, FontFace
    from fpdf.errors import FPDFException
    from fontTools.ttLib import TTFont
except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
    raise SystemExit('PDF export requires fpdf2 >= 2.8.4: python3 -m pip install -r requirements-pdf.txt') from exc


def find_font():
    configured = os.environ.get('ATLAS_FONT')
    candidates = [configured] if configured else FONT_CANDIDATES
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            with TTFont(candidate, fontNumber=0) as font:
                cff = 'CFF ' in font or 'CFF2' in font
            version = tuple(int(n) for n in importlib.metadata.version('fpdf2').split('.')[:3])
            if cff and version < (2, 8, 9):
                if configured:
                    raise ValueError('CFF fonts require fpdf2 >= 2.8.9 (Python 3.10+); use a TrueType CJK font on Python 3.9')
                continue
            return candidate
    raise ValueError('No CJK font found. Set ATLAS_FONT to a CJK TTF/TTC font or install Noto Sans CJK.')


class MD2PDF(FPDF):
    def __init__(self, title='', font_path=''):
        super().__init__('P', 'mm', 'A4')
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(True, 20)
        self.add_font('C', '', font_path)
        self.add_font('C', 'B', font_path)
        with TTFont(font_path, fontNumber=0) as font:
            self.characters = set(font.getBestCmap())
        self.doc_title = self._clean(title)
        self.set_title(self.doc_title)

    def _clean(self, text):
        for symbol, label in SYMBOLS.items():
            text = text.replace(symbol, label)
        text = text.replace('\ufe0f', '').replace('\ufe0e', '').replace('\u200d', '')
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'(?<!\w)\*([^*]+)\*(?!\w)', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Retain source URLs so the exported artifact remains independently usable.
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('\\|', '|')
        return ''.join(ch if ch in '\n\t' or ord(ch) in self.characters else '[U+{:X}]'.format(ord(ch)) for ch in text)

    def header(self):
        if self.page_no() > 1:
            self.set_font('C', '', 8)
            self.set_text_color(130, 130, 130)
            self.cell(0, 5, self.doc_title, align='C', new_x='LMARGIN', new_y='NEXT')
            self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('C', '', 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, '- {} -'.format(self.page_no()), align='C')

    def paragraph(self, text, size=9.5, indent=0):
        self.set_font('C', '', size)
        self.set_text_color(40, 40, 40)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.epw - indent, 5.5, self._clean(text), new_x='LMARGIN', new_y='NEXT', wrapmode='CHAR')

    def render(self, text):
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith('```'):
                code = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code.append(lines[i])
                    i += 1
                self._code(code)
            elif line.strip().startswith('|'):
                table = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    table.append(lines[i])
                    i += 1
                self._table(table)
                continue
            elif re.fullmatch(r'\s*-{3,}\s*', line):
                self.ln(3)
                self.set_draw_color(190, 190, 190)
                self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
                self.ln(3)
            elif re.match(r'^#{1,6}\s', line):
                match = re.match(r'^(#{1,6})\s+(.+)', line)
                level = len(match[1])
                self.set_font('C', 'B', {1: 18, 2: 13, 3: 11}.get(level, 10))
                self.set_text_color(25, 50, 65)
                # Reserve room for the heading and some following content.
                if self.get_y() + (40 if level <= 2 else 24) > self.page_break_trigger:
                    self.add_page()
                self.ln(3)
                self.multi_cell(0, 7, self._clean(match[2]), new_x='LMARGIN', new_y='NEXT', wrapmode='CHAR')
                self.ln(2)
            elif line.strip().startswith('>'):
                self.paragraph(line.strip().lstrip('> '), size=9, indent=4)
                self.ln(2)
            elif re.match(r'^\s*[-*]\s+', line):
                self.paragraph('- ' + re.sub(r'^\s*[-*]\s+', '', line), indent=4)
            elif re.match(r'^\s*\d+[.)]\s+', line):
                self.paragraph(line.strip(), indent=4)
            elif not line.strip():
                self.ln(2)
            else:
                self.paragraph(line)
            i += 1

    def _code(self, lines):
        self.set_fill_color(245, 245, 245)
        for line in lines:
            self.paragraph(line, size=8, indent=2)
        self.ln(2)

    def _table(self, lines):
        rows = []
        for line in lines:
            body = line.strip()[1:]
            if body.endswith('|'):
                body = body[:-1]
            cells = [cell.strip() for cell in re.split(r'(?<!\\)\|', body)]
            if all(re.fullmatch(r':?-+:?', cell) for cell in cells):
                continue
            rows.append([self._clean(cell) for cell in cells])
        if not rows:
            return
        cols = max(len(row) for row in rows)
        rows = [row + [''] * (cols - len(row)) for row in rows]
        self.set_font('C', '', 8)
        self.set_text_color(40, 40, 40)
        widths = [max(18, min(85, max(self.get_string_width(row[c]) for row in rows))) for c in range(cols)]
        self.set_x(self.l_margin)
        self.ln(2)
        with self.table(col_widths=widths, width=self.epw, line_height=4.5, padding=1.5, text_align='LEFT', wrapmode='CHAR', headings_style=FontFace(emphasis='BOLD', color=(255, 255, 255), fill_color=(35, 70, 85)), cell_fill_color=(242, 247, 249), cell_fill_mode='ROWS', borders_layout='SINGLE_TOP_LINE', repeat_headings=1) as table:
            for row in rows:
                tr = table.row()
                for cell in row:
                    tr.cell(cell)
        self.set_x(self.l_margin)
        self.ln(3)


def convert_file(path, font_path):
    source = Path(path)
    content = source.read_text(encoding='utf-8')
    heading = re.search(r'^#\s+(.+)', content, re.M)
    pdf = MD2PDF(title=heading[1] if heading else source.stem, font_path=font_path)
    pdf.add_page()
    pdf.render(content)
    output = source.with_suffix('.pdf')
    pdf.output(str(output))
    return str(output)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('target', type=Path)
    args = p.parse_args()
    try:
        if args.target.is_dir():
            sources = sorted(args.target.glob('*.md'))
        elif args.target.is_file() and args.target.suffix == '.md':
            sources = [args.target]
        else:
            raise ValueError('Input must be an existing .md file or directory')
        if not sources:
            raise ValueError('No .md files found')
        font_path = find_font()
        for source in sources:
            output = convert_file(source, font_path)
            print('OK {} -> {} ({:.0f} KB)'.format(source, output, Path(output).stat().st_size / 1024))
    except (OSError, ValueError, RuntimeError, FPDFException) as exc:
        print('PDF error: ' + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
