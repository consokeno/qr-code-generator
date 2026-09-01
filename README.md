# QR Code Generator

A Flask web application for generating, saving, and managing QR codes (links, Wi-Fi, contacts, text). Users can create QR codes, view them on a personal dashboard, and administrators can view/manage all codes.

## Requirements

- Docker
- Docker Compose

No local Python installation is required — the app and database both run in containers.

## Project Structure

```

codemain.py                  # Flask application
dockerfile                   # App container definition
requirements.txt             # Python dependencies
02_source_code/              # HTML templates
03_database/                 # SQL schema and seed data
04_docker/
   1-3_docker-compose.yml   # Compose file (app + PostgreSQL)
```

## How to Run

1. Clone the repository:
   ```
   git clone https://github.com/consokeno/qr-code-generator.git

   ```

1.2 Download docker:
 ```
https://www.docker.com/
 ```
2. Start the app and database by starting a command prompt in folder:
   ```
   cd 04_docker
   docker compose -f 1-3_docker-compose.yml up -d
   ```

3. Open the app in your browser:
   ```
   http://localhost:5000

   ```


To stop the containers(app):
```
docker compose -f 1-3_docker-compose.yml down
```

## Demo Accounts

The database has two test accounts you may add more in 03_database/1-3_seed_data.sql:

| Role          | Email                  | Password   |
| Administrator | admin@example.local    | admin123   |
| User          | user@example.local     | user123    |

## Features

- Public QR code generator (no login required)
- User login and session-based authentication
- Dashboard listing saved QR codes with search by title
- Create, view, and delete QR codes
- Administrators can view and manage all users' QR codes

## Configuration

The Flask app reads these environment variables (set in `1-3_docker-compose.yml`):

- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — Flask session secret key

## Ports

- `5000` — Flask app
- `5432` — PostgreSQL

## Tech Stack

- Python / Flask
- Flask-SQLAlchemy, Flask-Login
- PostgreSQL 15
- qrcode + Pillow (QR image generation)
- Bootstrap 5 (UI)
- Docker / Docker Compose
