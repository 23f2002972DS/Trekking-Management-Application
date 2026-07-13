from flask import Flask, redirect, url_for
from core.db_setup import db, Person
import os

def init_system():
    app = Flask(__name__, template_folder='views', static_folder='assets')
    
    base = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base, 'beta_sys_v2.db')}"
    app.config['SECRET_KEY'] = 'beta_brutalist_secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes.client_routes import client_bp
    from routes.guide_routes import guide_bp
    from routes.admin_routes import admin_bp
    
    app.register_blueprint(client_bp, url_prefix='/client')
    app.register_blueprint(guide_bp, url_prefix='/guide')
    app.register_blueprint(admin_bp, url_prefix='/manager')
    
    @app.route('/')
    def root_redir():
        return redirect(url_for('client.login'))

    return app

if __name__ == '__main__':
    app = init_system()
    with app.app_context():
        db.create_all()
        if not Person.query.filter_by(identity_handle='manager').first():
            mgr = Person(identity_handle='manager', profile_type='manager')
            mgr.set_sec_key('manager')
            db.session.add(mgr)
            db.session.commit()
            
    print("Project Beta Active on port 8112...")
    app.run(debug=True, port=8112)
