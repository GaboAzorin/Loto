import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

# Conectar a la base de datos
conexion = sqlite3.connect('loto.db')

# Consultar la tabla 'posibilidades'
query = "SELECT sorteo_id, n1_loto, n2_loto, n3_loto, n4_loto, n5_loto, n6_loto FROM posibilidades"
df = pd.read_sql_query(query, conexion)

# Cálculo de estadísticas descriptivas
print(df.describe())

# Cerrar conexión
conexion.close()

# Gráficos de línea para cada columna
for col in df.columns[1:]:
    plt.plot(df["sorteo_id"], df[col], label=col)
plt.legend()
plt.title("Tendencia de cada columna a lo largo de los sorteos")
plt.show()

# Histogramas
for col in df.columns[1:]:
    df[col].hist()
    plt.title(f"Distribución de {col}")
    plt.show()

# Boxplots
df[df.columns[1:]].boxplot()
plt.title("Boxplots de cada columna")
plt.show()

correlation_matrix = df[df.columns[1:]].corr()
print(correlation_matrix)

for col in df.columns[1:]:
    df[f"{col}_diff"] = df[col].diff().fillna(0)
print(df.head())

# Usando n1_loto_mas_comun para predecir n2_loto_mas_comun
X = df[["n1_loto"]]
y = df["n2_loto"]

model = LinearRegression().fit(X, y)
print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")

kmeans = KMeans(n_clusters=3)
df["cluster"] = kmeans.fit_predict(df[df.columns[1:]])

# Mostrar el centro de cada cluster
print(kmeans.cluster_centers_)

# Visualizar clusters para dos columnas (ejemplo: n1_loto_mas_comun y n2_loto_mas_comun)
plt.scatter(df["n1_loto"], df["n2_loto"], c=df["cluster"])
plt.show()