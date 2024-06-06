from decouple import config as env_config

class Config:
    SECRET_KEY = env_config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    PGSQL_HOST = env_config('PGSQL_HOST')
    PGSQL_USER = env_config('PGSQL_USER')
    PGSQL_PASSWORD = env_config('PGSQL_PASSWORD')
    PGSQL_DATABASE = env_config('PGSQL_DATABASE')
    DATABASE_URI = f'postgresql://{PGSQL_USER}:{PGSQL_PASSWORD}@{PGSQL_HOST}/{PGSQL_DATABASE}'

config = {
    'development': DevelopmentConfig
}
