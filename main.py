import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
from report_generator import ReportGenerator
from checklist_data import CHECKLIST_CATEGORIES

class GyrocompassChecklistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gyrocompass Overhaul Checklist")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.checklist_items = {}
        self.technician_name = tk.StringVar()
        self.equipment_id = tk.StringVar()
        self.start_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.notes = {}
        
        self.setup_ui()
        self.load_checklist_structure()
        
    def setup_ui(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Gyrocompass Overhaul Checklist", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        info_frame = ttk.LabelFrame(self.root, text="Maintenance Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text="Technician Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(info_frame, textvariable=self.technician_name, width=30).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(info_frame, text="Equipment ID:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(info_frame, textvariable=self.equipment_id, width=30).grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        
        ttk.Label(info_frame, text="Start Date:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(info_frame, textvariable=self.start_date, width=30).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(3, weight=1)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save Checklist", command=self.save_checklist).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Checklist", command=self.load_checklist).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate Report", command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset All", command=self.reset_checklist).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
    def load_checklist_structure(self):
        self.category_frames = {}
        self.category_items = {}
        
        for category_name, items in CHECKLIST_CATEGORIES.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=category_name)
            
            canvas = tk.Canvas(frame, bg="white")
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            self.category_items[category_name] = []
            
            for item_name in items:
                item_frame = ttk.Frame(scrollable_frame)
                item_frame.pack(fill=tk.X, padx=10, pady=5)
                
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(item_frame, text=item_name, variable=var)
                checkbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
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
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if not file_path:
            return
        
        data = {
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
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
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
        if not self.technician_name.get():
            messagebox.showwarning("Warning", "Please enter technician name!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"gyrocompass_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if not file_path:
            return
        
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
                start_date=self.start_date.get(),
                checklist_data=checklist_data
            )
            messagebox.showinfo("Success", f"Report generated:\n{file_path}")
        except ImportError:
            messagebox.showerror("Error", "reportlab not installed.\nInstall with: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")
    
    def reset_checklist(self):
        if messagebox.askyesno("Confirm", "Reset all items? This cannot be undone."):
            for category_items in self.category_items.values():
                for item in category_items:
                    item['var'].set(False)
                    item['notes_var'].set('')

def main():
    root = tk.Tk()
    app = GyrocompassChecklistApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()