from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import ServiceRequest, Professional, User
from database import db
from datetime import datetime

professional_bp = Blueprint('professional', __name__, url_prefix='/professional')

@professional_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'professional':
        return redirect(url_for('auth.login'))
    
    professional = Professional.query.filter_by(user_id=session['user_id']).first()
    service_requests = ServiceRequest.query.filter_by(
        professional_id=session['user_id']
    ).all()
    
    available_requests = ServiceRequest.query.filter_by(
        status='requested',
        professional_id=None
    ).all()
    
    return render_template('professional/dashboard.html',
                         service_requests=service_requests,
                         available_requests=available_requests,
                         professional=professional)

@professional_bp.route('/accept-request/<int:request_id>')
def accept_request(request_id):
    if session.get('role') != 'professional':
        return redirect(url_for('auth.login'))
        
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    if service_request.status == 'requested':
        service_request.professional_id = session['user_id']
        service_request.status = 'assigned'
        db.session.commit()
        flash('Service request accepted')
    
    return redirect(url_for('professional.dashboard'))

@professional_bp.route('/complete-request/<int:request_id>', methods=['POST'])
def complete_request(request_id):
    if session.get('role') != 'professional':
        return redirect(url_for('auth.login'))
        
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    if service_request.professional_id == session['user_id']:
        service_request.status = 'closed'
        service_request.date_of_completion = datetime.utcnow()
        db.session.commit()
        flash('Service request marked as completed')
    
    return redirect(url_for('professional.dashboard'))