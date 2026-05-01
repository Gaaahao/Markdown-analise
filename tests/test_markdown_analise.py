from markdown_analise import MarkdownStats, analyze_markdown


def test_analyze_markdown_counts_core_elements() -> None:
    content = """# Title

Some paragraph with a [link](https://example.com) and ![img](x.png).

## Subtitle

```python
print('hello')
```

Final line.
"""

    assert analyze_markdown(content) == MarkdownStats(
        headings=2,
        links=1,
        images=1,
        code_blocks=1,
        words=11,
    )


def test_unclosed_code_fence_does_not_crash() -> None:
    content = """# T

text before
```
no close
"""
    stats = analyze_markdown(content)
    assert stats.headings == 1
    assert stats.code_blocks == 0
    assert stats.words == 3


def test_does_not_count_markdown_inside_fenced_code() -> None:
    content = """```markdown
# Not heading
[not link](https://example.com)
![not image](x.png)
```
"""
    assert analyze_markdown(content) == MarkdownStats(
        headings=0,
        links=0,
        images=0,
        code_blocks=1,
        words=0,
    )


def test_image_link_counts_as_both_image_and_link() -> None:
    content = "[![alt](image.png)](https://example.com)"
    stats = analyze_markdown(content)
    assert stats.images == 1
    assert stats.links == 1


def test_supports_tilde_fenced_code_blocks() -> None:
    content = """~~~python
print('x')
~~~
"""
    stats = analyze_markdown(content)
    assert stats.code_blocks == 1
    assert stats.words == 0
