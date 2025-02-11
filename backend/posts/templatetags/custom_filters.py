import re

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
        "markdown.extensions.extra",  # 추가 확장 기능
        "markdown.extensions.toc",  # 목차 지원
        "markdown.extensions.meta",  # 메타데이터 지원
    ]

    extension_configs = {
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
            "use_pygments": False,  # Pygments 비활성화
            "noclasses": True,  # 인라인 스타일 사용
        }
    }

    # 이미지 태그 처리
    def handle_images(text):
        # 마크다운 이미지 문법 찾기
        pattern = r"!\[(.*?)\]\((.*?)\)"

        def replace_image(match):
            alt_text = match.group(1)
            image_url = match.group(2)
            # 모든 이미지 URL을 반응형 이미지 태그로 변환
            if image_url.startswith("http") or image_url.startswith("/media/"):
                return f'<img src="{image_url}" alt="{alt_text}" class="img-fluid rounded" style="max-height: 300px; width: auto;">'
            return match.group(0)

        return re.sub(pattern, replace_image, text)

    # 이미지 태그 처리
    value = handle_images(value)

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
    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
    html = md.convert(value)

    return mark_safe(html)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)


@register.filter
def get_first_image(content):
    # 업로드된 이미지 URL 패턴
    media_pattern = r"!\[.*?\]\(/media/[^)]+\)"
    # 외부 이미지 URL 패턴
    url_pattern = r"!\[.*?\]\(https?://[^)]+\)"

    # 모든 이미지 마크다운 문법 찾기
    all_images = re.findall(f"{media_pattern}|{url_pattern}", content)

    if all_images:
        # 첫 번째 이미지의 URL 추출
        first_image = all_images[0]
        url_match = re.search(r"\((.*?)\)", first_image)
        if url_match:
            return url_match.group(1)
    return None
