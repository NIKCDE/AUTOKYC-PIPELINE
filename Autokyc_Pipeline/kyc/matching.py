def match_customer_data(customer, extracted_data):
    score = 0

    full_name = f"{customer.first_name} {customer.last_name}".upper()

    if full_name == extracted_data.get("full_name"):
        score += 50

    if str(customer.date_of_birth) == extracted_data.get("dob"):
        score += 50

    return score  # out of 100