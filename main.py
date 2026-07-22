import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
from report_generator import ReportGenerator
from checklist_data import CHECKLIST_CATEGORIES, GYRO_MODELS, MODEL_NOTES

class ModelSelectionWindow:
    def __init__(self, root, on_model_selected):
        self.root = root
        self.root.title("Gyrocompass Model Selection")
        self.root.geometry("550x500")
        self.root.resizable(False, False)
        self.root.grab_set()
        
        self.on_model_selected = on_model_selected
        self.selected_model = None
        self.models_list = list(GYRO_MODELS.keys())
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create model selection interface"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Label(header_frame, text="Select Gyrocompass Model", 
                 font=("Arial", 16, "bold")).pack()
        ttk.Label(header_frame, text="Choose your gyrocompass model to load the appropriate checklist",
                 font=("Arial", 10)).pack()
        
        # Model selection frame
        selection_frame = ttk.LabelFrame(self.root, text="Available Models", padding=15)
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(selection_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.model_listbox = tk.Listbox(selection_frame, yscrollcommand=scrollbar.set, 
                                        font=("Arial", 12), height=10, width=40)
        self.model_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.model_listbox.yview)
        
        # Populate listbox
        for model in self.models_list:
            self.model_listbox.insert(tk.END, model)
        
        # Bind selection event to show details
        self.model_listbox.bind('<<ListboxSelect>>', self.on_model_select)
        self.model_listbox.bind('<Double-Button-1>', lambda e: self.continue_with_model())
        
        # Details frame
        details_frame = ttk.LabelFrame(self.root, text="Model Details", padding=10)
        details_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.details_text = tk.Text(details_frame, height=5, width=50, 
                                    font=("Arial", 9), wrap=tk.WORD, relief=tk.FLAT)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.config(state=tk.DISABLED)
        
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="Continue", 
                  command=self.continue_with_model, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit, width=15).pack(side=tk.RIGHT, padx=5)
        
        # Select first model by default and show its details
        if len(self.models_list) > 0:
            self.model_listbox.selection_set(0)
            self.on_model_select(None)
        
    def on_model_select(self, event):
        """Display model details when selected"""
        selection = self.model_listbox.curselection()
        if not selection:
            return
        
        model_name = self.models_list[selection[0]]
        model_info = GYRO_MODELS[model_name]
        
        # Update details text
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete('1.0', tk.END)
        
        details = f"""Model: {model_name}
Manufacturer: {model_info['manufacturer']}
Type: {model_info['type']}
Description: {model_info['description']}

Notes: {MODEL_NOTES.get(model_name, 'No specific notes')}
"""
        self.details_text.insert('1.0', details)
        self.details_text.config(state=tk.DISABLED)
        
    def continue_with_model(self):
        """Get selected model and continue"""
        selection = self.model_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a gyrocompass model")
            return
        
        self.selected_model = self.models_list[selection[0]]
        self.on_model_selected(self.selected_model)
        self.root.destroy()

