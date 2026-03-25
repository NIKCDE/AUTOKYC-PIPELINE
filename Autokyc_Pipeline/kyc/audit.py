from kyc.models import KYCAuditLog

def log_action(kyc_session, action, message="", data=None):
    KYCAuditLog.objects.create(
        kyc_session=kyc_session,
        action=action,
        message=message,
        data=data or {}
    )