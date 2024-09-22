import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class TimeSeriesTransformer(nn.Module):
    def __init__(self, input_size, d_model, nhead, num_encoder_layers, dim_feedforward, output_size):
        super(TimeSeriesTransformer, self).__init__()
        self.embedding = nn.Linear(input_size, d_model)
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=0.1
            ),
            num_layers=num_encoder_layers
        )
        self.fc = nn.Linear(d_model, output_size)

    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        
        # Tomar solo la última salida de la secuencia para cada ejemplo en el batch
        x = x[:, -1, :]  # Seleccionamos la última predicción de la secuencia
        
        return self.fc(x)

