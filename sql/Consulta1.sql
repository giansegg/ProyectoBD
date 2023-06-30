SELECT E.tipo_documento, E.numero_documento
FROM Empleado E NATURAL JOIN Abogado A
WHERE A.casos_ganados >= (
    SELECT percentile_cont(0.80) WITHIN GROUP ( ORDER BY A2.casos_ganados )
    FROM Abogado A2
    )
AND NOT E.tiempo_parcial
AND EXISTS(
    SELECT 1
    FROM Departamento D JOIN AbogadoTrabaja AT
    ON D.nombre = AT.nombre_departamento
    AND (A.tipo_documento, A.numero_documento) = (AT.tipo_documento_abogado, AT.numero_documento_abogado)
    WHERE D.fecha_creacion <= now() - INTERVAL '2 years'
)
AND now() - E.fecha_inicio >= INTERVAL '1 year'

