from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
APP_MODE = os.getenv('APP_MODE', 'original')
VERSION = os.getenv('VERSION', '1.0')

# In-memory storage for demo
visitors = []
messages = []

@app.route('/')
def home():
    """Main page for Carla's application"""
    return render_template('index.html', 
                         mode=APP_MODE, 
                         version=VERSION,
                         visitor_count=len(visitors))

@app.route('/visit', methods=['POST'])
def visit():
    """Record a visitor"""
    visitor_data = {
        'timestamp': datetime.now().isoformat(),
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')
    }
    visitors.append(visitor_data)
    return jsonify({
        'status': 'success',
        'total_visitors': len(visitors),
        'message': f'Welcome visitor #{len(visitors)}!'
    })

@app.route('/message', methods=['POST'])
def message():
    """Store a message"""
    data = request.get_json()
    message_data = {
        'timestamp': datetime.now().isoformat(),
        'name': data.get('name', 'Anonymous'),
        'message': data.get('message', '')
    }
    messages.append(message_data)
    return jsonify({
        'status': 'success',
        'message': 'Message stored successfully'
    })

@app.route('/stats')
def stats():
    """Show application statistics"""
    return jsonify({
        'mode': APP_MODE,
        'version': VERSION,
        'total_visitors': len(visitors),
        'total_messages': len(messages),
        'uptime': 'N/A'  # Could be calculated with start time
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'mode': APP_MODE,
        'version': VERSION
    })

if __name__ == '__main__':
    print(f"""
    ╔════════════════════════════════════════╗
    ║   Carla's Application - {APP_MODE.upper()}    ║
    ║   Version: {VERSION}                       ║
    ╚════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
