from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import ServiceRequest, Professional, Service, User
from database import db
from datetime import datetime, timedelta
from collections import defaultdict

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    service_requests = ServiceRequest.query.order_by(ServiceRequest.date_of_request.desc()).limit(5).all()
    pending_professionals = Professional.query.filter_by(is_verified=False).all()
    
    # Prepare data for the chart
    today = datetime.today()
    last_six_months = [(today - timedelta(days=30 * i)).strftime('%Y-%m') for i in range(6)]
    request_counts = defaultdict(int)

    for request in ServiceRequest.query.all():
        month = request.date_of_request.strftime('%Y-%m')
        if month in last_six_months:
            request_counts[month] += 1

    # Ensure all months are represented
    request_data = [request_counts[month] for month in last_six_months]

    return render_template('admin/dashboard.html', 
                           service_requests=service_requests,
                           pending_professionals=pending_professionals,
                           request_data=request_data,
                           last_six_months=last_six_months)

@admin_bp.route('/manage-services', methods=['GET', 'POST'])
def manage_services():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Collect form data
        service_name = request.form.get('service_name')
        base_price = request.form.get('base_price')
        time_required = request.form.get('time_required')
        description = request.form.get('description')
        
        # Ensure base_price is provided and valid
        if service_name and base_price:
            try:
                base_price = float(base_price)  # Convert to float
                new_service = Service(
                    name=service_name,
                    base_price=base_price,
                    time_required=time_required,
                    description=description
                )
                db.session.add(new_service)
                db.session.commit()
                flash('Service added successfully')
            except ValueError:
                flash('Invalid base price. Please enter a valid number.')
        else:
            flash('Service name and base price are required.')

    services = Service.query.all()
    return render_template('admin/manage_services.html', services=services)

@admin_bp.route('/verify-professionals')
def verify_professionals():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    professionals = Professional.query.filter_by(is_verified=False).all()
    return render_template('admin/verify_professionals.html', professionals=professionals)

@admin_bp.route('/manage-users')
def manage_users():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/verify-professional', methods=['POST'])
def verify_professional():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    professional_id = request.form.get('professional_id')
    if professional_id:
        professional = Professional.query.get_or_404(professional_id)
        professional.is_verified = True
        db.session.commit()
        flash('Professional verified successfully')
    else:
        flash('Professional ID is required.')

    return redirect(url_for('admin.verify_professionals'))

@admin_bp.route('/view-request/<int:request_id>')
def view_request(request_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    service_request = ServiceRequest.query.get_or_404(request_id)
    return render_template('admin/view_request.html', request=service_request)

@admin_bp.route('/delete-service', methods=['POST'])
def delete_service():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    service_id = request.form.get('delete_service_id')
    if service_id:
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully')
    else:
        flash('Service ID is required.')

    return redirect(url_for('admin.manage_services'))