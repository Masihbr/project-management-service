import environ

env = environ.Env()

environ.Env.read_env('.env')


def __get_env_variable(key: str, default_value=None) -> str:
    return env(key, default=default_value)


configs = {
    'SECRET_KEY': __get_env_variable('SECRET_KEY', 'DontLookAtMe'),
    'DEBUG': __get_env_variable('DEBUG', 'True').lower() == 'true',
    'ALLOWED_HOSTS': __get_env_variable('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1 [::1]').split(' '),
    'DEFAULT_DATABASE': {
        'ENGINE': __get_env_variable('DEFAULT_DATABASE_ENGINE', 'django.db.backends.postgresql'),
        'NAME': __get_env_variable('DEFAULT_DATABASE_NAME', 'project_management_db'),
        'USER': __get_env_variable('DEFAULT_DATABASE_USER', 'user'),
        'PASSWORD': __get_env_variable('DEFAULT_DATABASE_PASSWORD', 'password'),
        'HOST': __get_env_variable('DEFAULT_DATABASE_HOST', 'localhost'),
        'PORT': __get_env_variable('DEFAULT_DATABASE_PORT', '5432'),
    },
    'CSRF_TRUSTED_ORIGINS': __get_env_variable('CSRF_TRUSTED_ORIGINS', 'localhost').split(' '),
}


def get_config(config_name):
    return configs.get(config_name)
