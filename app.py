"""
Minimal Flask server for Inmersión Natural web demo.
Serves the standalone Immersion Mode game with 30 starter vocabulary cards.
Deploy to PythonAnywhere, Render, or any WSGI host.
"""
import os
import json
import random
from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__, static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'static', 'assets')
GAME_DATA_PATH = os.path.join(BASE_DIR, 'static', 'game_data.json')

# Load game data once at startup
with open(GAME_DATA_PATH, 'r', encoding='utf-8') as f:
    GAME_DATA = json.load(f)

print(f"[Inmersión] Loaded {len(GAME_DATA['cards'])} cards, {len(GAME_DATA.get('stages', []))} stages")


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static'), filename)


@app.route('/api/progression', methods=['GET'])
def get_progression():
    """Return default progression (client manages state via localStorage)."""
    return jsonify({
        'grammar_stage': 1,
        'stage_stats': {},
        'words_mastered': [],
        'total_rounds': 0,
        'starter_count': len(GAME_DATA.get('starter_vocabulary', []))
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"\n{'='*50}")
    print(f"  Inmersión Natural - Web Demo")
    print(f"  http://localhost:{port}")
    print(f"{'='*50}\n")
    app.run(host='0.0.0.0', port=port, debug=False)
