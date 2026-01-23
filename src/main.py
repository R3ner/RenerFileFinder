import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import ctypes
from search_engine import search_files, open_file_explorer

class RenerFileFinder(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW CONFIGURATION ---
        self.title("RenerFileFinder")
        self.geometry("900x700")
        
        # Load Icon safely
        icon_path = os.path.join("assets", "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1) # Results box expands

        # 1. Title
        self.label = ctk.CTkLabel(self, text="RENER FILE FINDER", font=("Helvetica", 24, "bold"))
        self.label.grid(row=0, column=0, pady=(20, 10))

        # 2. Folder Selection Frame
        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.path_entry = ctk.CTkEntry(self.folder_frame, placeholder_text="Target Directory...", width=500)
        self.path_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.browse_btn = ctk.CTkButton(self.folder_frame, text="Browse", width=100, command=self.browse_folder)
        self.browse_btn.pack(side="right", padx=10)

        # 3. Keyword & Deep Search Frame
        self.opt_frame = ctk.CTkFrame(self)
        self.opt_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.keyword_entry = ctk.CTkEntry(self.opt_frame, placeholder_text="Search keyword (filename or content)...", width=350)
        self.keyword_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        self.content_var = ctk.BooleanVar(value=False)
        self.content_check = ctk.CTkCheckBox(self.opt_frame, text="Deep search (inside files)", variable=self.content_var, command=self.toggle_ext_visibility)
        self.content_check.pack(side="left", padx=20)

        # 4. Custom Extensions Frame (Only useful for Deep Search)
        self.ext_frame = ctk.CTkFrame(self)
        self.ext_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.ext_label = ctk.CTkLabel(self.ext_frame, text="Extensions (comma separated):", font=("Helvetica", 12))
        self.ext_label.pack(side="left", padx=10)
        
        self.ext_entry = ctk.CTkEntry(self.ext_frame, placeholder_text=".txt, .js, .json, .py, .html", width=300)
        self.ext_entry.insert(0, ".txt, .js, .json, .py, .html") # Default values
        self.ext_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        # 5. Search Button
        self.search_btn = ctk.CTkButton(self, text="START SEARCH", font=("Helvetica", 14, "bold"), fg_color="#2ecc71", hover_color="#27ae60", height=40, command=self.run_search)
        self.search_btn.grid(row=4, column=0, pady=15)

        # 6. Results Area
        self.results_box = ctk.CTkTextbox(self, font=("Consolas", 12), cursor="hand2")
        self.results_box.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
        
        # Double click binding
        self.results_box.bind("<Double-Button-1>", self.on_double_click)

        # 7. Footer Info
        self.info_label = ctk.CTkLabel(self, text="💡 Tip: Double-click a result to open its folder location", font=("Helvetica", 11, "italic"), text_color="gray")
        self.info_label.grid(row=6, column=0, pady=(0, 10))

    def toggle_ext_visibility(self):
        """Visual hint: Disable extension entry if deep search is off."""
        if self.content_var.get():
            self.ext_entry.configure(state="normal", fg_color="#343638")
        else:
            self.ext_entry.configure(state="disabled", fg_color="#2b2b2b")

    def on_double_click(self, event):
        """Extract path from the clicked line and open it."""
        line_content = self.results_box.get("insert linestart", "insert lineend").strip()
        if line_content and os.path.exists(line_content):
            open_file_explorer(line_content)
        elif line_content:
            messagebox.showerror("Error", f"Path not found: {line_content}")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def run_search(self):
        folder = self.path_entry.get()
        keyword = self.keyword_entry.get()
        
        # Get extensions from entry
        ext_list = [e.strip() for e in self.ext_entry.get().split(",") if e.strip()]

        if not folder or not keyword:
            messagebox.showwarning("Input Error", "Please select a folder and enter a keyword.")
            return

        self.results_box.delete("1.0", "end")
        self.results_box.insert("end", "Searching... Please wait.\n")
        self.update_idletasks() # Refresh UI to show the message
        
        results = search_files(folder, keyword, self.content_var.get(), ext_list)
        
        self.results_box.delete("1.0", "end")
        if results:
            for path in results:
                self.results_box.insert("end", f"{path}\n")
        else:
            self.results_box.insert("end", "No matches found.")

if __name__ == "__main__":
    # --- ESTO ES LO QUE SOLUCIONA EL ICONO DE LA TASKBAR ---
    try:
        # Importamos ctypes solo aquí para no ensuciar el resto del código
        import ctypes
        # Creamos un ID único para tu aplicación
        myappid = u'rener.filefinder.v1' 
        # Le decimos a Windows: "No soy Python, soy RenerFileFinder"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        print(f"No se pudo establecer el ID de la aplicación: {e}")

    app = RenerFileFinder()
    app.mainloop()