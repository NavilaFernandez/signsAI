import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

# ─── CONFIGURACIÓN ────────────────────────────────────────────
DATASET_PATH = r"C:\wamp64\www\IA2\señas-ai\dataset\asl_alphabet_train"
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASES = 29

# ─── GENERADORES DE DATOS ─────────────────────────────────────
# Usamos solo 30% del dataset para que no tarde horas
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=10,
    zoom_range=0.1,
    horizontal_flip=True
)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    seed=42
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    seed=42
)

print(f"\n Clases encontradas: {train_data.class_indices}\n")

# ─── MODELO CON TRANSFER LEARNING ─────────────────────────────
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# Congelamos la base, solo entrenamos las capas nuevas
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(NUM_CLASES, activation='softmax')(x)

modelo = Model(inputs=base_model.input, outputs=output)

modelo.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ─── ENTRENAMIENTO ─────────────────────────────────────────────
print(" Iniciando entrenamiento...\n")

# Guardamos el mejor modelo automáticamente
checkpoint = tf.keras.callbacks.ModelCheckpoint(
    'modelo.h5',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

# Detenemos si no mejora después de 3 épocas
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=3,
    verbose=1
)

historia = modelo.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=[checkpoint, early_stopping]
)

# ─── RESULTADO FINAL ───────────────────────────────────────────
precision_final = max(historia.history['val_accuracy'])
print(f"\n Entrenamiento terminado")
print(f" Mejor precisión: {precision_final * 100:.2f}%")
print(f" Modelo guardado como modelo.h5")

# Guardamos las clases en un archivo para usarlas en la app
import json
clases = train_data.class_indices
clases_invertidas = {v: k for k, v in clases.items()}
with open('clases.json', 'w') as f:
    json.dump(clases_invertidas, f)
print(" Clases guardadas en clases.json")