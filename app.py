import os
import psutil
from flask import Flask, render_template, jsonify
from threading import Lock

app = Flask(__name__)
# Thread-safe lock for metrics collection
metrics_lock = Lock()

def get_system_metrics():
    """Get system metrics with thread safety"""
    with metrics_lock:
        return {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent
        }

@app.route('/')
def index():
    return render_template(
        'index.html',
        cpu_threshold=80,
        mem_threshold=80
    )

@app.route('/metrics')
def metrics():
    """Endpoint for real-time metrics"""
    return jsonify(get_system_metrics())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)