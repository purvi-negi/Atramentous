from flask import Flask, request, jsonify, send_from_directory
import random
import os

app = Flask(__name__)

# Serve the frontend files from the current directory
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print(f"Received prediction request: {data}")
        
        # Placeholder for actual habitability logic
        # radius, temperature, distance, period, star_type
        radius = float(data.get('radius', 1.0))
        temp = float(data.get('temperature', 288))
        
        # Simple heuristic logic for habitability
        # Earth-like temperature (200-350K) and size (0.5-2.0 Earth Radii)
        is_habitable = 200 <= temp <= 350 and 0.5 <= radius <= 2.0
        
        # Calculate a mock probability
        if is_habitable:
            probability = random.uniform(0.6, 0.98)
        else:
            probability = random.uniform(0.01, 0.45)
        
        return jsonify({
            'is_habitable': is_habitable,
            'probability': probability
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("Atramentous Backend starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
