SELECT AP.tipo_documento_abogado, AP.numero_documento_abogado, count((AP.tipo_documento_abogado, AP.numero_documento_abogado)) AS cantidad_casos
FROM AbogadoParticipa AP
         JOIN PersonaRepresenta PR ON AP.caso_codigo = PR.caso_codigo
WHERE PR.ruc = '61012275826'
AND (AP.tipo_documento_abogado, AP.numero_documento_abogado) IN (
    SELECT tipo_documento, numero_documento
    FROM Persona P NATURAL JOIN Empleado E NATURAL JOIN Abogado A
    WHERE P.sexo = 'F' AND E.fecha_inicio > now() - INTERVAL '1 year'
    ORDER BY A.casos_ganados DESC
    LIMIT (SELECT round(0.2*count((A2.tipo_documento, A2.numero_documento))) FROM Abogado A2)
    )
GROUP BY AP.tipo_documento_abogado, AP.numero_documento_abogado;

