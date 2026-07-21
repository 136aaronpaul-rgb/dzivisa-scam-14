import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Table
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    number = db.Column(db.String(20))
    platform = db.Column(db.String(20))
    result = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create table if it doesn't exist
with app.app_context():
    db.create_all()

# Simple scam checker
def check_scam(text):
    scam_words = ['otp', 'won', 'congratulations', 'send money', 'ecocash', 'loan', 'click link', 'agent']
    text_lower = text.lower()
    for word in scam_words:
        if word in text_lower:
            return "⚠️ SCAM DETECTED! Do not reply or send money."
    return "✅ Looks Safe. But still be careful."

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        message = request.form.get('message')
        result_text = check_scam(message)
        
        # Save to database
        new_report = Report(message=message, result=result_text)
        db.session.add(new_report)
        db.session.commit()
        
        result = result_text
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
