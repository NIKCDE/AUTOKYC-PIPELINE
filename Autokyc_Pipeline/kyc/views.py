from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Customer
from kyc.models import KYCSession
from documents.models import Document
from kyc.services import run_kyc_pipeline
from kyc.models import KYCAuditLog
from rest_framework.generics import ListAPIView
from rest_framework import serializers

class CreateKYCSessionView(APIView):
    #Create customer + KYC session
    def post(self, request):
        customer = Customer.objects.create(
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            date_of_birth=request.data.get("date_of_birth"),
            email=request.data.get("email"),
        )
        kyc_session = KYCSession.objects.create(customer=customer)
        return Response({
            "kyc_id": kyc_session.id,
            "message": "KYC session created"
        }, status=status.HTTP_201_CREATED)


class UploadDocumentView(APIView):
    # Upload ID / Selfie
    def post(self, request, kyc_id):
        kyc_session = KYCSession.objects.get(id=kyc_id)
        doc = Document.objects.create(
            kyc_session=kyc_session,
            doc_type=request.data.get("doc_type"),
            file=request.FILES.get("file")
        )
        return Response({
            "message": "Document uploaded"
        })


class RunKYCView(APIView):
    def post(self, request, kyc_id):
        kyc_session = KYCSession.objects.get(id=kyc_id)
        result = run_kyc_pipeline(kyc_session)
        return Response(result)
    


class AuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCAuditLog
        fields = '__all__'

class KYCLogListView(ListAPIView):
    serializer_class = AuditSerializer

    def get_queryset(self):
        kyc_id = self.kwargs.get("kyc_id")
        return KYCAuditLog.objects.filter(kyc_session_id=kyc_id).order_by('-created_at')