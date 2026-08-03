from flask import Blueprint, render_template, request, redirect, session
from Database.models import db, Person, Trek, Reservation
from datetime import datetime

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        h = request.form.get('handle')
        p = request.form.get('pwd')
        user = Person.query.filter_by(identity_handle=h).first()
        if user and user.verify_sec_key(p):
            if not user.is_active: return render_template('auth.html', error='Account disabled.')
            if user.profile_type == 'guide' and not user.is_approved: return render_template('auth.html', error='Not approved.')
            
            session['profile'] = user.profile_type
            if user.profile_type == 'manager':
                return redirect('/manager/dash')
            elif user.profile_type == 'guide':
                session['gid'] = user.pid
                return redirect('/guide/dash')
            else:
                session['cid'] = user.pid
                return redirect('/client/dash')
        return render_template('auth.html', error='Invalid credentials')
    return render_template('auth.html')

@client_bp.route('/dash')
def dashboard():
    if session.get('profile') != 'client': return redirect('/client/login')
    q = request.args.get('q', '')
    diff = request.args.get('diff', '')

    query = Trek.query.filter_by(trek_status='Open')

    if q:
        query = query.filter(Trek.destination.ilike(f'%{q}%'))
    if diff:
        # model uses `challenge_level` (not `diff`) so use the correct column
        query = query.filter(Trek.challenge_level == diff)

    treks_all = query.all()

    my_res = Reservation.query.filter_by(client_id=session['cid']).all()
    booked_tids = [r.trek_id for r in my_res]

    # Only show treks that have open slots and which the client hasn't already booked
    available_treks = [t for t in treks_all if t.tid not in booked_tids and t.open_slots > 0]

    # Counts to help frontend show helpful messages
    matched_count = len(treks_all)
    available_count = len(available_treks)

    return render_template('client_dash.html', treks=available_treks, my_res=my_res, q=q, diff=diff, booked_tids=booked_tids, matched_count=matched_count, available_count=available_count)

@client_bp.route('/book/<int:tid>', methods=['POST'])
def book_trek(tid):
    if session.get('profile') != 'client': return redirect('/client/login')
    t = Trek.query.get(tid)
    if t and t.open_slots > 0 and t.trek_status == 'Open':
        t.open_slots -= 1
        r = Reservation(client_id=session['cid'], trek_id=tid, status='Booked')
        db.session.add(r)
        db.session.commit()
    return redirect('/client/dash')

@client_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/client/login')
