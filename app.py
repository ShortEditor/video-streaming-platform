from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    videos = Video.query.all()
    return render_template('index.html', videos=videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if not current_user.is_admin:
        flash('Only admins can upload videos')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        video = request.files.get('video')
        title = request.form.get('title')
        description = request.form.get('description')
        
        if video and title:
            filename = video.filename
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            new_video = Video(title=title, filename=filename, description=description)
            db.session.add(new_video)
            db.session.commit()
            
            flash('Video uploaded successfully!')
            return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/delete/<int:video_id>', methods=['POST'])
@login_required
def delete_video(video_id):
    if not current_user.is_admin:
        flash('Only admins can delete videos')
        return redirect(url_for('index'))
    
    video = Video.query.get_or_404(video_id)
    try:
        # Delete the video file from uploads folder
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        if os.path.exists(video_path):
            os.remove(video_path)
        
        # Delete the database entry
        db.session.delete(video)
        db.session.commit()
        flash('Video deleted successfully!')
    except Exception as e:
        flash('Error deleting video: ' + str(e))
        db.session.rollback()
    
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
