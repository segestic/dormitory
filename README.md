## Hostel Managment System

# Dormitory Management System - Django Setup Guide

## Prerequisites
- Python 3.x installed on your system
- Docker (if using Docker)
- Basic knowledge of Django

## Setup with Docker

### 1. Clone the project repository to your local machine.
    ```
    git clone ...
    ```

### 2. Navigate to the project directory.
    ```
    cd dormitory
    ```

### 3. Create a `.env` file in the project directory by renaming the .env.example and fill in your variables

### 4. Open a terminal or command prompt and navigate to the project directory. 

### 5. Run the following command to start the Docker containers:

docker-compose up

### 6. Django will be accessible at http://localhost:8000.

## Setup with Virtual Environment

### Clone the project repository to your local machine.
    ```
    git clone ....
    ```

### Navigate to the project directory.
    ```
    cd dormitory
    ```
### Create a virtual environment by running the following command:
    ```
    python3 -m venv venv
    ```
    
### Activate the virtual environment:
- On macOS and Linux:
  ```
  source env/bin/activate
  ```
- On Windows:
  ```
  .\env\Scripts\activate
  ```

## Install the required dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```


## Apply the database migrations by running the following command:
    ```
    python manage.py migrate
    ```


## Apply the database migrations by running the following command:
    ```
    python manage.py migrate
    ```


## Collect static files
    ```
    python manage.py collectstatic
    ```


## Create superuser
python manage.py createsuperuser


## Start the Django development server by running the following command:
python manage.py runserver


Dormitory App will be accessible at http://localhost:8000.



