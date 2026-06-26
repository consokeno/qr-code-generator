# 1-3 Database Design

## Required Database Objects

The student must prepare a relational database schema for this project.

## Minimum Common Tables

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS qr_codes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(120) NOT NULL,              
    qr_type VARCHAR(50) NOT NULL,             
    content TEXT NOT NULL,                    
    status VARCHAR(50) NOT NULL DEFAULT 'active', 
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Project-specific Tables

The student must add project-specific tables for: QR Code Generator.

Examples of required modelling decisions:

- Identify the main entity of the application.
- Identify supporting entities.
- Add foreign keys.
- Add indexes for searchable fields.
- Add status fields where workflow is required.
- Add timestamps to important tables.

## Required Deliverables

- Entity relationship description.
- SQL schema file.
- Seed data file.
- Short explanation of each table.
- Screenshot proving that the database runs in Docker.
