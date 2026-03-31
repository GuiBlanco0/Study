import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import statsmodels.api as sm
import os

# ============================================================================
# CARREGAR OS DADOS
# ============================================================================

print("="*80)
print("REGRESSÃO LINEAR MÚLTIPLA")
print("Dispositivos + HorasUso + Temperatura → Consumo_kWh")
print("="*80)

# Encontrar o arquivo CSV
arquivos_csv = [f for f in os.listdir('.') if f.endswith('.csv')]

if arquivos_csv:
    nome_arquivo = arquivos_csv[0]
    print(f"\n📂 Arquivo encontrado: {nome_arquivo}")
    df = pd.read_csv(nome_arquivo)
    print(f"✅ Dados carregados: {df.shape[0]} linhas e {df.shape[1]} colunas")
else:
    print("❌ Arquivo CSV não encontrado!")
    exit()

# Mostrar primeiras linhas
print("\n" + "-"*50)
print("PRIMEIRAS 5 LINHAS DOS DADOS:")
print("-"*50)
print(df.head())

print("\n" + "-"*50)
print("ESTATÍSTICAS DESCRITIVAS:")
print("-"*50)
print(df.describe())

# ============================================================================
# ANÁLISE EXPLORATÓRIA
# ============================================================================

print("\n" + "="*80)
print("1. ANÁLISE EXPLORATÓRIA")
print("="*80)

# Matriz de correlação
correlacao = df[['Dispositivos', 'HorasUso', 'Temperatura', 'Consumo_kWh']].corr()
print("\nMatriz de Correlação:")
print(correlacao)

# Gráficos de dispersão
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Dispositivos vs Consumo
axes[0, 0].scatter(df['Dispositivos'], df['Consumo_kWh'], alpha=0.6, color='steelblue')
axes[0, 0].set_xlabel('Dispositivos')
axes[0, 0].set_ylabel('Consumo (kWh)')
axes[0, 0].set_title('Dispositivos vs Consumo')
axes[0, 0].grid(True, alpha=0.3)

# HorasUso vs Consumo
axes[0, 1].scatter(df['HorasUso'], df['Consumo_kWh'], alpha=0.6, color='steelblue')
axes[0, 1].set_xlabel('Horas de Uso')
axes[0, 1].set_ylabel('Consumo (kWh)')
axes[0, 1].set_title('Horas de Uso vs Consumo')
axes[0, 1].grid(True, alpha=0.3)

# Temperatura vs Consumo
axes[0, 2].scatter(df['Temperatura'], df['Consumo_kWh'], alpha=0.6, color='steelblue')
axes[0, 2].set_xlabel('Temperatura (°C)')
axes[0, 2].set_ylabel('Consumo (kWh)')
axes[0, 2].set_title('Temperatura vs Consumo')
axes[0, 2].grid(True, alpha=0.3)

# Heatmap de correlação
sns.heatmap(correlacao, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, fmt='.3f', ax=axes[1, 0])
axes[1, 0].set_title('Matriz de Correlação')

# Distribuição das variáveis
axes[1, 1].hist(df['Consumo_kWh'], bins=20, edgecolor='black', alpha=0.7, color='steelblue')
axes[1, 1].set_xlabel('Consumo (kWh)')
axes[1, 1].set_ylabel('Frequência')
axes[1, 1].set_title('Distribuição do Consumo')
axes[1, 1].grid(True, alpha=0.3)

