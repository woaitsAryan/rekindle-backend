# Rekindle Backend

This is the backend service for the Rekindle application. It's built with FastAPI and uses PostgreSQL as the database.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Docker installed on your machine to run the service.

### Installing

1. Clone the repository
2. Copy `.env.sample` to `.env` and fill in the necessary environment variables
3. Run `docker compose up` to start the service

## API Endpoints

The service has the following endpoints:

- `/auth`: Handles authentication related operations
- `/journal`: Handles operations related to journal entries
