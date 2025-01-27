import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def pybo_filter(value):
    extensions = [
        "markdown.extensions.fenced_code",  # 코드 펜스 지원
        "markdown.extensions.codehilite",  # 코드 하이라이팅
        "markdown.extensions.tables",  # 테이블 지원
        "markdown.extensions.nl2br",  # 줄바꿈 지원
        "markdown.extensions.sane_lists",  # 리스트 지원
    ]

    # 다이어그램 코드 블록 처리
    lines = value.split("\n")
    in_mermaid = False
    processed_lines = []

    for line in lines:
        if line.strip() == "```mermaid":
            in_mermaid = True
            processed_lines.append('<div class="mermaid">')
        elif line.strip() == "```" and in_mermaid:
            in_mermaid = False
            processed_lines.append("</div>")
        else:
            processed_lines.append(line)

    value = "\n".join(processed_lines)

    # 마크다운 변환
    md = markdown.Markdown(extensions=extensions)
    html = md.convert(value)

    return mark_safe(html)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)
