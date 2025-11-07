from flask import render_template
from task_manager import app

@app.route('/')
def home():
    return render_template('home.html')
