import tkinter as tk
from tkinter import ttk, messagebox
import json

class LogicGate:
    def __init__(self, gate_type, x, y, id=None):
        self.type = gate_type
        self.x = x
        self.y = y
        self.id = id
        self.inputs = []
        self.output = None
        self.connections = []
        self.label = ""
        
    def compute(self):
        """Вычисление выхода вентиля на основе входов"""
        if self.type == "AND":
            self.output = all(self.inputs) if self.inputs else False
        elif self.type == "OR":
            self.output = any(self.inputs) if self.inputs else False
        elif self.type == "NOT":
            self.output = not self.inputs[0] if self.inputs else True
        elif self.type == "XOR":
            if len(self.inputs) == 2:
                self.output = self.inputs[0] != self.inputs[1]
            else:
                self.output = False
        elif self.type == "NAND":
            self.output = not all(self.inputs) if self.inputs else True
        elif self.type == "NOR":
            self.output = not any(self.inputs) if self.inputs else True
        elif self.type == "INPUT":
            pass
        elif self.type == "OUTPUT":
            self.output = self.inputs[0] if self.inputs else False
        return self.output

class ModernLogicSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Симулятор Логических Схем - Современный Тёмный")
        self.root.geometry("1300x800")
        self.root.configure(bg='#1e1e1e')
        
        # Современная цветовая схема
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d30',
            'bg_tertiary': '#3e3e42',
            'accent': '#007acc',
            'accent_hover': '#1177bb',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'success': '#4ec9b0',
            'warning': '#ffcc02',
            'error': '#f44747',
            'gate_default': '#404040',
            'gate_input': '#4ec9b0',
            'gate_output': '#ffcc02',
            'gate_and': '#569cd6',
            'gate_or': '#c586c0',
            'gate_not': '#d16969',
            'gate_xor': '#ce9178',
            'gate_nand': '#9cdcfe',
            'gate_nor': '#d7ba7d',
            'wire': '#cccccc',
            'wire_active': '#ffffff',
            'connector_input': '#4ec9b0',
            'connector_output': '#ffcc02',
            'selection': '#007acc'
        }
        
        self.gates = []
        self.wires = []
        self.next_gate_id = 1
        self.selected_gate = None
        self.dragging = False
        self.connecting = False
        self.connection_start = None
        self.wire_start_point = None
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Настройка современных стилей"""
        style = ttk.Style()
        
        # Современная темная тема
        style.theme_use('clam')
        
        # Конфигурация стилей
        style.configure('Modern.TFrame', background=self.colors['bg_primary'])
        style.configure('Toolbar.TFrame', background=self.colors['bg_secondary'])
        style.configure('Canvas.TFrame', background=self.colors['bg_primary'])
        
        # Стили для кнопок
        style.configure('Modern.TButton',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8),
                       font=('Segoe UI', 10))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent']),
                           ('pressed', self.colors['accent_hover'])],
                 foreground=[('active', self.colors['text_primary'])]
                 )
        
        # Стили для вкладок и меток
        style.configure('Modern.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 9))
        
        style.configure('Title.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Status.TLabel',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 9),
                       padding=(10, 5))
        
    def setup_ui(self):
        """Настройка современного пользовательского интерфейса"""
        # Главный контейнер
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Панель инструментов (слева)
        toolbar = ttk.Frame(main_container, width=220, style='Toolbar.TFrame')
        toolbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 1))
        toolbar.pack_propagate(False)
        
        # Заголовок панели инструментов
        title_frame = ttk.Frame(toolbar, style='Toolbar.TFrame', height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        ttk.Label(title_frame, text="ЛОГИЧЕСКИЕ ВЕНТИЛИ", style='Title.TLabel').pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
        
        # Область с кнопками вентилей
        gates_frame = ttk.Frame(toolbar, style='Toolbar.TFrame')
        gates_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(gates_frame, text="КОМПОНЕНТЫ", style='Modern.TLabel', 
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 8))
        
        # Кнопки для добавления вентилей
        gates = [
            ("INPUT", "Вход (INPUT)", self.colors['gate_input']),
            ("OUTPUT", "Выход (OUTPUT)", self.colors['gate_output']),
            ("AND", "И (AND)", self.colors['gate_and']),
            ("OR", "ИЛИ (OR)", self.colors['gate_or']), 
            ("NOT", "НЕ (NOT)", self.colors['gate_not']),
            ("XOR", "Искл. ИЛИ (XOR)", self.colors['gate_xor']),
            ("NAND", "И-НЕ (NAND)", self.colors['gate_nand']),
            ("NOR", "ИЛИ-НЕ (NOR)", self.colors['gate_nor'])
        ]
        
        for gate_type, label, color in gates:
            self.create_gate_button(toolbar, gate_type, label, color)
        
        # Разделитель
        separator = ttk.Separator(toolbar, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=15, pady=15)
        
        # Панель управления
        control_frame = ttk.Frame(toolbar, style='Toolbar.TFrame')
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="УПРАВЛЕНИЕ", style='Modern.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 8))
        
        # Кнопки управления
        control_buttons = [
            ("🔗 Соединить", self.start_connection),
            ("🗑️ Удалить", self.delete_selected),
            ("✏️ Переименовать", self.rename_gate),
            ("📊 Таблица истинности", self.show_truth_table),
            ("🧪 Тестировать схему", self.test_circuit),
            ("🗑️ Очистить всё", self.clear_all)
        ]
        
        for text, command in control_buttons:
            btn = ttk.Button(control_frame, text=text, command=command, style='Modern.TButton')
            btn.pack(fill=tk.X, pady=3)
        
        # Область холста (справа)
        canvas_container = ttk.Frame(main_container, style='Canvas.TFrame')
        canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Заголовок холста
        canvas_header = ttk.Frame(canvas_container, style='Toolbar.TFrame', height=40)
        canvas_header.pack(fill=tk.X, pady=(0, 1))
        canvas_header.pack_propagate(False)
        
        ttk.Label(canvas_header, text="РАБОЧАЯ ОБЛАСТЬ", style='Title.TLabel').pack(expand=True, fill=tk.BOTH, padx=15)
        
        # Холст для рисования
        self.canvas = tk.Canvas(canvas_container, bg=self.colors['bg_primary'], 
                               relief='flat', highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Статусная панель
        status_bar = ttk.Frame(canvas_container, style='Toolbar.TFrame', height=30)
        status_bar.pack(fill=tk.X, pady=(1, 0))
        status_bar.pack_propagate(False)
        
        self.status_label = ttk.Label(status_bar, text="Готов к созданию логических схем", 
                                     style='Status.TLabel')
        self.status_label.pack(fill=tk.X, padx=1)
        
        # Привязка событий мыши
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)
        
    def create_gate_button(self, parent, gate_type, label, color):
        """Создание современной кнопки для вентиля"""
        btn_frame = ttk.Frame(parent, style='Toolbar.TFrame')
        btn_frame.pack(fill=tk.X, pady=2, padx=10)
        
        # Цветной индикатор
        color_indicator = tk.Frame(btn_frame, bg=color, width=4, height=20)
        color_indicator.pack(side=tk.LEFT, padx=(0, 10))
        
        btn = ttk.Button(btn_frame, text=label, 
                        command=lambda gt=gate_type: self.add_gate(gt),
                        style='Modern.TButton')
        btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def update_status(self, message):
        """Обновление статусной строки"""
        self.status_label.config(text=message)
        
    def add_gate(self, gate_type):
        """Добавление нового вентиля на холст"""
        x, y = 200, 150
        
        gate = LogicGate(gate_type, x, y, self.next_gate_id)
        gate.label = f"{gate_type}_{gate.id}"
        self.next_gate_id += 1
        self.gates.append(gate)
        
        self.draw_gate(gate)
        self.update_status(f"Добавлен вентиль: {gate_type}")
        
    def draw_gate(self, gate):
        """Отрисовка современного вентиля на холсте"""
        x, y = gate.x, gate.y
        
        # Цвет вентиля
        gate_colors = {
            "INPUT": self.colors['gate_input'],
            "OUTPUT": self.colors['gate_output'], 
            "AND": self.colors['gate_and'],
            "OR": self.colors['gate_or'],
            "NOT": self.colors['gate_not'],
            "XOR": self.colors['gate_xor'],
            "NAND": self.colors['gate_nand'],
            "NOR": self.colors['gate_nor']
        }
        
        color = gate_colors.get(gate.type, self.colors['gate_default'])
        selected_color = self.colors['selection'] if gate == self.selected_gate else color
        
        # Тень для эффекта глубины
        shadow_offset = 2
        self.canvas.create_rectangle(x-30+shadow_offset, y-20+shadow_offset, 
                                   x+30+shadow_offset, y+20+shadow_offset, 
                                   fill='#000000', outline='', tags=f"shadow_{gate.id}")
        
        # Основная фигура вентиля
        if gate.type == "INPUT":
            self.canvas.create_rectangle(x-30, y-20, x+30, y+20, 
                                       fill=selected_color, outline=self.colors['text_primary'], width=1,
                                       tags=f"gate_{gate.id}")
            self.canvas.create_text(x, y, text="INPUT", fill=self.colors['text_primary'], 
                                  font=('Segoe UI', 9, 'bold'), tags=f"gate_{gate.id}")
            # Точка выхода
            self.canvas.create_oval(x+25, y-5, x+35, y+5, fill=self.colors['connector_output'], 
                                  outline=self.colors['text_primary'], width=1, tags=f"output_{gate.id}")
            
        elif gate.type == "OUTPUT":
            self.canvas.create_rectangle(x-30, y-20, x+30, y+20, 
                                       fill=selected_color, outline=self.colors['text_primary'], width=1,
                                       tags=f"gate_{gate.id}")
            self.canvas.create_text(x, y, text="OUTPUT", fill=self.colors['text_primary'],
                                  font=('Segoe UI', 9, 'bold'), tags=f"gate_{gate.id}")
            # Точка входа
            self.canvas.create_oval(x-35, y-5, x-25, y+5, fill=self.colors['connector_input'],
                                  outline=self.colors['text_primary'], width=1, tags=f"input1_{gate.id}")
            
        elif gate.type in ["AND", "OR", "XOR", "NAND", "NOR"]:
            self.canvas.create_rectangle(x-30, y-20, x+30, y+20, 
                                       fill=selected_color, outline=self.colors['text_primary'], width=1,
                                       tags=f"gate_{gate.id}")
            self.canvas.create_text(x, y, text=gate.type, fill=self.colors['text_primary'],
                                  font=('Segoe UI', 9, 'bold'), tags=f"gate_{gate.id}")
            # Точки входа и выхода
            self.canvas.create_oval(x-35, y-10, x-25, y, fill=self.colors['connector_input'],
                                  outline=self.colors['text_primary'], width=1, tags=f"input1_{gate.id}")
            self.canvas.create_oval(x-35, y, x-25, y+10, fill=self.colors['connector_input'],
                                  outline=self.colors['text_primary'], width=1, tags=f"input2_{gate.id}")
            self.canvas.create_oval(x+25, y-5, x+35, y+5, fill=self.colors['connector_output'],
                                  outline=self.colors['text_primary'], width=1, tags=f"output_{gate.id}")
            
        elif gate.type == "NOT":
            self.canvas.create_rectangle(x-30, y-20, x+30, y+20, 
                                       fill=selected_color, outline=self.colors['text_primary'], width=1,
                                       tags=f"gate_{gate.id}")
            self.canvas.create_text(x, y, text="NOT", fill=self.colors['text_primary'],
                                  font=('Segoe UI', 9, 'bold'), tags=f"gate_{gate.id}")
            self.canvas.create_oval(x-35, y-5, x-25, y+5, fill=self.colors['connector_input'],
                                  outline=self.colors['text_primary'], width=1, tags=f"input1_{gate.id}")
            self.canvas.create_oval(x+25, y-5, x+35, y+5, fill=self.colors['connector_output'],
                                  outline=self.colors['text_primary'], width=1, tags=f"output_{gate.id}")
    
    def start_connection(self):
        """Начало процесса соединения вентилей"""
        self.connecting = True
        self.update_status("Режим соединения: кликните на выход одного вентиля, затем на вход другого")
    
    def on_canvas_click(self, event):
        """Обработка клика на холсте"""
        if self.connecting:
            self.handle_connection(event)
        else:
            self.handle_selection(event)
    
    def handle_connection(self, event):
        """Обработка соединения вентилей"""
        clicked_items = self.canvas.find_closest(event.x, event.y)
        
        if not clicked_items:
            return
            
        tags = self.canvas.gettags(clicked_items[0])
        
        for tag in tags:
            if tag.startswith("output_"):
                gate_id = int(tag.split("_")[1])
                gate = next((g for g in self.gates if g.id == gate_id), None)
                if gate:
                    self.connection_start = gate_id
                    self.wire_start_point = (gate.x + 30, gate.y)
                    if gate.type == "INPUT":
                        self.update_status(f"Выбран выход INPUT. Теперь выберите вход.")
                    elif gate.type == "OUTPUT":
                        self.update_status(f"Выбран выход OUTPUT. Теперь выберите вход.")
                    else:
                        self.update_status(f"Выбран выход {gate.type}. Теперь выберите вход.")
                return
                
            elif tag.startswith("input") and self.connection_start:
                gate_id = int(tag.split("_")[1])
                input_type = tag.split("_")[0]
                
                # Создание соединения
                self.create_connection(self.connection_start, gate_id, input_type)
                self.connection_start = None
                self.wire_start_point = None
                self.connecting = False
                self.update_status("Соединение создано")
                return
    
    def handle_selection(self, event):
        """Обработка выбора вентиля"""
        clicked_items = self.canvas.find_closest(event.x, event.y)
        
        if not clicked_items:
            self.selected_gate = None
            self.redraw_canvas()
            return
            
        tags = self.canvas.gettags(clicked_items[0])
        
        for tag in tags:
            if tag.startswith("gate_"):
                gate_id = int(tag.split("_")[1])
                self.selected_gate = next((g for g in self.gates if g.id == gate_id), None)
                self.dragging = True
                if self.selected_gate.type in ["INPUT", "OUTPUT"]:
                    self.update_status(f"Выбран: {self.selected_gate.type}")
                else:
                    self.update_status(f"Выбран: {self.selected_gate.label}")
                self.redraw_canvas()
                return
    
    def on_canvas_double_click(self, event):
        """Обработка двойного клика для переименования"""
        clicked_items = self.canvas.find_closest(event.x, event.y)
        
        if not clicked_items:
            return
            
        tags = self.canvas.gettags(clicked_items[0])
        
        for tag in tags:
            if tag.startswith("gate_"):
                gate_id = int(tag.split("_")[1])
                gate = next((g for g in self.gates if g.id == gate_id), None)
                if gate:
                    self.rename_gate_dialog(gate)
                return
    
    def rename_gate_dialog(self, gate):
        """Современный диалог для переименования вентиля"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Переименовать вентиль")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['bg_secondary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Центрирование диалога
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        if gate.type in ["INPUT", "OUTPUT"]:
            title_text = f"Переименовать {gate.type}"
        else:
            title_text = f"Переименовать вентиль {gate.type}"
            
        title = ttk.Label(dialog, text=title_text, style='Title.TLabel')
        title.pack(pady=20)
        
        instruction = ttk.Label(dialog, text="Введите новое имя:", style='Modern.TLabel')
        instruction.pack(pady=5)
        
        name_var = tk.StringVar(value=gate.label)
        entry = ttk.Entry(dialog, textvariable=name_var, font=('Segoe UI', 11), width=30)
        entry.pack(pady=15, ipady=5)
        entry.select_range(0, tk.END)
        entry.focus()
        
        def save_name():
            new_name = name_var.get().strip()
            if new_name:
                gate.label = new_name
                self.redraw_canvas()
                self.update_status(f"Переименовано в: {new_name}")
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog, style='Modern.TFrame')
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Сохранить", command=save_name, style='Modern.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy, style='Modern.TButton').pack(side=tk.LEFT, padx=5)
        
        dialog.bind('<Return>', lambda e: save_name())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    def rename_gate(self):
        """Переименование выбранного вентиля"""
        if self.selected_gate:
            self.rename_gate_dialog(self.selected_gate)
        else:
            messagebox.showwarning("Предупреждение", "Сначала выберите вентиль для переименования")
    
    def create_connection(self, from_gate_id, to_gate_id, input_type):
        """Создание соединения между вентилями"""
        from_gate = next((g for g in self.gates if g.id == from_gate_id), None)
        to_gate = next((g for g in self.gates if g.id == to_gate_id), None)
        
        if from_gate and to_gate:
            # Проверяем на дубликаты
            for wire in self.wires:
                if (wire['from_gate'] == from_gate_id and 
                    wire['to_gate'] == to_gate_id and 
                    wire['input_type'] == input_type):
                    messagebox.showwarning("Предупреждение", "Соединение уже существует")
                    return
            
            # Добавляем соединение
            connection = {
                'from_gate': from_gate_id,
                'to_gate': to_gate_id,
                'input_type': input_type
            }
            self.wires.append(connection)
            
            # Отрисовка провода
            self.draw_wire(from_gate, to_gate, input_type)
    
    def draw_wire(self, from_gate, to_gate, input_type):
        """Отрисовка современного провода"""
        x1 = from_gate.x + 30
        y1 = from_gate.y
        
        x2 = to_gate.x - 30
        if input_type == "input1":
            y2 = to_gate.y - 5
        elif input_type == "input2":
            y2 = to_gate.y + 5
        else:
            y2 = to_gate.y
            
        # Рисуем плавную изогнутую линию
        mid_x = (x1 + x2) / 2
        self.canvas.create_line(x1, y1, mid_x, y1, mid_x, y2, x2, y2, 
                               arrow=tk.LAST, fill=self.colors['wire'], 
                               width=2, smooth=False, capstyle=tk.ROUND)
    
    def on_canvas_drag(self, event):
        """Обработка перетаскивания вентиля"""
        if self.dragging and self.selected_gate:
            self.selected_gate.x = event.x
            self.selected_gate.y = event.y
            self.redraw_canvas()
    
    def on_canvas_release(self, event):
        """Обработка отпускания кнопки мыши"""
        self.dragging = False
    
    def redraw_canvas(self):
        """Перерисовка всего холста"""
        self.canvas.delete("all")
        
        # Перерисовываем все провода
        for wire in self.wires:
            from_gate = next((g for g in self.gates if g.id == wire['from_gate']), None)
            to_gate = next((g for g in self.gates if g.id == wire['to_gate']), None)
            if from_gate and to_gate:
                self.draw_wire(from_gate, to_gate, wire['input_type'])
        
        # Перерисовываем все вентили
        for gate in self.gates:
            self.draw_gate(gate)
    
    def delete_selected(self):
        """Удаление выбранного вентиля"""
        if self.selected_gate:
            # Удаляем все соединения с этим вентилем
            self.wires = [w for w in self.wires 
                         if w['from_gate'] != self.selected_gate.id 
                         and w['to_gate'] != self.selected_gate.id]
            
            # Удаляем вентиль
            self.gates = [g for g in self.gates if g.id != self.selected_gate.id]
            self.selected_gate = None
            self.redraw_canvas()
            self.update_status("Вентиль удален")
        else:
            messagebox.showwarning("Предупреждение", "Сначала выберите вентиль для удаления")
    
    def clear_all(self):
        """Очистка всего холста"""
        if messagebox.askyesno("Подтверждение", "Очистить всю рабочую область?"):
            self.gates = []
            self.wires = []
            self.selected_gate = None
            self.redraw_canvas()
            self.update_status("Рабочая область очищена")
    
    def simulate_circuit(self, input_values):
        """Моделирование схемы с заданными входными значениями"""
        # Сбрасываем все выходы
        for gate in self.gates:
            gate.output = None
            gate.inputs = []
        
        # Устанавливаем значения входных вентилей
        input_gates = [g for g in self.gates if g.type == "INPUT"]
        input_gates.sort(key=lambda g: g.id)
        
        for i, gate in enumerate(input_gates):
            if i < len(input_values):
                gate.output = input_values[i]
        
        # Вычисляем выходы всех вентилей
        changed = True
        iterations = 0
        max_iterations = 100
        
        while changed and iterations < max_iterations:
            changed = False
            iterations += 1
            
            for gate in self.gates:
                if gate.output is not None and gate.type != "INPUT":
                    continue
                    
                # Собираем входы для этого вентиля
                inputs_ready = True
                gate.inputs = []
                
                input_wires = [w for w in self.wires if w['to_gate'] == gate.id]
                
                for wire in input_wires:
                    from_gate = next((g for g in self.gates if g.id == wire['from_gate']), None)
                    if from_gate and from_gate.output is not None:
                        gate.inputs.append(from_gate.output)
                    else:
                        inputs_ready = False
                        break
                
                if inputs_ready and (gate.inputs or gate.type == "INPUT"):
                    old_output = gate.output
                    gate.compute()
                    if gate.output != old_output:
                        changed = True
        
        if iterations >= max_iterations:
            messagebox.showwarning("Предупреждение", "Достигнуто максимальное количество итераций. Возможно, в схеме есть цикл.")
        
        # Возвращаем выходные значения
        output_gates = [g for g in self.gates if g.type == "OUTPUT"]
        output_gates.sort(key=lambda g: g.id)
        
        return [gate.output for gate in output_gates if gate.output is not None]
    
    def test_circuit(self):
        """Тестирование схемы с ручным вводом значений"""
        input_gates = [g for g in self.gates if g.type == "INPUT"]
        if not input_gates:
            messagebox.showwarning("Предупреждение", "Добавьте хотя бы один INPUT вентиль")
            return
        
        # Создаем современный диалог
        dialog = tk.Toplevel(self.root)
        dialog.title("Тестирование схемы")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg_secondary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Центрирование
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        title = ttk.Label(dialog, text="Тестирование схемы", style='Title.TLabel')
        title.pack(pady=20)
        
        instruction = ttk.Label(dialog, text="Установите значения входов:", style='Modern.TLabel')
        instruction.pack(pady=10)
        
        input_vars = []
        input_frame = ttk.Frame(dialog, style='Modern.TFrame')
        input_frame.pack(pady=20, padx=30, fill=tk.X)
        
        for i, gate in enumerate(input_gates):
            row = ttk.Frame(input_frame, style='Modern.TFrame')
            row.pack(fill=tk.X, pady=8)
            
            ttk.Label(row, text=f"{gate.label}:", style='Modern.TLabel', 
                     width=15).pack(side=tk.LEFT)
            
            var = tk.StringVar(value="0")
            input_vars.append(var)
            
            ttk.Radiobutton(row, text="0 (Ложь)", variable=var, value="0",
                           style='Modern.TButton').pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(row, text="1 (Истина)", variable=var, value="1",
                           style='Modern.TButton').pack(side=tk.LEFT, padx=5)
        
        def calculate():
            input_values = [var.get() == "1" for var in input_vars]
            outputs = self.simulate_circuit(input_values)
            
            result_text = "Результаты:\n\n"
            output_gates = [g for g in self.gates if g.type == "OUTPUT"]
            output_gates.sort(key=lambda g: g.id)
            
            for i, (gate, output) in enumerate(zip(output_gates, outputs)):
                status = "🟢 1" if output else "🔴 0"
                result_text += f"{gate.label}: {status}\n"
            
            if not outputs:
                result_text += "Нет выходных значений"
            
            messagebox.showinfo("Результаты тестирования", result_text)
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog, style='Modern.TFrame')
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Рассчитать", command=calculate, 
                  style='Modern.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=10)
    
    def show_truth_table(self):
        """Показ таблицы истинности"""
        input_gates = [g for g in self.gates if g.type == "INPUT"]
        if not input_gates:
            messagebox.showwarning("Предупреждение", "Добавьте хотя бы один INPUT вентиль")
            return
        
        output_gates = [g for g in self.gates if g.type == "OUTPUT"]
        if not output_gates:
            messagebox.showwarning("Предупреждение", "Добавьте хотя бы один OUTPUT вентиль")
            return
        
        # Создаем современное окно
        truth_window = tk.Toplevel(self.root)
        truth_window.title("Таблица истинности")
        truth_window.geometry("900x600")
        truth_window.configure(bg=self.colors['bg_secondary'])
        
        # Заголовок
        title_frame = ttk.Frame(truth_window, style='Toolbar.TFrame', height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        ttk.Label(title_frame, text="ТАБЛИЦА ИСТИННОСТИ", style='Title.TLabel').pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        
        # Таблица с прокруткой
        table_container = ttk.Frame(truth_window, style='Modern.TFrame')
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Создаем Treeview с современным стилем
        columns = ["№"] + [gate.label for gate in input_gates] + [gate.label for gate in output_gates]
        
        # Стиль для таблицы
        style = ttk.Style()
        style.configure("Modern.Treeview", 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_primary'],
                       borderwidth=0)
        style.configure("Modern.Treeview.Heading", 
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       relief='flat')
        
        tree = ttk.Treeview(table_container, columns=columns, show="headings", style="Modern.Treeview")
        
        # Настраиваем заголовки
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80, anchor=tk.CENTER)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        # Генерируем таблицу
        num_inputs = len(input_gates)
        input_gates.sort(key=lambda g: g.id)
        output_gates.sort(key=lambda g: g.id)
        
        for i in range(2 ** num_inputs):
            input_comb = []
            for j in range(num_inputs):
                input_comb.append(bool((i >> (num_inputs - 1 - j)) & 1))
            
            outputs = self.simulate_circuit(input_comb)
            
            row_values = [str(i+1)] + ["1" if val else "0" for val in input_comb] + ["1" if val else "0" for val in outputs]
            tree.insert("", "end", values=row_values)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

# Запуск симулятора
if __name__ == "__main__":
    simulator = ModernLogicSimulator()
    simulator.run()
