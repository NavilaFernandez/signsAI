#  SeñasAI - Traductor de Lenguaje de Señas en Tiempo Real

SeñasAI es una aplicación de inteligencia artificial que reconoce letras del alfabeto del lenguaje de señas en tiempo real usando la cámara web.  
Está construida con **Flask + TensorFlow + OpenCV** y utiliza un modelo de **Transfer Learning con MobileNetV2**.


## ¿Qué hace este proyecto?

- Detecta la mano en tiempo real usando la webcam
- Clasifica letras del alfabeto ASL (A-Z)
- Muestra la letra predicha con porcentaje de confianza
- Permite deletrear palabras con sistema de verificación
- Interfaz web interactiva y visual


## Tecnologías utilizadas

- Python
- Flask
- TensorFlow / Keras
- OpenCV
- NumPy
- MobileNetV2 (Transfer Learning)
- HTML, CSS, JavaScript


##  Estructura del proyecto
senas-ai/
│
├── app.py 
├── entrenamiento.py 
├── modelo.h5 
├── clases.json
│
├── templates/
│ └── index.html 
│
├── static/
│ ├── style.css
│ ├── script.js
│ └── signs/ 
│
└── dataset/ 
├── asl_alphabet_test/
│── asl_alphabet_train/


---

##  Instalación

### 1. Clonar el repositorio

git clone https://github.com/tu_usuario/senas-ai.git
cd senas-ai

## Instalar dependencias

pip install -r requirements.txt

## Ejecutar la aplicación

python app.py

http://127.0.0.1:5000/