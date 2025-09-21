# 🏗️ Σύστημα Διαχείρισης Βιομηχανικών Αποθηκών

Ένα πλήρως λειτουργικό πληροφοριακό σύστημα για τη διαχείριση βιομηχανικών αποθηκών, υλοποιημένο με Flask, MongoDB και Docker.

## 📋 Περιεχόμενα

- [Επιπλέον Παραδοχές και Παρεκκλίσεις](#επιπλέον-παραδοχές-και-παρεκκλίσεις)
- [Τεχνολογίες που Χρησιμοποιήθηκαν](#τεχνολογίες-που-χρησιμοποιήθηκαν)
- [Περιγραφή Αρχείων](#περιγραφή-αρχείων)
- [Βάση Δεδομένων](#βάση-δεδομένων)
- [Τρόπος Εκτέλεσης](#τρόπος-εκτέλεσης)
- [Τρόπος Χρήσης](#τρόπος-χρήσης)
- [Αναφορές](#αναφορές)

## 🔧 Επιπλέον Παραδοχές και Παρεκκλίσεις από την Εκφώνηση

### Παραδοχές Σχεδιασμού

1. **Ρόλοι Χρηστών**: Οι Supervisors θεωρούνται επίσης Employees σύμφωνα με την εκφώνηση
2. **Product IDs**: Αυτόματη δημιουργία με format "P0001", "P0002", κλπ.
3. **Unit IDs**: Αυτόματη δημιουργία με format "001", "002", κλπ.
4. **Κέρδη/Ζημίες**: Διαχωρισμός σε πραγματοποιηθέντα και δυνητικά κέρδη
5. **Όγκος Αποθήκης**: Υπολογισμός βάσει product_volume × product_quantity

### Επιπλέον Χαρακτηριστικά (Bonus Features)

Πέρα από τις βασικές απαιτήσεις της εκφώνησης, το σύστημα περιλαμβάνει:

- **Modern UI**: Bootstrap 5 για καλύτερη user experience
- **Διαγράμματα**: Chart.js για οπτική αναπαράσταση δεδομένων
- **Real-time Updates**: Αυτόματη ενημέρωση δεδομένων
- **Enhanced Security**: Bcrypt hashing, session management
- **Performance Optimizations**: Database indexing, optimized queries
- **Advanced Analytics**: ROI calculations, profit margins
- **Responsive Design**: Mobile-friendly interface

### Παρεκκλίσεις

**Καμία παρέκκλιση από την εκφώνηση** - όλες οι απαιτήσεις καλύπτονται πλήρως.

## 🛠️ Τεχνολογίες που Χρησιμοποιήθηκαν

### Backend
- **Python 3.9**: Κύρια γλώσσα προγραμματισμού
- **Flask 2.3.3**: Web framework για το REST API
- **PyMongo 4.5.0**: MongoDB driver για Python
- **bcrypt 4.0.1**: Password hashing
- **python-dotenv 1.0.0**: Environment variables management

### Frontend
- **Jinja2**: Template engine (μέρος του Flask)
- **Bootstrap 5.3.0**: CSS framework για responsive design
- **Chart.js 3.9.1**: JavaScript library για διαγράμματα
- **Font Awesome 6.4.0**: Icons library

### Database
- **MongoDB 5.0**: NoSQL document database
- **Hybrid Schema Design**: Συνδυασμός σχεσιακής και μη-σχεσιακής προσέγγισης

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Docker Volume**: Data persistence

## 📁 Περιγραφή Αρχείων

```
logistics-warehouse-system/
├── compose.yaml                 # Docker Compose configuration
├── Dockerfile                   # Docker image definition
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
├── data/                        # MongoDB data volume
└── app/                         # Application source code
    ├── __init__.py             # Package initialization
    ├── main.py                 # Main Flask application & routes
    ├── database.py             # MongoDB connection & initialization
    ├── models.py               # Data models & business logic
    ├── admin_routes.py         # Admin-specific routes
    ├── supervisor_routes.py    # Supervisor-specific routes
    ├── employee_routes.py      # Employee-specific routes
    ├── static/                 # Static files (CSS, JS, images)
    └── templates/              # Jinja2 templates
        ├── base.html           # Base template
        ├── login.html          # Login page
        ├── profile.html        # User profile page
        ├── change_password.html # Password change page
        ├── admin/              # Admin templates
        │   ├── dashboard.html
        │   ├── view_units.html
        │   ├── create_unit.html
        │   ├── view_unit.html
        │   ├── edit_unit.html
        │   ├── view_supervisors.html
        │   ├── create_supervisor.html
        │   ├── change_supervisor_password.html
        │   ├── view_products.html
        │   ├── create_product.html
        │   ├── view_product.html
        │   ├── edit_product.html
        │   └── statistics.html
        ├── supervisor/         # Supervisor templates
        │   ├── dashboard.html
        │   ├── view_employees.html
        │   ├── create_employee.html
        │   ├── change_employee_password.html
        │   ├── purchase_product.html
        │   └── statistics.html
        └── employee/           # Employee templates
            ├── dashboard.html
            ├── view_products.html
            ├── view_product_details.html
            ├── product_details.html
            ├── sell_product.html
            └── quick_search.html
```

### Βασικά Αρχεία

#### `main.py`
Κύριο αρχείο εφαρμογής που περιέχει:
- Flask app initialization
- Session management
- Authentication & authorization
- Common routes (login, logout, profile, password change)
- Role-based access control

#### `database.py`
Διαχείριση βάσης δεδομένων:
- MongoDB connection setup
- Database indexes creation
- Default admin user creation
- Connection management

#### `models.py`
Business logic & data models:
- UserModel: User management (CRUD operations)
- UnitModel: Warehouse management
- ProductModel: Product management & financial calculations
- TransactionModel: Transaction logging

#### Route Files
- `admin_routes.py`: Admin-specific functionality
- `supervisor_routes.py`: Supervisor-specific functionality  
- `employee_routes.py`: Employee-specific functionality

## 🗄️ Βάση Δεδομένων

### MongoDB Collections

#### 1. `users` Collection
```javascript
{
  "_id": ObjectId,
  "username": "string",           // Unique username
  "password": "hashed_string",    // Bcrypt hashed password
  "name": "string",              // First name
  "surname": "string",           // Last name
  "role": "admin|supervisor|employee",
  "unit_id": "string|null",      // Associated warehouse (null for admin)
  "employee_username": "string", // Same as username (legacy field)
  "employee_name": "string",     // Full name
  "employee_unit": "string",     // Same as unit_id (legacy field)
  "employee_phone": "string",    // Phone number
  "employee_email": "string",    // Email address
  "employee_address": "string",  // Address
  "last_login": Date,           // Last login timestamp
  "created_at": Date,           // Creation timestamp
  "updated_at": Date            // Last update timestamp
}
```

**Παράδειγμα:**
```javascript
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d0"),
  "username": "admin",
  "password": "$2b$12$...", // bcrypt hash
  "name": "System",
  "surname": "Administrator",
  "role": "admin",
  "unit_id": null,
  "created_at": ISODate("2025-09-17T10:00:00Z")
}
```

#### 2. `units` Collection
```javascript
{
  "_id": ObjectId,
  "unit_id": "string",           // Unique unit identifier (001, 002, etc.)
  "unit_name": "string",         // Warehouse name
  "unit_volume": Number,         // Total storage volume (m³)
  "created_at": Date,           // Creation timestamp
  "updated_at": Date            // Last update timestamp
}
```

**Παράδειγμα:**
```javascript
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d1"),
  "unit_id": "001",
  "unit_name": "Αποθήκη Κεντρικής Αθήνας",
  "unit_volume": 1000.0,
  "created_at": ISODate("2025-09-17T10:30:00Z")
}
```

#### 3. `products_master` Collection
```javascript
{
  "_id": ObjectId,
  "product_id": "string",            // Unique product ID (P0001, P0002, etc.)
  "product_name": "string",          // Product name
  "product_weight": Number,          // Weight per unit (kg)
  "product_volume": Number,          // Volume per unit (m³)
  "product_category": "string",      // Product category
  "product_purchase_price": Number,  // Purchase price per unit (€)
  "product_selling_price": Number,   // Selling price per unit (€)
  "product_manufacturer": "string"   // Manufacturer name
}
```

**Παράδειγμα:**
```javascript
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d2"),
  "product_id": "P0001",
  "product_name": "Laptop Dell Inspiron",
  "product_weight": 2.5,
  "product_volume": 0.008,
  "product_category": "Ηλεκτρονικά",
  "product_purchase_price": 500.00,
  "product_selling_price": 650.00,
  "product_manufacturer": "Dell"
}
```

#### 4. `unit_products` Collection
```javascript
{
  "_id": ObjectId,
  "unit_id": "string",              // Reference to units.unit_id
  "product_id": "string",           // Reference to products_master.product_id
  "product_quantity": Number,       // Current stock quantity
  "product_unit_gain": Number       // Total profit/loss for this product in this unit
}
```

**Παράδειγμα:**
```javascript
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d3"),
  "unit_id": "001",
  "product_id": "P0001",
  "product_quantity": 25,
  "product_unit_gain": 750.00    // 5 units sold × (650-500) profit = 750€
}
```

#### 5. `transactions` Collection
```javascript
{
  "_id": ObjectId,
  "unit_id": "string",              // Warehouse where transaction occurred
  "product_id": "string",           // Product involved
  "transaction_type": "sale|purchase", // Type of transaction
  "quantity": Number,               // Quantity involved
  "unit_price": Number,            // Price per unit
  "total_amount": Number,          // Total transaction amount
  "performed_by": "string",        // Username who performed the transaction
  "timestamp": Date,               // Transaction timestamp
  "notes": "string"                // Additional notes
}
```

**Παράδειγμα:**
```javascript
{
  "_id": ObjectId("64f8a1b2c3d4e5f6a7b8c9d4"),
  "unit_id": "001",
  "product_id": "P0001",
  "transaction_type": "sale",
  "quantity": 2,
  "unit_price": 650.00,
  "total_amount": 1300.00,
  "performed_by": "employee1",
  "timestamp": ISODate("2025-09-18T14:30:00Z"),
  "notes": "Πώληση σε εταιρικό πελάτη"
}
```

### Database Indexing

Για βελτίωση απόδοσης:
```javascript
// Users collection
db.users.createIndex({"username": 1}, {unique: true})
db.users.createIndex({"unit_id": 1})

// Units collection  
db.units.createIndex({"unit_id": 1}, {unique: true})

// Products master collection
db.products_master.createIndex({"product_id": 1}, {unique: true})
db.products_master.createIndex({"product_name": 1})

// Unit products collection
db.unit_products.createIndex({"unit_id": 1, "product_id": 1}, {unique: true})
db.unit_products.createIndex({"unit_id": 1})

// Transactions collection
db.transactions.createIndex({"unit_id": 1})
db.transactions.createIndex({"product_id": 1})
db.transactions.createIndex({"timestamp": -1})
```

## 🚀 Τρόπος Εκτέλεσης Συστήματος

### Προαπαιτούμενα

1. **Docker & Docker Compose**: Εγκατάσταση του Docker Desktop
2. **Git**: Για clone του repository
3. **Port Availability**: Ports 5000 και 27017 πρέπει να είναι διαθέσιμοι

### Βήματα Εκτέλεσης

#### 1. Clone του Repository
```bash
git clone https://github.com/savvaskassas/YpoxreotikiErgasiaSept25_-20067_KASSAS_SAVVAS.git
cd YpoxreotikiErgasiaSept25_-20067_KASSAS_SAVVAS
```

#### 2. Εκτέλεση με Docker Compose
```bash
docker compose up -d --build
```

**Εξήγηση των παραμέτρων:**
- `up`: Εκκίνηση των containers
- `-d`: Detached mode (background execution)
- `--build`: Rebuild των images αν χρειάζεται

#### 3. Επαλήθευση Εκτέλεσης
```bash
# Έλεγχος κατάστασης containers
docker compose ps

# Έλεγχος logs
docker compose logs web
docker compose logs mongo
```

**Αναμενόμενη έξοδος:**
```bash
NAME                               COMMAND                  SERVICE   STATUS    PORTS
logistics-warehouse-system-web-1   "python -m flask run…"   web       Up        0.0.0.0:5000->5000/tcp
logistics-warehouse-system-mongo-1 "docker-entrypoint.s…"   mongo     Up        0.0.0.0:27017->27017/tcp
```

#### 4. Πρόσβαση στο Σύστημα
- **URL**: http://localhost:5000
- **Admin Credentials**: 
  - Username: `admin`
  - Password: `admin123`

### Διαχείριση Συστήματος

#### Διακοπή Συστήματος
```bash
docker compose down
```

#### Επανεκκίνηση
```bash
docker compose restart
```

#### Καθαρισμός (Διαγραφή δεδομένων)
```bash
docker compose down -v
docker system prune -f
```

#### Backup Δεδομένων
```bash
# Backup της data directory
cp -r data/ backup-$(date +%Y%m%d)/
```

### Troubleshooting

#### Port Conflicts
```bash
# Εύρεση διεργασιών που χρησιμοποιούν τα ports
netstat -tulpn | grep :5000
netstat -tulpn | grep :27017

# Αλλαγή ports στο compose.yaml αν χρειάζεται
```

#### Container Logs
```bash
# Λεπτομερή logs
docker compose logs -f web
docker compose logs -f mongo

# Logs συγκεκριμένης περιόδου
docker compose logs --since="1h" web
```

## 💻 Τρόπος Χρήσης Συστήματος

### 1. 🔐 Σύνδεση στο Σύστημα

#### Για Administrators
1. Μεταβείτε στο http://localhost:5000
2. Χρησιμοποιήστε τα διαπιστευτήρια:
   - **Username**: `admin`
   - **Password**: `admin123`

#### Για Supervisors & Employees
1. Ο admin πρέπει πρώτα να δημιουργήσει τους λογαριασμούς
2. Σύνδεση με unit_id, username, password

**Παράδειγμα Σύνδεσης Supervisor:**
```
Unit ID: 001
Username: supervisor1
Password: [όπως ορίστηκε από admin]
```

### 2. 👑 Admin Λειτουργικότητες

#### Δημιουργία Αποθήκης
1. **Navigation**: Admin Dashboard → Διαχείριση → Νέα Αποθήκη
2. **Πληροφορίες**:
   - Όνομα: "Αποθήκη Θεσσαλονίκης"
   - Όγκος: 1500 (m³)
3. **Αποτέλεσμα**: Auto-generated unit_id (π.χ. "002")

#### Δημιουργία Προϊόντος
1. **Navigation**: Admin Dashboard → Προϊόντα → Νέο Προϊόν
2. **Παράδειγμα δεδομένων**:
   ```
   Όνομα: Smartphone Samsung Galaxy
   Βάρος: 0.2 kg
   Όγκος: 0.0001 m³
   Κατηγορία: Ηλεκτρονικά
   Τιμή Αγοράς: 400 €
   Τιμή Πώλησης: 550 €
   Κατασκευαστής: Samsung
   Αρχική Ποσότητα: 50
   ```
3. **Αποτέλεσμα**: Το προϊόν προστίθεται σε όλες τις αποθήκες

#### Δημιουργία Supervisor
1. **Navigation**: Admin Dashboard → Προϊστάμενοι → Νέος Προϊστάμενος
2. **Πληροφορίες**:
   ```
   Όνομα: Ιωάννης
   Επώνυμο: Παπαδόπουλος
   Unit ID: 001
   Password: supervisor123
   ```

#### Στατιστικά Εταιρείας
- **Συνολικά Κέρδη**: €15,750.50
- **Χρήση Όγκου**: 45.2% (1,356 m³ από 3,000 m³)
- **Πλήθος Εργαζομένων**: 25 (συμπεριλαμβανομένων supervisors)

### 3. 👔 Supervisor Λειτουργικότητες

#### Δημιουργία Employee
1. **Login**: ως supervisor στην αποθήκη του
2. **Navigation**: Supervisor Dashboard → Υπάλληλοι → Νέος Υπάλληλος
3. **Πληροφορίες**:
   ```
   Όνομα: Μαρία
   Επώνυμο: Γεωργίου
   Password: employee123
   ```

#### Αγορά Προϊόντων
1. **Navigation**: Προϊόντα → [Επιλογή Προϊόντος] → Αγορά
2. **Παράδειγμα**:
   ```
   Προϊόν: P0001 (Laptop Dell)
   Ποσότητα: 10 τεμάχια
   Τιμή: 500 € ανά τεμάχιο
   Σύνολο: 5,000 €
   ```
3. **Αποτέλεσμα**: Ενημέρωση product_quantity (+10)

#### Στατιστικά Αποθήκης
- **Κέρδη Αποθήκης**: €3,250.00
- **Χρήση Όγκου**: 67.8%
- **Πλήθος Υπαλλήλων**: 8
- **Διαγράμματα**: Pie chart κατανομής κερδών ανά κατηγορία

### 4. 👨‍💼 Employee Λειτουργικότητες

#### Προβολή Προϊόντων
1. **Navigation**: Employee Dashboard → Προϊόντα
2. **Αναζήτηση**:
   ```
   Αναζήτηση: "laptop"
   Ταξινόμηση: Όνομα (Α-Ω)
   Φίλτρο Ποσότητας: 1-100 τεμάχια
   ```

#### Πώληση Προϊόντων
1. **Navigation**: Προϊόντα → [Επιλογή Προϊόντος] → Πώληση
2. **Παράδειγμα συναλλαγής**:
   ```
   Προϊόν: P0001 (Laptop Dell)
   Διαθέσιμη Ποσότητα: 25 τεμάχια
   Ποσότητα Πώλησης: 3 τεμάχια
   Τιμή Πώλησης: 650 € ανά τεμάχιο
   Συνολικό Ποσό: 1,950 €
   Κέρδος: 3 × (650-500) = 450 €
   ```
3. **Αποτέλεσμα**: 
   - product_quantity: 25 → 22
   - product_unit_gain: +450 €

#### Αναζήτηση Προϊόντων
**Βασική Αναζήτηση:**
```
Κείμενο: "Samsung"
Αποτελέσματα: Όλα τα προϊόντα που περιέχουν "Samsung"
```

**Προχωρημένη Αναζήτηση:**
```
Product ID: P0001
Ή
Ποσότητα από: 10, έως: 50
Ταξινόμηση: Ποσότητα (Φθίνουσα)
```

### 5. 📊 Παραδείγματα Αναφορών

#### Admin Dashboard
```
┌─────────────────────────────────────┐
│ Συνολικά Στατιστικά                 │
├─────────────────────────────────────┤
│ Πραγματοποιηθέν Κέρδος: €15,750.50  │
│ Δυνητικό Κέρδος: €23,890.75         │
│ Χρήση Όγκου: 45.2%                 │
│ Συνολικοί Εργαζόμενοι: 25           │
└─────────────────────────────────────┘

Πρόσφατες Αποθήκες:
001 | Κεντρική Αθήνα    | 1000.0 m³ | €3,250.00
002 | Θεσσαλονίκη       | 1500.0 m³ | €5,125.25
003 | Πάτρα             | 500.0 m³  | €1,875.75
```

#### Supervisor Statistics
```
┌─────────────────────────────────────┐
│ Στατιστικά Αποθήκης 001             │
├─────────────────────────────────────┤
│ Πραγματοποιηθέν Κέρδος: €3,250.00   │
│ Επένδυση Αποθέματος: €12,500.00     │
│ Πιθανά Έσοδα: €16,250.00           │
│ Δυνητικό Κέρδος: €3,750.00         │
│ Χρήση Όγκου: 67.8% (678/1000 m³)   │
│ Υπάλληλοι: 8                       │
└─────────────────────────────────────┘
```

### 6. 🛠️ Διαχείριση Προφίλ

#### Αλλαγή Κωδικού
1. **Navigation**: [Όνομα Χρήστη] → Αλλαγή Κωδικού
2. **Διαδικασία**:
   ```
   Τρέχων Κωδικός: [παλιός κωδικός]
   Νέος Κωδικός: [νέος κωδικός]
   Επιβεβαίωση: [νέος κωδικός]
   ```
3. **Αποτέλεσμα**: Αυτόματη αποσύνδεση και redirect στο login

#### Ενημέρωση Προφίλ
1. **Navigation**: [Όνομα Χρήστη] → Προφίλ
2. **Επεξεργάσιμα πεδία**:
   ```
   Τηλέφωνο: +30 210 1234567
   Email: user@company.com
   Διεύθυνση: Αθήνα, Ελλάδα
   ```

### 7. 🔍 Error Handling & Validation

#### Κοινά Μηνύματα Σφάλματος
```
❌ "Δεν έχετε δικαίωμα πρόσβασης!"
❌ "Μη έγκυρα στοιχεία σύνδεσης!"
❌ "Δεν υπάρχει αρκετό απόθεμα!"
❌ "Το όνομα χρήστη υπάρχει ήδη!"
✅ "Η λειτουργία ολοκληρώθηκε επιτυχώς!"
```

#### Validation Rules
- **Passwords**: Minimum 3 χαρακτήρες
- **Quantities**: Θετικοί αριθμοί
- **Prices**: Θετικοί αριθμοί με 2 δεκαδικά
- **Volume**: Θετικός αριθμός
- **Names**: Μη κενά strings

## 📚 Αναφορές

### Επίσημη Τεκμηρίωση
1. **Flask Documentation**: https://flask.palletsprojects.com/
2. **MongoDB Manual**: https://docs.mongodb.com/
3. **Docker Documentation**: https://docs.docker.com/
4. **Jinja2 Documentation**: https://jinja.palletsprojects.com/
5. **Bootstrap Documentation**: https://getbootstrap.com/docs/

### Python Libraries
1. **PyMongo**: https://pymongo.readthedocs.io/
2. **bcrypt**: https://pypi.org/project/bcrypt/
3. **python-dotenv**: https://pypi.org/project/python-dotenv/

### Frontend Libraries
1. **Chart.js**: https://www.chartjs.org/
2. **Font Awesome**: https://fontawesome.com/

### Tutorials & Resources
1. **Flask Mega-Tutorial**: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
2. **MongoDB University**: https://university.mongodb.com/
3. **Docker Getting Started**: https://docs.docker.com/get-started/

### Best Practices References
1. **Flask Best Practices**: https://flask.palletsprojects.com/en/2.3.x/patterns/
2. **MongoDB Schema Design**: https://docs.mongodb.com/manual/data-modeling/
3. **Security Best Practices**: https://owasp.org/

---

**Developed by**: Savvas Kassas  
**Student ID**: 20067  
**Course**: Πληροφοριακά Συστήματα  
**Date**: September 2025