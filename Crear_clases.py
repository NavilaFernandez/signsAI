import json
import os

# Ruta de tu dataset
DATASET_PATH = r"C:\wamp64\www\IA2\señas-ai\dataset\asl_alphabet_train"

# Lee las carpetas y las ordena igual que el entrenamiento
clases = sorted(os.listdir(DATASET_PATH))
clases_invertidas = {i: clase for i, clase in enumerate(clases)}

with open('clases.json', 'w') as f:
    json.dump(clases_invertidas, f)

print(" clases.json creado:")
print(clases_invertidas)