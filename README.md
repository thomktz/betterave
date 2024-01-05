<img src="https://github.com/thomktz/betterave/assets/82711723/4649d8fd-837b-4be4-93c5-6212d36d7d88" width="200" height="100" alt="betterave-logo">  


_ENSAE année 2023-2024 : Projet Infrastructures et systèmes logiciels_ 

## Table of Contents

- [Introduction](#betterave-pamplemousse-20)
- [Features](#features)
- [Repository Organization](#repository-organization)
- [Database Structure](#database-structure)
- [API Structure](#api-structure)
- [Frontend](#frontend)
- [Code Standards](#code-standards)
- [Deployment](#deployment)
- [Setup for Development](#setup-for-development)
- [Difficulties and Areas for Improvement](#difficulties-and-areas-for-improvement)


## **Better**ave: Pamplemousse 2.0

Betterave is a school management software designed for students and professors at ENSAE. It incorporates the main features of the existing software 'Pamplemousse' but also introduces new functionalities:
- Class schedule  
- Grades
- Photochart 
- **Class groupchats (new)**
- **Homework (new)**
- **Association events (new)**
- **Light/dark theme (new)**



<img width="1200" alt="image" src="https://github.com/thomktz/betterave/assets/60552083/353cdd6b-93d0-4354-9c99-0f1bbd496da7">
<img width="1200" alt="image" src="https://github.com/thomktz/betterave/assets/60552083/fc2ca296-6561-4ae6-9f07-64ac2f41b01e">


## Features

There are 4 types of user profiles in the software, each with different features and restrictions:

- **Student Profile:**
  - View schedule and grades
  - Manage course registrations and check assignments
  - Access the class roster
  - Subscribe to news from student associations at the school

- **Association Profile (managed by a student):**
  - Create events
  - Send notifications to subscribed students

- **Teacher Profile:**
  - View schedule
  - Enter grades
  - Assign homework to students

- **Administrator Profile:**
  - Add or remove users

Here you can find demonstration videos according to the type of users:

[Student demo](https://www.youtube.com/watch?v=zZC0X2hOou0)

[Association demo](https://www.youtube.com/watch?v=YLPqCE9lRXs&feature=youtu.be)

## Repository Organization

The repository is structured into three main directories:
- `backend`: Manages the definition of database structures, API development, and unit tests.
- `frontend`: Encompasses all aspects related to the user interface, including images, web scripts, and other frontend-specific files.
- `scripts`: Dedicated to scripts used for tasks such as generating the virtual environment or other related functionalities.

This organization ensures a clear separation of concerns between the backend and frontend, providing an organized space for frontend components, visual elements, and scripts. 


## Database Stucture

- User Table: Stores user information for the application (type of the user, name, username, email...).
- Grade Table: Stores student grades (student_id, class_id, grade...)
- Class Table: Stores information about a class (teacher,...). Each class has several lessons, groups, and homework.
- Lesson Table: Stores information about the different lessons of a class (date, place...).
- Homework Table: Stores information about homework of a specific class (content, due date...).
- Class_Group Table: Stores information about a specific group of a class (attending students, class_id ...)
- User_Class_Group Table: Stores the relationship between a student and the class that the student subscribed to.
- Group_Enrollment Table: Stores the relationship between a student and the specific class group that the student subscribed to.
- Homework Table: Stores information about a homework (corresponding class, due date, due time...).
- Event Table: Stores information about an event (association, date...).
- Event_Attendance Table: Stores the attending relationship between a student and an event. 

![Relationship diagram of de database](https://github.com/thomktz/betterave/assets/82711723/28393118-e898-405b-9c2a-8fb463c8a8af)

## API Structure 

This application is built using Flask-RESTful, a Flask extension designed to simplify the development of RESTful APIs. Flask-RESTful streamlines the process of creating API endpoints, managing resources, and incorporating RESTful features seamlessly.

### API Scripts Location

All scripts related to the API are centralized in the `backend/app/api` directory. Within this directory, you'll find various subfolders:

- `auth`
- `class_groups`
- `classes`
- `events`
- `lessons`
- `user_class_groups`
- `users`

### Key Files

- `routes.py`: This file contains the route definitions for different API endpoints.
- `models.py`: Here, you'll find the data models used by the application.

This organized structure enhances the clarity and maintainability of the API implementation.

## Frontend

The frontend of this application is built using [Vue.js](https://vuejs.org/), a progressive JavaScript framework. It provides a user-friendly interface for interacting with the backend services.
Within this directory, you'll find two main subfolders:
- `public` (houses logos, photos displayed on the app)
- `src` (houses the Vue scripts, font files, and style configurations that contribute to the frontend functionality and appearance...)


## Code standards 

- **Using Pre-Commit**  
  If you wish to integrate Pre-Commit into your workflow, simply follow these steps:
  - Install Pre-Commit in your Python environment using the following command:
     ```pip install pre-commit```
  - Run the following command to set up Pre-Commit in your repository:
     ```pre-commit install```
  - If you want to manually run hooks on files you've modified and staged, use the command:
      ```pre-commit run```
  - To run hooks across the entire codebase, including all files, use the command:
      ```pre-commit run --all-files```

- **Code review and Pull requests**  
  We encourage collaboration through the use of pull requests (PRs) for proposing changes to the codebase:
  - **Fork the Repo:** Fork the repository to your GitHub account.
  - **Create a Branch:** Start a new branch for your changes.
  - **Make Changes:** Implement your code changes in the branch.
  - **Commit & Push:** Commit changes and push to your fork.
  - **Open a Pull Request:** Propose changes through a pull request.
  - **Code Review:** Team members review and provide feedback.
  - **Address Feedback:** Make necessary changes based on feedback.
  - **Merge:** Once approved, changes are merged.

- **Testing**  
To test the code, execute `pytest` in the source directory. This command will run the unit tests (using pytest) and generate a coverage report. Currently, there are 68 tests coded, all of which have passed successfully.

## Deployment

Docker
Serveur
DNS

## Setup for development

- Install [Docker](https://docs.docker.com/get-docker/).
- Clone the repository.
- Navigate to the root of the repository. (`cd betterave`)
- For local development, you must generate the .env.local by running the script:

```bash
./scripts/generate_local_env.sh
```

- For server deployment, no need to generate the .env.local since the existing .env file will be used.
- Run the following command to start the containers:

```bash
docker compose up --build
```

Or, if you want to run the containers in the background:

```bash
docker compose up --build -d
```

To scrap ENSAE website, run : 
```bash
docker exec -it betterave-backend-1 python -m scripts.scraping
```

To initialize the database, run :
```bash
docker exec -it betterave-backend-1 python -m scripts.init_db
```

To shut down the containers:

```bash
docker compose down
```

And to see the logs,

```bash
docker compose logs
```


## Difficulties and Areas for Improvement 

- Notifications functionnality to be finished








