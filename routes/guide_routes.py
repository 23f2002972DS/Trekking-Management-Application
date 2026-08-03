from flask import Blueprint, render_template, session, redirect, request
from Database.models import db, Person, Trek, Reservation

guide_bp = Blueprint('guide', __name__, url_prefix='/guide')

@guide_bp.route('/dash')
def dashboard():
    if session.get('profile') != 'guide': return redirect('/client/login')
    treks = Trek.query.filter_by(coordinator_id=session['gid']).all()
    
    trek_reservations = {}
    for t in treks:
        trek_reservations[t.tid] = Reservation.query.filter_by(trek_id=t.tid).all()
        
    return render_template('guide_dash.html', treks=treks, trek_reservations=trek_reservations)

@guide_bp.route('/update_trek/<int:tid>', methods=['POST'])
def update_trek(tid):
    if session.get('profile') != 'guide': return redirect('/client/login')
    t = Trek.query.get(tid)
    if t and t.coordinator_id == session['gid']:
        t.trek_status = request.form.get('status')
        t.open_slots = int(request.form.get('slots'))
        db.session.commit()
    return redirect('/guide/dash')
