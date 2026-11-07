import sqlite3
import pandas as pd

conexion = sqlite3.connect("planta_v2.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON")   # en SQLite hay que activarlas

def consulta(sql):
    print(pd.read_sql(sql, conexion), "\n")

def probar(sql):
    try:
        cursor.execute(sql)
        conexion.commit()
        print("OK")
    except sqlite3.IntegrityError as e:
        print("RECHAZADO:", e)

# ── 1. BORRAR Y CREAR TABLAS ─────────────────────────────
cursor.executescript("""
DROP TABLE IF EXISTS consumos;
DROP TABLE IF EXISTS detenciones;
DROP TABLE IF EXISTS reactivos;
DROP TABLE IF EXISTS equipos;
DROP TABLE IF EXISTS turnos;

CREATE TABLE turnos (
    id_turno     INTEGER PRIMARY KEY,
    fecha        TEXT    NOT NULL,
    turno        TEXT    NOT NULL CHECK (turno IN ('A', 'B')),
    tonelaje     REAL    NOT NULL CHECK (tonelaje >= 0),
    ley_cabeza   REAL    CHECK (ley_cabeza BETWEEN 0 AND 100),
    recuperacion REAL    CHECK (recuperacion BETWEEN 0 AND 100),
    UNIQUE (fecha, turno)
);

CREATE TABLE equipos (
    id_equipo INTEGER PRIMARY KEY,
    nombre    TEXT NOT NULL UNIQUE,
    area      TEXT NOT NULL
);

CREATE TABLE reactivos (
    id_reactivo INTEGER PRIMARY KEY,
    nombre      TEXT NOT NULL UNIQUE,
    funcion     TEXT
);

CREATE TABLE detenciones (
    id_detencion INTEGER PRIMARY KEY,
    id_turno     INTEGER NOT NULL REFERENCES turnos (id_turno),
    id_equipo    INTEGER NOT NULL REFERENCES equipos (id_equipo),
    causa        TEXT,
    tipo         TEXT    NOT NULL CHECK (tipo IN ('Programada', 'No programada')),
    horas        REAL    NOT NULL CHECK (horas > 0)
);

CREATE TABLE consumos (
    id_consumo  INTEGER PRIMARY KEY,
    id_turno    INTEGER NOT NULL REFERENCES turnos (id_turno),
    id_reactivo INTEGER NOT NULL REFERENCES reactivos (id_reactivo),
    kg          REAL    NOT NULL CHECK (kg >= 0),
    UNIQUE (id_turno, id_reactivo)
);
""")

# ── 2. CARGAR DATOS: primero los padres ─────────────────
cursor.executemany(
    "INSERT INTO turnos (fecha, turno, tonelaje, ley_cabeza, recuperacion) VALUES (?, ?, ?, ?, ?)",
    [("2026-09-01", "A", 5200, 0.85, 88.5), ("2026-09-01", "B", 4900, 0.82, 87.1),
     ("2026-09-02", "A", 5350, 0.90, 89.2), ("2026-09-02", "B", 3100, 0.78, 84.0),
     ("2026-09-03", "A", 5100, 0.88, 88.9), ("2026-09-03", "B", 5000, 0.86, 88.0),
     ("2026-09-04", "A", 4700, 0.75, 83.5), ("2026-09-04", "B", 5250, 0.91, 89.8)])

cursor.executemany(
    "INSERT INTO equipos (nombre, area) VALUES (?, ?)",
    [("Molino SAG", "Molienda"), ("Celda de flotación", "Flotación"),
     ("Bomba de relaves", "Relaves"), ("Correa transportadora", "Chancado")])

cursor.executemany(
    "INSERT INTO reactivos (nombre, funcion) VALUES (?, ?)",
    [("Xantato isopropílico", "Colector"),
     ("Ditiofosfato",         "Colector"),
     ("MIBC",                 "Espumante"),
     ("Cal",                  "Regulador pH")])

# ── 3. CARGAR DATOS: después los hijos ──────────────────
cursor.executemany(
    "INSERT INTO detenciones (id_turno, id_equipo, causa, tipo, horas) VALUES (?, ?, ?, ?, ?)",
    [(4, 1, "Falla de motor",  "No programada", 4.5),
     (4, 2, "Ajuste de nivel", "No programada", 0.5),
     (7, 3, "Falla mecánica",  "No programada", 1.0)])

cursor.executemany(
    "INSERT INTO consumos (id_turno, id_reactivo, kg) VALUES (?, ?, ?)",
    [(1, 1, 146),
     (2, 2, 150),
     (1, 3, 128),
     (2, 4, 136)])

conexion.commit()

# ── 4. PRUEBAS: con los datos ya cargados ───────────────
probar("INSERT INTO reactivos (nombre, funcion) VALUES (NULL, 'Colector')")
probar("INSERT INTO consumos (id_turno, id_reactivo, kg) VALUES (4, 1, -145)")
probar("DELETE FROM reactivos WHERE id_reactivo = 1")
probar("""
UPDATE consumos
SET kg = 158
WHERE id_consumo = 1
""")

