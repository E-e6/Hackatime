from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# In-memory storage for simplicity
hackatime_logs = []

@app.route('/')
def home():
    total_hours = sum(log['hours'] for log in hackatime_logs)
    return render_template('index.html', logs=hackatime_logs, total_hours=total_hours)

@app.route('/log', methods=['GET', 'POST'])
def log_hours():
    if request.method == 'POST':
        hours = float(request.form['hours'])
        note = request.form['note']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hackatime_logs.append({'hours': hours, 'note': note, 'date': date})
        return redirect(url_for('home'))
    return render_template('log.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)