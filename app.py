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
    platform = db.Column(db.String(20))
    result = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create table
with app.app_context():
    db.create_all()

# Scam checker
def check_scam(text, platform):
    text_lower = text.lower()
    scam_words = ['otp', 'won', 'congratulations', 'send money', 'ecocash', 'loan', 'click link', 'agent', 'prize', 'verify']
    
    score = 0
    for word in scam_words:
        if word in text_lower:
            score += 1
    
    if '+263' in text or '077' in text or '078' in text:
        score += 1

    if score >= 2:
        return f"⚠️ SCAM DETECTED on {platform}! Do not reply or send money. Report to 111."
    elif score == 1:
        return f"⚠️ SUSPICIOUS on {platform}. Be very careful."
    else:
        return f"✅ Looks Safe on {platform}. But still be careful."

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        message = request.form.get('message')
        platform = request.form.get('platform')
        result_text = check_scam(message, platform)
        
        # Save to database
        new_report = Report(message=message, platform=platform, result=result_text)
        db.session.add(new_report)
        db.session.commit()
        result = result_text
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=False)
