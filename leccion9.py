import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ── Conexión 

import os
from dotenv import load_dotenv

load_dotenv()                              # .env

url = URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),  
    host="localhost",
    port=5432,
    database="planta",
)

engine = create_engine(url)

# ── Traer la tabla de turnos ────────────────────────────
df = pd.read_sql("""
SELECT * FROM turnos """, engine, parse_dates=["fecha"])
print(df)

#turnos con recuperación menor a 85.
print(df[df["recuperacion"] < 85])

#Se agrehga una columna cu_perdido y muestra fecha, turno y esa columna, ordenada de mayor a menor.


df["cu_alimentado"] = df["tonelaje"] * df["ley_cabeza"] / 100
df["cu_fino"] = df["cu_alimentado"] * df["recuperacion"] /100
df["cu_perdido"] = df["cu_alimentado"] - df["cu_fino"]

rec_planta = df["cu_fino"].sum() / df["cu_alimentado"].sum() * 100
print(round(rec_planta, 2))
print(df[["fecha", "turno", "cu_perdido"]].sort_values("cu_perdido", ascending=False)) #Recuperacion 

#Con groupby y agg, calcula por turno el tonelaje promedio y la recuperación máxima

calculo = df.groupby("turno").agg(
    tonelaje_promedio = ("tonelaje", "mean"),
    rec_promedio      = ("recuperacion", "mean"),
    rec_maxima        = ("recuperacion", "max"),
)
print(calculo)
#consumos con la función de cada reactivo y los kg totales por función (Colector, Espumante...).

df_consumos = pd.read_sql("""SELECT * FROM consumos """, engine , parse_dates=["fecha"])
df_reactivos = pd.read_sql("SELECT * FROM reactivos", engine)

print(df_consumos)
print(df_reactivos)

union = df_consumos.merge(df_reactivos, on="id_reactivo") 
resultado = union.groupby("funcion").agg(kg_totales = ("kg", "sum"))
print(resultado)

#por turno, el tonelaje total, la ley de cabeza mínima y la cantidad de turnos.

resumen = df.groupby("turno").agg(
    tonelaje_total = ("tonelaje", "sum"),
    ley_min      = ("ley_cabeza", "min"),
    turnos      = ("id_turno", "count"),
)
print(resumen)



#print(df.head(3))       # las primeras 3 filas
#print(df.shape)         # (filas, columnas)
#df.info()               # columnas, tipos y datos faltantes
print(df.describe())    # estadísticas de las columnas numéricas



#_____________________
#Trae a un DataFrame las detenciones con el nombre y el área del equipo. Pista: escribe el JOIN dentro del texto de pd.read_sql.
#df_det = pd.read_sql("""
 #   SELECT t.fecha,
  #         t.turno,
   #        e.nombre AS equipo,
    #       e.area,
     #      d.causa,
      #     d.horas
    #FROM detenciones AS d
    #INNER JOIN equipos AS e ON d.id_equipo = e.id_equipo
    #INNER JOIN turnos  AS t ON d.id_turno  = t.id_turno
    #ORDER BY t.fecha, t.turno
#""", engine, parse_dates=["fecha"])

#print(df_det)

# #  tabla por separado
# turnos      = pd.read_sql("SELECT * FROM turnos", engine, parse_dates=["fecha"])
# detenciones = pd.read_sql("SELECT * FROM detenciones", engine)
# equipos     = pd.read_sql("SELECT * FROM equipos", engine)

# # 2. Unir de a una, con merge (el JOIN de pandas)
# paso1 = detenciones.merge(equipos, on="id_equipo")    # detenciones + equipos
# paso2 = paso1.merge(turnos, on="id_turno")            # + turnos

# # 3. Elegir columnas y ordenar
# resultado = paso2[["fecha", "turno", "nombre", "area", "causa", "horas"]]
# print(resultado.sort_values(["fecha", "turno"]))



#Pregunta de analista: df.describe() muestra una recuperación promedio (mean) de 87,375 %.
#¿Puedes informar ese número como la recuperación de la planta? ¿Por qué?