# Boxplot
df_melt = df.melt(var_name='Variável', value_name='Valor')
sns.boxplot(data=df_melt, x='Variável', y='Valor', ax=axes[1, 2])
axes[1, 2].set_title('Boxplot das Variáveis')
axes[1, 2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# ============================================================================
# MODELO DE REGRESSÃO LINEAR MÚLTIPLA
# ============================================================================

print("\n" + "="*80)
print("2. MODELO DE REGRESSÃO LINEAR MÚLTIPLA")
print("="*80)

# Definir variáveis
X = df[['Dispositivos', 'HorasUso', 'Temperatura']]
y = df['Consumo_kWh']

# Modelo com scikit-learn
modelo_sk = LinearRegression()
modelo_sk.fit(X, y)

# Coeficientes
intercepto = modelo_sk.intercept_
coef_dispositivos = modelo_sk.coef_[0]
coef_horas = modelo_sk.coef_[1]
coef_temp = modelo_sk.coef_[2]

print(f"\n📈 EQUAÇÃO DO MODELO:")
print(f"Consumo_kWh = {intercepto:.4f} + {coef_dispositivos:.4f}·Dispositivos + {coef_horas:.4f}·HorasUso + {coef_temp:.4f}·Temperatura")

# Modelo com statsmodels (para estatísticas detalhadas)
X_const = sm.add_constant(X)
modelo_stats = sm.OLS(y, X_const).fit()

print("\n" + "-"*50)
print("RESUMO ESTATÍSTICO DETALHADO:")
print("-"*50)
print(modelo_stats.summary())

# ============================================================================
# INTERPRETAÇÃO DOS COEFICIENTES
# ============================================================================

print("\n" + "="*80)
print("3. INTERPRETAÇÃO DOS COEFICIENTES")
print("="*80)

print(f"""
β₀ (Intercepto) = {intercepto:.4f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interpretação: Quando todas as variáveis independentes são zero 
(0 dispositivos, 0 horas de uso, 0°C), o consumo estimado é de {intercepto:.4f} kWh.

Embora tecnicamente correto, este cenário não é realista na prática, 
pois é impossível ter temperatura de 0°C e consumo zero nestas condições.
O intercepto serve para ajustar a equação aos dados observados.
""")

print(f"""
β₁ (Dispositivos) = {coef_dispositivos:.4f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interpretação: Mantendo as horas de uso e a temperatura constantes, 
a cada 1 dispositivo adicional conectado, o consumo de energia 
aumenta em média {coef_dispositivos:.4f} kWh.

Exemplo: Se uma residência tem 5 dispositivos e aumenta para 6, 
mantendo as mesmas horas de uso e temperatura, o consumo aumentará 
aproximadamente {coef_dispositivos:.4f} kWh.
""")

print(f"""
β₂ (HorasUso) = {coef_horas:.4f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interpretação: Mantendo o número de dispositivos e a temperatura constantes, 
a cada 1 hora adicional de uso, o consumo de energia 
aumenta em média {coef_horas:.4f} kWh.

Exemplo: Se uma residência aumenta o tempo de uso de 5 para 6 horas, 
mantendo os mesmos dispositivos e temperatura, o consumo aumentará 
aproximadamente {coef_horas:.4f} kWh.
""")

print(f"""
β₃ (Temperatura) = {coef_temp:.4f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interpretação: Mantendo o número de dispositivos e as horas de uso constantes, 
a cada 1°C de aumento na temperatura ambiente, o consumo de energia 
aumenta em média {coef_temp:.4f} kWh.

Exemplo: Se a temperatura sobe de 25°C para 26°C, mantendo os mesmos 
dispositivos e horas de uso, o consumo aumentará aproximadamente 
{coef_temp:.4f} kWh.
""")

# ============================================================================
# MÉTRICAS DE AVALIAÇÃO
# ============================================================================

print("\n" + "="*80)
print("4. MÉTRICAS DE AVALIAÇÃO DO MODELO")
print("="*80)

# Previsões
y_pred = modelo_sk.predict(X)

# Calcular métricas
mse = mean_squared_error(y, y_pred)
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y, y_pred)

# R² ajustado
n = len(y)
k = X.shape[1]
r2_ajustado = 1 - (1 - r2) * (n - 1) / (n - k - 1)

print(f"\n📊 MSE (Mean Squared Error - Erro Quadrático Médio):")
print(f"MSE = {mse:.4f}")
print(f"Interpretação: Em média, o quadrado do erro é {mse:.4f} kWh²")

print(f"\n📊 MAE (Mean Absolute Error - Erro Absoluto Médio):")
print(f"MAE = {mae:.4f} kWh")
print(f"Interpretação: Em média, as previsões do modelo erram por {mae:.4f} kWh")

print(f"\n📊 RMSE (Root Mean Squared Error):")
print(f"RMSE = {rmse:.4f} kWh")
print(f"Interpretação: O desvio padrão dos erros é de aproximadamente {rmse:.4f} kWh")

print(f"\n📊 R² (Coeficiente de Determinação):")
print(f"R² = {r2:.4f}")
print(f"R² Ajustado = {r2_ajustado:.4f}")
print(f"Interpretação: {r2*100:.2f}% da variação do consumo de energia")
print(f"é explicada pelas variáveis Dispositivos, HorasUso e Temperatura")

# ============================================================================
# ANÁLISE DOS RESÍDUOS
# ============================================================================

print("\n" + "="*80)
print("5. ANÁLISE DOS RESÍDUOS")
print("="*80)

residuos = y - y_pred

print(f"\nEstatísticas dos resíduos:")
print(f"Média: {residuos.mean():.6f}")
print(f"Desvio Padrão: {residuos.std():.4f}")
print(f"Mínimo: {residuos.min():.4f}")
print(f"Máximo: {residuos.max():.4f}")

# Gráficos de resíduos
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Resíduos vs Valores Previstos
axes[0, 0].scatter(y_pred, residuos, alpha=0.6, color='steelblue')
axes[0, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0, 0].set_xlabel('Valores Previstos (kWh)')
axes[0, 0].set_ylabel('Resíduos')
axes[0, 0].set_title('Resíduos vs Valores Previstos')
axes[0, 0].grid(True, alpha=0.3)

