from flask import Flask, render_template, request, redirect, session, url_for
from database import init_user_table, init_feedback_table, save_feedback
import json
import os
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# 🌱 Initialize database tables on app startup
init_user_table()
init_feedback_table()

# 🔐 Reusable login guard
def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return view_func(*args, **kwargs)
    return wrapped_view

# 🌐 Load language file based on session
def get_language():
    lang_code = session.get('lang', 'en')
    file_path = os.path.join('static', 'lang', f'{lang_code}.json')

    if not os.path.exists(file_path):
        file_path = os.path.join('static', 'lang', 'en.json')

    with open(file_path, 'r', encoding='utf-8') as lang_file:
        return json.load(lang_file)

# 🌍 Set language
@app.route('/set_language')
def set_language():
    lang_code = request.args.get('lang_code', 'en')
    session['lang'] = lang_code
    return redirect(request.referrer or '/')

# 🔐 Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = get_language()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('bloombyte.db')
        c = conn.cursor()
        c.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        row = c.fetchone()
        conn.close()
        if row and check_password_hash(row[0], password):
            session['logged_in'] = True
            session['username'] = username
            return redirect('/?celebrate=true')
        else:
            error = 'Invalid credentials'
    return render_template('login.html', lang=lang, error=error)

# 📝 Register new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = get_language()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        try:
            conn = sqlite3.connect('bloombyte.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            conn.commit()
            conn.close()
            return redirect('/login?registered=true')
        except sqlite3.IntegrityError:
            return render_template('register.html', lang=lang, error='Username already taken')
    return render_template('register.html', lang=lang)

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 🏠 Homepage
@app.route('/')
@login_required
def index():
    lang = get_language()
    return render_template('index.html', lang=lang)

# 🧪 Sandbox page
@app.route('/sandbox')
@login_required
def sandbox():
    lang = get_language()
    return render_template('sandbox.html', lang=lang)

# 📚 Lessons page
@app.route('/lesson')
@login_required
def lesson():
    lang = get_language()
    return render_template('lesson.html', lang=lang)

@app.route('/lesson/<topic>')
@login_required
def lesson_detail(topic):
    lang = get_language()
    return render_template(f'lessons/{topic}.html', lang=lang)

# 💬 Feedback form
@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    lang = get_language()
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            save_feedback(message)
        return render_template('feedback.html', lang=lang, success=True)
    return render_template('feedback.html', lang=lang)

# 👤 Profile page
@app.route('/profile')
@login_required
def profile():
    username = session.get('username')
    lang = get_language()
    return render_template('profile.html', lang=lang, username=username)

# 🚀 Launch app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)