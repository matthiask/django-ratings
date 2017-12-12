from setuptools import setup, find_packages

setup(
    name='django-ratings',
    version=".".join(map(str, __import__('djangoratings').__version__)),
    author='David Cramer',
    author_email='dcramer@gmail.com',
    description='Generic Ratings in Django',
    url='http://github.com/dcramer/django-ratings',
    install_requires=[
        'Django>=1.7,<2.0',
    ],
    tests_require=[
        'dj-database-url==0.3.0',
        'psycopg2==2.6.1',
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
