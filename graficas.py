import matplotlib.pyplot as plt
from typing import List

# consulta1 = [[0.0042,0.0026,0.0026,0.003], [0.0047,0.0102,0.0736,0.9959]]
# consulta2 = [[0.003,0.0014,0.0038,0.5082],[0.0016,0.0014,0.0039,1.5847]]
# consulta3 = [[0.0032,0.0104,0.096,1.2603],[0.0043,0.0146,0.1004,1.1157]]
#
# consultas = [consulta1, consulta2, consulta3]
#

# for j in range(3):
#     # Crear la gráfica
#     plt.plot([0,0.5,1,2], consultas[j][0], label='sin índices', color='blue', marker='o')
#     plt.plot([0,0.5,1,2], consultas[j][1], label='con índices', color='red', marker='o')
#
#     # Título y etiquetas
#     plt.title('Consulta ' + str(j+1))
#     plt.xlabel('')
#     plt.ylabel('Tiempo promedio (ms)')
#
#     # Establecer las ubicaciones y etiquetas de las líneas en el eje x
#     plt.xticks([0,0.5,1,2], ['1k', '10k', '100k', '1M'])
#
#     # Leyenda
#     plt.legend()
#
#     # Mostrar la gráfica
#     plt.show()


def create_graphic(title, times: List[List[float]]):
    print(title)
    x = [0, 1, 2, 3]

    # Crear la gráfica
    plt.plot(x, times[0], label='sin índices', color='blue', marker='o')
    plt.plot(x, times[1], label='con índices', color='red', marker='o')

    # Título y etiquetas
    plt.title(title)
    plt.xlabel('')
    plt.ylabel('Tiempo promedio (s)')

    # Establecer las ubicaciones y etiquetas de las líneas en el eje x
    plt.xticks(x, ['1k', '10k', '100k', '1M'])

    # Leyenda
    plt.legend()

    # Mostrar la gráfica
    plt.show()