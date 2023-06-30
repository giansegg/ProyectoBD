select p.numero_documento, p.nombre, p.apellido, e.sueldo, a.casos_ganados, a.casos_perdidos
from ((select ap.numero_documento_abogado, ap.tipo_documento_abogado
       from abogadoparticipa ap
                join caso c on ap.caso_codigo = c.codigo
       where c.estado = 'EnProceso'
         and ap.tipo_documento_abogado = 'DNI'
       intersect
       select s.numero_documento_abogado, s.tipo_documento_abogado
       from secretarioasiste s
                join abogado ab on s.numero_documento_abogado = ab.numero_documento and
                                   s.tipo_documento_abogado = ab.tipo_documento) query
    join persona p on query.tipo_documento_abogado = p.tipo_documento and
                      query.numero_documento_abogado = p.numero_documento
    natural join empleado e natural join abogado a)
    where a.casos_ganados < 0.33*(a.casos_perdidos + a.casos_ganados)
    and e.tiempo_parcial = false and e.sueldo>(select avg(sueldo)from empleado natural join abogado);