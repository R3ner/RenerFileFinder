import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import ctypes
from search_engine import search_files, open_file_explorer

LANGUAGES = {
    "English": {
        "title": "RENER FILE FINDER",
        "browse": "Browse",
        "path_placeholder": "Target Directory...",
        "keyword_placeholder": "Search keyword...",
        "deep_search": "Deep search (inside files)",
        "extensions": "Extensions (comma separated):",
        "start_btn": "START SEARCH",
        "tip": "💡 Tip: Double-click a result to open its folder location",
        "searching": "Searching... Please wait.",
        "no_results": "No matches found.",
        "error_input": "Please select a folder and enter a keyword."
    },
    "Español": {
        "title": "RENER FILE FINDER",
        "browse": "Explorar",
        "path_placeholder": "Directorio objetivo...",
        "keyword_placeholder": "Palabra clave...",
        "deep_search": "Búsqueda profunda (dentro de archivos)",
        "extensions": "Extensiones (separadas por coma):",
        "start_btn": "INICIAR BÚSQUEDA",
        "tip": "💡 Consejo: Doble clic en un resultado para abrir su carpeta",
        "searching": "Buscando... Por favor espera.",
        "no_results": "No se encontraron resultados.",
        "error_input": "Por favor selecciona una carpeta y escribe una palabra clave."
    }
}

class RenerFileFinder(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RenerFileFinder")
        self.geometry("900x720")
        
        icon_path = os.path.join("assets", "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Language Switcher
        self.lang_var = ctk.StringVar(value="English")
        self.lang_switch = ctk.CTkSegmentedButton(self, values=["English", "Español"], command=self.change_language, variable=self.lang_var)
        self.lang_switch.grid(row=0, column=0, sticky="e", padx=20, pady=(10,0))

        # Title
        self.label = ctk.CTkLabel(self, text=LANGUAGES["English"]["title"], font=("Helvetica", 24, "bold"))
        self.label.grid(row=0, column=0, pady=20)

        # Folder Frame
        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.path_entry = ctk.CTkEntry(self.folder_frame, placeholder_text=LANGUAGES["English"]["path_placeholder"], width=500)
        self.path_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        self.browse_btn = ctk.CTkButton(self.folder_frame, text=LANGUAGES["English"]["browse"], width=100, command=self.browse_folder)
        self.browse_btn.pack(side="right", padx=10)

        # Keyword Frame
        self.opt_frame = ctk.CTkFrame(self)
        self.opt_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.keyword_entry = ctk.CTkEntry(self.opt_frame, placeholder_text=LANGUAGES["English"]["keyword_placeholder"], width=350)
        self.keyword_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        self.content_var = ctk.BooleanVar(value=False)
        self.content_check = ctk.CTkCheckBox(self.opt_frame, text=LANGUAGES["English"]["deep_search"], variable=self.content_var, command=self.toggle_ext_visibility)
        self.content_check.pack(side="left", padx=20)

        # Extensions Frame
        self.ext_frame = ctk.CTkFrame(self)
        self.ext_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.ext_label = ctk.CTkLabel(self.ext_frame, text=LANGUAGES["English"]["extensions"])
        self.ext_label.pack(side="left", padx=10)
        self.ext_entry = ctk.CTkEntry(self.ext_frame, placeholder_text=".txt, .js, .json", width=300, state="disabled", fg_color="#2b2b2b")
        self.ext_entry.insert(0, ".txt, .js, .json, .py, .html")
        self.ext_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        # Search Button
        self.search_btn = ctk.CTkButton(self, text=LANGUAGES["English"]["start_btn"], font=("Helvetica", 14, "bold"), fg_color="#2ecc71", hover_color="#27ae60", height=40, command=self.run_search)
        self.search_btn.grid(row=4, column=0, pady=15)

        # Results
        self.results_box = ctk.CTkTextbox(self, font=("Consolas", 12), cursor="hand2")
        self.results_box.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
        self.results_box.bind("<Double-Button-1>", self.on_double_click)

        # Footer
        self.info_label = ctk.CTkLabel(self, text=LANGUAGES["English"]["tip"], font=("Helvetica", 11, "italic"), text_color="gray")
        self.info_label.grid(row=6, column=0, pady=(0, 10))

    def change_language(self, lang):
        texts = LANGUAGES[lang]
        self.label.configure(text=texts["title"])
        self.browse_btn.configure(text=texts["browse"])
        self.path_entry.configure(placeholder_text=texts["path_placeholder"])
        self.keyword_entry.configure(placeholder_text=texts["keyword_placeholder"])
        self.content_check.configure(text=texts["deep_search"])
        self.ext_label.configure(text=texts["extensions"])
        self.search_btn.configure(text=texts["start_btn"])
        self.info_label.configure(text=texts["tip"])

    def toggle_ext_visibility(self):
        if self.content_var.get():
            self.ext_entry.configure(state="normal", fg_color="#343638")
        else:
            self.ext_entry.configure(state="disabled", fg_color="#2b2b2b")

    def on_double_click(self, event):
        line_content = self.results_box.get("insert linestart", "insert lineend").strip()
        if line_content and os.path.exists(line_content):
            open_file_explorer(line_content)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def run_search(self):
        lang = self.lang_var.get()
        folder = self.path_entry.get()
        keyword = self.keyword_entry.get()
        ext_list = [e.strip() for e in self.ext_entry.get().split(",") if e.strip()]

        if not folder or not keyword:
            messagebox.showwarning("Error", LANGUAGES[lang]["error_input"])
            return

        self.results_box.delete("1.0", "end")
        self.results_box.insert("end", LANGUAGES[lang]["searching"] + "\n")
        self.update_idletasks()
        
        results = search_files(folder, keyword, self.content_var.get(), ext_list)
        
        self.results_box.delete("1.0", "end")
        if results:
            for path in results:
                self.results_box.insert("end", f"{path}\n")
        else:
            self.results_box.insert("end", LANGUAGES[lang]["no_results"])

if __name__ == "__main__":
    try:
        myappid = u'rener.filefinder.v1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass
    app = RenerFileFinder()
    app.mainloop()
