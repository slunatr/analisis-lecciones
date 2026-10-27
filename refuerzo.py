import sqlite3
import pandas as pd

conexion = sqlite3.connect("planta.db")
cursor = conexion.cursor()

cursor.execute("DROP TABLE IF EXISTS reactivos")
cursor.execute("""
CREATE TABLE reactivos (
    fecha    TEXT,
    turno    TEXT,
    reactivo TEXT,
    kg       REAL
)
""")

reactivos = [
    ("2026-09-01", "A", "Colector", 156), ("2026-09-01", "A", "Espumante", 78),
    ("2026-09-01", "B", "Colector", 152), ("2026-09-01", "B", "Espumante", 74),
    ("2026-09-02", "A", "Colector", 160), ("2026-09-02", "A", "Espumante", 80),
    ("2026-09-02", "B", "Colector", 118), ("2026-09-02", "B", "Espumante", 52),
    ("2026-09-03", "A", "Colector", 150), ("2026-09-03", "A", "Espumante", 77),
    ("2026-09-03", "B", "Colector", 148), ("2026-09-03", "B", "Espumante", 75),
    ("2026-09-04", "A", "Colector", 165), ("2026-09-04", "A", "Espumante", 70),
    ("2026-09-04", "B", "Colector", 155), ("2026-09-04", "B", "Espumante", 79),
]
cursor.executemany("INSERT INTO reactivos VALUES (?, ?, ?, ?)", reactivos)
conexion.commit()

def consulta(sql):
    print(pd.read_sql(sql, conexion), "\n")


consulta("""
SELECT * FROM reactivos
WHERE reactivo = 'Colector'
""")


consulta("""
SELECT fecha, turno, SUM(kg) AS total_kg
FROM reactivos
GROUP BY fecha, turno   
""")

consulta("""
SELECT reactivo, turno, SUM(kg) AS total_kg 
FROM reactivos
GROUP BY reactivo,turno
""")

consulta("""
Select fecha, turno, reactivo, kg
FROM reactivos  
WHERE kg > 150
ORDER BY kg DESC
""")

consulta("""
select reactivo, sum(kg) as total_kg
from reactivos
group by reactivo
having total_kg > 600
""")

consulta("""
select fecha, turno, reactivo, kg,
    case when  kg > 155 then 'altO' else 'bajo' end As Nivel
from reactivos 
where reactivo = 'Colector'
""")




consulta("""
select p.fecha, p.turno, r.kg, ROUND (r.kg * 1000 / p.tonelaje  , 1 ) as g_por_tonelada
from producction as p
inner join reactivos as r
    on p.fecha = r.fecha and p.turno = r.turno
where r.reactivo = 'Colector'
""")

consulta("""
select p.turno, ROUND  (SUM(r.kg * 1000 )   / SUM(p.tonelaje)  , 1 ) as g_por_tonelada
from producction as p
inner join reactivos as r
    on p.fecha = r.fecha and p.turno = r.turno
where r.reactivo = 'Colector'
group by p.turno
""")

consulta("""
SELECT fecha, turno, recuperacion 
from producction 
where recuperacion > 88 
ORDER BY  recuperacion DESC
""")
consulta("""
select turno,reactivo,  ROUND (SUM(kg),1) as kg_total
from reactivos
where reactivo = 'Espumante' 
group by turno
""")

consulta(""" 
With det as(
    Select fecha, turno, SUM(horas) as horas_totales
    FROM detenciones
    Group by fecha, turno )

SELECT p.fecha, p.turno, p.tonelaje, d.horas_totales
from producction as p
inner join det as d
    on p.fecha =d.fecha AND p.turno = d.turno
where d.horas_totales > 0 



""")

consulta("""
SELECT fecha, turno, tonelaje,
      (tonelaje * 100 ) / sum(tonelaje) OVER () as porcentaje 
from producction

""")

consulta ("""
Select fecha, turno , tonelaje * ley_cabeza / 100 * recuperacion / 100 AS cu_fino,
SUM(tonelaje * ley_cabeza / 100 * recuperacion / 100) OVER (ORDER BY fecha, turno) as cu_Fino_Acumulado
from producction

""")

consulta("""
Select fecha, turno, reactivo, kg,
SUM(kg) over(PARTITION BY turno ORDER BY fecha, turno) as kg_acumuladdo
from reactivos
where reactivo = 'Colector'

""")


consulta("""
SELECT fecha, turno, tonelaje,
       LAG(tonelaje) OVER (ORDER BY fecha, turno) AS rec_anterior,
       ROUND(tonelaje - LAG(tonelaje) OVER ( ORDER BY fecha, turno), 1) AS cambio
FROM producction
""")

consulta("""
SELECT fecha,
       turno,
       tonelaje,
       LAG(tonelaje) OVER (PARTITION BY turno ORDER BY fecha)            AS ton_anterior,
       tonelaje - LAG(tonelaje) OVER (PARTITION BY turno ORDER BY fecha) AS cambio
FROM producction
ORDER BY turno, fecha
""")



consulta("""
SELECT turno,recuperacion,
       RANK() OVER (PARTITION BY turno ORDER BY recuperacion DESC) AS puesto
FROM producction

""")