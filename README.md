# Internal Menu Selection

[![forgather made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Getting started

- In this project, we are using the below mentioned version for the python
```sh
Python 3.8
```
- To start with the project, just run the following command in your virtual environment to get all the necessary packages
```sh
pip install -r requirements.txt
```

- After installing all the packages, we need to now migrate the models. So run the below command to migrate all of the models
```sh
python3 manage.py makemigrations
python3 manage.py migrate
```

## Add Configurations to `.env` file in root directory
```sh
SECRET_KEY=YOUR_SECRET_KEY
DATABASE_NAME=YOUR_DATABASE_NAME
DATABASE_USER=YOUR_DATABASE_USER
DATABASE_PASS=YOUR_DATABASE_PASSWORD
DATABASE_HOST=YOUR_DATABASE_HOST
```

## Run Project

```shell
python manage.py runserver
```

- To run any api mentioned in the urls, first of all we need to add the prefix in each and every url
- For the project you have to write the initial prefix in url as:
```sh
http://127.0.0.1:8000/api/v1/{ANY_API_URL}
```
- This will not allow you to access any API, if the authenticated person has the permissions.

## Overview of the project

- As the project is of menu selection, we have implemented it by using the **RBAC(ROLE BASED ACCESS CONTROL)** which allows only those users who have the permission to access specific operations. 
- So, we have made a running script for the implementation for the project named **add_permissions.py** in **users** module. It will create a **Super User**, necessary roles and all the permissions required for the different roles. So to run the file, write the below code in terminal
```sh
python manage.py runscript add_permissions
```
- Basically, there are 3 roles defined within, which includes: Admin, Restaurant_owner and Employee
- So, every role has been initialized with the permissions which are necessary for the authenticated user.
- Now the system will work accordingly as the permissions are granted to each user.
- Any time, the admin has the right to withdraw any permission from anyone. So, the code has been implemented dynamically by adding or removing any role or any permission.
- Every day, a menu will be uploaded and user will vote on that and then it will display the result of the votes as voted by the user.


## Project Description

- Currently, in the project, there are 4 modules namely: **Role**, **Users**, **Vote** and **Restaurant**
- Role module is for performing the operations on roles
- User module is for the operation on employees
- Vote module includes the vote related operations
- Restaurant module possesses the section of food items, menu and restaurant features.
- Only admin can add employee or restaurant owner
- Restaurant owner can perform the CRUD operation on the restaurant or the food items
- Employee can only view the food item or menu
- Everyday different restaurant owner can upload their own menu
- Then, the employee will vote for that particular day's menu
- Afterwards, the result of the voting is listed in the system

## Testing

- For testing all the test cases, run below command
```sh
pytest
```

- It will run all the test cases.


## Docker Implementation

- For the docker implementation, you have to just run the below commands

```sh
docker-compose build
docker-compose up
docker-compose exec db psql -U postgres -d postgres -c "create database internal_menu_selection;"
```

- It will complete the setup for the docker and the app will be dockerized.