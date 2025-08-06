from flask import Flask, render_template, redirect, url_for, jsonify, send_file
from simulator import start_campaign, stop_campaign, campaign_running
from database import get_stats
from report_generator import generate_pdf
import os

app = Flask(__name__)
app.secret_key = 'super-secret-phishing-simulator-key'

@app.route('/')
def index():
    stats = get_stats()
    return render_template("index.html", stats=stats, running=campaign_running())

@app.route('/start')
def start():
    success = start_campaign()
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    success = stop_campaign()
    return redirect(url_for('index'))

@app.route('/api/stats')
def api_stats():
    """API endpoint para obtener estadísticas en tiempo real"""
    stats = get_stats()
    return jsonify(stats)

@app.route('/report')
def report():
    try:
        filename = generate_pdf()
        return send_file(filename, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Vista del dashboard con gráficos detallados"""
    stats = get_stats()
    return render_template("dashboard.html", stats=stats, running=campaign_running())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)