import sqlite3
import pandas as pd

conexion = sqlite3.connect("planta.db")
cursor = conexion.cursor()

cursor.execute("DROP TABLE IF EXISTS detenciones")
cursor.execute("""
CREATE TABLE detenciones (
    fecha  TEXT,
    turno  TEXT,
    equipo TEXT,
    causa  TEXT,
    tipo   TEXT,
    horas  REAL
)
""")

detenciones = [
    ("2026-09-02", "B", "Molino SAG",            "Falla de motor",        "No programada", 4.5),
    ("2026-09-02", "B", "Celda de flotación",    "Ajuste de nivel",       "No programada", 0.5),
    ("2026-09-04", "A", "Bomba de relaves",      "Falla mecánica",        "No programada", 1.0),
    ("2026-09-05", "A", "Correa transportadora", "Mantención preventiva", "Programada",    2.0),
]
cursor.executemany("INSERT INTO detenciones VALUES (?, ?, ?, ?, ?, ?)", detenciones)
conexion.commit()

def consulta(sql):
    print(pd.read_sql(sql, conexion), "\n")




consulta("""
SELECT p.fecha, p.turno, p.tonelaje, d.equipo, d.horas
FROM producction AS p
INNER JOIN detenciones AS d
    ON p.fecha = d.fecha AND p.turno = d.turno
""")

consulta("""
SELECT p.fecha, p.turno, p.tonelaje, d.equipo, d.horas
FROM producction AS p
LEFT JOIN detenciones AS d
    ON p.fecha = d.fecha AND p.turno = d.turno
""")


consulta("""
SELECT p.fecha, p.turno, p.ley_cabeza, p.recuperacion, d.causa 
FROM producction AS p
INNER JOIN detenciones AS d
    ON p.fecha = d.fecha AND p.turno = d.turno
""")

consulta(""" 
SELECT p.fecha, p.turno
FROM producction AS p
LEFT JOIN detenciones AS d
    ON p.fecha = d.fecha AND p.turno = d.turno
    WHERE d.causa IS NULL
""")

consulta("""
SELECT p.fecha, p.turno, p.tonelaje, d.equipo, d.horas
FROM detenciones AS d
LEFT JOIN producction AS p
    ON d.fecha = p.fecha AND d.turno = p.turno
""")


consulta(""" 
SELECT p.fecha, p.turno, p.tonelaje, SUM(d.horas) AS horas_detencion
FROM producction AS p
LEFT JOIN detenciones AS d
    ON p.fecha = d.fecha AND p.turno = d.turno
    GROUP BY p.fecha, p.turno
""")


consulta("""
SELECT p.fecha, p.turno, p.tonelaje, d.horas_detencion
FROM producction AS p
LEFT JOIN (
    SELECT fecha, turno, SUM(horas) AS horas_detencion
    FROM detenciones
    GROUP BY fecha, turno
) AS d
    ON p.fecha = d.fecha AND p.turno = d.turno
""")




consulta("""
SELECT fecha, turno, tonelaje
FROM producction
WHERE tonelaje > (SELECT AVG(tonelaje) FROM producction)
""")



consulta("""
SELECT fecha, turno, recuperacion
FROM producction
WHERE recuperacion < (SELECT ROUND(
    SUM(tonelaje * ley_cabeza / 100 * recuperacion / 100)
    / SUM(tonelaje * ley_cabeza / 100)
    * 100
, 2) AS rec_ponderada FROM producction)
""")

consulta("""
SELECT fecha, turno, tonelaje
FROM producction
WHERE tonelaje = (SELECT MAX(tonelaje) FROM producction)
""")


consulta("""
WITH 
Tabla AS (
SELECT turno, ROUND(SUM(tonelaje * ley_cabeza / 100 * recuperacion / 100)
    / SUM(tonelaje * ley_cabeza / 100)
    * 100 , 2) AS rec_ponderada
FROM producction
GROUP BY turno

)
SELECT turno, rec_ponderada
FROM Tabla 
WHERE rec_ponderada = (SELECT MAX(rec_ponderada)
FROM Tabla)
""")    




consulta("""
WITH det AS (
    SELECT fecha, turno, SUM(horas) AS horas
    FROM detenciones
    GROUP BY fecha, turno
)
SELECT CASE WHEN d.horas IS NULL THEN 'Sin detención'
            ELSE 'Con detención'
       END AS grupo,
       COUNT(*)                  AS cantidad_turnos,
       ROUND(AVG(p.tonelaje), 0) AS tonelaje_promedio
FROM producction AS p
LEFT JOIN det AS d
    ON p.fecha = d.fecha AND p.turno = d.turno
GROUP BY CASE WHEN d.horas IS NULL THEN 'Sin detención'
              ELSE 'Con detención'
         END
""")


consulta("""
SELECT fecha, turno, recuperacion
FROM producction
WHERE recuperacion < (SELECT    SUM(tonelaje * ley_cabeza / 100 * recuperacion / 100)
    / SUM(tonelaje * ley_cabeza / 100)
    * 100
 FROM producction)
""")


consulta("""
SELECT fecha, turno, tonelaje, recuperacion, ley_cabeza 
FROM producction
WHERE ley_cabeza > 0.85
ORDER BY recuperacion DESC
""")


consulta("""
SELECT 
       turno,
       ROUND(tonelaje * ley_cabeza / 100 - tonelaje * ley_cabeza / 100 * recuperacion / 100, 1) AS cu_perdido
FROM producction
GROUP BY  turno
ORDER BY cu_perdido DESC
""")

consulta("""
SELECT
    fecha, 
    SUM(tonelaje * ley_cabeza / 100 * recuperacion / 100) as cu_fino
FROM producction
GROUP BY fecha
HAVING SUM(tonelaje * ley_cabeza / 100 * recuperacion / 100) > 75

""")

consulta("""
SELECT 
    d.fecha, d.turno,d.equipo, d.causa, d.horas,
    ROUND(p.tonelaje * p.ley_cabeza / 100 * p.recuperacion / 100, 1) as cu_fino
FROM detenciones AS d
INNER JOIN producction AS p
    ON  p.turno = d.turno  AND p.fecha = d.fecha
""")

consulta("""
SELECT turno,
       ROUND(SUM(tonelaje * ley_cabeza) / SUM(tonelaje), 3) AS ley_ponderada
FROM producction
GROUP BY turno
""")
