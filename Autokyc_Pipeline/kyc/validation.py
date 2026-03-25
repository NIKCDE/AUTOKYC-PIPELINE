def validate_documents(kyc_session):
    docs = kyc_session.documents.all()
    has_id = any(doc.doc_type == 'ID' for doc in docs)
    has_selfie = any(doc.doc_type == 'SELFIE' for doc in docs)
    errors = []
    if not has_id:
        errors.append("Missing ID document")
    if not has_selfie:
        errors.append("Missing Selfie")
    return errors