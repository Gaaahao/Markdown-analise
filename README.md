# Markdown-analise
none

一个用于统计 Markdown 文档基础指标的小工具。

## 功能

- 统计标题数量（`#` 到 `######`，基于去除 fenced code 后的正文）
- 统计普通链接数量（不含图片语法本身，但如 `[![alt](img.png)](url)` 这类外层链接会计入）
- 统计图片数量
- 统计围栏代码块数量（支持 ```` ``` ```` 和 `~~~`）
- 统计正文词数（排除 fenced code；按空白切分 token）

## 使用方式

```python
from markdown_analise import analyze_markdown

md = "# Hello\n\nThis is a [link](https://example.com)."
stats = analyze_markdown(md)
print(stats)
```

返回值是 `MarkdownStats` 数据类。

## 测试

```bash
pytest -q
```
