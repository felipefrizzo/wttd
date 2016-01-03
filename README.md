# Eventex

System of Events create in the course Welcome to the Django.

[![Build Status](https://travis-ci.org/felipefrizzo/wttd.svg?branch=master)](https://travis-ci.org/felipefrizzo/wttd)

## How to develop ?

1. Clone the repository.

    ```console
    git clone https://github.com/felipefrizzo/wttd.git wttd
    cd wttd
    ```
2. Create a virtualenv with Python 3.5.0

    ```console
    pyenv install 3.5.0
    ```

3. Activate your virtualenv.

    ```console
    pyenv virtualenv 3.5.0 wttd
    pyenv local wttd
    ```

4. Install the dependencies.

    ```console
    pip install -r requirements.txt
    cd contrib/env-sample .env
    ```
5. configure the instance with .env
6. Run the tests.

    ```console
    python manage.py test
    ```

## How to deploy ?

1. Create a instance in heroku.
2. Send the configurations for heroku.
3. Set a safe SECRET_KEY for instance.
4. Set DEBUG=False
5. Configure the email service.
6. Send the code for the heroku.

    ```console
    heroku create MyInstance
    heroku config:push
    heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
    heroku config:set DEBUG=False
    # Config email
    git push heroku master --force
    ```

