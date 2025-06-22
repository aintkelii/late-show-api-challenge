# Late Show API Challenge

A RESTful API built with Flask to manage a Late Night TV show system, featuring user authentication, guest and episode management, and appearance tracking. The API uses PostgreSQL for data storage, JWT for secure authentication, and is tested with Postman. It follows an MVC architecture for modularity and maintainability, built as part of a coding challenge to demonstrate backend development skills.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Author](#author)

## Overview

The Late Show API Challenge is a backend application designed to manage a late-night TV show’s operations. It allows users to register and log in with JWT authentication, view guests and episodes, create appearances linking guests to episodes, and delete episodes (authenticated users only). The API uses Flask for routing, PostgreSQL with Flask-SQLAlchemy for data persistence, and Flask-Migrate for schema management. A seed script populates the database with sample data, and a Postman collection is provided for testing all endpoints.

## Features

- **User Authentication:** Register and log in users with secure JWT tokens.
- **Guest Management:** Retrieve a list of guests with their names and occupations.
- **Episode Management:** List episodes, retrieve episode details with appearances, and delete episodes (authenticated).
- **Appearance Management:** Create appearances with ratings, linking guests to episodes (authenticated).
- **Database Management:** PostgreSQL with Flask-SQLAlchemy and Flask-Migrate for robust data handling.
- **Data Seeding:** Seed script to initialize the database with sample users, guests, episodes, and appearances.
- **API Testing:** Postman collection for comprehensive endpoint testing.

## Technologies

- Python: 3.10
- Flask: Web framework for API development
- Flask-SQLAlchemy: ORM for PostgreSQL integration
- Flask-Migrate: Database schema migrations
- Flask-JWT-Extended: JWT-based authentication
- PostgreSQL: Relational database
- psycopg2-binary: PostgreSQL adapter for Python
- python-dotenv: Environment variable management
- Postman: API testing tool
- Git: Version control

## Project Structure

late-show-api-challenge/
├── .env.example # Template for environment variables
├── .gitignore # Git ignore patterns
├── challenge-4-lateshow.postman_collection.json # Postman test collection
├── README.md # Project documentation (you are here)
├── requirements.txt # Python dependencies
├── server/ # API source code
│ ├── init.py # Package initialization
│ ├── app.py # Flask application setup
│ ├── config.py # Configuration settings
│ ├── seed.py # Database seed script
│ ├── models/ # Database models
│ │ ├── init.py
│ │ ├── appearance.py # Appearance model
│ │ ├── episode.py # Episode model
│ │ ├── guest.py # Guest model
│ │ ├── user.py # User model
│ ├── controllers/ # Route handlers
│ │ ├── init.py
│ │ ├── appearance_controller.py
│ │ ├── auth_controller.py
│ │ ├── episode_controller.py
│ │ ├── guest_controller.py
└── migrations/ # Database migration files

markdown
Copy

## Setup Instructions

### Prerequisites

- Python 3.10
- PostgreSQL (version 14 or later recommended)
- Postman (for API testing)
- Git
- Ubuntu or compatible Linux distribution

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Trev-our/late-show-api-challenge.git
   cd late-show-api-challenge
Set Up Virtual Environment

bash
Copy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Install PostgreSQL (if not installed)

bash
Copy
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
Configure PostgreSQL

Log in to PostgreSQL:

bash
Copy
sudo -u postgres psql
Set a password for the postgres user:

sql
Copy
\password postgres
Create the database:

sql
Copy
CREATE DATABASE late_show_db;
\q
Configure Environment Variables

Copy the example environment file:

bash
Copy
cp .env.example .env
Edit .env with your PostgreSQL credentials and secure keys:

plaintext
Copy
FLASK_APP=server.app
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
SQLALCHEMY_DATABASE_URI=postgresql://postgres:your-password@localhost:5432/late_show_db
Generate secure keys:

bash
Copy
python -c "import secrets; print(secrets.token_hex(16))"
Initialize the Database

bash
Copy
export PYTHONPATH=$PYTHONPATH:$(pwd)
flask db init
flask db migrate -m "initial migration"
flask db upgrade
python server/seed.py
Run the API

bash
Copy
flask run
The API will be available at http://localhost:5000.

API Endpoints
Endpoint Methods and Description
/register POST: Register a new user

/login POST: Log in and receive JWT token

/guests GET: List all guests

/episodes GET: List all episodes

/episodes/<id> GET: Get episode details with appearances

/episodes/<id> DELETE: Delete an episode

/appearances POST: Create a new appearance (authenticated)

Authentication
Register: Creates a user with a hashed password (stored as VARCHAR(256)).

Login: Returns a JWT token for authenticated requests.

Protected Routes: Require Authorization: Bearer <token> header for POST /appearances and DELETE /episodes/<id>.

Example Requests
Register
http
Copy
POST http://localhost:5000/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "testpass123"
}
Response: 201 Created

json
Copy
{
  "message": "User registered successfully"
}
Login
http
Copy
POST http://localhost:5000/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
Response: 200 OK

json
Copy
{
  "access_token": "<jwt-token>"
}
Get Guests
http
Copy
GET http://localhost:5000/guests
Response: 200 OK

json
Copy
[
  {"id": 1, "name": "John Doe", "occupation": "Actor"},
  {"id": 2, "name": "Jane Smith", "occupation": "Comedian"}
]
Create Appearance (Authenticated)
http
Copy
POST http://localhost:5000/appearances
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "rating": 3,
  "guest_id": 1,
  "episode_id": 1
}
Response: 201 Created

json
Copy
{
  "message": "Appearance created successfully"
}
Testing with Postman
Import Collection
Open Postman and import challenge-4-lateshow.postman_collection.json.

Set Up Environment
Create a Postman environment named Late Show API with:

base_url: http://localhost:5000

token: (leave blank initially)

Select the Late Show API environment in Postman.

Test Endpoints
Run requests in order:

POST /register: Register a new user (e.g., testuser).

POST /login: Log in as admin/password123 and save the access_token as token.

GET /guests: Verify guest list.

GET /episodes: Verify episode list.

GET /episodes/1: Verify episode details.

POST /appearances: Create an appearance (uses token).

DELETE /episodes/1: Delete an episode (uses token).

If DELETE removes data, re-run python server/seed.py to restore it.

Troubleshooting
Flask Server Errors: Check logs in debug mode (FLASK_ENV=development flask run), verify .env configuration, and reinstall dependencies if needed (pip install --force-reinstall ...).

Database Issues: Verify PostgreSQL status (sudo systemctl status postgresql), check database connection (psql -U postgres -d late_show_db), and rebuild the database if necessary (flask db ...).

Contributing
Contributions are welcome! To contribute:

Fork the repository.

Create a feature branch:

bash
Copy
git checkout -b feature/your-feature
Commit changes:

bash
Copy
git commit -m "Add your feature"
Push to your fork:

bash
Copy
git push origin feature/your-feature
Open a pull request with a clear description of your changes.

Please follow the coding style and include tests for new features.

License
This project is licensed under the MIT License.

Contact
For questions or feedback, contact:

GitHub: https://github.com/Trev-our/late-show-api-challenge.git

Author
George Keli