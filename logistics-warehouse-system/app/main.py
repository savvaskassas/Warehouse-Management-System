"""
Main Flask application
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Import models after app creation to avoid circular imports
from .models import user_model, unit_model, product_model, transaction_model
from .database import db_instance

# Initialize database and admin user
from .init_db import initialize_database, check_database_health

# Initialize database on startup
def setup_database():
    """Setup database and admin user"""
    print("\n" + "="*50)
    print("🏗️  LOGISTICS WAREHOUSE SYSTEM STARTUP")
    print("="*50)
    
    # Check database health
    if check_database_health():
        # Initialize admin and default data
        initialize_database()
    
    print("="*50 + "\n")

# Call setup on import
setup_database()

# Import and register blueprints
from .admin_routes import admin_bp
from .supervisor_routes import supervisor_bp
from .employee_routes import employee_bp

app.register_blueprint(admin_bp)
app.register_blueprint(supervisor_bp)
app.register_blueprint(employee_bp)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        return login()
    
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        unit_id = request.form.get('unit_id')  # Optional for admin
        
        # Authenticate user
        if username == 'admin':
            user = user_model.authenticate_user(username, password)
        else:
            user = user_model.authenticate_user(username, password, unit_id)
        
        if user:
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user['role']
            session['unit_id'] = user['unit_id']
            session['name'] = user['name']
            session['surname'] = user['surname']
            
            flash(f'Καλώς ήρθατε, {user["name"]} {user["surname"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Λάθος στοιχεία σύνδεσης!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Αποσυνδεθήκατε επιτυχώς!', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard - redirects based on role"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'supervisor':
        return redirect(url_for('supervisor_dashboard'))
    elif role == 'employee':
        return redirect(url_for('employee_dashboard'))
    else:
        flash('Άγνωστος ρόλος χρήστη!', 'error')
        return redirect(url_for('logout'))

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    if session.get('role') != 'admin':
        flash('Δεν έχετε δικαίωμα πρόσβασης!', 'error')
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('admin.dashboard'))

@app.route('/supervisor')
def supervisor_dashboard():
    """Supervisor dashboard"""
    if session.get('role') not in ['supervisor', 'admin']:
        flash('Δεν έχετε δικαίωμα πρόσβασης!', 'error')
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('supervisor.dashboard'))

@app.route('/employee')
def employee_dashboard():
    """Employee dashboard"""
    if session.get('role') not in ['employee', 'supervisor', 'admin']:
        flash('Δεν έχετε δικαίωμα πρόσβασης!', 'error')
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('employee.dashboard'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = user_model.get_user_by_username(session['username'])
    unit_info = None
    if user.get('unit_id'):
        unit_info = unit_model.get_unit_by_id(user['unit_id'])
    
    if request.method == 'POST':
        # Update profile information
        employee_name = request.form.get('employee_name', '').strip()
        employee_phone = request.form.get('employee_phone', '').strip()
        employee_email = request.form.get('employee_email', '').strip()
        employee_address = request.form.get('employee_address', '').strip()
        
        if not employee_name:
            flash('Το όνομα είναι υποχρεωτικό!', 'error')
        else:
            # Update profile
            update_data = {
                'employee_name': employee_name,
                'employee_phone': employee_phone,
                'employee_email': employee_email,
                'employee_address': employee_address
            }
            
            if user_model.update_user_profile(session['username'], update_data):
                flash('Το προφίλ ενημερώθηκε επιτυχώς!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Σφάλμα κατά την ενημέρωση του προφίλ!', 'error')
    
    return render_template('profile.html', user=user, unit_info=unit_info)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """Change user password"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not all([current_password, new_password, confirm_password]):
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία!', 'error')
        elif new_password != confirm_password:
            flash('Οι νέοι κωδικοί δεν ταιριάζουν!', 'error')
        elif len(new_password) < 8:
            flash('Ο κωδικός πρέπει να έχει τουλάχιστον 8 χαρακτήρες!', 'error')
        else:
            # Verify current password
            if user_model.verify_password(session['username'], current_password):
                if user_model.update_password(session['username'], new_password):
                    flash('Ο κωδικός άλλαξε επιτυχώς! Παρακαλώ συνδεθείτε ξανά.', 'success')
                    session.clear()
                    return redirect(url_for('login'))
                else:
                    flash('Σφάλμα κατά την αλλαγή κωδικού!', 'error')
            else:
                flash('Λάθος τρέχων κωδικός!', 'error')
    
    return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)