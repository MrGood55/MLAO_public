import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QMessageBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWebEngineWidgets
import json
from places_graph import PlacesGraph

class PlacesGraphGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.figsize_graph = (14, 14)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Places Graph GUI_222')

        # Frame for graph operations
        frame_operations = QVBoxLayout()
        # Set a fixed width and height for frame_operations
         
        


        # Buttons
        btn_create_graph = QPushButton('Create Graph', self)
        btn_create_graph.clicked.connect(self.create_graph)

        btn_draw_graph = QPushButton('Draw Graph', self)
        btn_draw_graph.clicked.connect(self.draw_graph)

        btn_shortest_path = QPushButton('Shortest Path', self)
        btn_shortest_path.clicked.connect(self.seek_shortest_path_gui)

        # Dropdowns for node selection
        self.start_node_combobox = QComboBox(self)
        self.end_node_combobox = QComboBox(self)
        # Set fixed size for QComboBox instances
        combo_box_width = 300  # Set your desired width
        combo_box_height = 30  # Set your desired height
        self.start_node_combobox.setFixedSize(combo_box_width, combo_box_height)
        self.end_node_combobox.setFixedSize(combo_box_width, combo_box_height)

        start_node_label = QLabel('Start Node:')
        end_node_label = QLabel('End Node:')

        # Canvas for Matplotlib Figure
        self.canvas_frame = QVBoxLayout()
        self.canvas = QtWebEngineWidgets.QWebEngineView(self)
        self.canvas_page = QVBoxLayout()
        self.canvas_page.addWidget(self.canvas)
        self.canvas_frame.addLayout(self.canvas_page)

        # Matplotlib Figure for graph display
        self.fig = Figure(figsize=self.figsize_graph)
        self.ax = self.fig.add_subplot(111)
        self.canvas_widget = FigureCanvas(self.fig)
        self.canvas_page.addWidget(self.canvas_widget)
        
        # Adding NavigationToolbar for zooming
        self.toolbar = NavigationToolbar(self.canvas_widget, self)
        self.canvas_page.addWidget(self.toolbar)

        # Button for removing an edge
        btn_remove_edge = QPushButton('Remove Edge', self)
        btn_remove_edge.clicked.connect(self.remove_edge)

        frame_operations.addWidget(btn_create_graph)
        frame_operations.addWidget(btn_draw_graph)
        frame_operations.addWidget(btn_shortest_path)

        frame_operations.addWidget(start_node_label)
        frame_operations.addWidget(self.start_node_combobox)

        frame_operations.addWidget(end_node_label)
        frame_operations.addWidget(self.end_node_combobox)
        frame_operations.addWidget(btn_remove_edge)

        # Overall layout
        layout = QHBoxLayout(self)
        layout.addLayout(frame_operations)
        layout.addLayout(self.canvas_frame)

        frame_operations.addStretch() # заполняет пространство между дном и верхними виджетами
        # frame_operations.QSize(300)

        self.setLayout(layout)
        self.setGeometry(100, 100, 1200, 900)

    def create_graph(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open JSON file', '', 'JSON files (*.json)')

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    places = list(data.keys())

                    self.places_graph = PlacesGraph(places, data)
                    self.places_graph.add_nodes()
                    self.places_graph.add_combinations_edges_from_nodes(add_distance_weight=True)

                    # Update comboboxes with available nodes
                    self.start_node_combobox.addItems(places)
                    self.end_node_combobox.addItems(places)

                    self.draw_graph()  # Display the graph immediately after creation
                except json.JSONDecodeError:
                    QMessageBox.information(self, 'Error', 'Invalid JSON format. Please provide a valid JSON file.')
        else:
            QMessageBox.information(self, 'Error', 'No file selected.')

    def draw_graph(self):
        if hasattr(self, 'places_graph'):
            self.ax.clear()
            self.places_graph.draw_graph(figsize=self.figsize_graph, ax=self.ax,with_labels_edges=False)
            self.canvas_widget.draw()
        else:
            QMessageBox.information(self, 'Error', 'Graph not created. Please create the graph first.')

    def seek_shortest_path_gui(self):
        if hasattr(self, 'places_graph'):
            start_node = self.start_node_combobox.currentText()
            end_node = self.end_node_combobox.currentText()

            if start_node and end_node:
                self.places_graph.seek_shortest_path(start_node, end_node)
                self.draw_graph()
            else:
                QMessageBox.information(self, 'Error', 'Please select both start and end nodes.')
        else:
            QMessageBox.information(self, 'Error', 'Graph not created. Please create the graph first.')

    def remove_edge(self):
        if hasattr(self, 'places_graph'):
            start_node = self.start_node_combobox.currentText()
            end_node = self.end_node_combobox.currentText()

            if start_node and end_node:
                self.places_graph.remove_edge(start_node, end_node)
                self.draw_graph()  # Display the graph after removing the edge
            else:
                QMessageBox.information(self, 'Error', 'Please select both nodes to remove the edge.')
        else:
            QMessageBox.information(self, 'Error', 'Graph not created. Please create the graph first.')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlacesGraphGUI()
    ex.show()
    sys.exit(app.exec_())
