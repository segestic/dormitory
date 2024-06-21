## Hostel Managment System


https://github.com/segestic/dormitory/assets/50618702/698f67ae-0b07-4eab-a3af-ce5b8029ca53


# Dormitory Management System - Django Setup Guide

## Prerequisites
- Python 3.x installed on your system
- Docker (if using Docker)
- Basic knowledge of Django

## Setup with Docker (OPTION 1)

### 1. Clone the project repository to your local machine.
    
    git clone https://github.com/segestic/dormitory.git
    

### 2. Navigate to the project directory.
    
    cd dormitory
    
### 3. Create a `.env` file in the project directory by renaming the .env.example and fill in your variables


### 4. Open a terminal or command prompt and navigate to the project directory. 


### 5. Run the following command to start the Docker containers:

    docker-compose up

### 6. Django will be accessible at http://localhost:7070.




## Setup with Virtual Environment (OPTION 2)

### Clone the project repository to your local machine.
    
    git clone https://github.com/segestic/dormitory.git
    

### Navigate to the project directory.
    
    cd dormitory
    
### Create a virtual environment by running the following command:
    
    python3 -m venv env
    
    
### Activate the virtual environment:
- On macOS and Linux:
  
  source env/bin/activate
  
- On Windows:
  
  .\env\Scripts\activate
  

## Install the required dependencies by running the following command:
    
    pip install -r requirements.txt
    


## Apply the database migrations by running the following command:
    
    python manage.py migrate
    
    

## Collect static files
    
    python manage.py collectstatic
    


## Create superuser
    python manage.py createsuperuser


## Start the Django development server by running the following command:
    python manage.py runserver


Dormitory App will be accessible at http://localhost:8000.



