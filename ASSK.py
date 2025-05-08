import tkinter as tk
from tkinter import ttk, messagebox, font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class KalkulatorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Augstuma starpības un slīpuma kalkulators")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        
        # Sagatavotie datu piemēri
        self.sample_data = {
            "Kalnu taka": {"start_height": 850, "end_height": 1200, "distance": 1500},
            "Pludmales ceļš": {"start_height": 1, "end_height": 15, "distance": 300},
            "Pilsētas iela": {"start_height": 120, "end_height": 135, "distance": 500},
            "Dzelzceļa posms": {"start_height": 200, "end_height": 180, "distance": 2000},
            "Kāpu reljefs": {"start_height": 5, "end_height": 30, "distance": 90}
        }
          # Tēmas iestatījumi
        self.themes = {
            "Standarta": {
                "bg": "#f0f0f0", 
                "fg": "#000000", 
                "accent": "#4CAF50", 
                "button_bg": "#e0e0e0", 
                "frame_bg": "#f5f5f5",
                "button_relief": tk.RAISED,
                "button_border": 2,
                "graph_color": "#4CAF50", 
                "point_colors": ["#d32f2f", "#388e3c", "#1976d2", "#ff5722", "#9c27b0", "#ff9800"]
            }
        }
        
        # Grafika un pogu dizaina iestatījumi
        self.graph_styles = {
            "Standarta": {"grid": True, "line_width": 2, "marker_size": 8, "fill_alpha": 0.15},
            "Minimāls": {"grid": False, "line_width": 1.5, "marker_size": 6, "fill_alpha": 0.1},
            "Tievāks": {"grid": True, "line_width": 0.5, "marker_size": 2, "fill_alpha": 0.25}
        }
        
        self.button_styles = {
            "Standarta": {"relief": tk.RAISED, "borderwidth": 2},
            "Plakans": {"relief": tk.FLAT, "borderwidth": 0},
            "Izcelts": {"relief": tk.GROOVE, "borderwidth": 8}
        }
          # Noklusējuma iestatījumu vērtības
        self.current_theme = "Standarta"
        self.current_graph_style = "Standarta"
        self.current_button_style = "Standarta"
        self.animation_enabled = True
        
        # Mainīgie saglabāto, bet vēl nepiemēroto iestatījumu vērtībām
        self.selected_graph_style = self.current_graph_style
        self.selected_button_style = self.current_button_style
        self.selected_animation = self.animation_enabled
        
        # Mainīgie papildus punktu ievadīšanai
        self.additional_points = []
        
        # Sākuma lapa
        self.show_start_page()
        
    def show_start_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
   
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
   
        title_font = font.Font(family="Arial", size=24, weight="bold")
        button_font = font.Font(family="Arial", size=12)
    
        title_frame = tk.Frame(self.root, bg=theme["bg"])
        title_frame.pack(pady=(50, 10))
        
        title_label = tk.Label(title_frame, text="Augstuma starpības un\nslīpuma kalkulators", 
                               font=title_font, bg=theme["bg"], fg=theme["fg"])
        title_label.pack()
       
        logo_canvas = tk.Canvas(self.root, width=120, height=80, bg=theme["bg"], highlightthickness=0)
        logo_canvas.pack(pady=10)
     
        logo_canvas.create_polygon(20, 60, 45, 20, 60, 40, 80, 10, 100, 60, fill=theme["accent"], outline="")
     
        if self.animation_enabled:
            def animate_logo():
                for i in range(10):
                    logo_canvas.create_line(20+i*9, 60, 20+i*9, 55, fill="white", width=1)
                    self.root.update()
                    self.root.after(50)
            self.root.after(500, animate_logo)
  
        button_frame = tk.Frame(self.root, bg=theme["bg"])
        button_frame.pack(pady=20)
 
        button_style_dict = self.button_styles[self.current_button_style]
        
        # Standarta pogu stili
        button_style = {"font": button_font, "width": 20, "height": 2, 
                       "bg": theme["button_bg"], "fg": theme["fg"], 
                       "activebackground": theme["accent"], "activeforeground": "white",
                       "relief": button_style_dict["relief"], 
                       "borderwidth": button_style_dict["borderwidth"]}
        
        start_button = tk.Button(button_frame, text="Sākt", command=self.show_calculator, **button_style)
        start_button.pack(pady=10)
        
        settings_button = tk.Button(button_frame, text="Iestatījumi", command=self.show_settings, **button_style)
        settings_button.pack(pady=10)
        
        info_button = tk.Button(button_frame, text="Info", command=self.show_info, **button_style)
        info_button.pack(pady=10)
        
        exit_button = tk.Button(button_frame, text="Izslēgt", command=self.root.quit, **button_style)
        exit_button.pack(pady=10)
   
        author_frame = tk.Frame(self.root, bg=theme["bg"])
        author_frame.pack(side=tk.BOTTOM, pady=20)
        
        author_label = tk.Label(author_frame, text="Laura Līva Kasparinska", 
                              font=font.Font(family="Arial", size=9),
                              bg=theme["bg"], fg=theme["fg"])
        author_label.pack()
    
    def show_settings(self):
        for widget in self.root.winfo_children():
            widget.destroy()
      
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
   
        title_font = font.Font(family="Arial", size=18, weight="bold")
        text_font = font.Font(family="Arial", size=12)
        small_font = font.Font(family="Arial", size=10)
   
        title_label = tk.Label(self.root, text="Iestatījumi", font=title_font, bg=theme["bg"], fg=theme["fg"])
        title_label.pack(pady=(20, 15))
  
        settings_frame = tk.Frame(self.root, bg=theme["frame_bg"], bd=2, relief=tk.GROOVE)
        settings_frame.pack(padx=50, pady=10, fill=tk.BOTH, expand=True)
      
        tabs_frame = tk.Frame(settings_frame, bg=theme["frame_bg"])
        tabs_frame.pack(fill=tk.X, padx=5, pady=5)
      
        active_tab_style = {"bg": theme["accent"], "fg": "white", "relief": tk.RAISED, "borderwidth": 1, "padx": 15, "pady": 5}
        if self.current_theme == "Tumšā":
            inactive_tab_style = {"bg": "#444444", "fg": "#878484", "relief": tk.FLAT, "borderwidth": 1, "padx": 15, "pady": 5}
        else:
            inactive_tab_style = {"bg": "#e0e0e0", "fg": "#333333", "relief": tk.FLAT, "borderwidth": 1, "padx": 15, "pady": 5}
 
        self.current_tab = tk.StringVar(value="grafiks")
        
        graph_tab_btn = tk.Button(tabs_frame, text="Grafiks", font=text_font, command=lambda: self.switch_settings_tab("grafiks"), **active_tab_style)
        graph_tab_btn.pack(side=tk.LEFT, padx=2, pady=5)
        
        button_tab_btn = tk.Button(tabs_frame, text="Pogas", font=text_font, command=lambda: self.switch_settings_tab("pogas"), **inactive_tab_style)
        button_tab_btn.pack(side=tk.LEFT, padx=2, pady=5)
        
        anim_tab_btn = tk.Button(tabs_frame, text="Animācijas", font=text_font, command=lambda: self.switch_settings_tab("animācijas"), **inactive_tab_style)
        anim_tab_btn.pack(side=tk.LEFT, padx=2, pady=5)
        
        # Saglabājam atsauces uz cilņu pogām
        self.tab_buttons = {
            "grafiks": graph_tab_btn,
            "pogas": button_tab_btn,
            "animācijas": anim_tab_btn
        }
        separator = ttk.Separator(settings_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=5)
     
        self.content_frame = tk.Frame(settings_frame, bg=theme["frame_bg"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.show_graph_settings()
        
    def switch_settings_tab(self, tab_name):
        """Pārslēdz cilni iestatījumos"""
        theme = self.themes[self.current_theme]

        inactive_tab_style = {"bg": theme["button_bg"], "fg": theme["fg"], 
                             "relief": tk.FLAT, "borderwidth": 1}
        active_tab_style = {"bg": theme["accent"], "fg": "white", 
                           "relief": tk.RAISED, "borderwidth": 2}
        
        for tab, btn in self.tab_buttons.items():
            if tab == tab_name:
                btn.configure(**active_tab_style)
            else:
                btn.configure(**inactive_tab_style)

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if tab_name == "grafiks":
            self.show_graph_settings()
        elif tab_name == "pogas":
            self.show_button_settings()
        elif tab_name == "animācijas":
            self.show_animation_settings()
        
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.current_tab = tab_name    
        
    def show_graph_settings(self):
        """Parāda grafika iestatījumus"""
        theme = self.themes[self.current_theme]
        text_font = font.Font(family="Arial", size=12)
        small_font = font.Font(family="Arial", size=10)
   
        graph_label = tk.Label(self.content_frame, text="Grafika stils:", font=text_font, 
                             bg=theme["frame_bg"], fg=theme["fg"])
        graph_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        graph_desc = tk.Label(self.content_frame, text="Izvēlieties, kā izskatīsies grafiskie elementi:", 
                           font=small_font, bg=theme["frame_bg"], fg=theme["fg"])
        graph_desc.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        self.graph_style_var = tk.StringVar(value=self.current_graph_style)

        graph_styles_container = tk.Frame(self.content_frame, bg=theme["frame_bg"])
        graph_styles_container.pack(fill=tk.X, padx=10, pady=10)

        for i, style_name in enumerate(self.graph_styles.keys()):
            graph_style = self.graph_styles[style_name]
            
            style_frame = tk.Frame(graph_styles_container, bg=theme["frame_bg"], bd=2, 
                                relief=tk.RIDGE if style_name == self.current_graph_style else tk.FLAT,
                                width=180, height=100)  
            style_frame.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            style_frame.grid_propagate(False) 
      
            rb = tk.Radiobutton(style_frame, text=style_name, variable=self.graph_style_var, 
                             value=style_name, bg=theme["frame_bg"], fg=theme["accent"],
                             selectcolor=theme["frame_bg"], font=small_font)
            rb.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
 
            params_frame = tk.Frame(style_frame, bg=theme["frame_bg"])
            params_frame.grid(row=1, column=0, padx=10, pady=2, sticky=tk.W)
          
            line_canvas = tk.Canvas(params_frame, width=80, height=10, bg=theme["frame_bg"], 
                                 highlightthickness=0)
            line_canvas.grid(row=0, column=0, sticky=tk.W)
            line_canvas.create_line(0, 5, 80, 5, fill=theme["accent"], 
                                  width=graph_style["line_width"])
            
            line_label = tk.Label(params_frame, text=f"Līnija: {graph_style['line_width']}px", 
                               font=("Arial", 8), bg=theme["frame_bg"], fg=theme["fg"])
            line_label.grid(row=0, column=1, padx=5, sticky=tk.W)
      
            grid_text = "Režģis: ✓" if graph_style["grid"] else "Režģis: ✗"
            grid_label = tk.Label(params_frame, text=grid_text, font=("Arial", 8),
                              bg=theme["frame_bg"], fg=theme["fg"])
            grid_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)
       
        spacer = tk.Frame(self.content_frame, height=20, bg=theme["frame_bg"])
        spacer.pack(fill=tk.X)

        btn_container = tk.Frame(self.content_frame, bg=theme["frame_bg"])
        btn_container.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
       
        right_btn_frame = tk.Frame(btn_container, bg=theme["frame_bg"])
        right_btn_frame.pack(side=tk.RIGHT)
   
        apply_btn = tk.Button(right_btn_frame, text="Saglabāt", 
                               bg=theme["accent"], fg="white", 
                               command=lambda: self.apply_specific_setting("graph"),
                               font=small_font, padx=15, pady=5)
        apply_btn.pack(side=tk.RIGHT, padx=5)
        
        back_btn = tk.Button(right_btn_frame, text="Atpakaļ", 
                         bg=theme["button_bg"], fg=theme["fg"], 
                         command=self.show_start_page,
                         font=small_font, padx=15, pady=5)
        back_btn.pack(side=tk.RIGHT, padx=5)
     
        self.buttons_frame = btn_container
    
    def show_button_settings(self):
        """Parāda pogu dizaina iestatījumus"""
        theme = self.themes[self.current_theme]
        text_font = font.Font(family="Arial", size=12)
        small_font = font.Font(family="Arial", size=10)
   
        button_label = tk.Label(self.content_frame, text="Pogu stils:", font=text_font, 
                              bg=theme["frame_bg"], fg=theme["fg"])
        button_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        button_desc = tk.Label(self.content_frame, text="Izvēlieties, kā izskatīsies pogas:", 
                            font=small_font, bg=theme["frame_bg"], fg=theme["fg"])
        button_desc.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        self.button_style_var = tk.StringVar(value=self.current_button_style)
    
        button_styles_container = tk.Frame(self.content_frame, bg=theme["frame_bg"])
        button_styles_container.pack(fill=tk.X, padx=10, pady=10)
   
        for i, style_name in enumerate(self.button_styles.keys()):
            button_style = self.button_styles[style_name]
            
            style_frame = tk.Frame(button_styles_container, bg=theme["frame_bg"], bd=2, 
                                 relief=tk.RIDGE if style_name == self.current_button_style else tk.FLAT,
                                 width=180, height=80) 
            style_frame.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            style_frame.grid_propagate(False) 
        
            rb = tk.Radiobutton(style_frame, text=style_name, variable=self.button_style_var, 
                             value=style_name, bg=theme["frame_bg"], fg=theme["accent"],
                             selectcolor=theme["frame_bg"], font=small_font)
            rb.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
      
            params_frame = tk.Frame(style_frame, bg=theme["frame_bg"])
            params_frame.grid(row=1, column=0, padx=10, pady=2, sticky=tk.W)
      
            relief_text = f"Reljefs: {button_style['relief']}"
            border_text = f"Apmale: {button_style['borderwidth']}px"
            
            relief_label = tk.Label(params_frame, text=relief_text, font=("Arial", 8),
                                 bg=theme["frame_bg"], fg=theme["fg"])
            relief_label.grid(row=0, column=0, sticky=tk.W)
            
            border_label = tk.Label(params_frame, text=border_text, font=("Arial", 8),
                                 bg=theme["frame_bg"], fg=theme["fg"])
            border_label.grid(row=1, column=0, sticky=tk.W)
     
            sample_btn = tk.Button(params_frame, text="Paraugs", 
                                relief=button_style["relief"], 
                                borderwidth=button_style["borderwidth"],
                                bg=theme["button_bg"], fg=theme["fg"],
                                width=8, height=1, font=("Arial", 8))
            sample_btn.grid(row=0, column=1, rowspan=2, padx=10, sticky=tk.E)
   
        spacer = tk.Frame(self.content_frame, height=20, bg=theme["frame_bg"])
        spacer.pack(fill=tk.X)
 
        btn_container = tk.Frame(self.content_frame, bg=theme["frame_bg"])
        btn_container.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
  
        right_btn_frame = tk.Frame(btn_container, bg=theme["frame_bg"])
        right_btn_frame.pack(side=tk.RIGHT)
 
        apply_btn = tk.Button(right_btn_frame, text="Saglabāt", 
                               bg=theme["accent"], fg="white", 
                               command=lambda: self.apply_specific_setting("button"),
                               font=small_font, padx=15, pady=5)
        apply_btn.pack(side=tk.RIGHT, padx=5)
        
        back_btn = tk.Button(right_btn_frame, text="Atpakaļ", 
                         bg=theme["button_bg"], fg=theme["fg"], 
                         command=self.show_start_page,
                         font=small_font, padx=15, pady=5)
        back_btn.pack(side=tk.RIGHT, padx=5)
       
        self.buttons_frame = btn_container
    
    def show_animation_settings(self):
        """Parāda animāciju iestatījumus"""
        theme = self.themes[self.current_theme]
        text_font = font.Font(family="Arial", size=12)
        small_font = font.Font(family="Arial", size=10)
    
        anim_label = tk.Label(self.content_frame, text="Animācijas:", font=text_font, 
                        bg=theme["frame_bg"], fg=theme["fg"])
        anim_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
      
        anim_desc = tk.Label(self.content_frame, text="Ieslēdziet vai izslēdziet animācijas efektus:", 
                        font=small_font, bg=theme["frame_bg"], fg=theme["fg"])
        anim_desc.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        self.animation_var = tk.BooleanVar(value=self.animation_enabled)
        
      
        anim_options_frame = tk.Frame(self.content_frame, bg=theme["frame_bg"])
        anim_options_frame.pack(fill=tk.X, padx=20, pady=10)
        
       
        anim_check = tk.Checkbutton(anim_options_frame, text="Ieslēgt animācijas", variable=self.animation_var,
                                bg=theme["frame_bg"], fg=theme["fg"], font=small_font,
                                selectcolor=theme["frame_bg"], activebackground=theme["frame_bg"])
        anim_check.pack(anchor=tk.W, pady=5)
  
        anim_note = tk.Label(anim_options_frame, text="Animācijas padara kalnu siluetu zīmēšanu plūstošāku", 
                        font=("Arial", 8), bg=theme["frame_bg"], fg=theme["fg"])
        anim_note.pack(anchor=tk.W, pady=(0, 10))
    
        spacer = tk.Frame(self.content_frame, height=20, bg=theme["frame_bg"])
        spacer.pack(fill=tk.X)
  
        btn_container = tk.Frame(self.content_frame, bg=theme["frame_bg"])
        btn_container.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    
        right_btn_frame = tk.Frame(btn_container, bg=theme["frame_bg"])
        right_btn_frame.pack(side=tk.RIGHT)
 
        apply_btn = tk.Button(right_btn_frame, text="Saglabāt", 
                               bg=theme["accent"], fg="white", 
                               command=lambda: self.apply_specific_setting("animation"),
                               font=small_font, padx=15, pady=5)
        apply_btn.pack(side=tk.RIGHT, padx=5)
        
        back_btn = tk.Button(right_btn_frame, text="Atpakaļ", 
                         bg=theme["button_bg"], fg=theme["fg"], 
                         command=self.show_start_page,
                         font=small_font, padx=15, pady=5)
        back_btn.pack(side=tk.RIGHT, padx=5)
        
        # Saglabājam atsauci uz pogu konteineri
        self.buttons_frame = btn_container    
        
    def apply_settings(self):
        """Piemēro visus iestatītus iestatījumus"""
        # Saglabā iepriekšējās vērtības, lai varētu noteikt, kas mainījās
        prev_graph_style = self.current_graph_style
        prev_button_style = self.current_button_style
        prev_animation = self.animation_enabled
        
        # Saglabā jaunos iestatījumus
        self.current_graph_style = self.graph_style_var.get()
        self.current_button_style = self.button_style_var.get()
        self.animation_enabled = self.animation_var.get()
        
        # Parāda paziņojumu ar informāciju par mainītajiem iestatījumiem
        changes = []
        if prev_graph_style != self.current_graph_style:
            changes.append(f"- Grafika stils: {self.current_graph_style}")
        if prev_button_style != self.current_button_style:
            changes.append(f"- Pogu stils: {self.current_button_style}")
        if prev_animation != self.animation_enabled:
            animation_status = "Ieslēgtas" if self.animation_enabled else "Izslēgtas"
            changes.append(f"- Animācijas: {animation_status}")
        
        if changes:
            message = "Iestatījumi veiksmīgi piemēroti!\n\n" + "\n".join(changes)
        else:
            message = "Iestatījumi veiksmīgi saglabāti!"
            
        messagebox.showinfo("Iestatījumi", message)
        
        # Atgriezties uz sākuma lapu ar jaunajiem iestatījumiem
        self.show_start_page()
    
    def show_info(self):
        # Notīrīt esošos widgetus
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Piemērot tēmu
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        
        # Stila iestatījumi
        title_font = font.Font(family="Arial", size=18, weight="bold")
        text_font = font.Font(family="Arial", size=12)
        
        # Virsraksts
        title_frame = tk.Frame(self.root, bg=theme["bg"])
        title_frame.pack(pady=(30, 20))
        
        title_label = tk.Label(title_frame, text="Par programmu", font=title_font, bg=theme["bg"], fg=theme["fg"])
        title_label.pack()
        
        # Informācijas konteiners
        info_frame = tk.Frame(self.root, bg=theme["frame_bg"], bd=2, relief=tk.GROOVE)
        info_frame.pack(padx=50, pady=20, fill=tk.BOTH, expand=True)
        
        # Programmas apraksts
        info_text = """
        Augstuma starpības un slīpuma kalkulators

        Šī programma ļauj aprēķināt augstuma starpību un slīpumu starp diviem punktiem.
        
        Lietošanas instrukcija:
        1. Ievadiet sākuma punkta augstumu metros
        2. Ievadiet beigu punkta augstumu metros
        3. Ievadiet attālumu starp punktiem metros
        4. Nospiediet "APRĒĶINĀT", lai iegūtu rezultātus
        
        Programma aprēķinās augstuma starpību un slīpuma procentu,
        kā arī uzzīmēs grafisku attēlojumu.
        
        Versija: 0.1
        Laura Līva Kasparinska, 12.b klase
        """
        
        info_label = tk.Label(info_frame, text=info_text, font=text_font, justify=tk.LEFT,
                             bg=theme["frame_bg"], fg=theme["fg"], padx=20, pady=20)
        info_label.pack()
        
        # Atpakaļ poga
        button_frame = tk.Frame(self.root, bg=theme["bg"])
        button_frame.pack(pady=20)
        
        back_button = tk.Button(button_frame, text="Atpakaļ", font=text_font, bg=theme["button_bg"], 
                              fg=theme["fg"], activebackground=theme["accent"], 
                              command=self.show_start_page, width=15)
        back_button.pack()
    
    def show_calculator(self):
        # Notīrīt esošos widgetus
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Piemērot tēmu
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        
        # Iegūt pogu stilu
        button_style_dict = self.button_styles[self.current_button_style]
        graph_style_dict = self.graph_styles[self.current_graph_style]
        
        # Galvenais rāmis
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pielāgot stilu
        style = ttk.Style()
        style.configure('TLabelframe', background=theme["frame_bg"])
        style.configure('TLabelframe.Label', background=theme["frame_bg"], foreground=theme["fg"], font=("Arial", 10, 'bold'))
        style.configure('TButton', background=theme["button_bg"], foreground=theme["fg"], font=("Arial", 10))
        style.configure('TLabel', background=theme["frame_bg"], foreground=theme["fg"], font=("Arial", 10))
        style.configure('TFrame', background=theme["frame_bg"])
        style.configure('TPanedwindow', background=theme["bg"])
        style.configure('TCombobox', background=theme["frame_bg"], fieldbackground=theme["frame_bg"], font=("Arial", 10))
        
        # Kreisais panelis - Grafiks
        self.left_frame = ttk.LabelFrame(main_frame, text="Grafiskais attēlojums")
        main_frame.add(self.left_frame, weight=1)
        
        # Grafika inicializācija
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.fig.patch.set_facecolor(theme["frame_bg"])
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Augstuma profils")
        self.ax.set_xlabel("Attālums (m)")
        self.ax.set_ylabel("Augstums (m)")
        self.ax.set_facecolor(theme["frame_bg"])
        
        self.ax.grid(graph_style_dict["grid"], linestyle='--', alpha=0.7)
        
        # Pielāgot asu un tekstus tēmai
        for item in ([self.ax.title, self.ax.xaxis.label, self.ax.yaxis.label] +
                     self.ax.get_xticklabels() + self.ax.get_yticklabels()):
            item.set_color(theme["fg"])
            item.set_fontfamily(["Arial"])
            
        self.canvas = FigureCanvasTkAgg(self.fig, self.left_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Informācijas sadaļa zem grafika
        info_frame = ttk.Frame(self.left_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        relief_info = ttk.Label(info_frame, text="""Slīpuma klasifikācija:
≤ 5% - Viegls reljefs
5-15% - Mērens reljefs
> 15% - Stāvs reljefs""", justify=tk.LEFT)
        relief_info.pack(side=tk.LEFT, anchor=tk.W)
        
        # Autora informācija
        author_label = ttk.Label(self.left_frame, text="© 2025 | Laura Līva Kasparinska")
        author_label.pack(side=tk.BOTTOM, padx=10, pady=5, anchor=tk.W)
        
        # Labais panelis - Ievades un Rezultāti
        self.right_frame = ttk.LabelFrame(main_frame, text="")
        main_frame.add(self.right_frame, weight=1)
        
        # Piemēru izvēle
        sample_frame = ttk.LabelFrame(self.right_frame, text="Sagatavotie dati:")
        sample_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(sample_frame, text="Izvēlies reljefu:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.sample_combo = ttk.Combobox(sample_frame, values=list(self.sample_data.keys()), state="readonly", width=18)
        self.sample_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.sample_combo.bind("<<ComboboxSelected>>", self.load_sample_data)
        
        load_btn = ttk.Button(sample_frame, text="Ielādēt datus", command=self.load_selected_sample)
        load_btn.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Ievades sadaļa
        input_frame = ttk.LabelFrame(self.right_frame, text="Ievadi:")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Validācijas funkcija (tikai cipariem un komatu)
        vcmd = (self.root.register(self.validate_float_input), '%P')
        
        # Sākuma punkta augstums
        ttk.Label(input_frame, text="Sākuma punkta augst:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.start_height = ttk.Entry(input_frame, validate="key", validatecommand=vcmd, font=("Arial", 10))
        self.start_height.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(input_frame, text="metros").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Beigu punkta augstums
        ttk.Label(input_frame, text="Beigu punkta augst:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.end_height = ttk.Entry(input_frame, validate="key", validatecommand=vcmd, font=("Arial", 10))
        self.end_height.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(input_frame, text="metros").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Attālums starp punktiem
        ttk.Label(input_frame, text="Attālums starp punktiem:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.distance = ttk.Entry(input_frame, validate="key", validatecommand=vcmd, font=("Arial", 10))
        self.distance.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(input_frame, text="metros").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Papildu punktu sadaļa
        additional_points_frame = ttk.LabelFrame(input_frame, text="Papildu punkti:")
        additional_points_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W + tk.E, padx=5, pady=10)
        
        # Saraksts esošajiem papildu punktiem
        self.points_listbox = tk.Listbox(additional_points_frame, width=30, height=4, font=("Arial", 9))
        self.points_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)
        self.update_points_listbox()
        
        # Papildu punkta ievade
        point_frame = ttk.Frame(additional_points_frame)
        point_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)
        
        ttk.Label(point_frame, text="Attālums:").grid(row=0, column=0, padx=2, sticky=tk.W)
        self.add_point_distance = ttk.Entry(point_frame, validate="key", validatecommand=vcmd, width=8, font=("Arial", 9))
        self.add_point_distance.grid(row=0, column=1, padx=2, sticky=tk.W)
        
        ttk.Label(point_frame, text="Augstums:").grid(row=0, column=2, padx=2, sticky=tk.W)
        self.add_point_height = ttk.Entry(point_frame, validate="key", validatecommand=vcmd, width=8, font=("Arial", 9))
        self.add_point_height.grid(row=0, column=3, padx=2, sticky=tk.W)
        
        # Pogas punktu pievienošanai/dzēšanai
        add_point_btn = ttk.Button(point_frame, text="Pievienot", command=self.add_point, width=8)
        add_point_btn.grid(row=0, column=4, padx=2, sticky=tk.W)
        
        remove_point_btn = ttk.Button(additional_points_frame, text="Dzēst izvēlēto", command=self.remove_point, width=15)
        remove_point_btn.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        
        clear_points_btn = ttk.Button(additional_points_frame, text="Dzēst visus", command=self.clear_points, width=15)
        clear_points_btn.grid(row=2, column=1, padx=5, pady=2, sticky=tk.E)
        
        # Ierobežojumi
        limit_label = ttk.Label(input_frame, text="Ierobežojumi:", font=("Arial", 9, 'bold'))
        limit_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=(15, 5))
        
        limit_text = ttk.Label(input_frame, text="• Vērtībām jābūt pozitīvām\n• Augstums: 0-8848 m\n• Attālums: 1-10000 m", font=("Arial", 9))
        limit_text.grid(row=5, column=0, columnspan=3, sticky=tk.W, padx=5, pady=0)
        
        # Rezultātu sadaļa
        result_frame = ttk.LabelFrame(self.right_frame, text="Rezultāts:")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Augstuma starpība
        ttk.Label(result_frame, text="Augstuma starpība:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.elevation_diff = ttk.Entry(result_frame, state="readonly", font=("Arial", 10))
        self.elevation_diff.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(result_frame, text="metri").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Slīpums
        ttk.Label(result_frame, text="Slīpums:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.slope = ttk.Entry(result_frame, state="readonly", font=("Arial", 10))
        self.slope.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(result_frame, text="%").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Pogu rāmis
        button_frame = ttk.Frame(self.right_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        calculate_btn = ttk.Button(button_frame, text="APRĒĶINĀT", command=self.calculate)
        clear_btn = ttk.Button(button_frame, text="DZĒST", command=self.clear)
        back_btn = ttk.Button(button_frame, text="ATPAKAĻ", command=self.show_start_page)
        
        # Pogu izvietojums
        calculate_btn.pack(side=tk.LEFT, padx=5)
        clear_btn.pack(side=tk.LEFT, padx=5)
        back_btn.pack(side=tk.LEFT, padx=5)
        
    def validate_float_input(self, value):
        if value == "":
            return True
        # Atļaut tikai ciparus, komatus un punktus
        if value.count('.') <= 1 and value.count(',') <= 1:
            if value.replace('.', '').replace(',', '').isdigit():
                return True
        return False
    
    def load_sample_data(self, event):
        # Funkcija, kas tiek izsaukta, kad lietotājs izvēlas piemēru no nolaižamā saraksta
        pass
    
    def load_selected_sample(self):
        selected = self.sample_combo.get()
        if selected in self.sample_data:
            data = self.sample_data[selected]
            
            # Notīra esošos laukus
            self.start_height.delete(0, tk.END)
            self.end_height.delete(0, tk.END)
            self.distance.delete(0, tk.END)
            
            # Ievada jaunās vērtības
            self.start_height.insert(0, str(data["start_height"]))
            self.end_height.insert(0, str(data["end_height"]))
            self.distance.insert(0, str(data["distance"]))
            
            # Automātiski aprēķina rezultātu
            self.calculate()
    
    def calculate(self):
        try:
            # Iegūst ievades vērtības
            start_h = float(self.start_height.get().replace(',', '.'))
            end_h = float(self.end_height.get().replace(',', '.'))
            dist = float(self.distance.get().replace(',', '.'))
            
            # Pārbauda ierobežojumus
            if start_h < 0 or end_h < 0 or dist <= 0:
                messagebox.showerror("Kļūda", "Visām vērtībām jābūt pozitīvām, un attālumam jābūt lielākam par 0.")
                return
                
            if start_h > 8848 or end_h > 8848:
                messagebox.showerror("Kļūda", "Augstums nevar pārsniegt 8848 metrus (Everesta augstums).")
                return
                
            if dist > 10000:
                messagebox.showerror("Kļūda", "Attālums nevar pārsniegt 10000 metrus šajā programmā.")
                return
            
            # Pārbauda vai papildu punktu attālums nepārsniedz kopējo attālumu
            for point in self.additional_points:
                if point["distance"] >= dist:
                    messagebox.showerror("Kļūda", "Papildu punktu attālumi nedrīkst pārsniegt kopējo attālumu starp sākuma un beigu punktiem.")
                    return
            
            # Aprēķini
            elevation_diff = end_h - start_h
            slope_percent = (elevation_diff / dist) * 100
            
            # Atjauno rezultātu laukus
            self.elevation_diff.config(state="normal")
            self.elevation_diff.delete(0, tk.END)
            self.elevation_diff.insert(0, f"{abs(elevation_diff):.1f}")
            self.elevation_diff.config(state="readonly")
            
            self.slope.config(state="normal")
            self.slope.delete(0, tk.END)
            self.slope.insert(0, f"{abs(slope_percent):.1f}")
            self.slope.config(state="readonly")
            
            # Iegūst tēmas un grafika stila iestatījumus
            theme = self.themes[self.current_theme]
            graph_style = self.graph_styles[self.current_graph_style]
            
            # Zīmē grafiku
            self.ax.clear()
            self.ax.set_title("Augstuma profils", fontfamily="Arial", fontsize=12)
            self.ax.set_xlabel("Attālums (m)", fontfamily="Arial", fontsize=10)
            self.ax.set_ylabel("Augstums (m)", fontfamily="Arial", fontsize=10)
            
            # Iestatīt režģu rādīšanu atkarībā no grafika stila
            self.ax.grid(graph_style["grid"], linestyle='--', alpha=0.7, color=theme["fg"], linewidth=0.5)
            
            # Sagatavo visus punktus (sākuma, papildu un beigu)
            points = [{"distance": 0, "height": start_h}]
            
            # Pievienot papildu punktus, sakārtotus pēc attāluma
            if self.additional_points:
                sorted_points = sorted(self.additional_points, key=lambda p: p["distance"])
                points.extend(sorted_points)
            
            # Pievienot beigu punktu
            points.append({"distance": dist, "height": end_h})
            
            # Izveido masīvus ar visiem punktiem grafikam
            x_values = [p["distance"] for p in points]
            y_values = [p["height"] for p in points]
            
            # Līnijas izskats atkarībā no tēmas un grafika stila
            line_color = theme["accent"]
            self.ax.plot(x_values, y_values, color=line_color, linestyle='-', 
                        linewidth=graph_style["line_width"])
            
            # Pievieno kalnu siluetus ar animāciju
            if self.animation_enabled:
                self.fig.canvas.draw()
                self.root.update()
                
                for i in range(10):
                    alpha = (i + 1) / 10
                    self.add_mountain_silhouette_with_points(points, alpha)
                    self.fig.canvas.draw()
                    self.root.update()
                    self.root.after(50)
            else:
                self.add_mountain_silhouette_with_points(points)
    
            # Pielāgo y ass robežas, lai rādītu nedaudz virs un zem punktiem
            min_h = min(y_values)
            max_h = max(y_values)
            padding = (max_h - min_h) * 0.2 if max_h != min_h else min_h * 0.1
            self.ax.set_ylim(min_h - padding, max_h + padding)
            
            # Pievienot punktus ar marķieriem
            marker_size = graph_style["marker_size"]
            
            # Izveidot krāsu ciklu no tēmas krāsām
            point_colors = theme["point_colors"]
            
            # Parāda katru punktu ar atbilstošu krāsu un marķieri
            for i, (x, y) in enumerate(zip(x_values, y_values)):
                # Katram punktam piešķir savu krāsu no pieejamajām krāsām
                color_index = i % len(point_colors)
                color = point_colors[color_index]
                
                # Pirmais un pēdējais punkts ir īpaši
                if i == 0:
                    label = 'Sākuma punkts'
                elif i == len(x_values) - 1:
                    label = 'Beigu punkts'
                else:
                    label = f'Punkts {i}'
                
                self.ax.plot(x, y, 'o', markersize=marker_size, 
                            color=color, label=label)
            
            # Ēnot zonu zem līnijas
            self.ax.fill_between(x_values, y_values, min_h - padding, alpha=graph_style["fill_alpha"], color=theme["accent"])
           
            legend = self.ax.legend(loc='upper right', fontsize=9)
            legend.get_frame().set_facecolor(theme["frame_bg"])
            legend.get_frame().set_edgecolor(theme["fg"])
            for text in legend.get_texts():
                text.set_color(theme["fg"])
                text.set_fontfamily(["Arial"])
            
            # Pievienot slīpuma tekstu grafikā
            mid_x = dist / 2
            mid_y = (start_h + end_h) / 2
            
            # Slīpuma teksta stils
            bbox_props = dict(boxstyle="round,pad=0.3", fc='white', alpha=0.7)
            text_color = theme["fg"]
                
            self.ax.annotate(f"Slīpums: {abs(slope_percent):.1f}%", 
                            xy=(mid_x, mid_y), 
                            xytext=(mid_x, mid_y + padding/2),
                            ha='center', va='bottom', color=text_color,
                            fontfamily="Arial", fontsize=10,
                            bbox=bbox_props)
            
            # Piemērot tēmu grafikam
            self.ax.set_facecolor(theme["frame_bg"])
            for item in ([self.ax.title, self.ax.xaxis.label, self.ax.yaxis.label] +
                         self.ax.get_xticklabels() + self.ax.get_yticklabels()):
                item.set_color(theme["fg"])
                try:
                    item.set_fontfamily(["Arial"])
                except:
                    pass
            
            self.canvas.draw()
            
            # Parāda slīpuma novērtējumu
            message = ""
            direction = "kāpums" if elevation_diff > 0 else "kritums"
            
            if abs(slope_percent) < 5:
                message = f"Ļoti viegls {direction} (< 5%).\nPiemērots visiem ceļotājiem."
            elif abs(slope_percent) < 15:
                message = f"Mērens {direction} (5-15%).\nNepieciešama vidēja fiziskā sagatavotība."
            else:
                message = f"Stāvs {direction} (> 15%).\nNepieciešama laba fiziskā sagatavotība un piesardzība."
            
            if elevation_diff > 0:
                title = "Kāpuma analīze"
            else:
                title = "Krituma analīze"
            
            # Standarta ziņojums
            messagebox.showinfo(title, message)
            
        except ValueError:
            messagebox.showerror("Kļūda", "Lūdzu ievadiet derīgus skaitļus.")
    
    def add_mountain_silhouette(self, start_h, end_h, dist, opacity=0.3):
        try:
            # Daudz detalizētāks kalnu siluets ar tēmas krāsām
            x = np.linspace(0, dist, 100)
            
            # Izveidojam reālistiskāku kalnu reljefu
            if dist > 1000:
                # Lielākiem attālumiem - izteiktākas reljefa izmaiņas
                noise_scale = dist / 40
            else:
                # Mazākiem attālumiem - smalkākas reljefa izmaiņas
                noise_scale = dist / 30
            
            noise1 = np.random.normal(0, noise_scale, 100)  
            noise2 = np.random.normal(0, noise_scale/3, 100)  
            noise3 = np.random.normal(0, noise_scale/8, 100)  
     
            y_base = np.linspace(start_h, end_h, 100)
            noise = noise1 + noise2 + noise3
            y = y_base + noise
            
            # Nodrošina, ka siluets nepārsniedz galveno līniju un neatrodas zem minimālā augstuma
            min_h = min(start_h, end_h)
            for i in range(len(y)):
                if end_h > start_h:
                    y[i] = min(y[i], start_h + (end_h - start_h) * i / 99)
                else:
                    y[i] = min(y[i], start_h - (start_h - end_h) * i / 99)
                    
                # Nodrošina, ka siluets neiet zem minimālā augstuma ar atstarpi
                min_allowed = min_h - abs(end_h - start_h) * 0.05
                y[i] = max(y[i], min_allowed)
            
            # Tēmas krāsas siluetam
            fill_color = "gray"
            
            # Uzzīmē kalnu siluetu
            self.ax.fill_between(x, y, min_h - abs(end_h - start_h) * 0.1, alpha=opacity, color=fill_color)
                
        except (ValueError, TypeError):
            pass
    
    def clear(self):
        # Notīra visus laukus
        self.start_height.delete(0, tk.END)
        self.end_height.delete(0, tk.END)
        self.distance.delete(0, tk.END)
        
        self.elevation_diff.config(state="normal")
        self.elevation_diff.delete(0, tk.END)
        self.elevation_diff.config(state="readonly")
        
        self.slope.config(state="normal")
        self.slope.delete(0, tk.END)
        self.slope.config(state="readonly")
        
        # Atjauno grafiku
        self.ax.clear()
        self.ax.set_title("Augstuma profils")
        self.ax.set_xlabel("Attālums (m)")
        self.ax.set_ylabel("Augstums (m)")
        
        # Piemērot tēmu grafikam
        theme = self.themes[self.current_theme]
        self.ax.set_facecolor(theme["frame_bg"])
        
    def apply_specific_setting(self, setting_type):
        """Piemēro konkrētu iestatījumu, atkarībā no tā, kurā cilnē atrodamies"""
        # Saglabājam iepriekšējās vērtības, lai varētu parādīt, kas mainījās
        prev_graph_style = self.current_graph_style
        prev_button_style = self.current_button_style
        prev_animation = self.animation_enabled
        
        changes = []
        
        if self.current_tab == "grafiks":
            # Piemērot grafika stila iestatījumus
            new_graph_style = self.graph_style_var.get()
            if new_graph_style != self.current_graph_style:
                self.current_graph_style = new_graph_style
                changes.append(f"Grafika stils: {self.current_graph_style}")
        
        elif self.current_tab == "pogas":
            # Piemērot pogu stila iestatījumus
            new_button_style = self.button_style_var.get()
            if new_button_style != self.current_button_style:
                self.current_button_style = new_button_style
                changes.append(f"Pogu stils: {self.current_button_style}")
        
        elif self.current_tab == "animācijas":
            # Piemērot animācijas iestatījumus
            new_animation = self.animation_var.get()
            if new_animation != self.animation_enabled:
                self.animation_enabled = new_animation
                animation_status = "Ieslēgtas" if self.animation_enabled else "Izslēgtas"
                changes.append(f"Animācijas: {animation_status}")
        
        # Parāda paziņojumu par veiktajām izmaiņām
        if changes:
            message = "Iestatījums veiksmīgi piemērots!\n\n- " + "\n- ".join(changes)
            messagebox.showinfo("Iestatījumi", message)
            
            # Atjauno skatu ar jaunajiem iestatījumiem
            self.show_settings()
            self.switch_settings_tab(self.current_tab)
        else:
            messagebox.showinfo("Iestatījumi", "Iestatījumi saglabāti bez izmaiņām.")

    def add_point(self):
        """Pievieno papildu punktu sarakstam"""
        try:
            # Iegūst ievades vērtības
            distance = float(self.add_point_distance.get().replace(',', '.'))
            height = float(self.add_point_height.get().replace(',', '.'))
            
            # Pārbauda ierobežojumus
            if distance <= 0 or height < 0:
                messagebox.showerror("Kļūda", "Attālumam jābūt lielākam par 0, un augstumam jābūt pozitīvam.")
                return
                
            if height > 8848:
                messagebox.showerror("Kļūda", "Augstums nevar pārsniegt 8848 metrus.")
                return
                
            if distance > 10000:
                messagebox.showerror("Kļūda", "Attālums nevar pārsniegt 10000 metrus.")
                return
            
            # Pievieno punktu sarakstam
            self.additional_points.append({"distance": distance, "height": height})
            
            # Atjauno sarakstu un notīra ievades laukus
            self.update_points_listbox()
            self.add_point_distance.delete(0, tk.END)
            self.add_point_height.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Kļūda", "Lūdzu ievadiet derīgus skaitļus.")
    
    def remove_point(self):
        """Noņem izvēlēto punktu no saraksta"""
        selected = self.points_listbox.curselection()
        if selected:
            index = selected[0]
            del self.additional_points[index]
            self.update_points_listbox()
    
    def clear_points(self):
        """Notīra visus papildu punktus"""
        self.additional_points = []
        self.update_points_listbox()
    
    def update_points_listbox(self):
        """Atjaunina punktu saraksta attēlojumu"""
        self.points_listbox.delete(0, tk.END)
        for point in self.additional_points:
            distance = point["distance"]
            height = point["height"]
            self.points_listbox.insert(tk.END, f"Attālums: {distance} m, Augstums: {height} m")

    def add_mountain_silhouette_with_points(self, points, opacity=0.3):
        """Ģenerē kalnu siluetu, izmantojot ievadītos punktus"""
        try:
            # Iegūst punktu datus masīvos
            x_values = [p["distance"] for p in points]
            y_values = [p["height"] for p in points]
            
            # Minimālais augstums
            min_h = min(y_values)
            
            # Maksimālais attālums
            max_dist = max(x_values)
            
            x = np.linspace(0, max_dist, 100)
     
            if max_dist > 1000:
                noise_scale = max_dist / 40
            else:
                noise_scale = max_dist / 30
            
            y_base = np.interp(x, x_values, y_values)
          
            noise1 = np.random.normal(0, noise_scale, 100)  
            noise2 = np.random.normal(0, noise_scale/3, 100)  
            noise3 = np.random.normal(0, noise_scale/8, 100)  
      
            noise = noise1 + noise2 + noise3
            y = y_base + noise
            
            # Pielāgo siluetu, lai tas ievērotu punktus un nepārsniegtu tos
            for i in range(len(y)):
                closest_idx = 0
                next_idx = 1
     
                for j in range(len(x_values) - 1):
                    if x[i] >= x_values[j] and x[i] <= x_values[j + 1]:
                        closest_idx = j
                        next_idx = j + 1
                        break
                
                # Neļauj siluetam pārsniegt līniju
                if y_values[next_idx] > y_values[closest_idx]:
                    max_allowed = y_values[closest_idx] + (y_values[next_idx] - y_values[closest_idx]) * \
                                 (x[i] - x_values[closest_idx]) / (x_values[next_idx] - x_values[closest_idx])
                    y[i] = min(y[i], max_allowed)
                else:
                    max_allowed = y_values[closest_idx] - (y_values[closest_idx] - y_values[next_idx]) * \
                                 (x[i] - x_values[closest_idx]) / (x_values[next_idx] - x_values[closest_idx])
                    y[i] = min(y[i], max_allowed)
                
                # Nodrošina, ka siluets neiet zem minimālā augstuma ar atstarpi
                height_range = max(y_values) - min(y_values)
                min_allowed = min_h - height_range * 0.05
                y[i] = max(y[i], min_allowed)
            
            # Tēmas krāsas siluetam
            theme = self.themes[self.current_theme]
            fill_color = "gray"  
            
            # Uzzīmē kalnu siluetu
            height_range = max(y_values) - min(y_values)
            self.ax.fill_between(x, y, min_h - height_range * 0.1, alpha=opacity, color=fill_color)
                
        except (ValueError, TypeError, IndexError) as e:
            print(f"Kļūda silueta zīmēšanā: {e}")
            if len(points) >= 2:
                start_point = points[0]
                end_point = points[-1]
                self.add_mountain_silhouette(start_point["height"], end_point["height"], end_point["distance"], opacity)

# Palaiž aplikāciju
if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorsApp(root)
    root.mainloop()