import sys

from os import getenv

try:
    from django.conf import settings

    settings.configure(
        DEBUG=False,
        USE_TZ=True,
        INSTALLED_APPS=[
            "django.contrib.staticfiles",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "djangoratings",
        ],
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
        }],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        STATIC_URL='/static/',
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError(
        "To fix this error, run: pip install -r requirements-test.txt"
    )


from django.test.utils import get_runner


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))
    sys.exit(0)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])