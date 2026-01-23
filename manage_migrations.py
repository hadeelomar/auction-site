#!/usr/bin/env python
"""
Database migration management script.
Handles migration from SQLite to PostgreSQL and ongoing migrations.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.commands.showmigrations import Command as ShowMigrationsCommand
from django.db import connection
import subprocess

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


def create_migration_backup():
    """Create a backup of current SQLite data before migration."""
    if connection.vendor == 'sqlite':
        print("📦 Creating SQLite data backup...")
        try:
            # Export data to JSON
            from django.core.management import call_command
            call_command('dumpdata', 'api', output='sqlite_backup.json', indent=2)
            print("✅ SQLite data backed up to sqlite_backup.json")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    return True


def run_migrations():
    """Run Django migrations."""
    print("🔄 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


def show_migration_status():
    """Show current migration status."""
    print("📊 Migration status:")
    try:
        execute_from_command_line(['manage.py', 'showmigrations'])
        return True
    except Exception as e:
        print(f"❌ Could not show migrations: {e}")
        return False


def create_initial_migration():
    """Create initial migration if none exist."""
    print("🔍 Checking for existing migrations...")
    try:
        # Check if migrations directory exists and has files
        migrations_dir = os.path.join('api', 'migrations')
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
        
        # Create __init__.py if it doesn't exist
        init_file = os.path.join(migrations_dir, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('')
        
        # Create initial migration
        execute_from_command_line(['manage.py', 'makemigrations', 'api', '--verbosity=2'])
        print("✅ Initial migration created")
        return True
    except Exception as e:
        print(f"❌ Failed to create initial migration: {e}")
        return False


def test_database_connection():
    """Test database connection and basic operations."""
    print("🔌 Testing database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print(f"✅ Database connection successful ({connection.vendor})")
                return True
            else:
                print("❌ Database connection test failed")
                return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def main():
    """Main migration management function."""
    print("🚀 Database Migration Manager")
    print("=" * 40)
    
    # Test current connection
    if not test_database_connection():
        print("❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Show current status
    show_migration_status()
    
    # Create backup if using SQLite
    if not create_migration_backup():
        print("⚠️  Warning: Backup failed, but continuing...")
    
    # Create initial migration if needed
    if not create_initial_migration():
        print("⚠️  Warning: Initial migration creation failed")
    
    # Run migrations
    if not run_migrations():
        print("❌ Migration process failed")
        sys.exit(1)
    
    # Show final status
    print("\n📊 Final migration status:")
    show_migration_status()
    
    print("\n✅ Migration process completed successfully!")
    print(f"📊 Current database: {connection.vendor}")


if __name__ == '__main__':
    main()
