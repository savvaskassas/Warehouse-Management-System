"""
Database connection and configuration
"""
import os
from pymongo import MongoClient
from datetime import datetime
import bcrypt

class Database:
    def __init__(self):
        self.mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/LogisticsDB')
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client.LogisticsDB
        self.initialize_indexes()
        self.create_admin_user()
    
    def initialize_indexes(self):
        """Create database indexes for performance"""
        # Users collection indexes
        self.db.users.create_index("username", unique=True)
        self.db.users.create_index("unit_id")
        
        # Units collection indexes
        self.db.units.create_index("unit_id", unique=True)
        
        # Products master collection indexes
        self.db.products_master.create_index("product_id", unique=True)
        self.db.products_master.create_index("product_name")
        
        # Unit products collection indexes
        self.db.unit_products.create_index([("unit_id", 1), ("product_id", 1)], unique=True)
        self.db.unit_products.create_index("unit_id")
        
        # Transactions collection indexes
        self.db.transactions.create_index("unit_id")
        self.db.transactions.create_index("product_id")
        self.db.transactions.create_index([("timestamp", -1)])
    
    def create_admin_user(self):
        """Create default admin user if not exists"""
        admin_exists = self.db.users.find_one({"username": "admin"})
        if not admin_exists:
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
            admin_user = {
                "username": "admin",
                "password": hashed_password,
                "name": "System",
                "surname": "Administrator",
                "role": "admin",
                "unit_id": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            self.db.users.insert_one(admin_user)
            print("Admin user created successfully")

# Global database instance
db_instance = Database()