# Roster Django API

This is the Python/Django implementation of the Roster API, ported from the original Laravel codebase.

## Prerequisites

- **Python**: 3.9+
- **Django**: 4.2.28
- **Database**: MySQL

## Setup and Installation

### 1. Clone the repository
```bash
git clone https://github.com/CHIRANTAN1455/api.py.joinroster.co.git
cd api.py.joinroster.co
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory based on the following template:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 3. Setup Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Server

Once the virtual environment is activated and dependencies are installed, start the development server:

```bash
python manage.py runserver 8000
```
Or use the direct path to the venv interpreter:
```bash
./venv/bin/python3 manage.py runserver 8000
```

## API Documentation

The project includes integrated Swagger and Redoc documentation:

- **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **Redoc**: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
- **OpenAPI Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

## Features

- **Standardized Responses**: Using a custom `ApiResponse` helper.
- **Terminal Visualization**: Custom middleware for color-coded request logging.
- **Automated Documentation**: Powered by `drf-spectacular`.
