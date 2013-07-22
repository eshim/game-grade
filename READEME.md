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
- Django
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
```

(format taken from https://github.com/rochacbruno/quokka/blob/master/README.md)
