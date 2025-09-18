"""
Supervisor routes for the Logistics Warehouse System
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from .models import user_model, unit_model, product_model, transaction_model
from .database import db_instance

supervisor_bp = Blueprint('supervisor', __name__, url_prefix='/supervisor')

def require_supervisor():
    """Decorator to require supervisor role or admin with temp unit access"""
    if session.get('role') not in ['supervisor', 'admin']:
        flash('Δεν έχετε δικαίωμα πρόσβασης!', 'error')
        return redirect(url_for('dashboard'))
    
    # Get unit_id (either from user or temp for admin)
    unit_id = session.get('temp_unit_id') if session.get('role') == 'admin' else session.get('unit_id')
    if not unit_id:
        flash('Δεν βρέθηκε αποθήκη!', 'error')
        return redirect(url_for('dashboard'))
    
    return None

def get_current_unit_id():
    """Get current unit ID for supervisor operations"""
    return session.get('temp_unit_id') if session.get('role') == 'admin' else session.get('unit_id')

@supervisor_bp.route('/')
def dashboard():
    """Supervisor dashboard"""
    check = require_supervisor()
    if check: return check
    
    unit_id = get_current_unit_id()
    unit_info = unit_model.get_unit_by_id(unit_id)
    
    if not unit_info:
        flash('Η αποθήκη δεν βρέθηκε!', 'error')
        return redirect(url_for('dashboard'))
    
    # Get employees in this unit
    employees = user_model.get_users_by_unit(unit_id)
    employees = [emp for emp in employees if emp['role'] == 'employee']
    
    # Get unit statistics
    unit_products = product_model.get_products_by_unit(unit_id)
    
    # Calculate financial summary
    financial_summary = product_model.calculate_unit_financial_summary(unit_id)
    
    # Calculate volume usage
    total_volume_used = 0
    for p in unit_products:
        if 'product_volume' in p and 'product_quantity' in p:
            total_volume_used += p['product_volume'] * p['product_quantity']
    
    volume_usage_percentage = (total_volume_used / unit_info['unit_volume'] * 100) if unit_info['unit_volume'] > 0 else 0
    
    return render_template('supervisor/dashboard.html',
                         unit_info=unit_info,
                         employees=employees,
                         financial_summary=financial_summary,
                         volume_usage_percentage=volume_usage_percentage,
                         employee_count=len(employees),
                         is_admin_access=session.get('role') == 'admin')

@supervisor_bp.route('/create_employee', methods=['GET', 'POST'])
def create_employee():
    """Create new employee"""
    check = require_supervisor()
    if check: return check
    
    unit_id = get_current_unit_id()
    unit_info = unit_model.get_unit_by_id(unit_id)
    
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        
        # Generate username (name.surname.unitid)
        username = f"{name.lower()}.{surname.lower()}.{unit_id}"
        
        if user_model.get_user_by_username(username):
            flash('Το όνομα χρήστη υπάρχει ήδη!', 'error')
        elif all([name, surname, password]):
            user_model.create_user(username, password, name, surname, 'employee', unit_id)
            flash(f'Ο υπάλληλος "{name} {surname}" δημιουργήθηκε επιτυχώς! Username: {username}', 'success')
            return redirect(url_for('supervisor.view_employees'))
        else:
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία!', 'error')
    
    return render_template('supervisor/create_employee.html', unit_info=unit_info)

@supervisor_bp.route('/employees')
def view_employees():
    """View and manage employees"""
    check = require_supervisor()
    if check: return check
    
    unit_id = get_current_unit_id()
    employees = user_model.get_users_by_unit(unit_id)
    employees = [emp for emp in employees if emp['role'] == 'employee']
    
    unit_info = unit_model.get_unit_by_id(unit_id)
    
    return render_template('supervisor/view_employees.html', 
                         employees=employees, 
                         unit_info=unit_info,
                         is_admin_access=session.get('role') == 'admin')

@supervisor_bp.route('/delete_employee/<username>')
def delete_employee(username):
    """Delete employee"""
    check = require_supervisor()
    if check: return check
    
    employee = user_model.get_user_by_username(username)
    unit_id = get_current_unit_id()
    
    # Verify employee belongs to this unit
    if not employee or employee['unit_id'] != unit_id or employee['role'] != 'employee':
        flash('Ο υπάλληλος δεν βρέθηκε ή δεν ανήκει στην αποθήκη σας!', 'error')
        return redirect(url_for('supervisor.view_employees'))
    
    user_model.delete_user(username)
    flash('Ο υπάλληλος διαγράφηκε επιτυχώς!', 'success')
    return redirect(url_for('supervisor.view_employees'))

@supervisor_bp.route('/change_employee_password/<username>', methods=['GET', 'POST'])
def change_employee_password(username):
    """Change employee password"""
    check = require_supervisor()
    if check: return check
    
    employee = user_model.get_user_by_username(username)
    unit_id = get_current_unit_id()
    
    # Verify employee belongs to this unit
    if not employee or employee['unit_id'] != unit_id or employee['role'] != 'employee':
        flash('Ο υπάλληλος δεν βρέθηκε ή δεν ανήκει στην αποθήκη σας!', 'error')
        return redirect(url_for('supervisor.view_employees'))
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Οι κωδικοί δεν ταιριάζουν!', 'error')
        elif new_password:
            user_model.update_password(username, new_password)
            flash('Ο κωδικός άλλαξε επιτυχώς!', 'success')
            return redirect(url_for('supervisor.view_employees'))
        else:
            flash('Παρακαλώ εισάγετε κωδικό!', 'error')
    
    return render_template('supervisor/change_employee_password.html', 
                         employee=employee,
                         is_admin_access=session.get('role') == 'admin')

@supervisor_bp.route('/statistics')
def unit_statistics():
    """View unit statistics"""
    check = require_supervisor()
    if check: return check
    
    unit_id = get_current_unit_id()
    unit_info = unit_model.get_unit_by_id(unit_id)
    
    # Get detailed statistics
    unit_products = product_model.get_products_by_unit(unit_id)
    employees = user_model.get_users_by_unit(unit_id)
    employees = [emp for emp in employees if emp['role'] == 'employee']
    
    # Calculate financial summary
    financial_summary = product_model.calculate_unit_financial_summary(unit_id)
    
    # Calculate volume usage
    total_volume_used = 0
    for p in unit_products:
        if 'product_volume' in p and 'product_quantity' in p:
            total_volume_used += p['product_volume'] * p['product_quantity']
    
    volume_usage_percentage = (total_volume_used / unit_info['unit_volume'] * 100) if unit_info['unit_volume'] > 0 else 0
    
    # Get recent transactions
    recent_transactions = transaction_model.get_transactions_by_unit(unit_id, 20)
    
    return render_template('supervisor/statistics.html',
                         unit_info=unit_info,
                         products=unit_products,
                         employees=employees,
                         financial_summary=financial_summary,
                         total_volume_used=total_volume_used,
                         volume_usage_percentage=volume_usage_percentage,
                         employee_count=len(employees),
                         recent_transactions=recent_transactions,
                         is_admin_access=session.get('role') == 'admin')

@supervisor_bp.route('/purchase_product/<product_id>', methods=['GET', 'POST'])
def purchase_product(product_id):
    """Purchase product quantities"""
    check = require_supervisor()
    if check: return check
    
    unit_id = get_current_unit_id()
    product = product_model.get_product_details(unit_id, product_id)
    
    if not product:
        flash('Το προϊόν δεν βρέθηκε!', 'error')
        return redirect(url_for('employee.view_products'))
    
    if request.method == 'POST':
        try:
            quantity = int(request.form['quantity'])
            if quantity <= 0:
                flash('Η ποσότητα πρέπει να είναι μεγαλύτερη από 0!', 'error')
            else:
                # Update product quantity
                success = product_model.update_product_quantity(
                    unit_id, product_id, quantity, 'purchase'
                )
                
                if success:
                    # Record transaction
                    transaction_model.record_transaction(
                        unit_id, product_id, 'purchase', quantity,
                        product['product_purchase_price'],
                        session['username'],
                        f"Αγορά {quantity} τεμαχίων"
                    )
                    
                    flash(f'Αγοράστηκαν επιτυχώς {quantity} τεμάχια του προϊόντος!', 'success')
                    return redirect(url_for('employee.view_product_details', product_id=product_id))
                else:
                    flash('Σφάλμα κατά την ενημέρωση του προϊόντος!', 'error')
        
        except ValueError:
            flash('Παρακαλώ εισάγετε έγκυρη ποσότητα!', 'error')
    
    return render_template('supervisor/purchase_product.html', 
                         product=product,
                         is_admin_access=session.get('role') == 'admin')

@supervisor_bp.route('/return_to_admin')
def return_to_admin():
    """Return to admin dashboard from temporary unit access"""
    if session.get('role') == 'admin':
        session.pop('temp_unit_id', None)
        session.pop('temp_unit_name', None)
        flash('Επιστροφή στον πίνακα διαχειριστή', 'info')
        return redirect(url_for('admin.dashboard'))
    else:
        return redirect(url_for('supervisor.dashboard'))