import os
import io
import base64
import qrcode
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__, template_folder='02_source_code')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://student:[REDACTED]@localhost:5432/practice_project')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='user')

class QRCode(db.Model):
    __tablename__ = 'qr_codes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    qr_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='active')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_qr_base64(data):
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/')
def index():
    qr_code = None
    text = request.args.get('text')
    if text:
        qr_code = generate_qr_base64(text)
    return render_template('index.html', qr_code=qr_code)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный email или пароль')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    search = request.args.get('search', '')
    if current_user.role == 'administrator':
        query = QRCode.query
    else:
        query = QRCode.query.filter_by(user_id=current_user.id)
    
    if search:
        query = query.filter(QRCode.title.ilike(f'%{search}%'))
        
    qrs = query.all()
    return render_template('dashboard.html', qrs=qrs)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        qr_type = request.form.get('qr_type')
        content = request.form.get('content')
        if not title or not content:
            flash('Заполните все поля!')
            return redirect(url_for('create'))
        
        new_qr = QRCode(title=title, qr_type=qr_type, content=content, user_id=current_user.id)
        db.session.add(new_qr)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create.html')

@app.route('/view/<int:id>')
@login_required
def view_qr(id):
    qr = QRCode.query.get_or_404(id)
    if current_user.role != 'administrator' and qr.user_id != current_user.id:
        flash('У вас нет доступа к этому QR-коду!')
        return redirect(url_for('dashboard'))
    qr_code = generate_qr_base64(qr.content)
    return render_template('view_qr.html', qr=qr, qr_code=qr_code)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    qr = QRCode.query.get_or_404(id)
    if current_user.role == 'administrator' or qr.user_id == current_user.id:
        db.session.delete(qr)
        db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
