from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    try:
        input_data = np.array([[
            float(data['radius']),
            float(data['mass']),
            float(data['orbital_period']),
            float(data['temperature']),
            float(data['star_temp']),
            float(data['distance'])
        ]])

        input_scaled = scaler.transform(input_data)

        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]

        return jsonify({
            "prediction": "Habitable" if prediction == 1 else "Not Habitable",
            "probability": round(probability * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/visualize', methods=['GET'])
def visualize():
    import plotly
    import plotly.express as px
    import pandas as pd
    import json

    # Load dataset (Kepler mission data)
    df = pd.read_csv('exoplanets.csv')

    # Remove rows with missing values in key columns
    df = df.dropna(subset=['koi_teq', 'koi_prad', 'koi_period', 'koi_insol'])

    # Create habitability column based on equilibrium temperature and planet radius
    df['habitable'] = (
        (df['koi_teq'] > 240) & (df['koi_teq'] < 320) &
        (df['koi_prad'] < 2.5)
    ).astype(int)

    # Plot 1: Scatter Plot - Insolation vs Temperature
    fig1 = px.scatter(
        df,
        x='koi_insol',
        y='koi_teq',
        color='habitable',
        title="Insolation Flux vs Equilibrium Temperature",
        labels={
            'koi_insol': 'Insolation Flux (Earth Flux)',
            'koi_teq': 'Equilibrium Temperature (K)',
            'habitable': 'Potentially Habitable'
        },
        color_discrete_map={0: '#f87171', 1: '#4ade80'}
    )

    # Plot 2: Histogram - Planet Radius Distribution
    fig2 = px.histogram(
        df,
        x='koi_prad',
        nbins=50,
        title="Planet Radius Distribution",
        labels={'koi_prad': 'Planet Radius (Earth Radii)'}
    )

    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({
        'chart1': json.loads(graphJSON1),
        'chart2': json.loads(graphJSON2)
    })