class GyrocompassChecklistApp:
    def __init__(self, root, model_name):
        self.root = root
        self.root.title(f"Gyrocompass Overhaul Checklist - {model_name}")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        self.model_name = model_name
        self.model_info = GYRO_MODELS.get(model_name, {})
        
        # Data storage
        self.checklist_items = {}
        self.technician_name = tk.StringVar()
        self.equipment_id = tk.StringVar()
        self.start_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.notes = {}
        
        self.setup_ui()
        self.load_checklist_structure()
        
    def setup_ui(self):
        """Create the main UI layout"""
        # Header Frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_text = f"Gyrocompass Overhaul Checklist - {self.model_name}"
        ttk.Label(header_frame, text=title_text, 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        model_details = f"{self.model_info.get('manufacturer')} | {self.model_info.get('type')}"
        ttk.Label(header_frame, text=model_details, 
                 font=("Arial", 10), foreground="gray").pack(side=tk.LEFT, padx=20)
        
        # Info Frame
        info_frame = ttk.LabelFrame(self.root, text="Maintenance Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text="Technician Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(info_frame, textvariable=self.technician_name, width=25).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(info_frame, text="Equipment ID:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(info_frame, textvariable=self.equipment_id, width=25).grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        
        ttk.Label(info_frame, text="Start Date:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(info_frame, textvariable=self.start_date, width=25).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(info_frame, text="Gyro Model:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(info_frame, text=self.model_name, 
                 font=("Arial", 10, "bold")).grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(3, weight=1)
        
        # Checklist Frame with Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save Checklist", command=self.save_checklist).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Checklist", command=self.load_checklist).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate Report", command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset All", command=self.reset_checklist).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Select Model", command=self.select_model).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
    def load_checklist_structure(self):
        """Load checklist categories into notebook tabs"""
        self.category_frames = {}
        self.category_items = {}
        
        for category_name, items in CHECKLIST_CATEGORIES.items():
            # Create a frame for each category
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=category_name)
            
            # Create scrollable area
            canvas = tk.Canvas(frame, bg="white")
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add items to scrollable frame
            self.category_items[category_name] = []
            
            for item_name in items:
                item_frame = ttk.Frame(scrollable_frame)
                item_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Checkbox
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(item_frame, text=item_name, variable=var)
                checkbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # Notes entry
                notes_var = tk.StringVar()
                notes_entry = ttk.Entry(item_frame, textvariable=notes_var, width=30)
                notes_entry.pack(side=tk.RIGHT, padx=5)
                
                self.category_items[category_name].append({
                    'name': item_name,
                    'var': var,
                    'notes_var': notes_var,
                    'widget': checkbox
                })
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            self.category_frames[category_name] = scrollable_frame
    
    def save_checklist(self):
        """Save checklist data to JSON file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"checklist_{self.model_name.replace(' ', '_').replace('/', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if not file_path:
            return
        
        data = {
            'model': self.model_name,
            'manufacturer': self.model_info.get('manufacturer'),
            'technician': self.technician_name.get(),
            'equipment_id': self.equipment_id.get(),
            'start_date': self.start_date.get(),
            'completion_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'categories': {}
        }
        
        for category_name, items in self.category_items.items():
            data['categories'][category_name] = []
            for item in items:
                data['categories'][category_name].append({
                    'name': item['name'],
                    'completed': item['var'].get(),
                    'notes': item['notes_var'].get()
                })
        
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Success", f"Checklist saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save checklist:\n{str(e)}")
    
    def load_checklist(self):
        """Load checklist data from JSON file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Warn if different model
            if data.get('model') != self.model_name:
                response = messagebox.askyesno(
                    "Model Mismatch",
                    f"This checklist is for {data.get('model')} but you're using {self.model_name}.\nContinue loading anyway?"
                )
                if not response:
                    return
            
            self.technician_name.set(data.get('technician', ''))
            self.equipment_id.set(data.get('equipment_id', ''))
            self.start_date.set(data.get('start_date', datetime.now().strftime("%Y-%m-%d")))
            
            for category_name, items in data.get('categories', {}).items():
                if category_name in self.category_items:
                    for i, saved_item in enumerate(items):
                        if i < len(self.category_items[category_name]):
                            self.category_items[category_name][i]['var'].set(saved_item.get('completed', False))
                            self.category_items[category_name][i]['notes_var'].set(saved_item.get('notes', ''))
            
            messagebox.showinfo("Success", "Checklist loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load checklist:\n{str(e)}")
    
    def generate_report(self):
        """Generate PDF report"""
        if not self.technician_name.get():
            messagebox.showwarning("Warning", "Please enter technician name!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"gyrocompass_report_{self.model_name.replace(' ', '_').replace('/', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if not file_path:
            return
        
        # Compile checklist data
        checklist_data = {}
        for category_name, items in self.category_items.items():
            checklist_data[category_name] = []
            for item in items:
                checklist_data[category_name].append({
                    'name': item['name'],
                    'completed': item['var'].get(),
                    'notes': item['notes_var'].get()
                })
        
        try:
            report_gen = ReportGenerator()
            report_gen.generate(
                file_path=file_path,
                technician=self.technician_name.get(),
                equipment_id=self.equipment_id.get(),
                model=self.model_name,
                manufacturer=self.model_info.get('manufacturer'),
                start_date=self.start_date.get(),
                checklist_data=checklist_data
            )
            messagebox.showinfo("Success", f"Report generated:\n{file_path}")
        except ImportError:
            messagebox.showerror("Error", "reportlab not installed.\nInstall with: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")
    
    def reset_checklist(self):
        """Reset all checkboxes and notes"""
        if messagebox.askyesno("Confirm", "Reset all items? This cannot be undone."):
            for category_items in self.category_items.values():
                for item in category_items:
                    item['var'].set(False)
                    item['notes_var'].set('')
    
    def select_model(self):
        """Open model selection window"""
        response = messagebox.askyesno("Switch Model", 
                                       "This will close the current checklist. Continue?")
        if response:
            self.root.destroy()
            main()

def main():
    # First window: Model Selection
    model_root = tk.Tk()
    model_selection = ModelSelectionWindow(model_root, on_model_selected)
    model_root.mainloop()

def on_model_selected(model_name):
    """Callback when model is selected"""
    # Open main application with selected model
    main_root = tk.Tk()
    app = GyrocompassChecklistApp(main_root, model_name)
    main_root.mainloop()

if __name__ == "__main__":
    main()
