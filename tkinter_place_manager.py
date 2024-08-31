import tkinter as tk
from tkinter import filedialog

class DragAndDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title('tkinter - Place manager')

        # Full-screen weergave
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.dragging_widget = None
        self.selected_widget = None
        self.draggable_widgets = {}
        self.copied_widgets = []
        self.resizing_widget = False  # Houd bij of een widget wordt gewijzigd in grootte
        self.widget_counters = {
            "Label": 0, "Button": 0, "Entry": 0, "Listbox": 0,
            "Checkbutton": 0, "Radiobutton": 0, "Scale": 0,
            "Text": 0, "Spinbox": 0
        }  # Houd bij hoeveel exemplaren van elke widget zijn toegevoegd

        # self.widget_name_label = tk.Label(self.root, text="", fg='blue')
        # self.widget_name_label.place(x=10, y=5)

        self.create_frames()
        self.create_widgets_in_left_frame()
        self.create_drag_toggle_button()
        self.create_resize_entries()
        self.create_delete_button()
        self.create_save_button()


    def create_frames(self):
        # Bereken de breedtes van de frames
        self.left_frame_width = int(self.root.winfo_screenwidth() * 0.25)
        self.right_frame_width = int(self.root.winfo_screenwidth() * 0.75)

        # Gebruik screen_height in plaats van root.winfo_height()
        screen_height = self.root.winfo_screenheight()

        # Maak linker, boven en rechter frames
        self.top_frame = tk.Frame(self.root, bg="white", height=40)
        self.top_frame.pack(side="top", fill="x")

        self.left_frame = tk.Frame(self.root, bg="lightgrey", width=self.left_frame_width,
                                   height=screen_height - 40)  # Trek de hoogte van top_frame af
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = tk.Frame(self.root, bg="gray13", width=self.right_frame_width,
                                    height=screen_height - 40)
        self.right_frame.pack(side="right", fill="both", expand=True)

    def create_widgets_in_left_frame(self):
        # Maak een lijst van alle widgets
        widgets = [
            tk.Label(self.left_frame, text="Label", bg="lightblue"),
            tk.Button(self.left_frame, text="Button", bg="lightgreen"),
            tk.Entry(self.left_frame),
            tk.Listbox(self.left_frame),
            tk.Checkbutton(self.left_frame, text="Checkbutton"),
            tk.Radiobutton(self.left_frame, text="Radiobutton"),
            tk.Scale(self.left_frame, from_=0, to=10),
            tk.Text(self.left_frame, height=3, width=20),
            tk.Spinbox(self.left_frame, from_=0, to=10),
        ]

        # Plaats de widgets in het linkerframe
        self.widget_name_label = tk.Label(self.left_frame, text="", fg='blue', bg='lightgrey')
        self.widget_name_label.pack(side="top",pady=20)
        for idx, widget in enumerate(widgets):
            widget.pack(pady=5)
            widget.bind("<Button-1>", self.start_copy)  # Start kopieactie
            widget.bind("<Enter>", self.show_widget_name)
            widget.bind("<Leave>", self.hide_widget_name)

    def create_drag_toggle_button(self):
        # Maak een knop om het verslepen aan/uit te schakelen voor een widget
        self.toggle_button = tk.Button(self.top_frame, text="Verslepen: Ja", command=self.toggle_drag)
        self.toggle_button.pack(side="left", padx=10)

    def create_resize_entries(self):
         # Maak invoervelden voor breedte en hoogte
        tk.Label(self.top_frame, text="Breedte:").pack(side="left", padx=5)
        self.width_entry = tk.Entry(self.top_frame, width=5)
        self.width_entry.pack(side="left")

        tk.Label(self.top_frame, text="Hoogte:").pack(side="left", padx=5)
        self.height_entry = tk.Entry(self.top_frame, width=5)
        self.height_entry.pack(side="left")

        resize_button = tk.Button(self.top_frame, text="Toepassen", command=self.apply_resize)
        resize_button.pack(side="left", padx=10)

    def create_delete_button(self):
        # Voeg een knop toe om de geselecteerde widget te verwijderen
        delete_button = tk.Button(self.top_frame, text="Verwijder geselecteerde widget", command=self.delete_selected_widget)
        delete_button.pack(side="left", padx=10)

    def create_save_button(self):
        # Voeg een knop toe om de layout op te slaan als een Python-bestand
        save_button = tk.Button(self.top_frame, text="Opslaan als Python-bestand", command=self.save_as_python)
        save_button.pack(side="left", padx=10)

    def toggle_drag(self):
        # Wissel de "verslepen"-status van de geselecteerde widget
        if self.selected_widget:
            current_status = self.draggable_widgets.get(self.selected_widget, True)
            new_status = not current_status
            self.draggable_widgets[self.selected_widget] = new_status
            self.toggle_button.config(text=f"Verslepen: {'Ja' if new_status else 'Nee'}")

    def start_copy(self, event):
        # Start kopieactie voor een widget
        original_widget = event.widget
        widget_class = original_widget.winfo_class()
        # Verhoog de teller voor het type widget en maak een unieke naam
        self.widget_counters[widget_class] += 1
        unique_name = f"{widget_class} {self.widget_counters[widget_class]}"

        # Maak een kopie van de widget voor het rechterframe
        new_widget = None
        if widget_class == "Label":
            new_widget = tk.Label(self.right_frame, text=unique_name, bg=original_widget.cget("bg"))
        elif widget_class == "Button":
            new_widget = tk.Button(self.right_frame, text=unique_name, bg=original_widget.cget("bg"))
        elif widget_class == "Entry":
            new_widget = tk.Entry(self.right_frame)
        elif widget_class == "Listbox":
            new_widget = tk.Listbox(self.right_frame)
        elif widget_class == "Checkbutton":
            new_widget = tk.Checkbutton(self.right_frame, text=unique_name)
        elif widget_class == "Radiobutton":
            new_widget = tk.Radiobutton(self.right_frame, text=unique_name)
        elif widget_class == "Scale":
            new_widget = tk.Scale(self.right_frame, from_=0, to=10)
        elif widget_class == "Text":
            new_widget = tk.Text(self.right_frame, height=3, width=20)
        elif widget_class == "Spinbox":
            new_widget = tk.Spinbox(self.right_frame, from_=0, to=10)

        # Configureer de gekopieerde widget
        if new_widget:
            new_widget.place(x=50, y=50)  # Plaats op een standaardlocatie
            new_widget.bind("<Button-1>", self.select_widget)
            new_widget.bind("<B1-Motion>", self.do_drag)
            new_widget.bind("<ButtonRelease-1>", self.stop_drag)
            new_widget.bind("<Enter>", self.show_widget_name)
            new_widget.bind("<Leave>", self.hide_widget_name)
            new_widget.bind("<Button-3>", self.start_resize)  # Rechterklik om te beginnen met het aanpassen van de grootte
            self.draggable_widgets[new_widget] = True  # Maak standaard versleepbaar
            self.copied_widgets.append(new_widget)  # Voeg de nieuwe widget toe aan de lijst

    def select_widget(self, event):
        # Selecteer de widget die aangeklikt wordt
        self.selected_widget = event.widget
        current_status = self.draggable_widgets.get(self.selected_widget, True)
        self.toggle_button.config(text=f"Verslepen: {'Ja' if current_status else 'Nee'}")
        if current_status:
            self.dragging_widget = self.selected_widget
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            # Update de invoervelden met de huidige breedte en hoogte van de widget
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, self.selected_widget.winfo_width())
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, self.selected_widget.winfo_height())

    def do_drag(self, event):
        # Verplaats de widget als deze versleept mag worden
        if self.dragging_widget and self.draggable_widgets.get(self.dragging_widget, True):
            x = self.dragging_widget.winfo_x() - self.drag_start_x + event.x
            y = self.dragging_widget.winfo_y() - self.drag_start_y + event.y
            self.dragging_widget.place(x=x, y=y)

    def stop_drag(self, event):
        # Stop het verslepen van de widget
        self.dragging_widget = None

    def start_resize(self, event):
        # Start het aanpassen van de grootte
        self.selected_widget = event.widget
        self.resizing_widget = True

    def apply_resize(self):
        # Pas de grootte van de geselecteerde widget aan
        if self.selected_widget:
            try:
                new_width = int(self.width_entry.get())
                new_height = int(self.height_entry.get())
                self.selected_widget.config(width=new_width, height=new_height)
            except ValueError:
                pass  # Negeer ongeldige invoer

    def delete_selected_widget(self):
        # Verwijder de geselecteerde widget
        if self.selected_widget:
            self.selected_widget.destroy()
            self.copied_widgets.remove(self.selected_widget)  # Verwijder uit de lijst van gekopieerde widgets
            self.selected_widget = None

    def save_as_python(self):
        # Functie om de configuratie van het rechterframe op te slaan als een Python-bestand
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("import tkinter as tk\n\n")
                file.write("root = tk.Tk()\n")
                file.write("root.geometry('800x600')\n")
                file.write("frame = tk.Frame(root, bg='red')\n")
                file.write("frame.pack(fill='both', expand=True)\n")

                for widget in self.copied_widgets:
                    widget_type = type(widget).__name__
                    widget_text = widget.cget("text") if widget_type in ["Label", "Button", "Checkbutton", "Radiobutton"] else ""
                    x, y = widget.winfo_x(), widget.winfo_y()
                    width, height = widget.winfo_width(), widget.winfo_height()

                    if widget_type == "Label":
                        file.write(f"w = tk.Label(frame, text='{widget_text}', bg='{widget.cget('bg')}')\n")
                    elif widget_type == "Button":
                        file.write(f"w = tk.Button(frame, text='{widget_text}', bg='{widget.cget('bg')}')\n")
                    elif widget_type == "Entry":
                        file.write(f"w = tk.Entry(frame)\n")
                    elif widget_type == "Listbox":
                        file.write(f"w = tk.Listbox(frame)\n")
                    elif widget_type == "Checkbutton":
                        file.write(f"w = tk.Checkbutton(frame, text='{widget_text}')\n")
                    elif widget_type == "Radiobutton":
                        file.write(f"w = tk.Radiobutton(frame, text='{widget_text}')\n")
                    elif widget_type == "Scale":
                        file.write(f"w = tk.Scale(frame, from_=0, to=10)\n")
                    elif widget_type == "Text":
                        file.write(f"w = tk.Text(frame, height=3, width=20)\n")
                    elif widget_type == "Spinbox":
                        file.write(f"w = tk.Spinbox(frame, from_=0, to=10)\n")

                    file.write(f"w.place(x={x}, y={y}, width={width}, height={height})\n")

                file.write("root.mainloop()\n")

    def show_widget_name(self, event):
        # Toon de naam of tekst van de widget als de muis eroverheen gaat
        widget = event.widget
        widget_text = widget.cget("text") if isinstance(widget, (tk.Label, tk.Button, tk.Checkbutton, tk.Radiobutton)) else str(widget)
        self.widget_name_label.config(text=f"Widget: {widget_text}")

    def hide_widget_name(self, event):
        # Verberg de naam van de widget als de muis weggaat
        self.widget_name_label.config(text="")


# Initialiseer de hoofdtoepassing
if __name__ == "__main__":
    root = tk.Tk()
    app = DragAndDropApp(root)
    root.mainloop()
