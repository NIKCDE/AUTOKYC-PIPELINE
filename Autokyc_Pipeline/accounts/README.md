# Automated KYC Pipeline (Django)

A production-style backend system for automating customer identity verification (KYC) in banking and fintech applications.

This project simulates how real financial systems handle:

* Document uploads (ID and selfie)
* OCR-based data extraction
* Background processing
* Identity verification workflows

---

## Features

* Upload ID card and selfie
* Store documents securely using Django media system
* Extract text from ID using OCR (Tesseract)
* Background processing using Celery and Redis
* Track KYC status (Pending, Processing, Verified, Rejected)
* REST API built with Django REST Framework

---

## System Architecture

```
Client (Web / Mobile)
        │
        ▼
Django REST API
        │
        ▼
PostgreSQL Database
        │
        ▼
Redis (Message Broker)
        │
        ▼
Celery Workers
        │
        ▼
OCR Engine (Tesseract)
        │
        ▼
Verification Engine
        │
        ▼
KYC Status Updated
```

---

## Tech Stack

* Backend Framework: Django
* API Layer: Django REST Framework
* Database: PostgreSQL (or SQLite for development)
* Task Queue: Celery
* Message Broker: Redis
* OCR Engine: Tesseract OCR
* Image Processing: Pillow

---

## Project Structure

```
AUTOKYC/
│
├── AUTOKYC/                # Project configuration
├── auto_kyc/              # Main KYC app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── urls.py
│
├── media/                 # Uploaded documents
│   ├── id_cards/
│   └── selfies/
│
├── manage.py
└── requirements.txt
```

---

## Installation Guide

### 1. Clone the Repository

```
git clone https://github.com/your-username/auto-kyc.git
cd auto-kyc
```

---

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Run Migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Start Django Server

```
python manage.py runserver
```

---

## Redis Setup (Required for Background Tasks)

### Option 1 — Docker (Recommended)

```
docker run -d -p 6379:6379 redis
```

---

### Option 2 — Windows (Memurai)

Install Memurai and ensure Redis is running on port 6379.

---

## Start Celery Worker

```
celery -A AUTOKYC worker --loglevel=info
```

---

## API Endpoints

### Upload KYC Documents

```
POST /kyc/upload/
```

Form Data:

* user (int)
* id_image (file)
* selfie_image (file)

---

### Check KYC Status

```
GET /kyc/status/<user_id>/
```

Response Example:

```
{
    "status": "PENDING",
    "submitted_at": "2026-03-25T10:00:00"
}
```

---

## Media Access

Uploaded files are stored in:

```
/media/id_cards/
/media/selfies/
```

Access via browser:

```
http://127.0.0.1:8000/media/<file_path>
```

---

## KYC Status Flow

```
PENDING → PROCESSING → VERIFIED / REJECTED
```

---

## Testing

You can test endpoints using:

* Postman
* Curl
* Django Browsable API

---

## Future Improvements

* Face recognition (selfie vs ID match)
* Fraud detection system
* Integration with government ID APIs
* Email and SMS notification system
* Admin dashboard for manual review

---

## Notes

* This project is for educational purposes
* Not production-ready without:

  * encryption
  * secure storage (e.g., AWS S3)
  * proper authentication (JWT/OAuth)

---

## Author

Nicholas Nyamekey Dadzie

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## License

This project is licensed under the MIT License.
