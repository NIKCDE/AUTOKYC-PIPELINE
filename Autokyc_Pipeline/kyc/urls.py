from django.urls import path
from .views import CreateKYCSessionView, KYCLogListView, UploadDocumentView, RunKYCView
urlpatterns = [
    path('create/', CreateKYCSessionView.as_view()),
    path('<int:kyc_id>/upload/', UploadDocumentView.as_view()),
    path('<int:kyc_id>/run/', RunKYCView.as_view()),
    path('<int:kyc_id>/logs/', KYCLogListView.as_view()),
]