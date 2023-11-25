# Spam Detection System

Spam detection system is a web application developed using Django, providing user registration, authentication, personal contacts, spam detection, and search features.

## Features

1. **User Registration and Authentication:**
   - Users can register with their name, phone number, and an optional email.
   - Phone numbers are unique, and users can log in using their phone numbers and passwords.

2. **Personal Contacts:**
   - Registered users can manage their personal contacts.
   - Each contact can have a name, phone number, and optional email.

3. **Spam Detection:**
   - Users can mark a phone number as spam, helping others identify potential spammers.
   - Spam numbers contain information such as name and email (if available).

4. **Search:**
   - Users can search for people by name or phone number in the global database.
   - Search results display names, phone numbers, and spam likelihood.
   - Clicking a result shows detailed information, including spam likelihood and email (if in the user's contact list).

## Getting Started

### Prerequisites

1. Python: [Download Python](https://www.python.org/downloads/)
2. Django: [Install Django](https://www.djangoproject.com/download/)
3. Other dependencies: Install using `pip install -r requirements.txt`

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/Hriitz/spamDetectionSys.git
   cd spamDetectionSys


2. ```pip install -r requirements.txt```

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

4. Run app using: ```python manage.py runserver```


5. Implemented Swagger-UI for API Testing
   for local Environment it is running at http://127.0.0.1:8000/swagger/
