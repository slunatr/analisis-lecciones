# un JOIN de tres tablas, muestra fecha, turno, nombre del reactivo y kg.


from leccion7 import consulta


consulta("""
SELECT t.turno, t.fecha, r.nombre AS reactivo, c.kg
FROM turnos AS t
INNER JOIN consumos AS c  ON t.id_turno = c.id_turno
INNER JOIN reactivos AS r ON c.id_reactivo = r.id_reactivo
""")

#El consumo de colector del 09-01 A se registró mal: eran 158 kg, no 156.4
# #Corrígelo con UPDATE. Primero haz el SELECT para verificar qué fila vas a tocar.
#Pregunta de diseño: ¿por qué conviene tener una tabla equipos aparte, en vez de escribir el nombre del equipo en cada detención? 
#Piensa en qué pasa si el “Molino SAG” cambia de nombre.

consulta("""
Select c.id_consumo,t.fecha, t.turno, r.nombre AS reactivo, c.kg
FROM turnos AS t
INNER JOIN consumos AS c ON t.id_turno = c.id_turno
INNER JOIN reactivos AS r ON c.id_reactivo = r.id_reactivo
WHERE t.fecha = '2026-09-01'  AND t.turno = 'A' 
""")

consulta("""
select * from consumos
""")