# Histograma dos resíduos
axes[0, 1].hist(residuos, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
axes[0, 1].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[0, 1].set_xlabel('Resíduos')
axes[0, 1].set_ylabel('Frequência')
axes[0, 1].set_title('Distribuição dos Resíduos')
axes[0, 1].grid(True, alpha=0.3)

# Q-Q Plot
import scipy.stats as stats
stats.probplot(residuos, dist="norm", plot=axes[0, 2])
axes[0, 2].set_title('Q-Q Plot - Normalidade dos Resíduos')
axes[0, 2].grid(True, alpha=0.3)

# Resíduos vs Dispositivos
axes[1, 0].scatter(df['Dispositivos'], residuos, alpha=0.6, color='steelblue')
axes[1, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Dispositivos')
axes[1, 0].set_ylabel('Resíduos')
axes[1, 0].set_title('Resíduos vs Dispositivos')
axes[1, 0].grid(True, alpha=0.3)

# Resíduos vs HorasUso
axes[1, 1].scatter(df['HorasUso'], residuos, alpha=0.6, color='steelblue')
axes[1, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Horas de Uso')
axes[1, 1].set_ylabel('Resíduos')
axes[1, 1].set_title('Resíduos vs Horas de Uso')
axes[1, 1].grid(True, alpha=0.3)

# Resíduos vs Temperatura
axes[1, 2].scatter(df['Temperatura'], residuos, alpha=0.6, color='steelblue')
axes[1, 2].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1, 2].set_xlabel('Temperatura (°C)')
axes[1, 2].set_ylabel('Resíduos')
axes[1, 2].set_title('Resíduos vs Temperatura')
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Teste de normalidade
shapiro_stat, shapiro_p = stats.shapiro(residuos)
print(f"\nTeste de Shapiro-Wilk (normalidade):")
print(f"Estatística: {shapiro_stat:.4f}")
print(f"p-valor: {shapiro_p:.4f}")
if shapiro_p > 0.05:
    print("✅ Resíduos seguem distribuição normal (p > 0.05)")
else:
    print("⚠️  Resíduos podem não seguir distribuição normal (p < 0.05)")

# ============================================================================
# PREVISÕES COM O MODELO
# ============================================================================

print("\n" + "="*80)
print("6. PREVISÕES COM O MODELO")
print("="*80)

# Criar cenários para previsão
cenarios = [
    {"Dispositivos": 5, "HorasUso": 4, "Temperatura": 25, "descricao": "Cenário 1: Uso moderado"},
    {"Dispositivos": 8, "HorasUso": 6, "Temperatura": 28, "descricao": "Cenário 2: Uso intenso, dia quente"},
    {"Dispositivos": 10, "HorasUso": 8, "Temperatura": 30, "descricao": "Cenário 3: Uso muito intenso, dia muito quente"},
    {"Dispositivos": 3, "HorasUso": 2, "Temperatura": 22, "descricao": "Cenário 4: Uso leve, dia ameno"},
    {"Dispositivos": 12, "HorasUso": 9, "Temperatura": 31, "descricao": "Cenário 5: Uso extremo, calor intenso"}
]

print("\nPrevisões de consumo para diferentes cenários:")
print("-"*80)
for cenario in cenarios:
    pred = modelo_sk.predict([[cenario["Dispositivos"], cenario["HorasUso"], cenario["Temperatura"]]])[0]
    print(f"\n{cenario['descricao']}:")
    print(f"  Dispositivos: {cenario['Dispositivos']} | Horas: {cenario['HorasUso']}h | Temp: {cenario['Temperatura']}°C")
    print(f"  Consumo previsto: {pred:.2f} kWh")

# ============================================================================
# COMPARAÇÃO COM MODELO SIMPLES
# ============================================================================

print("\n" + "="*80)
print("7. COMPARAÇÃO: MODELO SIMPLES vs MODELO MÚLTIPLO")
print("="*80)

# Modelo simples (apenas Dispositivos)
X_simples = df[['Dispositivos']]
modelo_simples = LinearRegression()
modelo_simples.fit(X_simples, y)
y_pred_simples = modelo_simples.predict(X_simples)
r2_simples = r2_score(y, y_pred_simples)
mse_simples = mean_squared_error(y, y_pred_simples)
mae_simples = mean_absolute_error(y, y_pred_simples)

print(f"\nModelo Simples (apenas Dispositivos):")
print(f"  R²: {r2_simples:.4f}")
print(f"  MSE: {mse_simples:.4f}")
print(f"  MAE: {mae_simples:.4f} kWh")

print(f"\nModelo Múltiplo (Dispositivos + HorasUso + Temperatura):")
print(f"  R²: {r2:.4f}")
print(f"  MSE: {mse:.4f}")
print(f"  MAE: {mae:.4f} kWh")

print(f"\n📊 Melhoria do modelo múltiplo:")
print(f"  R² aumentou em: {(r2 - r2_simples)*100:.2f}%")
print(f"  MSE reduziu em: {(1 - mse/mse_simples)*100:.2f}%")
print(f"  MAE reduziu em: {(1 - mae/mae_simples)*100:.2f}%")

# ============================================================================
# RESPOSTAS FINAIS
# ============================================================================

print("\n" + "="*80)
print("8. RESUMO FINAL - RESPOSTAS DAS PERGUNTAS")
print("="*80)

print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    RESPOSTAS DAS PERGUNTAS - REGRESSÃO MÚLTIPLA            ║
╚════════════════════════════════════════════════════════════════════════════╝

1️⃣ EQUAÇÃO DO MODELO:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Consumo_kWh = {intercepto:.4f} + {coef_dispositivos:.4f}·X₁ + {coef_horas:.4f}·X₂ + {coef_temp:.4f}·X₃
   
   Onde:
   X₁ = Dispositivos
   X₂ = HorasUso
   X₃ = Temperatura

2️⃣ INTERPRETAÇÃO DO COEFICIENTE β₀ (Intercepto = {intercepto:.4f}):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Quando não há dispositivos (0), zero horas de uso (0) e temperatura de 0°C,
   o consumo estimado é de {intercepto:.4f} kWh.
   
   ⚠️  Observação: Este é um valor teórico, pois na prática não ocorrem 
   temperaturas de 0°C com consumo zero.

3️⃣ INTERPRETAÇÃO DO COEFICIENTE β₁ (Dispositivos = {coef_dispositivos:.4f}):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Mantendo as horas de uso e temperatura constantes, a cada 1 dispositivo
   adicional, o consumo aumenta em média {coef_dispositivos:.4f} kWh.

4️⃣ INTERPRETAÇÃO DO COEFICIENTE β₂ (HorasUso = {coef_horas:.4f}):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Mantendo dispositivos e temperatura constantes, a cada 1 hora adicional
   de uso, o consumo aumenta em média {coef_horas:.4f} kWh.

5️⃣ INTERPRETAÇÃO DO COEFICIENTE β₃ (Temperatura = {coef_temp:.4f}):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Mantendo dispositivos e horas de uso constantes, a cada 1°C de aumento
   na temperatura, o consumo aumenta em média {coef_temp:.4f} kWh.

6️⃣ MSE (Mean Squared Error):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   MSE = {mse:.4f}
   
   Interpretação: A média dos quadrados dos erros é {mse:.4f} kWh².

7️⃣ MAE (Mean Absolute Error):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   MAE = {mae:.4f} kWh
   
   Interpretação: Em média, as previsões do modelo erram por {mae:.4f} kWh.

8️⃣ R² (Coeficiente de Determinação):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   R² = {r2:.4f}
   R² Ajustado = {r2_ajustado:.4f}
   
   Interpretação: {r2*100:.2f}% da variação do consumo de energia é explicada
   pelas variáveis Dispositivos, HorasUso e Temperatura.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ O modelo apresenta um ajuste {'EXCELENTE' if r2 > 0.95 else 'MUITO BOM' if r2 > 0.9 else 'BOM'}
   com R² = {r2:.4f} e erros baixos (MAE = {mae:.4f} kWh).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# Salvar resultados em arquivo
with open('resultados_regressao_multipla.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("RESULTADOS DA REGRESSÃO LINEAR MÚLTIPLA\n")
    f.write("="*80 + "\n\n")
    f.write(f"EQUAÇÃO: Consumo_kWh = {intercepto:.4f} + {coef_dispositivos:.4f}·Dispositivos + {coef_horas:.4f}·HorasUso + {coef_temp:.4f}·Temperatura\n\n")
    f.write(f"MSE: {mse:.4f}\n")
    f.write(f"MAE: {mae:.4f} kWh\n")
    f.write(f"R²: {r2:.4f}\n")
    f.write(f"R² Ajustado: {r2_ajustado:.4f}\n\n")
    
    f.write("COEFICIENTES:\n")
    f.write(f"β₀ (Intercepto): {intercepto:.4f}\n")
    f.write(f"β₁ (Dispositivos): {coef_dispositivos:.4f}\n")
    f.write(f"β₂ (HorasUso): {coef_horas:.4f}\n")
    f.write(f"β₃ (Temperatura): {coef_temp:.4f}\n")
    f.write("="*80 + "\n")

print("\n📁 Resultados salvos em 'resultados_regressao_multipla.txt'")
print("\n✅ ANÁLISE CONCLUÍDA COM SUCESSO!")