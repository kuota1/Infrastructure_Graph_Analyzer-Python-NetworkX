import networkx as nx
import matplotlib.pyplot as pit
import numpy as np

# esta funcion sera para crear las aristas u y v son los nodes o vertices w sera el peso di direccional
# el grafo se llamara G. tambien nos sirve por si no queremos hacerla direccional
def agregar_arista (G,u,v,w=1, di=True):
    G.add_edge(u,v,weight=w)
    if not di:
        G.add_edge(v,u, weight=w)

if __name__== "__main__":
    G= nx.DiGraph()  #crea el grafo dirigido al pasar las aristas se creara los vertices
    #pasar datos incluyendo el peso
    agregar_arista(G,"C","LB",80)
    agregar_arista(G, "LB", "WS", 10)
    agregar_arista(G, "WS", "AS", 5)
    agregar_arista(G,"AS","D",25)
    agregar_arista(G, "AS", "CH", 3)
    agregar_arista(G, "AS", "IP", 8)
    agregar_arista(G, "IP", "D", 20)
    agregar_arista(G, "AS", "MQ", 4)
    agregar_arista(G, "AS", "LS", 2)
    agregar_arista(G, "MQ", "LS", 2)

    forma= nx.layout.planar_layout(G)
    nx.draw_networkx(G,forma)
    etiquetas= nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G,forma, edge_labels=etiquetas)
    pit.title("Grafo descrubir cuello botella")
    pit.show()




