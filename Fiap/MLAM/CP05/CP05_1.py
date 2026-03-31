import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
import os

# ============================================================================
# CARREGAR OS DADOS
# ============================================================================

# Encontrar o arquivo CSV
arquivos_csv = [f for f in os.listdir('.') if f.endswith('.csv')]
if arquivos_csv:
    df = pd.read_csv(arquivos_csv[0])
    print("✅ Dados carregados com sucesso!")
    print(f"Shape: {df.shape}")
else:
    print("❌ Arquivo CSV não encontrado!")
    exit()

# ============================================================================
# REGRESSÃO LINEAR SIMPLES
# ============================================================================

# Definir variáveis
X = df[['Dispositivos']]  # Variável independente
y = df['Consumo_kWh']      # Variável dependente

# Ajustar modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Coeficientes
intercepto = modelo.intercept_
coeficiente = modelo.coef_[0]

print("\n" + "="*60)
print("RESULTADOS DA REGRESSÃO LINEAR SIMPLES")
print("="*60)

print(f"\n📈 EQUAÇÃO DO MODELO:")
print(f"Consumo_kWh = {intercepto:.4f} + {coeficiente:.4f} × Dispositivos")

# ============================================================================
# CÁLCULO DO R²
# ============================================================================

y_pred = modelo.predict(X)
r2 = r2_score(y, y_pred)

print(f"\n📊 COEFICIENTE DE DETERMINAÇÃO (R²):")
print(f"R² = {r2:.4f}")
print(f"O modelo explica {r2*100:.2f}% da variação do consumo")

# ============================================================================
# CÁLCULO DO MSE
# ============================================================================

mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)

print(f"\n📉 MSE (Mean Squared Error):")
print(f"MSE = {mse:.4f}")
print(f"RMSE = {rmse:.4f} kWh")

# ============================================================================
# ANÁLISE DETALHADA (statsmodels)
# ============================================================================

X_const = sm.add_constant(X)
modelo_stats = sm.OLS(y, X_const).fit()

print("\n" + "="*60)
print("ANÁLISE ESTATÍSTICA DETALHADA")
print("="*60)
print(modelo_stats.summary())

# ============================================================================
# GRÁFICOS
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Gráfico de dispersão com reta de regressão
axes[0, 0].scatter(X, y, alpha=0.6, s=50, color='steelblue')
axes[0, 0].plot(X, y_pred, color='red', linewidth=2)
axes[0, 0].set_xlabel('Número de Dispositivos')
axes[0, 0].set_ylabel('Consumo (kWh)')
axes[0, 0].set_title(f'Regressão Linear: Dispositivos vs Consumo\nR² = {r2:.4f}')
axes[0, 0].grid(True, alpha=0.3)

# 2. Resíduos
residuos = y - y_pred
axes[0, 1].scatter(y_pred, residuos, alpha=0.6, s=50, color='steelblue')
axes[0, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0, 1].set_xlabel('Valores Previstos (kWh)')
axes[0, 1].set_ylabel('Resíduos')
axes[0, 1].set_title('Análise de Resíduos')
axes[0, 1].grid(True, alpha=0.3)

# 3. Histograma dos resíduos
axes[1, 0].hist(residuos, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Resíduos')
axes[1, 0].set_ylabel('Frequência')
axes[1, 0].set_title('Distribuição dos Resíduos')
axes[1, 0].grid(True, alpha=0.3)

# 4. Valores reais vs previstos
axes[1, 1].scatter(y, y_pred, alpha=0.6, s=50, color='steelblue')
axes[1, 1].plot([y.min(), y.max()], [y.min(), y.max()], 'r--', linewidth=2)
axes[1, 1].set_xlabel('Valores Reais (kWh)')
axes[1, 1].set_ylabel('Valores Previstos (kWh)')
axes[1, 1].set_title('Valores Reais vs Previstos')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================================
# PREVISÕES
# ============================================================================

print("\n" + "="*60)
print("PREVISÕES DO MODELO")
print("="*60)

dispositivos_teste = [2, 5, 8, 10, 12]
print(f"\n{'Dispositivos':<15} {'Consumo Previsto (kWh)':<20}")
print("-"*35)

for disp in dispositivos_teste:
    pred = modelo.predict([[disp]])[0]
    print(f"{disp:<15} {pred:.2f}")

# ============================================================================
# RESPOSTAS FINAIS
# ============================================================================

print("\n" + "="*60)
print("RESPOSTAS DAS PERGUNTAS")
print("="*60)

print(f"""
1️⃣ EQUAÇÃO DE REGRESSÃO LINEAR:
   
   Consumo_kWh = {intercepto:.4f} + {coeficiente:.4f} × Dispositivos

2️⃣ COEFICIENTE DE DETERMINAÇÃO (R²):
   
   R² = {r2:.4f}
   
   Interpretação: {r2*100:.2f}% da variação do consumo de energia 
   é explicada pelo número de dispositivos conectados.

3️⃣ MSE (Mean Squared Error):
   
   MSE = {mse:.4f}
   RMSE = {rmse:.4f} kWh
   
   Interpretação: Em média, as previsões do modelo erram 
   por aproximadamente {rmse:.2f} kWh.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 INTERPRETAÇÃO DOS COEFICIENTES:

• Coeficiente angular ({coeficiente:.4f}): 
  A cada dispositivo adicional, o consumo aumenta em média {coeficiente:.4f} kWh.

• Intercepto ({intercepto:.4f}): 
  Consumo base estimado quando não há dispositivos conectados.

• R² = {r2:.4f}: 
  {'Excelente ajuste!' if r2 > 0.95 else 'Bom ajuste!' if r2 > 0.8 else 'Ajuste moderado.'}

• MSE = {mse:.4f}: 
  O erro quadrático médio indica a precisão do modelo.
""")

print("="*60)