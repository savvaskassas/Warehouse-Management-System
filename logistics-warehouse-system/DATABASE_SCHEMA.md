# Database Schema Design για LogisticsDB

## Collections Overview

### 1. users
Αποθηκεύει όλους τους χρήστες (Admin, Supervisors, Employees)
```json
{
  "_id": ObjectId,
  "username": "string", // Μοναδικό για κάθε χρήστη
  "password": "string", // Hashed password
  "name": "string",
  "surname": "string", 
  "role": "admin|supervisor|employee",
  "unit_id": "string", // null για admin, unit_id για supervisors/employees
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### 2. units (Αποθήκες)
Αποθηκεύει πληροφορίες για κάθε αποθήκη
```json
{
  "_id": ObjectId,
  "unit_id": "string", // Μοναδικός κωδικός αποθήκης
  "unit_name": "string",
  "unit_volume": number, // Συνολικός αποθηκευτικός χώρος
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### 3. products_master (Κεντρικός κατάλογος προϊόντων)
Κεντρικός κατάλογος όλων των προϊόντων της εταιρείας
```json
{
  "_id": ObjectId,
  "product_id": "string", // Μοναδικός κωδικός προϊόντος
  "product_name": "string",
  "product_weight": number,
  "product_volume": number,
  "product_category": "string",
  "product_purchase_price": number,
  "product_selling_price": number,
  "product_manufacturer": "string",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### 4. unit_products (Προϊόντα ανά αποθήκη)
Συνδέει προϊόντα με αποθήκες και διατηρεί τοπικές πληροφορίες
```json
{
  "_id": ObjectId,
  "unit_id": "string",
  "product_id": "string",
  "product_quantity": number,
  "product_sold_quantity": number, // Συνολικά πουλημένα
  "product_unit_gain": number, // Κέρδος/ζημία για αυτή την αποθήκη
  "last_updated": ISODate
}
```

### 5. transactions (Συναλλαγές)
Καταγραφή όλων των κινήσεων (αγορές, πωλήσεις)
```json
{
  "_id": ObjectId,
  "unit_id": "string",
  "product_id": "string",
  "transaction_type": "purchase|sale",
  "quantity": number,
  "unit_price": number,
  "total_amount": number,
  "performed_by": "string", // username του χρήστη
  "timestamp": ISODate,
  "notes": "string" // Προαιρετικό
}
```

## Indexes για Performance
- users: { "username": 1 }, { "unit_id": 1 }
- units: { "unit_id": 1 }
- products_master: { "product_id": 1 }, { "product_name": 1 }
- unit_products: { "unit_id": 1, "product_id": 1 }, { "unit_id": 1 }
- transactions: { "unit_id": 1 }, { "product_id": 1 }, { "timestamp": -1 }

## Πλεονεκτήματα αυτής της προσέγγισης:
1. Κεντρικός έλεγχος προϊόντων μέσω products_master
2. Ευελιξία στη διαχείριση των αποθηκών
3. Ιστορικό συναλλαγών για auditing
4. Αποδοτικές queries για στατιστικά
5. Εύκολη επεκτασιμότητα