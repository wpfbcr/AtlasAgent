# Markdown → PDF 导出

安装可选依赖：

```bash
python3 -m pip install -r "$ATLAS_ROOT/requirements-pdf.txt"
python3 "$ATLAS_ROOT/scripts/md2pdf.py" itinerary.md
```

支持连续正文、标题、引用、列表、代码和自动换行的表格。表格跨页重复表头；长内容完整保留，不以字符数截断。来源链接的 URL 保留到 PDF 中，饮食标签转换为文字，星级转换为可显示的星号。

字体自动查找 macOS、Linux 和 Windows 的 CJK 字体。可通过 `ATLAS_FONT` 指定 TTF/TTC 文件。TrueType字体最低fpdf2版本为2.8.4；CFF字体（如Noto Sans CJK）要求fpdf2≥2.8.9和Python≥3.10。Python3.9的Linux环境可安装fonts-wqy-zenhei使用TrueType字体；旧 PyFPDF 与 fpdf2 共用导入名，建议使用独立虚拟环境。

限制：不支持内嵌图片或完整 HTML。单行表格内容如果高于整页可用高度，导出会报错，需在源文档拆成多行；不会静默丢弃文字。缺少字形时显示 Unicode 编码占位，便于核查。

验证：检查连续正文、长表格末尾、跨页表头、语义标签和来源链接，再渲染每页查看布局。
