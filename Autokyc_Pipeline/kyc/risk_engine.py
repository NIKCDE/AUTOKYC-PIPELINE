def calculate_risk(validation_errors, match_score):
    risk_score = 0
    risk_score += len(validation_errors) * 20
    if match_score < 50:
        risk_score += 40
    elif match_score < 80:
        risk_score += 20

    return risk_score