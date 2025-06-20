from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your own secure key!

# 🌐 Load correct language file
def get_language():
    lang = session.get('lang', 'en')  # Default to English
    lang_path = os.path.join('static', 'lang', f'{lang}.json')
    try:
        with open(lang_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(os.path.join('static', 'lang', 'en.json'), 'r') as file:
            return json.load(file)

# 🔁 Change language route
@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    session['lang'] = lang_code
    return redirect(request.referrer or '/')

# 🏠 Homepage
@app.route('/')
def index():
    lang = get_language()
    return render_template('index.html', lang=lang)

# 🧪 Code playground
@app.route('/sandbox')
def sandbox():
    lang = get_language()
    return render_template('sandbox.html', lang=lang)

# 📚 Lessons
@app.route('/lesson')
def lesson():
    lang = get_language()
    return render_template('lesson.html', lang=lang)

# 💬 Feedback/contact
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    lang = get_language()
    if request.method == 'POST':
        message = request.form.get('message')
        # Save or email feedback if needed
        return render_template('feedback.html', lang=lang, success=True)
    return render_template('feedback.html', lang=lang)

if __name__ == '__main__':
    app.run(debug=True)