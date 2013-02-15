paprika
=======

Django based blog and web board system

## Main features
 1. Multiple blogs (using board)
 2. Simple design using Bootstrap
 3. Select markup language in (markdown, textile, restructuredtext, tinymce)
 4. Site management using Django admin

## Installation

    $ git clone https://github.com/yong27/paprika
    $ cd paprika
    $ virtualenv .
    $ source bin/activate
    $ cat > lib/python2.7/sitecustomize.py << EOF
    import sys
    sys.setdefaultencoding('utf-8')
    EOF
    $ pip install pip-requirements.txt
    $ cd paprikasite
    $ vi paprikasite/settings.py   ## add your settings here
    $ python manage.py syncdb
    $ python manage.py runserver

## License

The code is freely available under the [MIT license][1].

[1]: http://www.opensource.org/licenses/mit-license.html
