# Markdown → PDF 转换

AtlasAgent 行程导出为可打印 PDF。

## 依赖

```bash
pip3 install fpdf2
```

## 字体

| 平台 | 路径 |
|------|------|
| macOS | `/System/Library/Fonts/Supplemental/Arial Unicode.ttf` |
| Linux | `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` |
| Windows | `C:\Windows\Fonts\msyh.ttc` |

脚本自动检测可用字体。

## 用法

```bash
python3 ~/AtlasAgent/scripts/md2pdf.py examples/tokyo-7days-zh.md
python3 ~/AtlasAgent/scripts/md2pdf.py examples/
```

## 支持格式

- `#` 标题层级
- 表格（交替行底色）
- 列表、引用、代码块
- 粗体/链接（链接转为纯文本）

## 限制

- Emoji 可能不渲染（非关键）
- 不支持内嵌图片
- 表格单元格 >45 字符截断
