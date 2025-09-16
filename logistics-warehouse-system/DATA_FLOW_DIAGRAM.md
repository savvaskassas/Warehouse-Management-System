# Διάγραμμα Ροής Δεδομένων - Σύστημα Διαχείρισης Αποθηκών

## Περιγραφή Διαγράμματος Ροής

Το διάγραμμα ροής δεδομένων παρουσιάζει την κίνηση πληροφοριών μέσα στο σύστημα διαχείρισης αποθηκών, από την εισαγωγή δεδομένων μέχρι την επεξεργασία και παρουσίασή τους.

## Κύρια Στοιχεία Διαγράμματος

### 1. Εξωτερικές Οντότητες (External Entities)
- **Admin**: Διαχειριστής του συστήματος
- **Supervisor**: Προϊστάμενος αποθήκης
- **Employee**: Υπάλληλος αποθήκης
- **External Systems**: Εξωτερικά συστήματα (αναφορές, backup)

### 2. Διεργασίες (Processes)
- **P1: Authentication**: Επαλήθευση ταυτότητας χρηστών
- **P2: Unit Management**: Διαχείριση αποθηκών
- **P3: Product Management**: Διαχείριση προϊόντων
- **P4: User Management**: Διαχείριση χρηστών
- **P5: Transaction Processing**: Επεξεργασία συναλλαγών
- **P6: Statistics Generation**: Παραγωγή στατιστικών
- **P7: Inventory Control**: Έλεγχος αποθέματος

### 3. Αποθήκες Δεδομένων (Data Stores)
- **D1: Users Collection**: Στοιχεία χρηστών
- **D2: Units Collection**: Στοιχεία αποθηκών
- **D3: Products Master Collection**: Κεντρικός κατάλογος προϊόντων
- **D4: Unit Products Collection**: Προϊόντα ανά αποθήκη
- **D5: Transactions Collection**: Ιστορικό συναλλαγών

### 4. Ροές Δεδομένων (Data Flows)

#### Από Admin:
- **Login Credentials** → P1: Authentication
- **Unit Data** → P2: Unit Management
- **Product Data** → P3: Product Management
- **Supervisor Data** → P4: User Management

#### Από Supervisor:
- **Login Credentials** → P1: Authentication
- **Employee Data** → P4: User Management
- **Purchase Orders** → P5: Transaction Processing

#### Από Employee:
- **Login Credentials** → P1: Authentication
- **Sales Data** → P5: Transaction Processing
- **Search Queries** → P7: Inventory Control

#### Προς Αποθήκες Δεδομένων:
- P1 → **User Session Data** → D1: Users
- P2 → **Unit Information** → D2: Units
- P3 → **Product Catalog** → D3: Products Master
- P5 → **Transaction Records** → D5: Transactions
- P7 → **Inventory Updates** → D4: Unit Products

#### Από Αποθήκες Δεδομένων:
- D1 → **User Info** → P6: Statistics Generation
- D2 → **Unit Stats** → P6: Statistics Generation
- D4 → **Inventory Data** → P7: Inventory Control
- D5 → **Transaction History** → P6: Statistics Generation

## Χρησιμότητα του Διαγράμματος Ροής

### 1. Κατανόηση Συστήματος
- **Οπτικοποίηση**: Παρέχει οπτική αναπαράσταση της ροής δεδομένων
- **Επικοινωνία**: Διευκολύνει την επικοινωνία μεταξύ αναλυτών, προγραμματιστών και χρηστών
- **Τεκμηρίωση**: Αποτελεί μέρος της τεχνικής τεκμηρίωσης του συστήματος

### 2. Ανάλυση και Σχεδίαση
- **Εντοπισμός Προβλημάτων**: Βοηθά στον εντοπισμό πιθανών προβλημάτων στη ροή δεδομένων
- **Βελτιστοποίηση**: Επιτρέπει τον εντοπισμό σημείων για βελτιστοποίηση
- **Ασφάλεια**: Αναδεικνύει σημεία όπου απαιτούνται μέτρα ασφαλείας

### 3. Ανάπτυξη και Συντήρηση
- **Σχεδίαση API**: Καθοδηγεί τη σχεδίαση των API endpoints
- **Database Design**: Βοηθά στο σχεδιασμό της βάσης δεδομένων
- **Testing**: Προσδιορίζει σενάρια δοκιμών για τη ροή δεδομένων

### 4. Εκπαίδευση και Ενημέρωση
- **Νέοι Προγραμματιστές**: Διευκολύνει την κατανόηση του συστήματος από νέα μέλη
- **Stakeholders**: Βοηθά στην ενημέρωση των εμπλεκομένων μερών
- **Αλλαγές**: Αναδεικνύει τις επιπτώσεις των αλλαγών στο σύστημα

## Σημείωση
Αυτό το διάγραμμα αντιπροσωπεύει τη λογική ροή δεδομένων και όχι την φυσική αρχιτεκτονική του συστήματος. Στην πραγματικότητα, όλες οι διεργασίες εκτελούνται εντός της Flask εφαρμογής και όλες οι αποθήκες δεδομένων βρίσκονται στη MongoDB βάση δεδομένων.