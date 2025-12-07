from flask import Flask, request, jsonify
import os
import time
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@metrics.histogram('http_request_latency_seconds', 'Request Latency Histogram', buckets=[0.1, 0.5, 1, 2, 5, 10])
@app.route('/compute', methods=['POST'])

@app.route('/healthz', methods=['GET'])
def health_check():
    return '', 200

@app.route('/readyz', methods=['GET'])
def readiness_check():
    return '', 200

@app.route('/version', methods=['GET'])
def version():
    return jsonify(version=os.environ.get('APP_VERSION', 'unknown')), 200

@app.route('/compute', methods=['POST'])
def compute():
    data = request.json
    n = data.get('n', 0)
    
    start_time = time.time()
    data = request.json
    n = data.get('n', 0)

    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    start_time = time.time()
    result = fibonacci(n)
    latency = time.time() - start_time
    if n < 0:
        return jsonify(result=result, latency=latency), 200
    else:
        return jsonify(result="Invalid input; n must be non-negative."), 400

@app.route('/metrics', methods=['GET'])
def metrics():
    return 'metrics', 200

def metrics_endpoint():
    return metrics.wsgi_app(environ, start_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
