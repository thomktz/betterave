# betterave
Projet Infrastructures et systèmes logiciels

## Setup
- Clone the repository.
- From there, go into the `backend` folder on the terminal (`cd backend`)
- Install poetry in your base environment (`pip install poetry`)
Package management is done with poetry. To add a new dependency, run `poetry add <package_name>`, then commit the changes made to the `pyproject.toml` and `poetry.lock` files to the repo.
- Install the dependencies with `poetry install`
- Activate the virtual environment with `poetry shell`

You can now run scripts using
`python -m scripts.init_db` 
`python -m scripts.add_student`
etc.

## Folder structure
```
betterave/
│
├── backend/                    # Backend server and API code
│   ├── app/                    # Main application directory
│   │   ├── database/           # Database configuration, models and utilities
│   │   │   ├── operations.py   # Database operations and queries
│   │   │   └── session.py      # Database session management
│   │   │
│   │   ├── models/             # Database models and ORM entities
│   │   │   ├── class_.py       # 'Class' entity definition and related functions
│   │   │   └── student.py      # 'Student' entity definition and related functions
│   │   │
│   │   └── ...                 # Other app-specific modules, utilities, and configuration
│   │
│   ├── scripts/                # Scripts for database setup and other utilities
│   │   ├── init_db.py          # Database initialization script
│   │   └── ...                 # Other utility scripts and management tasks
│   │
│   ├── tests/                  # Test suite for the application
│   │   ├── test_operations.py  # Tests for database operations
│   │   └── ...                 # Other test files and related resources
│   │
│   └── README.md               # Backend-specific documentation
│
├── frontend/                   # Frontend application code
│   ├── assets/                 # Static files like images, fonts, etc.
│   ├── components/             # Reusable UI components
│   ├── views/                  # Main UI views or pages
│   ├── App.js                  # Main application entry point
│   └── ...                     # Other frontend-specific modules and configurations
│
└── README.md                   # Project overview and documentation for both frontend and backend
```

## To-do:
- Scrape ENSAE website to fill the classes database -> Scripts folder? Or new folder in backend?
- Create authenticated app with flask -> Handle login and sessions
- Create API routes
- Create frontend
- Add unit testing to existing code
