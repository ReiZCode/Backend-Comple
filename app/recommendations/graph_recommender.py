# app/recommendations/graph_recommender.py

import pandas as pd
import networkx as nx
import math
import heapq as hq



def construir_grafo_desde_df(df: pd.DataFrame):
    """
    Recibe un DataFrame con columnas:
    - CustomerID
    - StockCode
    - Description
    - TotalPrize

    y devuelve:
    - G: grafo NetworkX
    - nodes_list: lista de nodos en orden
    - node_to_idx: mapeo nodo -> índice
    - adj: lista de adyacencia para Dijkstra
    """

    # Aseguramos que TotalPrize sea numérico
    df = df.copy()
    df["TotalPrize"] = pd.to_numeric(df["TotalPrize"], errors="coerce").fillna(0)

    G = nx.Graph()

    # --- Clientes ---
    for customer_id in df["CustomerID"].dropna().unique():
        G.add_node(customer_id, tipo="customer", label=customer_id)

    # --- Productos ---
    for _, row in df[["StockCode", "Description"]].drop_duplicates().iterrows():
        G.add_node(row["StockCode"], tipo="stock", label=row["Description"])

    # --- Aristas con peso ---
    for (customer, product), grupo in df.groupby(["CustomerID", "StockCode"]):
        monto_total = grupo["TotalPrize"].sum()
        costo = 1 / (1 + float(monto_total))  # más gasto = costo más pequeño

        G.add_edge(
            customer,
            product,
            tipo="transaccion",
            gasto=float(monto_total),
            weight=costo,
        )

    # Mapeos para Dijkstra 
    nodes_list = list(G.nodes())
    node_to_idx = {node: i for i, node in enumerate(nodes_list)}
    adj = [[] for _ in range(len(nodes_list))]

    for u, v, data in G.edges(data=True):
        w = data.get("weight", 1.0)
        ui = node_to_idx[u]
        vi = node_to_idx[v]
        adj[ui].append((vi, w))
        adj[vi].append((ui, w))

    return G, nodes_list, node_to_idx, adj



def dijkstra(adj, s):
    
    n = len(adj)
    visited = [False] * n
    path = [-1] * n
    cost = [math.inf] * n

    cost[s] = 0
    pqueue = [(0, s)]

    while pqueue:
        g, u = hq.heappop(pqueue)
        if not visited[u]:
            visited[u] = True
            for v, w in adj[u]:
                if not visited[v]:
                    f = g + w
                    if f < cost[v]:
                        cost[v] = f
                        path[v] = u
                        hq.heappush(pqueue, (f, v))

    return path, cost


def reconstruir_camino(path, destino_idx):
    """
    Reconstruye el camino desde el origen hasta 'destino_idx'
    usando el arreglo 'path', devolviendo una lista de índices.
    """
    camino = []
    actual = destino_idx
    while actual != -1:
        camino.append(actual)
        actual = path[actual]
    camino.reverse()
    return camino



def recomendar_productos_para_cliente(df: pd.DataFrame, customer_id: str, k: int = 5):
    """
    Construye el grafo a partir del df y devuelve hasta k productos recomendados
    para el cliente dado, usando el Dijkstra implementado a mano.
    """

    # Construimos grafo y estructuras
    G, nodes_list, node_to_idx, adj = construir_grafo_desde_df(df)

    if customer_id not in node_to_idx:
        raise ValueError(f"El cliente {customer_id} no existe en el grafo")

    origen_idx = node_to_idx[customer_id]

    # Ejecutar Dijkstra
    path, cost = dijkstra(adj, origen_idx)

    # Productos que YA compró
    productos_comprados = set(df[df["CustomerID"] == customer_id]["StockCode"])

    recomendaciones = []

    for idx, distancia in enumerate(cost):
        nodo = nodes_list[idx]
        datos_nodo = G.nodes[nodo]

        if (
            datos_nodo.get("tipo") == "stock"
            and nodo not in productos_comprados
            and distancia < math.inf
        ):
            camino_idx = reconstruir_camino(path, idx)
            camino_nodos = [nodes_list[i] for i in camino_idx]

            recomendaciones.append(
                {
                    "StockCode": nodo,
                    "Descripcion": datos_nodo.get("label"),
                    "distancia": distancia,
                    "camino": camino_nodos,
                }
            )

    recomendaciones.sort(key=lambda x: x["distancia"])
    return recomendaciones[:k]
