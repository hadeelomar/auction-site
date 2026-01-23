import os

from django.conf import settings


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}


def config():
    """
    Database configuration with environment-based selection.
    - Local development: SQLite (default)
    - Production: PostgreSQL (when DATABASE_SERVICE_NAME is set)
    """
    service_name = os.getenv('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
    environment = os.getenv('DJANGO_ENV', 'development').lower()
    
    if service_name or environment == 'production':
        # Production: Use PostgreSQL
        engine = engines.get(os.getenv('DATABASE_ENGINE', 'postgresql'), engines['postgresql'])
        name = os.getenv('DATABASE_NAME', 'auction_site')
        user = os.getenv('DATABASE_USER', 'postgres')
        password = os.getenv('DATABASE_PASSWORD', 'postgres')
        host = os.getenv('DATABASE_HOST', os.getenv('{}_SERVICE_HOST'.format(service_name), 'localhost'))
        port = os.getenv('DATABASE_PORT', os.getenv('{}_SERVICE_PORT'.format(service_name), '5432'))
    else:
        # Development: Use SQLite
        engine = engines['sqlite']
        name = os.getenv('DATABASE_NAME', os.path.join(settings.BASE_DIR, 'db.sqlite3'))
        user = None
        password = None
        host = None
        port = None
    
    config = {
        'ENGINE': engine,
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }
    
    # Add PostgreSQL-specific optimizations
    if engine == engines['postgresql']:
        config.update({
            'OPTIONS': {
                'connect_timeout': 60,
                'MAX_CONNS': 20,
                'MIN_CONNS': 5,
            },
            'CONN_HEALTH_CHECKS': True,
            'CONN_MAX_AGE': 600,  # 10 minutes
        })
    
    return config
