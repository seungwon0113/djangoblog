from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from contacts.models import Inquiry
from contacts.services import InquiryService


class InquiryView(View):
    def get(self, request):
        return render(request, "contact/contact.html")

    def post(self, request):
        try:
            # Inquiry 객체 생성
            inquiry = Inquiry(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone", ""),
                message=request.POST.get("message"),
            )

            # 문의 생성 및 이메일 발송
            InquiryService.create_inquiry(inquiry)

            # 성공 메시지 추가
            messages.success(
                request,
                "문의가 성공적으로 전송되었습니다. 빠른 시일 내에 답변 드리겠습니다.",
            )
            return redirect("index")

        except Exception as e:
            messages.error(request, str(e))
            return render(request, "contact/contact.html")
