import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def pybo_filter(value):
    extensions = [
        "markdown.extensions.fenced_code",  # 코드 펜스 지원 (```로 감싸진 코드 블록)
        "markdown.extensions.codehilite",  # 코드 하이라이팅
        "markdown.extensions.tables",  # 테이블 지원
        "markdown.extensions.nl2br",  # 줄바꿈 지원
        "markdown.extensions.sane_lists",  # 리스트 지원
    ]

    # 백틱(`)을 HTML 엔티티로 변환
    value = value.replace("'''", "```")

    # 마크다운 변환
    md = markdown.Markdown(extensions=extensions)
    html = md.convert(value)

    return mark_safe(html)
