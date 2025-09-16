"""
Database models for the Logistics Warehouse System
"""
from datetime import datetime
from bson import ObjectId
import bcrypt
from .database import db_instance

class UserModel:
    def __init__(self):
        self.collection = db_instance.db.users
    
    def create_user(self, username, password, name, surname, role, unit_id=None):
        """Create a new user"""
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            "username": username,
            "password": hashed_password,
            "name": name,
            "surname": surname,
            "role": role,
            "unit_id": unit_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def authenticate_user(self, username, password, unit_id=None):
        """Authenticate user credentials"""
        query = {"username": username}
        if unit_id:
            query["unit_id"] = unit_id
            
        user = self.collection.find_one(query)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user
        return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        return self.collection.find_one({"username": username})
    
    def get_users_by_unit(self, unit_id):
        """Get all users in a specific unit"""
        return list(self.collection.find({"unit_id": unit_id}))
    
    def get_all_supervisors(self):
        """Get all supervisors"""
        return list(self.collection.find({"role": "supervisor"}))
    
    def update_password(self, username, new_password):
        """Update user password"""
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        return self.collection.update_one(
            {"username": username},
            {"$set": {"password": hashed_password, "updated_at": datetime.utcnow()}}
        )
    
    def delete_user(self, username):
        """Delete user"""
        return self.collection.delete_one({"username": username})

