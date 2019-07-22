import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False

    DEBUG_TOOLBAR_ENABLED = True
    REST_URL_PREFIX = '/aiden'
    API_VERSION_V1 = 1


class DevelopmentConfig(Config):
    """Configurations for Development."""
    TESTING = True
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True


class DevelopmentEnvironmentConfig(Config):
    """Configurations for Development Environment."""
    DEBUG = True


class ProductionEnvironmentConfig(Config):
    """Configurations for the Production Environment."""
    DEBUG = False
    TESTING = False

app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'dev': DevelopmentEnvironmentConfig,
    'prod': ProductionEnvironmentConfig,
}