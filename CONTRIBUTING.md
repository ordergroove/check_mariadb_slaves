## Code of conduct

Please remember to extend the same courtesy to others as you would wish them to extend to you. The [Angular code of conduct][angular-code-of-conduct] and [Django code of conduct][django-code-of-conduct] provide some concise and useful guidelines. 

Keep it clean, constructive and creative. Let's make sure everyone feels welcome.

## Issues and Feature Requests

For now, issues and feature requests will have to be tracked through the github issue tracker while we decide the best forum(s) for different types of requests.

Don't be bashful though - feel free to create a pull request with your proposed feature/bug fix.

## Development

As for most python projects, create a virtualenv for your local version of the project. To start development, clone the repository and install the requirements:

    git clone git@github.com:ordergroove/check_mariadb_slaves.git
    cd check_mariadb_slaves
    pip install -r requirements.txt

### Running Tests

    python -m unittest tests

Always run the tests before submitting pull requests. Once you've made a pull request take a look at the Travis build status in the GitHub interface and make sure the tests are running as you'd expect.

[angular-code-of-conduct]: https://github.com/angular/code-of-conduct/blob/master/CODE_OF_CONDUCT.md
[django-code-of-conduct]: https://www.djangoproject.com/conduct/
