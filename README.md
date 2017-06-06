# DALME

A work in progress port of the current FileMaker-based DALME database to the Python Django framework.

## Setup for Development

### Software Required

The software required is listed below, along with commands for installation on OSX.

- Python 3
  - `brew install python3`
- Virtualenv
  - `pip install virtualenv`

### Setup

1. Clone this repo
  - `git clone https://github.com/DALME/dalme.git`
2. Set up a virtualenv for development. In this case, we're calling the environment "dalme" and placing it in a directory called `virtualenvs` in the home directory, but you can call it whatever you want and put it wherever you want.
  - `virtualenv -p python3 ~/virtualenvs/dalme`
3. Install the dependencies
  - (in the directory for this repository) `pip install -r requirements.txt`
4. Get a copy of db.cnf from someone else in the project to use the database connection, then place it in the root of the repository's directory
5. Test the local development setup
  - `python manage.py runserver`
6. Check out the site at `localhost:8000`
