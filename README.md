Sales Data

A backend system for analyzing large sales datasets with millions of records. The system provides data loading, storage, and analytical capabilities through a RESTful API.

Features
- Efficient CSV data loading into normalized database
- Daily automated data refresh
- Revenue analysis by product/category/region
- Top products identification
- Customer behavior metrics
- RESTful API for all functionality

Prerequisites
- Python 3.10
- PostgreSQL 17
- Redis 6+

Technologies Used
- Backend: Django 4.2, Django REST Framework
- Database: PostgreSQL
- Task Queue: Celery with Redis
- API Documentation: OpenAPI (through DRF)

Setup Instructions

1. Clone the Repository

```bash
git clone https://github.com/saransaran46/lumel_backend_developer_assessment.git
cd .\backend_assessment\

2. SETUP Environment
python -m venv venv
source venv/bin/activate  --> On Windows: venv\Scripts\activate

3. Intall the Requirements.txr file

Using This Command -->  pip install -r requirements.txt

4. Setup Database in your local system postgresql pgadmin

Set the username and password that is related to your local database username and password

5. Migrate the data

Using this command --> python manage.py makemigrations
after the above step --> python manage.py migrate

6. Run the server

Using this command --> python manage.py runserver
