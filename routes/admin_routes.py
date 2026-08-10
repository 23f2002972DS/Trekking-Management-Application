from flask import Blueprint, render_template, request, redirect, session, url_for
from Database.models import db, Person, Trek, Reservation
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/manager')

@admin_bp.route('/dash')
def dashboard():
    if session.get('profile') != 'manager': return redirect('/client/login')
    
    q = request.args.get('q', '').strip()
    
    treks_q = Trek.query
    guides_q = Person.query.filter_by(profile_type='guide')
    clients_q = Person.query.filter_by(profile_type='client')
    
    if q:
        treks_q = treks_q.filter(Trek.destination.ilike(f'%{q}%') | Trek.region.ilike(f'%{q}%'))
        guides_q = guides_q.filter(Person.identity_handle.ilike(f'%{q}%'))
        clients_q = clients_q.filter(Person.identity_handle.ilike(f'%{q}%'))
        
    treks = treks_q.all()
    guides = guides_q.all()
    clients = clients_q.all()
    reservations = Reservation.query.order_by(Reservation.timestamp.desc()).all()
    
    stats = {
        'total_treks': Trek.query.count(),
        'total_clients': Person.query.filter_by(profile_type='client').count(),
        'total_guides': Person.query.filter_by(profile_type='guide').count(),
        'total_reservations': Reservation.query.count()
    }
    
    return render_template('manager_dash.html', treks=treks, guides=guides, clients=clients, reservations=reservations, stats=stats, q=q)

@admin_bp.route('/add_trek', methods=['POST'])
def add_trek():
    if session.get('profile') != 'manager': return redirect('/client/login')
    d1 = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
    d2 = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    dur = request.form.get('duration')
    t = Trek(
        destination=request.form.get('dest'),
        region=request.form.get('region'),
        challenge_level=request.form.get('difficulty'),
        duration=int(dur) if dur else None,
        capacity=int(request.form.get('cap')),
        open_slots=int(request.form.get('cap')),
        commencement_date=d1,
        end_date=d2,
        coordinator_id=request.form.get('guide_id') or None,
        trek_status='Open'
    )
    db.session.add(t)
    db.session.commit()
    return redirect('/manager/dash')

@admin_bp.route('/edit_trek/<int:tid>', methods=['GET', 'POST'])
def edit_trek(tid):
    if session.get('profile') != 'manager': return redirect('/client/login')
    t = Trek.query.get_or_404(tid)
    if request.method == 'POST':
        t.destination = request.form.get('dest')
        t.region = request.form.get('region')
        t.challenge_level = request.form.get('difficulty')
        dur = request.form.get('duration')
        t.duration = int(dur) if dur else None
        t.capacity = int(request.form.get('cap'))
        t.open_slots = int(request.form.get('open_slots'))
        t.commencement_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        t.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        t.trek_status = request.form.get('trek_status')
        g_id = request.form.get('guide_id')
        t.coordinator_id = g_id if g_id else None
        db.session.commit()
        return redirect('/manager/dash')
    guides = Person.query.filter_by(profile_type='guide', is_approved=True).all()
    return render_template('edit_trek.html', t=t, guides=guides)

@admin_bp.route('/delete_trek/<int:tid>', methods=['POST'])
def delete_trek(tid):
    if session.get('profile') != 'manager': return redirect('/client/login')
    t = Trek.query.get(tid)
    if t:
        db.session.delete(t)
        db.session.commit()
    return redirect('/manager/dash')

@admin_bp.route('/approve/<int:pid>', methods=['POST'])
def approve_guide(pid):
    if session.get('profile') != 'manager': return redirect('/client/login')
    g = Person.query.get(pid)
    if g:
        g.is_approved = True
        db.session.commit()
    return redirect('/manager/dash')

@admin_bp.route('/ban/<int:pid>', methods=['POST'])
def ban_person(pid):
    if session.get('profile') != 'manager': return redirect('/client/login')
    p = Person.query.get(pid)
    if p:
        p.is_active = False
        db.session.commit()
    return redirect('/manager/dash')

@admin_bp.route('/delete_user/<int:pid>', methods=['POST'])
def delete_user(pid):
    if session.get('profile') != 'manager': return redirect('/client/login')
    prof = Person.query.get(pid)
    if prof:
        Reservations = Reservation.query.filter_by(client_id=pid).delete()
        db.session.delete(prof)
        db.session.commit()
    return redirect('/manager/dash') 