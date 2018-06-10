## Code of conduct

Please remember to extend the same courtesy to others as you would wish them to extend to you. The [Angular code of conduct][angular-code-of-conduct] and [Django code of conduct][django-code-of-conduct] provide some concise and useful guidelines. 

Keep it clean, constructive and creative. Let's make sure everyone feels welcome.

## Issues, Features, and Questions

Usage questions should be directed to the [discussion group][google-group]. Feature requests, bug reports and other issues should be raised on the GitHub issue tracker.

Don't be bashful though - feel free to create a pull request with your proposed feature/bug fix.

## Development

As for most python projects, create a virtualenv for your local version of the project. To start development, clone the repository and install the requirements:

    git clone git@github.com:ordergroove/check_mariadb_slaves.git
    cd check_mariadb_slaves
    pip install -r requirements.txt

### Running Tests

There are a couple of ways to do this and both are recommended:

    pip install pytest pytest-cov tox
    pytest --cov=.

which will run all the tests in your environment's version of python and provide you with a full coverage report.

Once you're happy with your feature, please use `tox` to test the supported versions of python

    tox

Always run the tests before submitting pull requests. Once you've made a pull request take a look at the Travis build status in the GitHub interface and make sure the tests are running as you'd expect.

If you're unfamiliar with tox or py.test, please check these links out:
- [tox][tox]
- [py.test][pytest]
- [py.test + tox][pytest-tox]

[angular-code-of-conduct]: https://github.com/angular/code-of-conduct/blob/master/CODE_OF_CONDUCT.md
[django-code-of-conduct]: https://www.djangoproject.com/conduct/
[google-group]: https://groups.google.com/forum/?fromgroups#!forum/maria-db-slave-nagios-plugin
[tox]: https://tox.readthedocs.org/en/latest/
[pytest]: http://pytest.org/latest/
[pytest-tox]: http://tox.readthedocs.org/en/latest/example/pytest.html
