import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(24)

class Prod(Config):
    DB_USER=#<MARIADB OR MYSQL DB USER>
    DB_PW=#<MARIADB OR MYSQL DB PW>
    DB_HOST=#<PRODUCTION DB  HOSTNAME OR IP>
    USER_POOL_ID=#<AWS USER POOL ID>
    COGNITO_CLIENT_ID=#<AWS COGNITO CLIENT ID>
    COGNITO_REDIRECT_URI=#"https://<PRODUCTION URL>/auth"
    AUTH_URL=#<AWS COGNITO OAUTH2 TOKEN URL>
    LOGIN_URL=#<AWS COGNITO LOGIN URL>

class Dev(Config):
    DEBUG = True
    DB_USER=#<MARIADB OR MYSQL DB USER>
    DB_PW=#<MARIADB OR MYSQL DB PW>
    DB_HOST="127.0.0.1"
    USER_POOL_ID=#<AWS USER POOL ID>
    COGNITO_CLIENT_ID=#<AWS COGNITO CLIENT ID>
    COGNITO_REDIRECT_URI="https://127.0.0.1:5000/auth"
    AUTH_URL=#<AWS COGNITO OAUTH2 TOKEN URL>
    LOGIN_URL=#<AWS COGNITO LOGIN URL>
class Test(Config):
    TESTING = True
    DB_USER=#<MARIADB OR MYSQL DB USER>
    DB_PW=#<MARIADB OR MYSQL DB PW>
    DB_HOST=#<TESTING DB  HOSTNAME OR IP>
    USER_POOL_ID=#<AWS USER POOL ID>
    COGNITO_CLIENT_ID=#<AWS COGNITO CLIENT ID>
    COGNITO_REDIRECT_URI=#"https://<TESTING URL>/auth"
    AUTH_URL=#<AWS COGNITO OAUTH2 TOKEN URL>
    LOGIN_URL=#<AWS COGNITO LOGIN URL>
