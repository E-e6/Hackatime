from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hours.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class HourLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<HourLog {self.hours} hours>'

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Log route
@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        hours = float(request.form['hours'])
        new_log = HourLog(hours=hours)
        db.session.add(new_log)
        db.session.commit()
        return redirect(url_for('log'))
    
    total_hours = sum([log.hours for log in HourLog.query.all()])
    logs = HourLog.query.order_by(HourLog.timestamp.desc()).all()
    return render_template('log.html', total_hours=total_hours, logs=logs)

# About route
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=False)