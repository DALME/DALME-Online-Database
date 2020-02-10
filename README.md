# DALME

A work in progress port of the current FileMaker-based DALME database to the Python Django framework.

## Setup for Development

### Software Required

The software required is listed below, along with commands for installation on OSX.

- Python 3
  - `brew install python3`
- Virtualenv
  - `pip install virtualenv`
- Postgres
    - `brew install postgresql`
- MySQL
    - `brew install mysql`

### Setup

1. Clone this repo and `cd` into the project.
```
git clone https://github.com/DALME/dalme.git
````

2. Set up a virtualenv for development. In this case, we're calling the environment "dalme" and placing it in a directory called `virtualenvs` in the home directory, but you can call it whatever you want and put it wherever you want.
```
virtualenv -p python3 ~/virtualenvs/dalme
```

4. Activate the virtual environment.
```
source ~/virtualenvs/dalme/bin/activate
```

3. Install the dependencies.
    - (in the directory for this repository) `pip install -r requirements.txt`
    - Some installations may fail, try installing command line tools:
        - `xcode-select --install`
    - Also try installing `psycopg` and/or `mysqlclient` with the following pip commands:
        - `env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip --no-cache install psycopg2`
        - `env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip --no-cache install mysqlclient`
    - Alternatively, for compilers to find openssl you can set:
        - `export LDFLAGS="-L/usr/local/opt/openssl/lib"`
        - `export CPPFLAGS="-I/usr/local/opt/openssl/include"`

4. Get a copy of the `env` and `db.cnf` files from someone else in the project and place it in the root of the repository's directory.

5. Prime your filesystem for logging.
```
sudo mkdir /var/log/django && \
  sudo touch /var/log/django/dalme_app.log && \
  sudo chown -R $(whoami) /var/log/django
```

6. Source the environment settings.
```
source ./env
```

7. Restore the db dump and create the application db user.
```
$ mysql -u root < path_to_db_dump.sql
$ mysql -u root
-- Where `$PASSWORD` == `password` found in the `db.cnf` file.
mysql> CREATE USER 'dalme_app'@'localhost' IDENTIFIED BY '$PASSWORD';
mysql> GRANT ALL PRIVILEGES ON ebdb.* TO 'dalme_app'@'localhost';
mysql> FLUSH PRIVILEGES;
-- While we are in the mysql shell let's set your `User` record (which should
-- already be in the database dump) as a local superuser.
-- First find the pk of your row and then update it.
mysql> USE ebdb;
mysql> SELECT username, id FROM auth_user;
mysql> UPDATE auth_user SET is_superuser = 1 WHERE id = $YOUR_USER_PK;
```

Change your local password if you need to.
```
$ python manage.py changepassword $YOUR_USERNAME
```

If you don't already have a record in the database, create one.
```
python manage.py createsuperuser
```

8. Test the local development setup.
```
python manage.py runserver
```

If you create a new terminal to do this, you'll need to make sure that you're in your environment with `source ~/virtualenvs/dalme/bin/activate`.

9. Check out the site at `localhost:8000`.

10. You can monitor the log output if you feel like it. Open a separate terminal and call:
```
$ tail -f /var/log/django/dalme_app.log
```
