from .validation import validate_documents
from .ocr import extract_id_data
from .matching import match_customer_data
from .risk_engine import calculate_risk
from .face_verification import verify_face
from .audit import log_action
def run_kyc_pipeline(kyc_session):
    customer = kyc_session.customer
    docs = kyc_session.documents.all()
    #  Validation
    errors = validate_documents(kyc_session)
    # Get ID document
    id_doc = next((doc for doc in docs if doc.doc_type == 'ID'), None)
    extracted_data = {}
    match_score = 0
    if id_doc:
        #OCR
        extracted_data = extract_id_data(id_doc)
        #Matching
        match_score = match_customer_data(customer, extracted_data)
    #Risk calculation
    risk_score = calculate_risk(errors, match_score)
    #Decision
    if risk_score >= 70:
        status = "REJECTED"
    elif risk_score >= 40:
        status = "REVIEW"
    else:
        status = "APPROVED"
    #Save results
    kyc_session.risk_score = risk_score
    kyc_session.status = status
    kyc_session.save()

    return {
        "status": status,
        "risk_score": risk_score,
        "match_score": match_score,
        "errors": errors,
        "extracted_data": extracted_data
    }



def run_kyc_pipeline(kyc_session):
    customer = kyc_session.customer
    docs = kyc_session.documents.all()
    # Validation
    errors = validate_documents(kyc_session)
    id_doc = next((doc for doc in docs if doc.doc_type == 'ID'), None)
    selfie_doc = next((doc for doc in docs if doc.doc_type == 'SELFIE'), None)
    extracted_data = {}
    match_score = 0
    face_result = {}
    # OCR + Matching
    if id_doc:
        extracted_data = extract_id_data(id_doc)
        match_score = match_customer_data(customer, extracted_data)

    # FACE VERIFICATION
    if id_doc and selfie_doc:
        face_result = verify_face(id_doc.file.path, selfie_doc.file.path)

        if not face_result.get("verified"):
            errors.append("Face mismatch")
    # Risk calculation
    risk_score = calculate_risk(errors, match_score)
    # Decision
    if risk_score >= 70:
        status = "REJECTED"
    elif risk_score >= 40:
        status = "REVIEW"
    else:
        status = "APPROVED"

    kyc_session.risk_score = risk_score
    kyc_session.status = status
    kyc_session.save()

    return {
        "status": status,
        "risk_score": risk_score,
        "match_score": match_score,
        "face_verified": face_result.get("verified"),
        "errors": errors,
    }

    from .audit import log_action

def run_kyc_pipeline(kyc_session):
    customer = kyc_session.customer
    docs = kyc_session.documents.all()

    log_action(kyc_session, "PIPELINE_STARTED")

    # Validation
    errors = validate_documents(kyc_session)
    log_action(kyc_session, "VALIDATION_COMPLETED", data={"errors": errors})

    id_doc = next((doc for doc in docs if doc.doc_type == 'ID'), None)
    selfie_doc = next((doc for doc in docs if doc.doc_type == 'SELFIE'), None)

    extracted_data = {}
    match_score = 0
    face_result = {}

    # OCR
    if id_doc:
        extracted_data = extract_id_data(id_doc)
        log_action(kyc_session, "OCR_COMPLETED", data=extracted_data)

        match_score = match_customer_data(customer, extracted_data)
        log_action(kyc_session, "DATA_MATCHED", data={"match_score": match_score})

    # Face Verification
    if id_doc and selfie_doc:
        face_result = verify_face(id_doc.file.path, selfie_doc.file.path)

        log_action(kyc_session, "FACE_VERIFICATION", data=face_result)

        if not face_result.get("verified"):
            errors.append("Face mismatch")

    # Risk
    risk_score = calculate_risk(errors, match_score)
    log_action(kyc_session, "RISK_CALCULATED", data={"risk_score": risk_score})

    # Decision
    if risk_score >= 70:
        status = "REJECTED"
    elif risk_score >= 40:
        status = "REVIEW"
    else:
        status = "APPROVED"

    kyc_session.risk_score = risk_score
    kyc_session.status = status
    kyc_session.save()

    log_action(kyc_session, "FINAL_DECISION", data={"status": status})

    return {
        "status": status,
        "risk_score": risk_score,
        "match_score": match_score,
        "face_verified": face_result.get("verified"),
        "errors": errors,
    }