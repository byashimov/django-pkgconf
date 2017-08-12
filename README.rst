django-pkgconf
==============

Yet another application settings helper.

Rationale
---------

It's a common practice to put a settings file in a distribution package with some predefined stuff which can be overridden later in global project's settings.
But there is also a good reason to separate all your settings within your apps just like you do so with common python code: models, views, etc.
That's not a big thing if your project doesn't come with dozen apps, but if it does, flushing out non-project stuff is a good way to not mess things around and keep them way simple.

.. _quickstart:

Quickstart
----------

Lets say you have an email service application in your project dir and it stores some configuration in ``settings.py``:

.. code-block:: python

    MYEMAILSERVICE_USERNAME = 'username'
    MYEMAILSERVICE_PASSWORD = 'password'
    ...

It's a big temptation to write short ``USERNAME``, but you have to use prefixes to prevent conflicts with other application settings and tell collaborators *this is for the email app*. And then:

.. code-block:: python

    # emails/foo.py
    from django.conf import settings.

    service = Service(username=settings.MYEMAILSERVICE_USERNAME,
                      password=settings.MYEMAILSERVICE_PASSWORD,
                      ...)

Prefixes are everywhere. You always have to say ``MYEMAILSERVICE_`` in every single place you need to access the settings. How about this one:

.. code-block:: python

    # Package settings in emails/conf.py
    from pkgconf import Conf

    class MyEmailService(Conf):
        USERNAME = 'username'
        PASSWORD = 'password'

        @property
        def DEBUG(self):
            return self.USERNAME.startswith('test_')

There is nothing more to say:

.. code-block:: python

    # emails/foo.py
    # Note: your MyEmailService class becomes a module,
    # you import it directly
    from . import conf

    service = Service(username=conf.USERNAME, password=conf.PASSWORD, ...)

**django-pkgconf** wraps your application settings and provides a handy shortcut.

But what about test or dev settings? Just define them like you always do (configuration class name becomes a prefix).

Old style:

.. code-block:: python

    # local_settings.py
    MYEMAILSERVICE_USERNAME = 'test_username'

Cool style (django-configurations_ way):

.. code-block:: python

    # settings.py
    class Prod(Configuration):
        # No email service settings at all
        pass

    class Test(Prod):
        MYEMAILSERVICE_USERNAME = 'test_username'

It looks for the required setting in django's configuration file first and returns original value if it's not overridden:

.. code-block:: python

    # emails/foo.py
    from . import conf

    conf.USERNAME  # 'test_username'
    conf.PASSWORD  # 'password' - returns original value
    conf.DEBUG  # True


Since ``0.3.0`` mixins are supported:

.. code-block:: python

    from pkgconf import Conf

    class FacebookMixin:
        FACEBOOK_APP_ID = 'foo'
        FACEBOOK_SECRET = 'bar'


    class TwitterMixin:
        TWITTER_APP_ID = 'foo'
        TWITTER_SECRET = 'bar'


    class InstagramMixin:
        INSTAGRAM_APP_ID = 'foo'
        INSTAGRAM_SECRET = 'bar'


    class SocialAppConf(FacebookMixin, TwitterMixin, InstagramMixin, Conf):
        DEBUG = True


Installation
------------

Install the package:

.. code-block:: console

    pip install -U django-pkgconf

Read the quickstart_.


Compatability
-------------

.. image:: https://travis-ci.org/byashimov/django-pkgconf.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/byashimov/django-pkgconf

.. image:: https://codecov.io/gh/byashimov/django-pkgconf/branch/master/graph/badge.svg
    :alt: Codecov
    :target: https://codecov.io/gh/byashimov/django-pkgconf

Tested on py 2.7, 3.4, 3.5 with django 1.8, 1.9, 1.10.


Powered siblings
----------------

There are more advanced apps with (probably) some extra (better?) options: django-appsettings_, django-appconf_, etc. The reason I've published this one is those apps are too big and tricky to do this little work, so you might prefer them instead.


Limitations
-----------

- Due to the code simplicity, ``property`` descriptor is used to *get* data from the settings. That means you can not *set* (or *change*) configuration values *in action*. I don't know why you would do that, but I have to warn you.
- Since your app's settings are defined in separate file, they are not accessible via ``django.conf.settings`` (until you override them in your project settings). This application doesn't create backward compatibility links. You should always use package configuration module.


Changelog
---------

v0.3.0
~~~~~~
- Added mixins support.

v0.2.1 - 0.2.2
~~~~~~~~~~~~~~
- Added ``import *`` support.
- ``__prefix__`` is generated automatically if not presented in class.
  That may help to build graceful exceptions like ``'foo_value' was not found in MYAPP_FOO_SETTING``.

v0.2.0
~~~~~~
- Added ``__prefix__`` attribute to support prefix-names with underscores.
- Added instance method and property support.
- **Backward incompatible change:** functions must have ``self`` as the first argument now.

v0.1.0
~~~~~~
- First public release

.. _django-appsettings: https://github.com/jaredly/django-appsettings
.. _django-appconf: https://github.com/django-compressor/django-appconf
.. _django-configurations: https://github.com/jezdez/django-configurations