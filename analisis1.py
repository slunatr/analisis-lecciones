import sqlite3
from tkinter import ROUND
import pandas as pd

conexion = sqlite3.connect("planta.db")
cursor =    conexion.cursor()


#Se crea la tabla   

cursor.execute("DROP TABLE IF EXISTS producction")
cursor.execute("""
CREATE TABLE producction (
fecha       TEXT,
turno       TEXT,
tonelaje    REAL,
ley_cabeza  REAL,
recuperacion    REAL)""")


datos = [
    ("2026-09-01", "A", 5200, 0.85, 88.5),
    ("2026-09-01", "B", 4900, 0.82, 87.1),
    ("2026-09-02", "A", 5350, 0.90, 89.2),
    ("2026-09-02", "B", 3100, 0.78, 84.0),
    ("2026-09-03", "A", 5100, 0.88, 88.9),
    ("2026-09-03", "B", 5000, 0.86, 88.0),
    ("2026-09-04", "A", 4700, 0.75, 83.5),
    ("2026-09-04", "B", 5250, 0.91, 89.8),   
    
    ]

cursor.executemany("INSERT INTO producction VALUES  (?, ?, ?, ?,? )", datos)
conexion.commit()

def consulta(sql):
    print(pd.read_sql(sql, conexion), "\n")

#Dada la tabla realizar consultas 

consulta("SELECT * FROM producction")
#consulta("SELECT fecha, turno, recuperacion FROM producction")
#consulta("SELECT * FROM producction WHERE turno = 'A'")
#consulta("SELECT * FROM producction WHERE recuperacion > 85")
#consulta("SELECT * FROM producction ORDER BY tonelaje DESC LIMIT 3")

#ejercicios1


#consulta("SELECT fecha, tonelaje FROM producction WHERE turno = 'B'")
#consulta ("SELECT * FROM producction WHERE tonelaje > 5000")
#consulta("SELECT * FROM producction ORDER BY recuperacion DESC LIMIT 1")
#consulta("SELECT * FROM producction WHERE ley_cabeza >= 0.85 AND recuperacion > 88")



#consulta("""
#SELECT COUNT(*)          AS cantidad_turnos,
 #      SUM(tonelaje)     AS tonelaje_total,
  #     AVG(recuperacion) AS recuperacion_promedio
#FROM producction

#""")

consulta("""
SELECT turno,
       COUNT(*)                    AS cantidad,
       SUM(tonelaje)               AS tonelaje_total,
       ROUND(AVG(recuperacion), 1) AS recuperacion_promedio
FROM producction
GROUP BY turno
""")



# consulta(""" 
# SELECT COUNT(*) AS cantidad,
#        MAX(tonelaje) AS tonelaje_maximo,
#        MIN(tonelaje) AS tonelaje_minimo
# FROM producction
# """)

# consulta(""" 
# SELECT fecha,
#         count(*) AS cantidad_turnos,
#         SUM(tonelaje) AS tonelaje_total
# FROM producction
# GROUP BY fecha          
# """)
#Calcula la ley de cabeza promedio por turno, redondeada a 2 decimales.

# consulta("""
# SELECT turno, 
#         ROUND(AVG(ley_cabeza), 2) AS ley_cabeza_promedio
# FROM producction
# GROUP BY turno
# """)

# consulta("""
# SELECT fecha,
#         SUM(tonelaje) AS tonelaje_total
# FROM producction
# GROUP BY fecha
# ORDER BY tonelaje_total DESC, fecha
# """)


consulta("""
SELECT fecha,
       turno,
       tonelaje,
       ROUND(tonelaje * ley_cabeza / 100, 1)                      AS cu_alimentado,
       ROUND(tonelaje * ley_cabeza / 100 * recuperacion / 100, 1) AS cu_fino,
       ROUND(tonelaje * ley_cabeza /100 - tonelaje * ley_cabeza / 100 * recuperacion / 100, 1) AS cu_perdido
FROM producction
ORDER BY cu_perdido DESC
""")

# consulta(""" 
# SELECT fecha,
#         turno,
#         ROUND(tonelaje  * ley_cabeza /100 * recuperacion / 100, 1) AS cu_fino
# FROM producction
# GROUP BY turno

# """)

# consulta(""" 
# SELECT  turno,
#         ROUND(SUM(tonelaje), 1 ) AS tonelaje_total
# FROM producction
# GROUP BY turno
# HAVING SUM(tonelaje)>19000
#  """)

consulta("""
SELECT fecha,
       turno,
       tonelaje,
       CASE
           WHEN tonelaje >= 4500 THEN 'Bueno' 
           ELSE 'Bajo' 
       END AS estado,
       COUNT( CASE WHEN tonelaje >= 4500 THEN 1 END ) AS cantidad_bueno,
       COUNT( CASE WHEN tonelaje < 4500 THEN 1 END  ) AS cantidad_bajo
FROM producction
""")