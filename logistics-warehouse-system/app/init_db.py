"""
Database initialization script for the Logistics Warehouse System
Creates default admin user and sets up initial data if needed
"""
from .models import user_model
from .database import db_instance

def initialize_admin():
    """Create default admin user if it doesn't exist"""
    try:
        # Check if admin user already exists
        admin_user = user_model.get_user_by_username('admin')
        
        if not admin_user:
            # Create admin user
            admin_id = user_model.create_user(
                username='admin',
                password='admin123',
                name='Administrator',
                surname='System',
                role='admin',
                unit_id=None
            )
            print("✓ Default admin user created successfully!")
            print("  Username: admin")
            print("  Password: admin123")
            return True
        else:
            print("✓ Admin user already exists")
            return True
            
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        return False

def initialize_database():
    """Initialize database with default data"""
    try:
        print("🚀 Initializing Logistics Warehouse System Database...")
        
        # Initialize admin user
        admin_success = initialize_admin()
        
        if admin_success:
            print("✅ Database initialization completed successfully!")
            return True
        else:
            print("❌ Database initialization failed!")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def check_database_health():
    """Check database connectivity and collections"""
    try:
        # Test database connection
        db_instance.db.command('ping')
        print("✓ Database connection successful")
        
        # Check collections
        collections = db_instance.db.list_collection_names()
        required_collections = ['users', 'units', 'products_master', 'unit_products', 'transactions']
        
        for collection in required_collections:
            if collection in collections:
                count = db_instance.db[collection].count_documents({})
                print(f"✓ Collection '{collection}': {count} documents")
            else:
                print(f"! Collection '{collection}' will be created on first use")
        
        return True
        
    except Exception as e:
        print(f"✗ Database health check failed: {e}")
        return False