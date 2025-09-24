import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# -----------------------------
# Datos de ejemplo
# -----------------------------
data = {
    "Componente": [
        "Motor","Motor","Motor",
        "Sensor","Sensor","Sensor",
        "CPU","CPU","CPU"
    ],
    "Modo": [0,1,1, 0,1,1, 0,1,1],
    "ConsumoWh": [0.2,1.5,1.7, 0.05,0.3,0.35, 0.1,0.8,1.0]
}

df = pd.DataFrame(data)

# Variables de entrada y salida
X = df[["Componente", "Modo"]]
y = df["ConsumoWh"]

# -----------------------------
# Preprocesador
# -----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("componente", OneHotEncoder(), ["Componente"])
    ],
    remainder="passthrough"
)

# -----------------------------
# Pipeline
# -----------------------------
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# Entrenar
pipeline.fit(X, y)

# -----------------------------
# Predicciones nuevas
# -----------------------------
nuevos_datos = pd.DataFrame({
    "Componente": ["Motor","Sensor","CPU"],
    "Modo": [1,0,1]
})

predicciones = pipeline.predict(nuevos_datos)

print("Predicciones de consumo energético (Wh):")
for dato, consumo in zip(nuevos_datos.to_dict(orient="records"), predicciones):
    print(f"{dato} → {consumo:.2f} Wh")