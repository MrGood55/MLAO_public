


import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import math

class PlacesGraph:
    """
    Класс для работы с графами, представляющими места.

    Attributes:
    - places (List): Список мест (узлов) в графе.
    - graph (nx.Graph): Граф, представляющий связи между местами.
    - coordinates (dict): Словарь с координатами мест.

    Methods:
    - add_nodes(): Добавляет узлы (места) в граф.
    - add_combinations_edges_from_nodes(add_distance_weight: Optional[bool] = False): Добавляет рёбра в граф, представляющие все возможные комбинации мест.
    - add_edges(edges_with_weights: List[Tuple]): Добавляет рёбра в граф с весами.
    - add_edge_with_weight(node1: str, node2: str, weight: float): Добавляет вес к ребру графа, если ребро уже существует.
    - remove_edge(node1: str, node2: str): Удаляет ребро между указанными узлами.
    - clear_graph(): Очищает граф.
    - draw_graph(): Рисует граф с использованием библиотеки Matplotlib.
    - seek_shortest_path(start_node: str, end_node: str) -> List[str]: Ищет кратчайший путь от start_node до end_node.

    """

    def __init__(self, places: list[str], coordinates: dict)->None:
        """
        Инициализация объекта PlacesGraph.

        Parameters:
        - places (List): Список мест (узлов) в графе.
        - coordinates (dict): Словарь с координатами мест.
        """
        self.places = places
        self.graph = nx.Graph()
        self.coordinates = coordinates
        self.shortest_nodes = []
        self.shortest_path = []
    
    def evaluate_distance(self,list_of_coordinates:list[float])->int:
        # pi - число pi, rad - радиус сферы (Земли)
        rad = 6372795
        # координаты двух точек
        llat1 = list_of_coordinates[0]
        llong1 = list_of_coordinates[1]
        llat2 = list_of_coordinates[2]
        llong2 = list_of_coordinates[3]
        # в радианах
        lat1 = llat1 * math.pi / 180.
        lat2 = llat2 * math.pi / 180.
        long1 = llong1 * math.pi / 180.
        long2 = llong2 * math.pi / 180.

        # косинусы и синусы широт и разницы долгот
        cl1 = math.cos(lat1)
        cl2 = math.cos(lat2)
        sl1 = math.sin(lat1)
        sl2 = math.sin(lat2)
        delta = long2 - long1
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)

        # вычисления длины большого круга
        y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
        x = sl1 * sl2 + cl1 * cl2 * cdelta
        ad = math.atan2(y, x)
        dist = int(ad * rad)
        return dist
    
    def add_nodes(self)->None:
        """Добавляет узлы (места) в граф."""
        self.graph.add_nodes_from(self.places)

    def add_combinations_edges_from_nodes(self, add_distance_weight:bool = False)->None:
        """
        Добавляет рёбра в граф, представляющие все возможные комбинации мест.

        Parameters:
        - add_distance_weight (Optional[bool]): Опциональный параметр для добавления весов, характеризующих длину пути на основе данных координат.
        """
        node_combinations = list(combinations(self.places, 2))
        for node1, node2 in node_combinations:
            if add_distance_weight:
                coordinates1 = self.coordinates[node1]["Координаты"]
                coordinates2 = self.coordinates[node2]["Координаты"]
                distance_weight = self.evaluate_distance(coordinates1 + coordinates2)
                self.graph.add_edge(node1, node2, weight=distance_weight)
            else:
                self.graph.add_edge(node1, node2)

    def add_edges(self, edges_with_weights: list[tuple]|list[tuple[tuple, float]])->None:
        """
        Добавляет рёбра в граф.

        Parameters:
        - edges_with_weights (Union[List[Tuple], List[Tuple[Tuple, float]]]): Список рёбер с весами.
        """
        if len(edges_with_weights[0]) > 2:
            self.graph.add_weighted_edges_from(edges_with_weights)
        else:
            self.graph.add_edges_from(edges_with_weights)
        

    def add_edge_with_weight(self, node1: str, node2: str, weight: float)->None:
        """
        Добавляет вес к ребру графа, если ребро уже существует.

        Parameters:
        - node1 (str): Первый узел ребра.
        - node2 (str): Второй узел ребра.
        - weight (float): Вес, который нужно добавить.
        """
        if self.graph.has_edge(node1, node2):
            self.graph[node1][node2]['weight'] = weight
            print(f"Добавлен вес {weight} к ребру между {node1} и {node2}.")
        else:
            print(f"Ребро между {node1} и {node2} не существует.")

    def remove_edge(self, node1: str, node2: str)->None:
        """
        Удаляет ребро между указанными узлами.

        Parameters:
        - node1 (str): Первый узел.
        - node2 (str): Второй узел.
        """
        if self.graph.has_edge(node1, node2):
            self.graph.remove_edge(node1, node2)
            print(f"Ребро между {node1} и {node2} удалено.")
        else:
            print(f"Ребро между {node1} и {node2} не существует.")
    def seek_shortest_path(self, start_node: str, end_node: str) -> None:
        """
        Ищет кратчайший путь от start_node до end_node.

        Parameters:
        - start_node (str): Начальный узел пути.
        - end_node (str): Конечный узел пути.

        Returns:
        - None 
        (преобразует переменные self.shortest_nodes, self.shortest_path)
        """
        try:
            pos = nx.circular_layout(self.graph)
            self.shortest_nodes = nx.shortest_path(self.graph, start_node, end_node)
            self.shortest_path = [[self.shortest_nodes[i],self.shortest_nodes[i+1]] for i,_ in enumerate(self.shortest_nodes) if i!=len(self.shortest_nodes)-1]

        except nx.NetworkXNoPath:
            print(f"Нет пути от {start_node} до {end_node}.")
            
        
    def clear_graph(self):
        """Очищает граф."""
        self.graph.clear()
        print("Граф очищен.")

    def draw_graph(self, figsize: tuple[int, int] = (5, 5),ax=None,with_labels_edges=True):
        """
        Рисует граф с использованием библиотеки Matplotlib.

        Parameters:
        - figsize (Tuple[int, int]): Размер графика в дюймах (ширина, высота).
        """
        # pos = nx.spring_layout(self.graph)
        pos = nx.circular_layout(self.graph)
        plt.figure(figsize=figsize)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', edge_color='gray', font_size=8,ax=ax)

        # Добавляем отображение весов на рёбрах
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        if with_labels_edges:
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red',ax=ax)
        if self.shortest_nodes != [] and self.shortest_path != []:
            nx.draw_networkx_nodes(self.graph, pos, nodelist=self.shortest_nodes,node_size=700, node_color='mediumseagreen',ax=ax)
            nx.draw_networkx_edges(self.graph, pos, edgelist=self.shortest_path, edge_color='r', width=3,ax=ax)
    def get_shortest_path_distance(self) -> float:
        """
        Вычисляет общее расстояние по кратчайшему пути.

        Returns:
        - float: Общее расстояние по кратчайшему пути.
        """
        total_distance = 0.0

        for i in range(len(self.shortest_nodes) - 1):
            node1 = self.shortest_nodes[i]
            node2 = self.shortest_nodes[i + 1]

            if self.graph.has_edge(node1, node2):
                total_distance += self.graph[node1][node2].get('weight', 1.0)
            else:
                print(f"Edge between {node1} and {node2} does not exist.")

        return total_distance