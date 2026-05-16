from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Fungsi TOPSIS sesuai rumus di Bab II dokumen lu
def calculate_topsis(matrix, weights):
    X = np.array(matrix)
    # Normalisasi [cite: 125]
    norm_X = X / np.sqrt((X**2).sum(axis=0))
    # Pembobotan [cite: 126]
    weighted_X = norm_X * weights
    
    # Solusi Ideal Positif & Negatif [cite: 127]
    ais_pos = np.max(weighted_X, axis=0)
    ais_neg = np.min(weighted_X, axis=0)
    
    # Jarak Euclidean [cite: 128]
    d_pos = np.sqrt(((weighted_X - ais_pos)**2).sum(axis=1))
    d_neg = np.sqrt(((weighted_X - ais_neg)**2).sum(axis=1))
    
    # Kedekatan Relatif (RC) [cite: 129]
    performance_score = d_neg / (d_pos + d_neg)
    return performance_score

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        # Data alternatif menu dari Tabel 3.7 laporan lu 
        # Kriteria: Energi, Protein, Lemak, Karbohidrat, Serat [cite: 83, 177]
        menus = [
            {"nama": "Menu 1 (Ayam Popcorn)", "data": [775, 24.6, 29.4, 96.7, 1]},
            {"nama": "Menu 6 (Siomay Kukus)", "data": [814, 33.4, 35.5, 96.4, 3.5]},
            {"nama": "Menu 7 (Ayam Kuning)", "data": [681, 26.8, 29.8, 83.1, 2.2]}
        ]
        
        # Bobot kriteria (contoh default)
        weights = [0.3, 0.25, 0.15, 0.2, 0.1]
        
        matrix = [m['data'] for m in menus]
        scores = calculate_topsis(matrix, weights)
        
        for i, score in enumerate(scores):
            menus[i]['score'] = round(score, 4)
            
        results = sorted(menus, key=lambda x: x['score'], reverse=True)
        
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)