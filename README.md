# Phone-Book-API

A RESTful API for managing contacts in a phone book application, built with FastAPI and MySQL, containerized using
Docker and Docker Compose.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Metrics and Monitoring](#metrics-and-monitoring)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- CRUD Operations: Create, Read, Update, and Delete contacts.
- Search Functionality: Search contacts by phone number, first name, last name, or address.
- Input Validation: Ensures phone numbers are valid and fields meet specified criteria.
- Metrics Endpoint: Exposes Prometheus metrics for monitoring.
- API Documentation: Interactive documentation with Swagger UI.
- Dockerized: Easily deployable using Docker and Docker Compose.

## Requirements

- Docker
- Docker Compose

## Installation

### Clone the Repository

```bash
git clone https://github.com/orbad/phonebook_api.git
cd phonebook_api
```

### Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```dotenv
# .env
# Database Configuration
MYSQL_DATABASE=phonebook_db
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=rootpassword

# SQLAlchemy Database URL
DATABASE_URL=mysql+pymysql://user:password@db:3306/phonebook_db
```

Replace `user`, `password`, and `rootpassword` with your desired credentials.

## Configuration

- **Docker Compose**: The `docker-compose.yml` file defines the services:
    - `db`: MySQL database
    - `api`: FastAPI application
    - `prometheus` (optional): For metrics collection
    - `grafana` (optional): For visualization
- **Prometheus Configuration**: The `prometheus/prometheus.yml` file configures Prometheus to scrape metrics from the
  API.

## Running the Application

### Build and Run Services

```bash
docker-compose up --build
```

### Access the API

The API will be available at `http://localhost:8000`

### Access API Documentation

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Access Metrics

Metrics are exposed at `http://localhost:8000/metrics`

### Access Grafana Dashboard (Optional)

Grafana is available at `http://localhost:3000`

## API Documentation

### Endpoints

#### Create a Contact

- **URL**: `POST /contacts/`
- **Description**: Create a new contact.
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "address": "123 Main St"
  }
  ```

#### Get All Contacts

- **URL**: `GET /contacts/`
- **Description**: Retrieve a list of contacts.
- **Query Parameters**:
    - `offset`: Pagination offset (default: 0)
    - `limit`: Pagination limit (default: 10)

#### Search Contacts

- **URL**: `GET /contacts/search`
- **Description**: Search for contacts by various criteria.
- **Query Parameters**:
    - `phone_number`
    - `first_name`
    - `last_name`
    - `address`

#### Update a Contact

- **URL**: `PUT /contacts/{phone_number}`
- **Description**: Update an existing contact.
- **Path Parameter**:
    - `phone_number`: The phone number of the contact to update.
- **Request Body**:
  ```json
  {
    "first_name": "Jane",
    "last_name": "Doe",
    "address": "456 Elm St"
  }
  ```

#### Delete a Contact

- **URL**: `DELETE /contacts/{phone_number}`
- **Description**: Delete a contact.
- **Path Parameter**:
    - `phone_number`: The phone number of the contact to delete.

## Metrics and Monitoring

- **Prometheus Metrics**: Exposed at `http://localhost:8000/metrics`
- **Grafana Dashboard**:
    - URL: `http://localhost:3000`
    - Default Credentials: `admin` / `admin`
    - Add Prometheus as a data source to visualize metrics.

## Testing

### Running Tests

#### Install Dependencies

Ensure you have the required Python packages installed.

```bash
pip install -r requirements.txt
```

#### Run Tests

```bash
pytest tests/
```

### Test Coverage

The tests cover the main functionalities of the API, including creating, reading, updating, and deleting contacts.

## Project Structure

```
phonebook_api/
├── app/
│   ├── main.py
│   ├── Dockerfile
│   ├── models/
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── crud/
│   │   └── contact.py
│   └── db/
│       ├── session.py
│       ├── Dockerfile
│       └── database_phonebook.sql
│    
├── tests/
│   └── test_contacts.py
├── prometheus/
│   └── prometheus.yml
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```
