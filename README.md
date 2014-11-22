# ifqsync2

IFQ Sync version 2


## Setup a new virtualenv with python3

```bash

$ which python3
/usr/local/bin/python3

$ mkvirtualenv --python=/usr/local/bin/python3 django-ifqsync2 
Running virtualenv with interpreter /usr/local/bin/python3
Using base prefix '/Library/Frameworks/Python.framework/Versions/3.4'
New python executable in django-ifqsync2/bin/python3
Also creating executable in django-ifqsync2/bin/python
Installing setuptools, pip...done.

$ python -V
Python 3.4.2

```

## Install required packages

```bash

$ pip install -r requirements/dev.txt

```

## Set environment variables 


```bash

$ export DJANGO_SETTINGS_MODULE=ifqsync2.settings.dev
$ export IFQ_USERNAME="username"
$ export IFQ_PASSWORD="password"

```

## Run Django server


```bash

$ cd ifqsync2 

$ python manage.py runserver

```
