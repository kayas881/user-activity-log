# Flask-based GUI for User Activity Monitoring Tool
from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

LOGFILE = 'activity.log'
REPORTFILE = 'daily_report.log'

def run_command(cmd):
	try:
		result = subprocess.check_output(cmd, shell=True, text=True)
	except subprocess.CalledProcessError as e:
		result = e.output or str(e)
	return result

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/monitor')
def monitor():
	users = run_command('w')
	processes = run_command('ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -10')
	return render_template('monitor.html', users=users, processes=processes)

@app.route('/log_snapshot')
def log_snapshot():
	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	with open(LOGFILE, 'a') as f:
		f.write(f"----- {now} -----\n")
		f.write(run_command('w'))
		f.write(run_command('ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -10'))
	flash(f"Snapshot saved to {LOGFILE}")
	return redirect(url_for('index'))

@app.route('/daily_report')
def daily_report():
	now = datetime.datetime.now().strftime('%Y-%m-%d')
	with open(REPORTFILE, 'w') as f:
		f.write(f"===== Report for {now} =====\n")
		f.write(run_command('last -n 5'))
		f.write("\nTop 5 processes today:\n")
		f.write(run_command('ps -eo comm,%cpu,%mem --sort=-%cpu | head -5'))
	with open(REPORTFILE) as f:
		report = f.read()
	return render_template('message.html', title='Daily Report', message=report)

@app.route('/alerts')
def alerts():
	alert_output = run_command("ps -eo pid,comm,%cpu,%mem --sort=-%cpu | awk '$3 > 20 || $4 > 20 {print \"ALERT:\", $0}'")
	if not alert_output.strip():
		alert_output = 'No high resource usage detected.'
	return render_template('alerts.html', alerts=alert_output)

@app.route('/session_history')
def session_history():
	history = run_command('last -n 10')
	return render_template('session_history.html', history=history)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5050)
