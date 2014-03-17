paprika
=======

Django based blog and web board system. It supports Python3.3

## Main features
 1. Multiple blogs (using board)
 2. Simple design using Bootstrap
 3. Select markup language in (markdown, textile, restructuredtext, tinymce)
 4. Site management using Django admin

## Installation (python3.3)

    $ git clone https://github.com/yong27/paprika
    $ cd paprika
    $ virtualenv . -p python3.3
    $ source bin/activate
    $ pip install -r pip-requirements.txt
    $ wget https://github.com/twbs/bootstrap/releases/download/v3.1.1/bootstrap-3.1.1-dist.zip
    $ unzip bootstrap-3.1.1-dist.zip
    $ mv bootstrap-3.1.1-dist paprikasite/paprika/static/paprika/bootstrap
    $ cd paprikasite
    $ vi paprikasite/settings_yours.py   ## add your settings here. refer settings.py
    $ python manage.py syncdb
    $ python manage.py test paprika
    $ python manage.py runserver

## Installation (python2.7)

    $ git clone https://github.com/yong27/paprika
    $ cd paprika
    $ virtualenv .
    $ source bin/activate
    $ cat > lib/python2.7/sitecustomize.py << EOF
    import sys
    sys.setdefaultencoding('utf-8')
    EOF
    $ pip install -r pip-requirements.txt
    $ wget https://github.com/twbs/bootstrap/releases/download/v3.1.1/bootstrap-3.1.1-dist.zip
    $ unzip bootstrap-3.1.1-dist.zip
    $ mv bootstrap-3.1.1-dist paprikasite/paprika/static/paprika/bootstrap
    $ cd paprikasite
    $ vi paprikasite/settings_yours.py   ## add your settings here. refer settings.py
    $ python manage.py syncdb
    $ python manage.py test paprika
    $ python manage.py runserver

## License

The code is freely available under the [MIT license][1].

[1]: http://www.opensource.org/licenses/mit-license.html
