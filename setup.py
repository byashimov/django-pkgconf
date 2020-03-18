from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='django-pkgconf',
    version='0.4.0',
    description='Yet another application settings helper.',
    long_description=long_description,
    url='https://github.com/byashimov/django-pkgconf',
    author='Murad Byashimov',
    author_email='byashimov@gmail.com',
    packages=['pkgconf'],
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
    ],
)