class UnitModel:
    def __init__(self):
        self.collection = db_instance.db.units
    
    def create_unit(self, unit_name, unit_volume):
        """Create a new warehouse unit"""
        # Generate unit_id (simple increment - in production use better method)
        last_unit = self.collection.find().sort("unit_id", -1).limit(1)
        try:
            last_id = int(list(last_unit)[0]["unit_id"])
            unit_id = str(last_id + 1).zfill(3)
        except (IndexError, ValueError):
            unit_id = "001"
        
        unit_data = {
            "unit_id": unit_id,
            "unit_name": unit_name,
            "unit_volume": unit_volume,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(unit_data)
        return unit_id
    
    def get_unit_by_id(self, unit_id):
        """Get unit by unit_id"""
        return self.collection.find_one({"unit_id": unit_id})
    
    def get_all_units(self):
        """Get all units"""
        return list(self.collection.find())
    
    def delete_unit(self, unit_id):
        """Delete unit"""
        return self.collection.delete_one({"unit_id": unit_id})

class ProductModel:
    def __init__(self):
        self.master_collection = db_instance.db.products_master
        self.unit_products_collection = db_instance.db.unit_products
    
    def create_product(self, product_name, product_weight, product_volume, 
                      product_category, product_purchase_price, product_selling_price,
                      product_manufacturer):
        """Create a new product in master catalog"""
        # Generate product_id
        last_product = self.master_collection.find().sort("product_id", -1).limit(1)
        try:
            last_id = int(list(last_product)[0]["product_id"][1:])  # Remove 'P' prefix
            product_id = f"P{str(last_id + 1).zfill(4)}"
        except (IndexError, ValueError):
            product_id = "P0001"
        
        product_data = {
            "product_id": product_id,
            "product_name": product_name,
            "product_weight": product_weight,
            "product_volume": product_volume,
            "product_category": product_category,
            "product_purchase_price": product_purchase_price,
            "product_selling_price": product_selling_price,
            "product_manufacturer": product_manufacturer,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.master_collection.insert_one(product_data)
        
        # Add product to all existing units with 0 quantity
        units = db_instance.db.units.find()
        for unit in units:
            self.add_product_to_unit(unit["unit_id"], product_id, 0)
        
        return product_id
    
    def add_product_to_unit(self, unit_id, product_id, quantity=0):
        """Add product to specific unit"""
        unit_product_data = {
            "unit_id": unit_id,
            "product_id": product_id,
            "product_quantity": quantity,
            "product_sold_quantity": 0,
            "product_unit_gain": 0.0,
            "last_updated": datetime.utcnow()
        }
        
        # Use upsert to avoid duplicates
        return self.unit_products_collection.update_one(
            {"unit_id": unit_id, "product_id": product_id},
            {"$set": unit_product_data},
            upsert=True
        )
    
    def get_products_by_unit(self, unit_id, search_params=None, sort_params=None):
        """Get products for specific unit with optional search and sort"""
        # Base query
        query = {"unit_id": unit_id}
        
        # Add search filters if provided
        if search_params:
            if 'product_name' in search_params:
                # Get product_ids from master that match name
                name_regex = {"$regex": search_params['product_name'], "$options": "i"}
                matching_products = self.master_collection.find({"product_name": name_regex})
                product_ids = [p["product_id"] for p in matching_products]
                query["product_id"] = {"$in": product_ids}
            
            if 'product_id' in search_params:
                query["product_id"] = search_params['product_id']
            
            if 'quantity_min' in search_params or 'quantity_max' in search_params:
                quantity_filter = {}
                if 'quantity_min' in search_params:
                    quantity_filter["$gte"] = search_params['quantity_min']
                if 'quantity_max' in search_params:
                    quantity_filter["$lte"] = search_params['quantity_max']
                query["product_quantity"] = quantity_filter
        
        # Execute query
        cursor = self.unit_products_collection.find(query)
        
        # Add sorting if provided
        if sort_params:
            cursor = cursor.sort(sort_params['field'], sort_params['order'])
        
        unit_products = list(cursor)
        
        # Enrich with master product data
        for up in unit_products:
            master_product = self.master_collection.find_one({"product_id": up["product_id"]})
            if master_product:
                up.update(master_product)
        
        return unit_products
    
    def get_product_details(self, unit_id, product_id):
        """Get complete product details for specific unit"""
        unit_product = self.unit_products_collection.find_one({
            "unit_id": unit_id, 
            "product_id": product_id
        })
        
        if unit_product:
            master_product = self.master_collection.find_one({"product_id": product_id})
            if master_product:
                unit_product.update(master_product)
        
        return unit_product
    
    def update_product_quantity(self, unit_id, product_id, quantity_change, transaction_type):
        """Update product quantity and gain"""
        unit_product = self.unit_products_collection.find_one({
            "unit_id": unit_id,
            "product_id": product_id
        })
        
        if not unit_product:
            return False
        
        master_product = self.master_collection.find_one({"product_id": product_id})
        if not master_product:
            return False
        
        # Calculate new values
        new_quantity = unit_product["product_quantity"]
        new_sold_quantity = unit_product["product_sold_quantity"]
        new_gain = unit_product["product_unit_gain"]
        
        if transaction_type == "sale":
            if new_quantity >= quantity_change:
                new_quantity -= quantity_change
                new_sold_quantity += quantity_change
                new_gain += quantity_change * master_product["product_selling_price"]
            else:
                return False  # Not enough stock
        
        elif transaction_type == "purchase":
            new_quantity += quantity_change
            new_gain -= quantity_change * master_product["product_purchase_price"]
        
        # Update database
        return self.unit_products_collection.update_one(
            {"unit_id": unit_id, "product_id": product_id},
            {"$set": {
                "product_quantity": new_quantity,
                "product_sold_quantity": new_sold_quantity,
                "product_unit_gain": new_gain,
                "last_updated": datetime.utcnow()
            }}
        )

class TransactionModel:
    def __init__(self):
        self.collection = db_instance.db.transactions
    
    def record_transaction(self, unit_id, product_id, transaction_type, quantity, unit_price, performed_by, notes=""):
        """Record a transaction"""
        transaction_data = {
            "unit_id": unit_id,
            "product_id": product_id,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": quantity * unit_price,
            "performed_by": performed_by,
            "timestamp": datetime.utcnow(),
            "notes": notes
        }
        
        result = self.collection.insert_one(transaction_data)
        return str(result.inserted_id)
    
    def get_transactions_by_unit(self, unit_id, limit=100):
        """Get recent transactions for unit"""
        return list(self.collection.find({"unit_id": unit_id})
                   .sort("timestamp", -1)
                   .limit(limit))

# Initialize model instances
user_model = UserModel()
unit_model = UnitModel()
product_model = ProductModel()
transaction_model = TransactionModel()