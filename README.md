# betterave
*Projet Infrastructures et systèmes logiciels*



## Setup

- Clone the repository.


**Backend**  
- From there, go into the `backend` folder on the terminal (`cd backend`)
- Install poetry in your base environment (`pip install poetry`)
Package management is done with poetry. To add a new dependency, run `poetry add <package_name>`, then commit the changes made to the `pyproject.toml` and `poetry.lock` files to the repo.
- Install the dependencies with `poetry install`
- Activate the virtual environment with `poetry shell`

You can now run scripts using
`python -m scripts.init_db` 
`python -m scripts.add_student`
etc.

- Run the frontend: python main.py

**Frontend**
- Install Node.js
- Go into the `frontend` folder on the terminal (`cd frontend` or `cd ../frontend` if you're in the backend folder)
- Install the dependencies with `npm install`
- Run the frontend: `npm run serve` 

## Folder structure
```
betterave/
│
├── backend/                           # Backend server and API code     
│   ├── app/                           # Main application directory
│   │   ├── models/                    # SQLAlchemy models
│   │   │   ├── class_.py
│   │   │   ├── event.py  
│   │   │   ├── lesson.py 
│   │   │   ├── message.py 
│   │   │   ├── notification.py 
│   │   │   ├── relationship_tables.py 
│   │   │   └── user.py   
│   │   ├── operations/                # Database operations
│   │   │   ├── asso_operations.py 
│   │   │   ├── class_operations.py 
│   │   │   ├── event_operations.py 
│   │   │   ├── lesson_operations.py 
│   │   │   ├── message_operations.py 
│   │   │   ├── student_operations.py 
│   │   │   └── user_operations.py 
│   │   └── routes/                    # API routes
│   │       ├── api_routes.py 
│   │       └── auth_routes.py 
│   ├── create_app.py                  # Flask app factory
│   ├── extensions.py                  # Flask version of packages
│   ├── main.py                        # Main file to run the backend
│   ├── poetry.lock 
│   ├── pyproject.toml 
│   ├── scripts/                       # Scripts to perform DB operations
│   │   ├── add_class.py 
│   │   ├── add_user.py 
│   │   ├── display_user.py 
│   │   └── init_full_db.py 
│   └── tests/                         # Unit tests
│       └── test_operations.py 
│
├── frontend/                   
│   ├── public/                        # Static files
│   │   ├── photos/
│   │   └── ...
│   ├── src/
│   │   ├── App.vue                    # Main Vue component
│   │   ├── components/                # Reusable UI components
│   │   │   ├── Chat.vue
│   │   │   ├── ColumnNextclasses.vue
│   │   │   ├── DarkModeToggle.vue
│   │   │   ├── InfoColumn.vue
│   │   │   ├── ProfilePill.vue
│   │   │   └── UserCalendar.vue
│   │   ├── main.js 
│   │   ├── plugins/
│   │   ├── router/                    # Vue Router configuration and routes
│   │   │   └── index.js
│   │   └── views/                     # Main UI views or pages
│   │       ├── AssoList.vue
│   │       ├── ClassPage.vue
│   │       ├── HomePage.vue
│   │       ├── Login.vue
│   │       ├── MainLayout.vue
│   │       └── Photochart.vue
│   ├── package-lock.json 
│   └── package.json  
│
└── README.md  

```

## To-do:
- Finish scraping classes and lessons
- Add notifications and events
- Add Controls page
- Add Grades model, operations and routes
- Add a Classes page, with grades + ECTS table


