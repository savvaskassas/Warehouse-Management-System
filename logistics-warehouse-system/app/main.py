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

@app.route('/profile')
def profile():
    """User profile"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = user_model.get_user_by_username(session['username'])
    unit_info = None
    if user['unit_id']:
        unit_info = unit_model.get_unit_by_id(user['unit_id'])
    
    return render_template('profile.html', user=user, unit_info=unit_info)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """Change user password"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Verify current password
        user = user_model.authenticate_user(session['username'], current_password, session.get('unit_id'))
        if not user:
            flash('Λάθος τρέχων κωδικός!', 'error')
        elif new_password != confirm_password:
            flash('Οι νέοι κωδικοί δεν ταιριάζουν!', 'error')
        else:
            user_model.update_password(session['username'], new_password)
            flash('Ο κωδικός άλλαξε επιτυχώς!', 'success')
            return redirect(url_for('profile'))
    
    return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)