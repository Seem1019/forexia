import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from transformer_model import TimeSeriesTransformer
from data_preparation import preparar_datos

# Parámetros del modelo
input_size = 4  # Precios de apertura, cierre, máximo, mínimo
d_model = 64
nhead = 4
num_encoder_layers = 2
dim_feedforward = 128
output_size = 1  # Predicción binaria: call o put
sequence_length = 20
batch_size = 128  # Ajustado el tamaño del batch
num_epochs = 1000  # Reducido el número de epochs

# Cargar las velas históricas desde el CSV generado
file_path = "data/historical_candles.csv"
df = pd.read_csv(file_path)

# Convertir el DataFrame en una lista de diccionarios (uno por cada vela)
velas = df.to_dict(orient="records")

# Preparar los datos (convertir a secuencias)
X, Y = preparar_datos(velas, sequence_length)

# Dividir en conjunto de entrenamiento y validación
X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=42)

# Convertir los datos en tensores de PyTorch
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
Y_train_tensor = torch.tensor(Y_train, dtype=torch.float32)
X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
Y_val_tensor = torch.tensor(Y_val, dtype=torch.float32)

# Crear el modelo Transformer
model = TimeSeriesTransformer(input_size=input_size, d_model=d_model, nhead=nhead,
                              num_encoder_layers=num_encoder_layers, dim_feedforward=dim_feedforward,
                              output_size=output_size)

# Definir el optimizador y la función de pérdida
optimizer = optim.Adam(model.parameters(), lr=0.00005)  # Reducida la tasa de aprendizaje
criterion = nn.BCEWithLogitsLoss()

# Implementar LR Scheduler (Reducción de la tasa de aprendizaje)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5, verbose=True)

# Variables para Early Stopping
best_val_loss = float("inf")
patience = 50  # Número de epochs sin mejora antes de detener el entrenamiento
trigger_times = 0

# Entrenamiento del modelo con Early Stopping
for epoch in range(num_epochs):
    model.train()  # Poner el modelo en modo de entrenamiento
    optimizer.zero_grad()

    # Forward (pasar los datos a través del modelo)
    outputs = model(X_train_tensor)
    loss = criterion(outputs.squeeze(), Y_train_tensor)

    # Backward (retropropagación del error)
    loss.backward()
    optimizer.step()

    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')

    # Evaluación en el conjunto de validación
    model.eval()  # Poner el modelo en modo de evaluación
    with torch.no_grad():
        val_outputs = model(X_val_tensor)
        val_loss = criterion(val_outputs.squeeze(), Y_val_tensor)
        print(f'Validation Loss: {val_loss.item()}')

        # Guardar el mejor modelo y verificar para Early Stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            trigger_times = 0
            torch.save(model.state_dict(), 'transformer_model_best.pth')  # Guardar el mejor modelo
            print(f"Mejor modelo guardado en epoch {epoch+1}")
        else:
            trigger_times += 1
            print(f"No improvement in validation loss. Trigger times: {trigger_times}/{patience}")

        # Detener el entrenamiento si no hay mejora en `patience` epochs
        if trigger_times >= patience:
            print("Early stopping triggered!")
            break

    # Actualizar la tasa de aprendizaje según el LR Scheduler
    scheduler.step(val_loss)

# Guardar el modelo entrenado
torch.save(model.state_dict(), 'transformer_model.pth')
