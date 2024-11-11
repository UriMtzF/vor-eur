import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Heuristica import Heuristica

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualización de Heurística")
        self.heuristica = Heuristica()
        
        # Configurar botones
        self.start_button = tk.Button(root, text="Iniciar", command=self.start_process)
        self.start_button.pack(pady=10, side=tk.TOP)

        self.reset_button = tk.Button(root, text="Repetir", command=self.reset_process, state=tk.DISABLED)
        self.reset_button.pack(pady=10, side=tk.TOP)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10, side=tk.TOP)

        # Configurar canvas para gráfica
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT)

        # Cuadro de texto para mostrar los pasos
        self.text_steps = tk.Text(root, width=40, height=20, state=tk.DISABLED)
        self.text_steps.pack(side=tk.RIGHT, padx=10, pady=10)

    def start_process(self):
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.result_label.config(text="")
        self.text_steps.config(state=tk.NORMAL)
        self.text_steps.delete(1.0, tk.END)  # Limpiar cuadro de texto
        self.visualize_process()

    def reset_process(self):
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.result_label.config(text="")
        self.ax.clear()  # Limpiar gráfica
        self.canvas.draw()  # Actualizar el canvas
        self.text_steps.config(state=tk.NORMAL)
        self.text_steps.delete(1.0, tk.END)  # Limpiar cuadro de texto
        self.text_steps.config(state=tk.DISABLED)

    def visualize_process(self):
        G = nx.Graph()
        
        for node, connections in self.heuristica.graph.items():
            for connection in connections:
                G.add_edge(node, connection[0], weight=connection[1])

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", font_weight="bold", node_size=700, ax=self.ax)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=self.ax)
        self.ax.set_title("Grafo original con todas las aristas")
        self.canvas.draw()

        # Visualizar cada paso del algoritmo
        route = []
        total_weight = 0  # Inicializar la suma total de pesos
        for step, edge in enumerate(self.heuristica.heuristic(), start=1):
            route.append(edge)
            total_weight += edge[2]  # Sumar el peso de la arista actual
            self.ax.clear()  # Limpiar para actualizar cada paso

            # Dibujar el grafo base con todos los nodos y etiquetas de los pesos de las aristas
            nx.draw(G, pos, with_labels=True, node_color="lightblue", font_weight="bold", node_size=700, ax=self.ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=self.ax)
            
            # Dibujar las aristas seleccionadas en rojo
            edge_colors = ["red" if (u, v, d['weight']) in route or (v, u, d['weight']) in route else "black" for u, v, d in G.edges(data=True)]
            nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=700, edge_color=edge_colors, ax=self.ax)
            
            # Agregar el paso al cuadro de texto
            self.text_steps.insert(tk.END, f"Paso {step}: Añadir arista {edge[0]}-{edge[1]} (peso {edge[2]})\n")
            
            self.ax.set_title(f"Paso {step}: Añadir arista {edge[0]}-{edge[1]} (peso {edge[2]})")
            self.canvas.draw()  # Actualizar canvas en cada paso
            self.root.update()  # Actualizar ventana de tkinter para ver el cambio
            self.root.after(1000)  # Pausa de 1 segundo entre pasos

        self.result_label.config(text="Ruta más corta encontrada")
        self.text_steps.insert(tk.END, f"\nPeso total de la ruta: {total_weight}\n")
        self.text_steps.config(state=tk.DISABLED)  # Desactivar edición en cuadro de texto
        messagebox.showinfo("Resultado", f"Ruta más corta encontrada con un peso total de {total_weight}")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
