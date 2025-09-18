"""
Admin routes for the Logistics Warehouse System
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from .models import user_model, unit_model, product_model, transaction_model
from .database import db_instance

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def require_admin():
    """Decorator to require admin role"""
    if session.get('role') != 'admin':
        flash('Δεν έχετε δικαίωμα πρόσβασης!', 'error')
        return redirect(url_for('dashboard'))
    return None

@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    check = require_admin()
    if check: return check
    
    # Get company statistics
    units = unit_model.get_all_units()
    supervisors = user_model.get_all_supervisors()
    
    # Calculate total profits and volume usage
    total_realized_gain = 0
    total_potential_gain = 0
    total_volume_used = 0
    total_volume_capacity = 0
    total_employees = 0
    
    for unit in units:
        # Get financial summary for each unit
        financial_summary = product_model.calculate_unit_financial_summary(unit['unit_id'])
        unit['financial_summary'] = financial_summary  # Add to unit object
        total_realized_gain += financial_summary['total_realized_gain']
        total_potential_gain += financial_summary['total_potential_gain']
        
        # Get unit products for volume calculations
        unit_products = product_model.get_products_by_unit(unit['unit_id'])
        
        # Calculate volume usage
        unit_volume_used = 0
        for p in unit_products:
            if 'product_volume' in p and 'product_quantity' in p:
                unit_volume_used += p['product_volume'] * p['product_quantity']
        
        total_volume_used += unit_volume_used
        total_volume_capacity += unit['unit_volume']
        
        # Count employees in this unit
        unit_employees = user_model.get_users_by_unit(unit['unit_id'])
        total_employees += len(unit_employees)
    
    # Add supervisors to employee count
    total_employees += len(supervisors)
    
    # Calculate volume usage percentage
    volume_usage_percentage = (total_volume_used / total_volume_capacity * 100) if total_volume_capacity > 0 else 0
    
    return render_template('admin/dashboard.html',
                         units=units,
                         supervisors=supervisors,
                         total_realized_gain=total_realized_gain,
                         total_potential_gain=total_potential_gain,
                         volume_usage_percentage=volume_usage_percentage,
                         total_employees=total_employees,
                         unit_count=len(units))

@admin_bp.route('/create_unit', methods=['GET', 'POST'])
def create_unit():
    """Create new warehouse unit"""
    check = require_admin()
    if check: return check
    
    if request.method == 'POST':
        unit_name = request.form['unit_name']
        unit_volume = float(request.form['unit_volume'])
        
        if unit_name and unit_volume > 0:
            unit_id = unit_model.create_unit(unit_name, unit_volume)
            
            # Add all existing products to this unit with 0 quantity
            products = list(db_instance.db.products_master.find())
            for product in products:
                product_model.add_product_to_unit(unit_id, product['product_id'], 0)
            
            flash(f'Η αποθήκη "{unit_name}" δημιουργήθηκε επιτυχώς με κωδικό {unit_id}!', 'success')
            return redirect(url_for('admin.view_units'))
        else:
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία σωστά!', 'error')
    
    return render_template('admin/create_unit.html')

@admin_bp.route('/units')
def view_units():
    """View and manage warehouse units"""
    check = require_admin()
    if check: return check
    
    units = unit_model.get_all_units()
    
    # Calculate financial summary for each unit
    for unit in units:
        financial_summary = product_model.calculate_unit_financial_summary(unit['unit_id'])
        unit['financial_summary'] = financial_summary
    
    return render_template('admin/view_units.html', units=units)

@admin_bp.route('/delete_unit/<unit_id>')
def delete_unit(unit_id):
    """Delete warehouse unit"""
    check = require_admin()
    if check: return check
    
    # Check if unit has employees or supervisors
    employees = user_model.get_users_by_unit(unit_id)
    if employees:
        flash('Δεν μπορείτε να διαγράψετε αποθήκη που έχει υπαλλήλους!', 'error')
        return redirect(url_for('admin.view_units'))
    
    # Delete unit products and unit
    db_instance.db.unit_products.delete_many({"unit_id": unit_id})
    db_instance.db.transactions.delete_many({"unit_id": unit_id})
    unit_model.delete_unit(unit_id)
    
    flash('Η αποθήκη διαγράφηκε επιτυχώς!', 'success')
    return redirect(url_for('admin.view_units'))

@admin_bp.route('/create_product', methods=['GET', 'POST'])
def create_product():
    """Create new product"""
    check = require_admin()
    if check: return check
    
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_weight = float(request.form['product_weight'])
        product_volume = float(request.form['product_volume'])
        product_category = request.form['product_category']
        product_purchase_price = float(request.form['product_purchase_price'])
        product_selling_price = float(request.form['product_selling_price'])
        product_manufacturer = request.form['product_manufacturer']
        initial_quantity = int(request.form.get('initial_quantity', 0))
        
        if all([product_name, product_weight >= 0, product_volume >= 0, 
                product_category, product_purchase_price >= 0, 
                product_selling_price >= 0, product_manufacturer]):
            
            product_id = product_model.create_product(
                product_name, product_weight, product_volume,
                product_category, product_purchase_price, 
                product_selling_price, product_manufacturer,
                initial_quantity
            )
            
            flash(f'Το προϊόν "{product_name}" δημιουργήθηκε επιτυχώς με κωδικό {product_id} και αρχική ποσότητα {initial_quantity}!', 'success')
            return redirect(url_for('admin.view_products'))
        else:
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία σωστά!', 'error')
    
    return render_template('admin/create_product.html')

@admin_bp.route('/products')
def view_products():
    """View all products"""
    check = require_admin()
    if check: return check
    
    # Get all master products
    products = list(db_instance.db.products_master.find())
    
    # Enrich with total quantities across all units
    for product in products:
        # Get total quantity across all units
        unit_products = list(db_instance.db.unit_products.find({
            "product_id": product["product_id"]
        }))
        
        total_quantity = sum(up.get("product_quantity", 0) for up in unit_products)
        
        product["total_quantity"] = total_quantity
    
    return render_template('admin/view_products.html', products=products)

@admin_bp.route('/create_supervisor', methods=['GET', 'POST'])
def create_supervisor():
    """Create new supervisor"""
    check = require_admin()
    if check: return check
    
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        unit_id = request.form['unit_id']
        
        # Generate username (name.surname.unitid)
        username = f"{name.lower()}.{surname.lower()}.{unit_id}"
        
        # Check if unit exists
        unit = unit_model.get_unit_by_id(unit_id)
        if not unit:
            flash('Η αποθήκη δεν υπάρχει!', 'error')
        elif user_model.get_user_by_username(username):
            flash('Το όνομα χρήστη υπάρχει ήδη!', 'error')
        elif all([name, surname, password, unit_id]):
            user_model.create_user(username, password, name, surname, 'supervisor', unit_id)
            flash(f'Ο προϊστάμενος "{name} {surname}" δημιουργήθηκε επιτυχώς! Username: {username}', 'success')
            return redirect(url_for('admin.view_supervisors'))
        else:
            flash('Παρακαλώ συμπληρώστε όλα τα πεδία!', 'error')
    
    units = unit_model.get_all_units()
    return render_template('admin/create_supervisor.html', units=units)

@admin_bp.route('/supervisors')
def view_supervisors():
    """View and manage supervisors"""
    check = require_admin()
    if check: return check
    
    supervisors = user_model.get_all_supervisors()
    
    # Add unit names to supervisors
    for supervisor in supervisors:
        if supervisor['unit_id']:
            unit = unit_model.get_unit_by_id(supervisor['unit_id'])
            supervisor['unit_name'] = unit['unit_name'] if unit else 'Άγνωστη'
        else:
            supervisor['unit_name'] = 'Καμία'
    
    return render_template('admin/view_supervisors.html', supervisors=supervisors)

@admin_bp.route('/delete_supervisor/<username>')
def delete_supervisor(username):
    """Delete supervisor"""
    check = require_admin()
    if check: return check
    
    user_model.delete_user(username)
    flash('Ο προϊστάμενος διαγράφηκε επιτυχώς!', 'success')
    return redirect(url_for('admin.view_supervisors'))

@admin_bp.route('/change_supervisor_password/<username>', methods=['GET', 'POST'])
def change_supervisor_password(username):
    """Change supervisor password"""
    check = require_admin()
    if check: return check
    
    supervisor = user_model.get_user_by_username(username)
    if not supervisor:
        flash('Ο προϊστάμενος δεν βρέθηκε!', 'error')
        return redirect(url_for('admin.view_supervisors'))
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Οι κωδικοί δεν ταιριάζουν!', 'error')
        elif new_password:
            user_model.update_password(username, new_password)
            flash('Ο κωδικός άλλαξε επιτυχώς!', 'success')
            return redirect(url_for('admin.view_supervisors'))
        else:
            flash('Παρακαλώ εισάγετε κωδικό!', 'error')
    
    return render_template('admin/change_supervisor_password.html', supervisor=supervisor)

@admin_bp.route('/access_unit/<unit_id>')
def access_unit_as_supervisor(unit_id):
    """Access unit with supervisor privileges"""
    check = require_admin()
    if check: return check
    
    unit = unit_model.get_unit_by_id(unit_id)
    if not unit:
        flash('Η αποθήκη δεν βρέθηκε!', 'error')
        return redirect(url_for('admin.view_units'))
    
    # Temporarily set admin as supervisor for this unit
    session['temp_unit_id'] = unit_id
    session['temp_unit_name'] = unit['unit_name']
    
    flash(f'Πρόσβαση ως προϊστάμενος στην αποθήκη "{unit["unit_name"]}"', 'info')
    return redirect(url_for('supervisor.dashboard'))

@admin_bp.route('/statistics')
def company_statistics():
    """View company-wide statistics"""
    check = require_admin()
    if check: return check
    
    # Get all units and calculate comprehensive statistics
    units = unit_model.get_all_units()
    supervisors = user_model.get_all_supervisors()
    
    # Initialize statistics containers
    total_realized_gain = 0
    total_potential_gain = 0
    total_volume_used = 0
    total_volume_capacity = 0
    total_employees = 0
    unit_financial_data = []
    product_categories = {}
    employee_performance = []
    monthly_sales = {}
    
    for unit in units:
        # Get financial summary for each unit
        financial_summary = product_model.calculate_unit_financial_summary(unit['unit_id'])
        total_realized_gain += financial_summary['total_realized_gain']
        total_potential_gain += financial_summary['total_potential_gain']
        
        # Store unit financial data
        unit_financial_data.append({
            'unit_name': unit['unit_name'],
            'unit_id': unit['unit_id'],
            'financial_summary': financial_summary
        })
        
        # Get unit products for other calculations
        unit_products = product_model.get_products_by_unit(unit['unit_id'])
        
        # Calculate volume usage
        unit_volume_used = 0
        for p in unit_products:
            if 'product_volume' in p and 'product_quantity' in p:
                unit_volume_used += p['product_volume'] * p['product_quantity']
            
            # Collect product categories
            category = p.get('product_category', 'Άλλα')
            if category in product_categories:
                product_categories[category] += p.get('product_quantity', 0)
            else:
                product_categories[category] = p.get('product_quantity', 0)
        
        total_volume_used += unit_volume_used
        total_volume_capacity += unit['unit_volume']
        
        # Count employees in this unit
        unit_employees = user_model.get_users_by_unit(unit['unit_id'])
        employees_only = [emp for emp in unit_employees if emp['role'] == 'employee']
        total_employees += len(employees_only)
        
        # Get employee performance (sales data from transactions)
        for employee in employees_only:
            # Get transactions performed by this employee
            employee_transactions = list(db_instance.db.transactions.find({
                "unit_id": unit['unit_id'],
                "performed_by": employee['username'],
                "transaction_type": "sale"
            }))
            
            total_sales = sum(t.get('total_amount', 0) for t in employee_transactions)
            total_quantity = sum(t.get('quantity', 0) for t in employee_transactions)
            
            if total_sales > 0:  # Only include employees with sales
                employee_performance.append({
                    'name': f"{employee['name']} {employee['surname']}",
                    'unit_name': unit['unit_name'],
                    'total_sales': total_sales,
                    'total_quantity': total_quantity,
                    'transactions_count': len(employee_transactions)
                })
    
    # Add supervisors to employee count
    total_employees += len(supervisors)
    
    # Calculate volume usage percentage
    volume_usage_percentage = (total_volume_used / total_volume_capacity * 100) if total_volume_capacity > 0 else 0
    
    # Get monthly sales data for charts
    from datetime import datetime, timedelta
    import calendar
    
    # Get transactions from last 12 months
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=365)
    
    transactions = list(db_instance.db.transactions.find({
        "timestamp": {"$gte": start_date, "$lte": end_date},
        "transaction_type": "sale"
    }))
    
    for transaction in transactions:
        month_key = transaction['timestamp'].strftime('%Y-%m')
        month_name = calendar.month_name[transaction['timestamp'].month] + ' ' + str(transaction['timestamp'].year)
        
        if month_key in monthly_sales:
            monthly_sales[month_key]['amount'] += transaction.get('total_amount', 0)
            monthly_sales[month_key]['quantity'] += transaction.get('quantity', 0)
        else:
            monthly_sales[month_key] = {
                'month_name': month_name,
                'amount': transaction.get('total_amount', 0),
                'quantity': transaction.get('quantity', 0)
            }
    
    # Sort employee performance by sales
    employee_performance.sort(key=lambda x: x['total_sales'], reverse=True)
    
    # Sort unit financial data
    unit_financial_data.sort(key=lambda x: x['financial_summary']['total_potential_gain'], reverse=True)
    
    # Sort monthly sales
    monthly_sales_list = sorted(monthly_sales.items(), key=lambda x: x[0])
    
    return render_template('admin/statistics.html',
                         units=units,
                         total_realized_gain=total_realized_gain,
                         total_potential_gain=total_potential_gain,
                         volume_usage_percentage=volume_usage_percentage,
                         total_employees=total_employees,
                         unit_financial_data=unit_financial_data,
                         product_categories=product_categories,
                         employee_performance=employee_performance[:10],  # Top 10
                         monthly_sales=monthly_sales_list,
                         unit_count=len(units))