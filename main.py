from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import tratado as tr

app = Flask(__name__)

# Carga del modelo SVM
svm_model = joblib.load('modelo_svm.joblib')

# Ruta principal para cargar la página HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/csv')
def csv():
    # Lógica para renderizar la plantilla HTML del formulario de carga de CSV
    return render_template('csv.html')

@app.route('/review')
def review():
    # Lógica para renderizar la plantilla HTML del formulario de carga de texto
    return render_template('review.html')

# Rutas para la predicción de texto
@app.route('/predict_text', methods=['POST', 'GET'])
def predict_text():
    if request.method == 'POST':
        data = request.json
        text = data['text']
    elif request.method == 'GET':
        text = request.args.get('text', '')

    text = tr.limpiar_texto(text)
    prediction = svm_model.predict([text])[0]
    prediction = int(prediction)  # Convertir la predicción a tipo int
    return jsonify({'prediction': prediction})

# Rutas para la predicción de archivos CSV
@app.route('/predict_csv', methods=['POST', 'GET'])
def predict_csv():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        df = df.dropna(subset=['Review'])
        df = df.drop_duplicates(subset=['Review'])
        df = df.explode('Review')
        df = df.reset_index(drop=True)
        df["Review"] = df["Review"].str.replace(r'\n', '')
        texto = df['Review'].apply(tr.limpiar_texto)
        df['prediction'] = svm_model.predict(texto)
        df['prediction'] = df['prediction'].astype(int)  # Convertir la columna 'prediction' a tipo int
        df['ID'] = df.index + 1  # Añade la columna de ID
        reviews = df[['Review', 'prediction', 'ID']].to_dict(orient='records')  # Convertir DataFrame a lista de diccionarios
        return jsonify({'reviews': reviews})  # Enviar objeto JSON con las reseñas y predicciones
    elif request.method == 'GET':
        resultado = {'mensaje': 'Predicción de CSV aún no implementada'}  
        return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)
