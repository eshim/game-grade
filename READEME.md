Game and Grade - Python and Django powered educational CMS

An open source web application for programming instructors that manages many of the troubleshooting obstacles new programming students face in setup, coding, submission and evaluation.

Recommended Experience
======================
- Unit Testing
- Content Management


Software Requirements
=====================
- pylint
- Python 2.7
- Django 1.5.1
- sqlite3
- south 


Setup
=====

#### On a *nix shell, do:

```bash
~/$ git clone https://github.com/plikarish/game-grade.git
~/$ ...cloning in to game-grade
(authentication)
~/$ cd gamegrade
~/$ python manage.py syncdb
~/$ Syncing ...
~/$ Creating tables ...
(create super user)
~/$ ./manage.py migrate submissions
~/$ Running migrations for submissions:
(migration occurs)
```
#### To run the application, do:

```bash
~/$ python manage.py runserver
~/$ Validating models...
```

Use
===

#### Login as admin:
1. Open a web browser
2. Navigate to http://127.0.0.1:8000/admin
3. Enter account information

#### Create a task:
1. Navigate to http://127.0.0.1:8000/admin
2. Find the field "Tasks" under "Submissions"
3. Click on the "+ Add" link for "Tasks"
4. Fill out the required information
5. Click on the "Save" button to the bottom right

#### Upload and associate a unit test:
1. Navigate to http://127.0.0.1:8000/admin
2. Find the "Unit tests" field under "Submissions"
3. Click on the "+ Add" link for "Unit tests"
4. Fill out the required information and click on the task you would like the unit test to be associated with
5. Click on the "Save" button to the bottom right


(format taken from https://github.com/rochacbruno/quokka/blob/master/README.md)
