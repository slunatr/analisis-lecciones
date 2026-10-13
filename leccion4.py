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