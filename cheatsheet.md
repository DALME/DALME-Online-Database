# DALME Django Cheatsheet

This is intended as a resource for operations surrounding the DALME site created with Django, to make regular operations easier.

## Managing the database

- After you've changed a data model in a `models.py` file, you'll need to run the following commands:
  - `python manage.py makemigrations` to generate the SQL to update the database
  - `python manage.py migrate` to run that SQL on the database and update the data models
  - `python manage.py migrate --settings dalme.devSettings` to update the development database
