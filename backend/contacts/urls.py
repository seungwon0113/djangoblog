from django.urls import path

from contacts.views import InquiryView

app_name = "contacts"

urlpatterns = [
    path("", InquiryView.as_view(), name="contact_inquiry"),
]
