from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///huntclub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for iOS app
CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    active_checkin = db.relationship('StandCheckIn', backref='hunter', lazy=True, 
                                     foreign_keys='StandCheckIn.user_id')
    harvests = db.relationship('Harvest', backref='hunter', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class HuntingStand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(500))
    max_hunters = db.Column(db.Integer, default=1)
    checkins = db.relationship('StandCheckIn', backref='stand', lazy=True)
    
    def get_active_checkins(self):
        return [c for c in self.checkins if c.checkout_time is None]
    
    def is_available(self):
        active = len(self.get_active_checkins())
        return active < self.max_hunters

class StandCheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stand_id = db.Column(db.Integer, db.ForeignKey('hunting_stand.id'), nullable=False)
    checkin_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow())
    checkout_time = db.Column(db.DateTime)

class Harvest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow())
    location = db.Column(db.String(200))
    notes = db.Column(db.Text)

# Register API blueprints for iOS app
from api import register_api_blueprints
register_api_blueprints(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get active hunters
    active_checkins = StandCheckIn.query.filter_by(checkout_time=None).all()
    
    # Get user's current check-in
    user_checkin = StandCheckIn.query.filter_by(
        user_id=current_user.id, 
        checkout_time=None
    ).first()
    
    return render_template('dashboard.html', 
                         active_checkins=active_checkins,
                         user_checkin=user_checkin)

@app.route('/stands')
@login_required
def stands():
    all_stands = HuntingStand.query.all()
    user_checkin = StandCheckIn.query.filter_by(
        user_id=current_user.id, 
        checkout_time=None
    ).first()
    return render_template('stands.html', stands=all_stands, user_checkin=user_checkin)

@app.route('/checkin/<int:stand_id>', methods=['POST'])
@login_required
def checkin(stand_id):
    # Check if user is already checked in
    existing = StandCheckIn.query.filter_by(
        user_id=current_user.id, 
        checkout_time=None
    ).first()
    
    if existing:
        flash('You are already checked in to a stand. Please check out first.', 'warning')
        return redirect(url_for('stands'))
    
    stand = HuntingStand.query.get_or_404(stand_id)
    
    if not stand.is_available():
        flash(f'{stand.name} is currently at capacity.', 'danger')
        return redirect(url_for('stands'))
    
    checkin = StandCheckIn(user_id=current_user.id, stand_id=stand_id)
    db.session.add(checkin)
    db.session.commit()
    
    flash(f'Checked in to {stand.name}!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    checkin = StandCheckIn.query.filter_by(
        user_id=current_user.id, 
        checkout_time=None
    ).first()
    
    if not checkin:
        flash('You are not currently checked in.', 'warning')
        return redirect(url_for('dashboard'))
    
    checkin.checkout_time = datetime.utcnow()
    db.session.commit()
    
    flash('Checked out successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/harvest', methods=['GET', 'POST'])
@login_required
def harvest():
    if request.method == 'POST':
        game_type = request.form.get('game_type')
        location = request.form.get('location')
        notes = request.form.get('notes')
        
        harvest_record = Harvest(
            user_id=current_user.id,
            game_type=game_type,
            location=location,
            notes=notes
        )
        db.session.add(harvest_record)
        db.session.commit()
        
        flash('Harvest logged successfully!', 'success')
        return redirect(url_for('harvest'))
    
    harvests = Harvest.query.order_by(Harvest.date.desc()).all()
    return render_template('harvest.html', harvests=harvests)

@app.route('/admin/stands', methods=['GET', 'POST'])
@login_required
def admin_stands():
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        max_hunters = request.form.get('max_hunters', 1, type=int)
        
        stand = HuntingStand(name=name, description=description, max_hunters=max_hunters)
        db.session.add(stand)
        db.session.commit()
        
        flash('Stand added successfully!', 'success')
        return redirect(url_for('admin_stands'))
    
    stands = HuntingStand.query.all()
    return render_template('admin_stands.html', stands=stands)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Create admin user if doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            # SECURITY WARNING: Change this password immediately in production
            admin.set_password('admin123')
            db.session.add(admin)
            print("=" * 60)
            print("SECURITY WARNING: Default admin account created!")
            print("Username: admin")
            print("Password: admin123")
            print("CHANGE THIS PASSWORD IMMEDIATELY!")
            print("=" * 60)
        
        # Create sample stands if none exist
        if HuntingStand.query.count() == 0:
            stands = [
                HuntingStand(name='North Ridge', description='Elevated stand overlooking the north ridge', max_hunters=1),
                HuntingStand(name='Creek Bottom', description='Ground blind near the creek', max_hunters=2),
                HuntingStand(name='Oak Grove', description='Tree stand in oak grove', max_hunters=1),
                HuntingStand(name='South Field', description='Open field stand on south boundary', max_hunters=1),
            ]
            for stand in stands:
                db.session.add(stand)
        
        db.session.commit()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
    # Set debug=False in production for security
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5001)
