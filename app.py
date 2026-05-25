from flask import Flask, render_template, Response, jsonify
import tensorflow as tf
import cv2
import numpy as np
import json

app = Flask(__name__)

#cargar modelo y las clases json
modelo = tf.keras.models.load_model(r"C:\wamp64\www\IA2\señas-ai\modelo.h5")

with open(r"C:\wamp64\www\IA2\señas-ai\clases.json", 'r') as f:
    clases = json.load(f)

# configuracion camara
camara = cv2.VideoCapture(0)
ultima_prediccion = {"letra": "", "confianza": 0}

# procesamiento dle framw
def preprocesar(frame):
    img = cv2.resize(frame, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# video
def generar_frames():
    global ultima_prediccion
    contador = 0

    while True:
        success, frame = camara.read()
        if not success:
            break
        frame = cv2.flip(frame, 1) #invierte la camara 


        # cuadro verde
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = w//2 - 150, h//2 - 150, w//2 + 150, h//2 + 150
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, "Pon tu mano aqui", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # cada 15fps predice
        contador += 1
        if contador % 15 == 0:
            roi = frame[y1:y2, x1:x2]
            if roi.size > 0:
                img = preprocesar(roi)
                prediccion = modelo.predict(img, verbose=0)
                indice = np.argmax(prediccion)
                confianza = float(np.max(prediccion))
                letra = clases[str(indice)]
                ultima_prediccion = {
                    "letra": letra,
                    "confianza": round(confianza * 100, 2)
                }

        # prediccion
        letra = ultima_prediccion.get("letra", "")
        confianza = ultima_prediccion.get("confianza", 0)
        if letra:
            cv2.putText(frame, f"{letra} ({confianza}%)",
                        (x1, y2 + 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                        (0, 255, 0), 3)

        # Convertir a jpg
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame_bytes + b'\r\n')
# rutas de archivos
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(
        generar_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/prediccion')
def prediccion():
    return jsonify(ultima_prediccion)


# start app
if __name__ == '__main__':
    app.run(debug=False)

