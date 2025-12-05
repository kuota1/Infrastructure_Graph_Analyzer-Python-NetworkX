import networkx as nx
import matplotlib.pyplot as pit
import pandas as pd
import os

# primer funcion agrego las aristas como en V1
def agregar_arista (G,u,v,w=1, di=True):
    G.add_edge(u,v,weight=w)
    if not di:
        G.add_edge(v,u, weight=w)

# 2da funcion agrego metadata al nodo. segun documentacion se usa comando
# G de grafo .add_node()
def agregar_vertice(G, clave, nombre, servicio):
    G.add_node(clave, nombre=nombre, servicio=servicio)

# 3er funcion informaciond e las aristas desde excel con pandas
def cargar_aristas(G, nombre_cluster):
    df_aristas = pd.read_excel("aristas.xlsx")

    # Filtrar por cluster
    aristas_cluster = df_aristas[df_aristas["cluster"] == nombre_cluster]

    # Agregar aristas al grafo
    for _, row in aristas_cluster.iterrows():
        agregar_arista(G, row["u"], row["v"], row["weight"], di=True)

    # Determinar cuello de botella
    edge_weights = nx.get_edge_attributes(G, "weight")
    cuello = max(edge_weights, key=edge_weights.get)

    print(f"Cuello de botella: {cuello}, latencia: {edge_weights[cuello]} ms, "
          f"en cluster {nombre_cluster}")

# 4ta funcion ingreso los nodos o vertices desde Excel
def cargar_vertices(G, nombre_cluster):
    df_vertices = pd.read_excel("informacion_cluster.xlsx")

    # Filtrar por cluster
    vertices_cluster = df_vertices[df_vertices["cluster"] == nombre_cluster]

    # Agregar nodos con metadata
    for _, row in vertices_cluster.iterrows():
        agregar_vertice(G, row["clave"], row["nombre"], row["servicio"])

# 5ta funcion para dibujar el grafo
def dibujar_grafo(G, cluster):
    pos = nx.planar_layout(G)

    # Dibujar nodos y aristas
    nx.draw_networkx(G,pos,with_labels=True,node_color="blue",
                     node_size=1800, font_color="white", font_size=15, font_weight="bold",
                     font_family="Arial", edge_color="red",width=6)

    posicion_notas= {}
    for node,(x,y) in pos.items():
        posicion_notas[node]=(x,y+.08)


    etiquetas_nodo= {n:(d["servicio"]) for n,d in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos=posicion_notas,labels=etiquetas_nodo,font_color="black", font_size=10, font_weight="bold" )


    # Dibujar pesos (latencias)
    etiquetas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)

    pit.title(f"Grafo del {cluster}")
    pit.show()

# 6ta funcion centralidad de grafos
def centralidad_grafo(G, cluster):
    # Crear carpeta de reportes si no existe
    if not os.path.exists("reportes"):
        os.makedirs("reportes")

    ruta_reporte = f"reportes/reporte_{cluster}.txt"

    with open(ruta_reporte, "w", encoding="utf-8") as file:

        file.write("=" * 60 + "\n")
        file.write(f"      REPORTE DE CENTRALIDAD DEL GRAFO ({cluster})\n")
        file.write("=" * 60 + "\n\n")

        # CENTRALIDAD DE GRADO: Mide cuantas conecciones directas tiene un nodo
        grado = nx.degree_centrality(G)
        grado_ordenado = sorted(grado.items(), key=lambda x: x[1], reverse=True)
        file.write("CENTRALIDAD DE GRADO\n")
        for nodo, valor in grado_ordenado:
            file.write(f"  {nodo}: {valor:.4f}\n")
        file.write(f"Nodo más importante por grado: {grado_ordenado[0][0]}\n\n")

        # CENTRALIDAD DE CERCANÍA: Que tan rapido un nodo puede llegar a todos los
        # demas
        cercania = nx.closeness_centrality(G)
        cercania_ordenada = sorted(cercania.items(), key=lambda x: x[1], reverse=True)
        file.write("CENTRALIDAD DE CERCANÍA\n")
        for nodo, valor in cercania_ordenada:
            file.write(f"  {nodo}: {valor:.4f}\n")
        file.write(f"Nodo más cercano al resto: {cercania_ordenada[0][0]}\n\n")

        # CENTRALIDAD DE INTERMEDIACIÓN: Mide cuantas veces un nodo aparece
        # en las rutas mas cortas entre los nodos
        intermediacion = nx.betweenness_centrality(G)
        intermediacion_ordenada = sorted(intermediacion.items(), key=lambda x: x[1], reverse=True)
        file.write("CENTRALIDAD DE INTERMEDIACIÓN\n")
        for nodo, valor in intermediacion_ordenada:
            file.write(f"  {nodo}: {valor:.4f}\n")
        file.write(f"Nodo más crítico como puente: {intermediacion_ordenada[0][0]}\n\n")

        file.write("=" * 60 + "\n")
        file.write("FIN DEL REPORTE\n")
        file.write("=" * 60 + "\n")

    print(f"\nReporte generado en: {ruta_reporte}\n")


#agrego el main para las funciones
if __name__ == "__main__":
    nombre = input("¿Qué cluster le gustaría analizar? (cluster01 / cluster02): ")
    # Normalizar entradas comunes
    nombre = nombre.lower().replace(" ", "")

    # Lista de clusters válidos
    clusters_validos = ["cluster01", "cluster02"]

    if nombre not in clusters_validos:
        print(f"Error: el cluster '{nombre}' no existe.")
        exit()

    G = nx.DiGraph()

    cargar_vertices(G, nombre)
    cargar_aristas(G, nombre)
    dibujar_grafo(G, nombre)
    centralidad_grafo(G, nombre)

    # Layout del grafo
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos)

