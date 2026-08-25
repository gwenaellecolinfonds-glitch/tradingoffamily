import os
import random
import time
from datetime import datetime, timezone
from flask import Flask, render_template, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Clé de sécurité unique pour le Trading
ACCESS_CODE_TRADING = "TRAG679DGA"

# Routes de navigation
@app.route('/')
@app.route('/hub')
def hub_page():
    return render_template('hub.html')

@app.route('/trading')
def trading_page():
    return render_template('trading.html')

# API - Trading VIP (Signaux & Rendement)
@app.route('/api/signal', methods=['POST'])
def generate_signal():
    data = request.get_json() or {}
    user_code = data.get('access_code', '').strip().upper()

    if user_code != ACCESS_CODE_TRADING:
        return jsonify({'error': 'Code d\'accès invalide'}), 401

    asset = data.get('asset', 'EUR/USD (OTC)')
    timeframe = data.get('timeframe', '30s')

    # Simulation d'un calcul algorithmique temps réel
    time.sleep(random.uniform(0.6, 1.2))

    direction = random.choice(['HAUT (CALL) 📈', 'BAS (PUT) 📉'])
    confidence = f"{random.randint(88, 98)}%"
    timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")

    return jsonify({
        'asset': asset,
        'timeframe': timeframe,
        'direction': direction,
        'confidence': confidence,
        'timestamp': timestamp,
        'status': 'success'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)