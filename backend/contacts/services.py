import logging

from django.conf import settings
from django.core.mail import send_mail

from contacts.models import Inquiry

logger = logging.getLogger(__name__)


class InquiryService:
    @staticmethod
    def create_inquiry(inquiry: Inquiry):
        inquiry.save()
        InquiryService.send_inquiry_email(inquiry)

    @staticmethod
    def send_inquiry_email(inquiry: Inquiry):
        try:
            action =  "접수"
            subject = f"[Slog] 새로운 문의가 {action}되었습니다."
            message = f"""
안녕하세요, Slog 관리자님

새로운 문의가 {action}되었습니다.

▶ 문의 정보
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 문의번호: {inquiry.id}
• 이름: {inquiry.name}
• 이메일: {inquiry.email}
• 전화번호: {inquiry.phone or '미입력'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

▶ 문의 내용
{inquiry.message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 메일은 자동으로 발송되었습니다.
"""

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            logger.info(f"이메일 발송 성공: 문의번호 {inquiry.id} ({action})")

        except Exception as e:
            logger.error(f"이메일 발송 실패: {str(e)}")
            raise
