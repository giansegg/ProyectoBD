select numero_documento, nombre, apellido, sueldo, casos_ganados, casos_perdidos
from ((select numero_documento_abogado, tipo_documento_abogado
       from abogadoparticipa a
                join casos c on a.caso_codigo = c.codigo
       where c.estado = 'En proceso'
         and tipo_documento_abogado = 'DNI'
       intersect
       select numero_documento_abogado, tipo_documento_abogado
       from secretarioasiste s
                join abogados ab on s.numero_documento_abogado = ab.numero_documento and
                                    s.tipo_documento_abogado = ab.tipo_documento) query
    join abogados a
      on query.tipo_documento_abogado = a.tipo_documento and query.numero_documento_abogado = a.numero_documento)
where 2*a.casos_ganados < a.casos_perdidos and a.tiempo_parcial = false and a.sueldo>(select avg(sueldo)from abogados); 