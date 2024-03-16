import tkinter as tk  # Importación de la biblioteca Tkinter para la interfaz gráfica
import time
import threading

class Frame:
    # Clase que representa un bloque de memoria en el sistema principal
    def __init__(self, frame_id, process_id=None):
        # Inicialización de un frame con un ID y un posible ID de proceso asignado
        self.frame_id = frame_id  
        self.process_id = process_id  
        self.color = "white"  

class Memory:
    # Clase que gestiona la memoria principal del sistema
    def __init__(self, size):
        # Inicialización de la memoria con un tamaño dado y una lista de frames
        self.size = size  
        self.frames = [Frame(i) for i in range(size)]  

    def allocate_frames(self, process_id, num_frames):
        # Método para asignar frames a un proceso
        allocated_frames = []  
        free_frames = [frame for frame in self.frames if frame.process_id is None]  
        if len(free_frames) >= num_frames:  
            for i in range(num_frames):  
                free_frames[i].process_id = process_id  
                free_frames[i].color = colors[process_id]  
                allocated_frames.append(free_frames[i])  
            return allocated_frames  
        else:
            return None  

    def deallocate_frames(self, process_id):
        # Método para liberar los frames asignados a un proceso
        for frame in self.frames:  
            if frame.process_id == process_id:  
                frame.process_id = None  
                frame.color = "white"  

class VirtualMemory:
    # Clase que gestiona la memoria virtual del sistema
    def __init__(self, size):
        # Inicialización de la memoria virtual con un tamaño dado y una lista de frames
        self.size = size  
        self.frames = [Frame(i) for i in range(size)]  

    def allocate_frames(self, process_id, num_frames):
        # Método para asignar frames a un proceso en memoria virtual
        allocated_frames = []  
        free_frames = [frame for frame in self.frames if frame.process_id is None]  
        if len(free_frames) >= num_frames:  
            for i in range(num_frames):  
                free_frames[i].process_id = process_id  
                free_frames[i].color = colors[process_id]  
                allocated_frames.append(free_frames[i])  
            return allocated_frames  
        else:
            return None  

    def deallocate_frames(self, process_id):
        # Método para liberar los frames asignados a un proceso en memoria virtual
        for frame in self.frames:  
            if frame.process_id == process_id:  
                frame.process_id = None  
                frame.color = "white"  

class Process:
    # Clase que representa un proceso en el sistema
    def __init__(self, process_id, size, duration):
        # Inicialización de un proceso con un ID, tamaño y duración
        self.process_id = process_id  
        self.size = size  
        self.duration = duration  

class OperatingSystem:
    # Clase que controla la carga, ejecución y descarga de procesos en el sistema
    def __init__(self, memory_size, virtual_memory_size):
        # Inicialización del sistema operativo con tamaños de memoria y otros atributos
        self.memory = Memory(memory_size)  
        self.virtual_memory = VirtualMemory(virtual_memory_size)  
        self.processes = {}  
        self.running = True  

    def load_process(self, process):
        # Método para cargar un proceso en la memoria principal o virtual
        allocated_frames = self.memory.allocate_frames(process.process_id, process.size)  
        if allocated_frames:  
            self.processes[process.process_id] = {"frames": allocated_frames, "duration": process.duration}  
            print(f"Process {process.process_id} loaded into frames {[frame.frame_id for frame in allocated_frames]}")  
            return True
        else:
            allocated_frames = self.virtual_memory.allocate_frames(process.process_id, process.size)  
            if allocated_frames:  
                self.processes[process.process_id] = {"frames": allocated_frames, "duration": process.duration}  
                print(f"Process {process.process_id} loaded into virtual memory")  
                return True
            else:
                print(f"Not enough memory to load process {process.process_id}")  
                return False

    def unload_process(self, process_id):
        # Método para descargar un proceso del sistema
        if process_id in self.processes:  
            for frame in self.processes[process_id]["frames"]:  
                frame_id = frame.frame_id  
                frame.process_id = None  
                frame.color = "white"  
                print(f"Frame {frame_id} released")  
            del self.processes[process_id]  
            print(f"Process {process_id} unloaded")  
            return True
        else:
            print(f"Process {process_id} is not currently loaded")  
            return False

    def run_processes(self):
        # Método para ejecutar los procesos cargados en el sistema
        while self.running:  
            for process_id, data in list(self.processes.items()):  
                duration = data["duration"]  
                if duration > 0:  
                    time.sleep(1)  
                    data["duration"] -= 1  
                else:
                    self.unload_process(process_id)  
            time.sleep(0.1)  

def update_gui():
    # Función para actualizar la interfaz gráfica y reflejar los cambios en la asignación de memoria y el estado de los procesos
    while os.running:  
        for frame in os.memory.frames:  
            frame_label = frame_labels[frame.frame_id]  
            frame_label.config(bg=frame.color)  
        for frame in os.virtual_memory.frames:  
            frame_label = virtual_frame_labels[frame.frame_id]  
            frame_label.config(bg=frame.color)  
        for process_id, data in list(os.processes.items()):  
            process_label = process_labels[process_id]  
            process_label["text"] = f"Process {process_id} - Time Left: {data['duration']}"  
        root.update()  
        time.sleep(0.1)  

def start_simulation():
    # Función para iniciar la simulación ejecutando los procesos en subprocesos separados
    threading.Thread(target=os.run_processes).start()  
    threading.Thread(target=update_gui).start()  

colors = {1: "red", 2: "green", 3: "blue"}  # Colores para los procesos

root = tk.Tk()  # Creación de la ventana principal
root.title("Memory Management Simulation")  # Configuración del título de la ventana

memory_frame = tk.Frame(root)  # Creación de un marco para la memoria principal
memory_frame.pack()  

frame_labels = []  # Lista para almacenar las etiquetas de los frames de la memoria principal
for i in range(10):  
    frame_label = tk.Label(memory_frame, text=f"Frame {i}", relief=tk.RAISED, width=10, height=2)  
    frame_label.grid(row=0, column=i)  
    frame_labels.append(frame_label)  

virtual_memory_frame = tk.Frame(root)  # Creación de un marco para la memoria virtual
virtual_memory_frame.pack()  

virtual_frame_labels = []  # Lista para almacenar las etiquetas de los frames de la memoria virtual
for i in range(10):  
    frame_label = tk.Label(virtual_memory_frame, text=f"Virtual Frame {i}", relief=tk.RAISED, width=15, height=2)  
    frame_label.grid(row=0, column=i)  
    virtual_frame_labels.append(frame_label)  

process_frame = tk.Frame(root)  # Creación de un marco para mostrar el estado de los procesos
process_frame.pack()  

process_labels = {}  # Diccionario para almacenar las etiquetas de los procesos
for i in range(1, 4):  
    process_label = tk.Label(process_frame, text=f"Process {i} - Time Left: 0", relief=tk.RAISED, width=25, height=2)  
    process_label.grid(row=i, column=0)  
    process_labels[i] = process_label  

os = OperatingSystem(memory_size=10, virtual_memory_size=10)  # Creación del sistema operativo

os.load_process(Process(process_id=1, size=6, duration=5))  
os.load_process(Process(process_id=2, size=4, duration=3))  
os.load_process(Process(process_id=3, size=5, duration=2))  

start_button = tk.Button(root, text="Start Simulation", command=start_simulation)  # Botón para iniciar la simulación
start_button.pack()  

root.mainloop()  # Inicio del bucle principal de la interfaz gráfica
