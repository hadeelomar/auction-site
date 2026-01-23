#!/bin/bash

# PostgreSQL Deployment Script for OpenShift
# This script handles database initialisation and migration for production

set -e 

echo "🚀 PostgreSQL Deployment Script"
echo "================================"

# Function to check if database is ready
check_database() {
    echo "🔍 Checking database connection..."
    python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"
}

# Function to run migrations
run_migrations() {
    echo "🔄 Running database migrations..."
    python manage.py migrate --verbosity=2
    echo "✅ Migrations completed"
}

# Function to create superuser if needed
create_superuser() {
    echo "👤 Checking for superuser..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print('✅ Superuser created (username: admin, password: admin123)')
else:
    print('✅ Superuser already exists')
"
}

# Function to collect static files
collect_static() {
    echo "📦 Collecting static files..."
    python manage.py collectstatic --noinput
    echo "✅ Static files collected"
}

# Function to check application health
health_check() {
    echo "🏥 Running health checks..."
    
    # Check database health
    echo "Checking database health..."
    curl -f http://localhost:8000/health/database || {
        echo "❌ Database health check failed"
        exit 1
    }
    
    # Check application health
    echo "Checking application health..."
    curl -f http://localhost:8000/health/application || {
        echo "❌ Application health check failed"
        exit 1
    }
    
    echo "✅ All health checks passed"
}

# Main deployment process
main() {
    echo "📍 Starting PostgreSQL deployment..."
    
    # Wait for database to be ready (OpenShift specific)
    if [ -n "$DATABASE_SERVICE_NAME" ]; then
        echo "⏳ Waiting for PostgreSQL service to be ready..."
        sleep 10
    fi
    
    # Check database connection
    check_database
    
    # Run migrations
    run_migrations
    
    # Create superuser if needed
    create_superuser
    
    # Collect static files
    collect_static
    
    # Health checks
    health_check
    
    echo ""
    echo "🎉 PostgreSQL deployment completed successfully!"
    echo "📊 Database engine: $(python manage.py shell -c 'from django.db import connection; print(connection.vendor)')"
    echo "🌐 Health endpoints available at:"
    echo "   - /health (basic)"
    echo "   - /health/database (detailed)"
    echo "   - /health/application (overall)"
}

# Run the deployment
main "$@"
