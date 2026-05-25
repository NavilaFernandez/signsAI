from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ruta de tu dataset (la misma que usaste)
DATASET_PATH = r"C:\wamp64\www\IA2\señas-ai\dataset\asl_alphabet_train"

IMG_SIZE = 224
BATCH_SIZE = 32

# solo normalización (NO augmentation aquí)
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    seed=42
)

# cargar modelo ya entrenado
modelo = load_model(r"C:\wamp64\www\IA2\señas-ai\modelo.h5")

# evaluar
loss, acc = modelo.evaluate(val_data)

print("Loss:", loss)
print("Accuracy:", acc)