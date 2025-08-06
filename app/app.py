from flask import Flask, render_template, redirect, url_for
from simulator import start_campaign, stop_campaign, campaign_running
from database import get_stats
from report_generator import generate_pdf

app = Flask(__name__)
app.secret_key = 'super-secret'

@app.route('/')
def index():
    stats = get_stats()
    return render_template("index.html", stats=stats, running=campaign_running())

@app.route('/start')
def start():
    start_campaign()
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    stop_campaign()
    return redirect(url_for('index'))

@app.route('/report')
def report():
    generate_pdf()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)