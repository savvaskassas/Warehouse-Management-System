"""
Employee routes for the Logistics Warehouse System
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from .models import user_model, unit_model, product_model, transaction_model
from .database import db_instance

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

def require_employee():
    """Decorator to require employee, supervisor, or admin role"""
    if session.get('role') not in ['employee', 'supervisor', 'admin']:
        flash('Δεν έχετε δικαίωμα πρόσβασης!', 'error')
        return redirect(url_for('dashboard'))
    
    # Get unit_id (either from user or temp for admin)
    unit_id = get_current_unit_id()
    if not unit_id:
        flash('Δεν βρέθηκε αποθήκη!', 'error')
        return redirect(url_for('dashboard'))
    
    return None

def get_current_unit_id():
    """Get current unit ID for employee operations"""
    if session.get('role') == 'admin':
        return session.get('temp_unit_id')
    else:
        return session.get('unit_id')

@employee_bp.route('/')
def dashboard():
    """Employee dashboard"""
    check = require_employee()
    if check: return check
    
    unit_id = get_current_unit_id()
    unit_info = unit_model.get_unit_by_id(unit_id)
    
    if not unit_info:
        flash('Η αποθήκη δεν βρέθηκε!', 'error')
        return redirect(url_for('dashboard'))
    
    # Get recent products (top 10 by quantity)
    products = product_model.get_products_by_unit(
        unit_id, 
        sort_params={'field': 'product_quantity', 'order': -1}
    )[:10]
    
    return render_template('employee/dashboard.html',
                         unit_info=unit_info,
                         products=products,
                         is_supervisor=session.get('role') in ['supervisor', 'admin'])

@employee_bp.route('/products')
def view_products():
    """View products in warehouse with search and sort"""
    check = require_employee()
    if check: return check
    
    unit_id = get_current_unit_id()
    unit_info = unit_model.get_unit_by_id(unit_id)
    
    # Get search and sort parameters
    search_params = {}
    sort_params = None
    
    # Search filters
    if request.args.get('product_name'):
        search_params['product_name'] = request.args.get('product_name')
    
    if request.args.get('product_id'):
        search_params['product_id'] = request.args.get('product_id')
    
    if request.args.get('quantity_min'):
        try:
            search_params['quantity_min'] = int(request.args.get('quantity_min'))
        except ValueError:
            pass
    
    if request.args.get('quantity_max'):
        try:
            search_params['quantity_max'] = int(request.args.get('quantity_max'))
        except ValueError:
            pass
    
    # Sort parameters
    sort_field = request.args.get('sort_field', 'product_name')
    sort_order = int(request.args.get('sort_order', 1))  # 1 for ascending, -1 for descending
    
    if sort_field in ['product_name', 'product_quantity', 'product_sold_quantity']:
        sort_params = {'field': sort_field, 'order': sort_order}
    
    # Get products
    products = product_model.get_products_by_unit(unit_id, search_params, sort_params)
    
    return render_template('employee/view_products.html',
                         products=products,
                         unit_info=unit_info,
                         search_params=request.args,
                         is_supervisor=session.get('role') in ['supervisor', 'admin'])

@employee_bp.route('/product/<product_id>')
def view_product_details(product_id):
    """View detailed product information"""
    check = require_employee()
    if check: return check
    
    unit_id = get_current_unit_id()
    product = product_model.get_product_details(unit_id, product_id)
    
    if not product:
        flash('Το προϊόν δεν βρέθηκε!', 'error')
        return redirect(url_for('employee.view_products'))
    
    # Get recent transactions for this product
    recent_transactions = list(db_instance.db.transactions.find({
        "unit_id": unit_id,
        "product_id": product_id
    }).sort("timestamp", -1).limit(10))
    
    return render_template('employee/product_details.html',
                         product=product,
                         recent_transactions=recent_transactions,
                         is_supervisor=session.get('role') in ['supervisor', 'admin'])

@employee_bp.route('/sell_product/<product_id>', methods=['GET', 'POST'])
def sell_product(product_id):
    """Sell product quantities"""
    check = require_employee()
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
            elif quantity > product['product_quantity']:
                flash(f'Δεν υπάρχει αρκετή ποσότητα! Διαθέσιμα: {product["product_quantity"]} τεμάχια', 'error')
            else:
                # Update product quantity
                success = product_model.update_product_quantity(
                    unit_id, product_id, quantity, 'sale'
                )
                
                if success:
                    # Record transaction
                    transaction_model.record_transaction(
                        unit_id, product_id, 'sale', quantity,
                        product['product_selling_price'],
                        session['username'],
                        f"Πώληση {quantity} τεμαχίων"
                    )
                    
                    flash(f'Πουλήθηκαν επιτυχώς {quantity} τεμάχια του προϊόντος!', 'success')
                    return redirect(url_for('employee.view_product_details', product_id=product_id))
                else:
                    flash('Σφάλμα κατά την ενημέρωση του προϊόντος!', 'error')
        
        except ValueError:
            flash('Παρακαλώ εισάγετε έγκυρη ποσότητα!', 'error')
    
    return render_template('employee/sell_product.html', 
                         product=product,
                         is_supervisor=session.get('role') in ['supervisor', 'admin'])

@employee_bp.route('/search_products')
def search_products_api():
    """API endpoint for product search (AJAX)"""
    check = require_employee()
    if check: return check
    
    unit_id = get_current_unit_id()
    search_term = request.args.get('q', '')
    
    if len(search_term) < 2:
        return jsonify([])
    
    # Search by name or ID
    search_params = {}
    if search_term.startswith('P') and search_term[1:].isdigit():
        # Search by product ID
        search_params['product_id'] = search_term
    else:
        # Search by name
        search_params['product_name'] = search_term
    
    products = product_model.get_products_by_unit(unit_id, search_params)
    
    # Return simplified product data for AJAX
    results = []
    for product in products[:10]:  # Limit to 10 results
        results.append({
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'product_quantity': product['product_quantity'],
            'product_category': product.get('product_category', 'N/A')
        })
    
    return jsonify(results)

@employee_bp.route('/product_categories')
def get_product_categories():
    """Get all product categories for filtering"""
    check = require_employee()
    if check: return check
    
    categories = list(db_instance.db.products_master.distinct('product_category'))
    return jsonify(categories)

@employee_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """View and edit employee profile"""
    check = require_employee()
    if check: return check
    
    current_user = user_model.get_user_by_username(session['username'])
    
    if not current_user:
        flash('Το προφίλ δεν βρέθηκε!', 'error')
        return redirect(url_for('employee.dashboard'))
    
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
                return redirect(url_for('employee.profile'))
            else:
                flash('Σφάλμα κατά την ενημέρωση του προφίλ!', 'error')
    
    return render_template('employee/profile.html',
                         current_user=current_user,
                         is_supervisor=session.get('role') in ['supervisor', 'admin'])

@employee_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """Change employee password"""
    check = require_employee()
    if check: return check
    
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
    
    return render_template('employee/change_password.html',
                         is_supervisor=session.get('role') in ['supervisor', 'admin'])

@employee_bp.route('/quick_search')
def quick_search():
    """Quick search page for products"""
    check = require_employee()
    if check: return check
    
    unit_id = get_current_unit_id()
    unit_info = unit_model.get_unit_by_id(unit_id)
    
    return render_template('employee/quick_search.html',
                         unit_info=unit_info,
                         is_supervisor=session.get('role') in ['supervisor', 'admin'])