from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Service, ServiceRequest, User
from database import db
from datetime import datetime

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'customer':
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    service_requests = ServiceRequest.query.filter_by(customer_id=user_id).all()
    return render_template('customer/dashboard.html', service_requests=service_requests)

@customer_bp.route('/services')
def services():
    search_query = request.args.get('search', '')
    services = Service.query
    
    if search_query:
        services = services.filter(Service.name.ilike(f'%{search_query}%'))
    
    services = services.all()
    return render_template('customer/services.html', services=services, search_query=search_query)

@customer_bp.route('/request-service/<int:service_id>', methods=['GET', 'POST'])
def request_service(service_id):
    if session.get('role') != 'customer':
        return redirect(url_for('auth.login'))
        
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        service_request = ServiceRequest(
            service_id=service_id,
            customer_id=session['user_id'],
            remarks=request.form.get('remarks')
        )
        db.session.add(service_request)
        db.session.commit()
        flash('Service request submitted successfully')
        return redirect(url_for('customer.dashboard'))
        
    return render_template('customer/request_service.html', service=service)