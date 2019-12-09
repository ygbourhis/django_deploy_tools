# Django Deployement Tools

Tools to help deploy a django application.

## INSTALLATION:

    pip install Django-Deployment-Tools

## CONFIGURATION:

Add `'django_deploy_tools',` in your `settings.INSTALLED_APPS`.

Add a `STATIC_ROOT` variable in your django `settings.py` file.

See <https://docs.djangoproject.com/en/3.0/ref/settings/#static-files>,
<https://docs.djangoproject.com/en/3.0/ref/settings/#static-root> and
<https://docs.djangoproject.com/en/3.0/howto/static-files/> for more
details.

## USAGE:

First collect static files:

    python manage.py collectstatic

If you have django-compressor (optional) run:

    python manage.py compress

(see <https://django-compressor.readthedocs.io/en/stable/> for more details).

Then, create a wsgi file:

    python manage.py make_sgi --wsgi --out path/to/wsgi_file

And then generate an apache configuration file:

    python manage.py make_apache_conf --wsgi path/to/wsgi_file --sll --out /path/to/apache_conf_file

For more information check :

    python manage.py make_apache_conf -h

Especially to define the proper ssl certificates. If not specified when
creating the configuration file you will have to edit the generated apache
configuration.
