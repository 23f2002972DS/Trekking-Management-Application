from flask import Blueprint, render_template, request, redirect, session, url_for
from Database.models import db,Person

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identity = request.form.get('identity')
        p = request.form.get('password')
        ac = Person.query.filter_by(identity_handle=identity).first()
        if ac and ac.check_sec_key(p):
            if not ac.is_active:
                return render_template('auth.html', error='Account is banned.')
            if not ac.is_authorized:
                return render_template('auth.html', error='Account pending for authorization.')
            session['pid'] = ac.pid
            session['prof'] = ac.profile_type
            if ac.profile_type == 'client':
                return redirect('/client/dash')
            elif ac.profile_type == 'guide':
                return redirect('/guide/dash')
            elif ac.profile_type == 'manager':
                return redirect('/manager/dash')
        return render_template('auth.html', error='Invalid credentials.')
    return render_template('auth.html') 

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        identity = request.form.get('identity')
        p = request.form.get('password')
        prof = request.form.get('profile')
        if Person.query.filter_by(identity_handle=identity).first():
            return render_template('register.html', error='Account submitted . Awaiting approval by manager.')

        is_auth = (prof == 'client')
        new_person = Person(identity_handle=identity, profile_type=prof, is_active=True, is_approved=is_auth)
        new_person.set_sec_key(p)
        db.session.add(new_person)
        db.session.commit()

        if is_auth:
            session['pid'] = new_person.pid
            session['prof'] = new_person.profile_type
            return redirect('/client/dash')
        else:
            return render_template('auth.html', error='Account submitted . Awaiting approval by manager.')

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login')) 