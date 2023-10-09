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



## To-do:
- Scrape ENSAE website to fill the classes database
- Create authenticated app with flask
- Create API points
- Create frontend
- Add unit testing
