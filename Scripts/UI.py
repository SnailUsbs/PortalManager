import tkinter as tk
from tkinter import ttk, filedialog


class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Portal Manager")
        self.root.geometry("800x600")
        
        self.setup_black_theme()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.game_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.game_tab, text='GAME')
        
        self.portal_gun_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.portal_gun_tab, text='Skins')

        self.maps_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.maps_tab, text='Maps')

    def setup_maps_tab(self, custom_maps, delete_callback, add_map_callback):
        top_frame = tk.Frame(self.maps_tab, bg='#1e1e1e')
        top_frame.pack(fill='x', padx=10, pady=(10, 0))

        ttk.Button(top_frame, text="Add Custom Map", style='Blue.TButton',
                   command=add_map_callback).pack(side='right')

        list_frame = tk.Frame(self.maps_tab, bg='#1e1e1e')
        list_frame.pack(side='left', fill='y', padx=10, pady=10)

        tk.Label(list_frame, text="Custom Maps", bg='#1e1e1e', fg='white',
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 5))

        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        self.maps_listbox = tk.Listbox(
            list_frame,
            bg='#2e2e2e', fg='white',
            selectbackground='#3e3e3e', selectforeground='white',
            borderwidth=0, highlightthickness=0,
            width=30, height=20,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.maps_listbox.yview)
        self.maps_listbox.pack(side='left', fill='y')
        scrollbar.pack(side='left', fill='y')

        action_frame = tk.Frame(self.maps_tab, bg='#1e1e1e')
        action_frame.pack(side='left', fill='y', padx=(10, 0), pady=10)

        tk.Label(action_frame, text="", bg='#1e1e1e').pack(pady=(18, 0))

        style = ttk.Style()
        style.configure('Red.TButton', background='#dc3545', foreground='white',
                        font=('Arial', 10, 'bold'), padding=6)
        style.map('Red.TButton', background=[('active', '#c82333')])

        self.map_delete_btn = ttk.Button(
            action_frame, text="Delete", style='Red.TButton',
            command=lambda: delete_callback(self.maps_listbox.get(self.maps_listbox.curselection()))
        )

        def on_select(event):
            if self.maps_listbox.curselection():
                self.map_delete_btn.pack(anchor='n')
            else:
                self.map_delete_btn.pack_forget()

        self.maps_listbox.bind('<<ListboxSelect>>', on_select)

        self.refresh_maps_list(custom_maps)
        return self.maps_listbox

    def refresh_maps_list(self, custom_maps):
        self.maps_listbox.delete(0, 'end')
        for map_name in sorted(custom_maps):
            self.maps_listbox.insert('end', map_name)
        if hasattr(self, 'map_delete_btn'):
            self.map_delete_btn.pack_forget()
    
    def setup_black_theme(self):
        bg_color = '#1e1e1e'
        fg_color = '#ffffff'
        select_bg = '#3e3e3e'
        select_fg = '#ffffff'
        
        self.root.configure(bg=bg_color)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background=bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background=bg_color, foreground=fg_color, 
                       padding=[10, 5], borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', select_bg)])
        
        style.configure('TFrame', background=bg_color)
        
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        
        style.configure('TButton', background=select_bg, foreground=fg_color, 
                       borderwidth=1, focuscolor='none')
        style.map('TButton', background=[('active', '#4e4e4e')])
        
        style.configure('Green.TButton', background='#28a745', foreground='white',
                       font=('Arial', 14, 'bold'), padding=20)
        style.map('Green.TButton', background=[('active', '#218838')])

        style.configure('Blue.TButton', background='#5bc0de', foreground='white',
                       font=('Arial', 10, 'bold'), padding=8)
        style.map('Blue.TButton', background=[('active', '#31b0d5')])
        
        style.configure('TEntry', fieldbackground='#2e2e2e', foreground='white',
                       borderwidth=1, insertcolor='white')
        
        style.configure('TCombobox', fieldbackground='#2e2e2e', foreground='black',
                       borderwidth=1, arrowcolor='white')
    
    def setup_game_tab(self, browse_callback, save_callback, start_game_callback, add_skin_callback):
        top_frame = tk.Frame(self.game_tab, bg='#1e1e1e')
        top_frame.pack(fill='x', padx=10, pady=10)
        
        path_frame = tk.Frame(top_frame, bg='#1e1e1e')
        path_frame.pack(side='left')
        
        path_label = tk.Label(path_frame, text="Portal 1 Path:", bg='#1e1e1e', fg='white')
        path_label.pack(side='left', padx=(0, 5))
        
        self.portal_path_entry = ttk.Entry(path_frame, width=25)
        self.portal_path_entry.pack(side='left', padx=(0, 5))
        
        browse_button = ttk.Button(path_frame, text="Browse...", command=browse_callback)
        browse_button.pack(side='left', padx=(0, 5))
        
        save_button = ttk.Button(path_frame, text="Save", command=save_callback)
        save_button.pack(side='left')
        
        start_button = ttk.Button(top_frame, text="Start Game", style='Green.TButton', command=start_game_callback)
        start_button.pack(side='right')

        button_frame = tk.Frame(self.game_tab, bg='#1e1e1e')
        button_frame.pack(anchor='e', padx=10, pady=(0, 5))
        add_skin_button = ttk.Button(button_frame, text="Add Skin Mod", style='Blue.TButton', command=add_skin_callback)
        add_skin_button.pack()
        
        return self.portal_path_entry
    
    def setup_portal_gun_tab(self, gun_change_callback, portal_change_callback, cube_change_callback, turret_change_callback, chell_change_callback, glados_change_callback):
        gun_frame = tk.Frame(self.portal_gun_tab, bg='#1e1e1e')
        gun_frame.pack(fill='x', padx=10, pady=10)
        
        gun_label = tk.Label(gun_frame, text="Portal Gun Model/Texture:", bg='#1e1e1e', fg='white')
        gun_label.pack(side='left', padx=(0, 5))
        
        self.gun_model_combobox = ttk.Combobox(gun_frame, values=[], width=25, state='readonly')
        self.gun_model_combobox.pack(side='left', padx=(0, 5))
        
        change_button = ttk.Button(gun_frame, text="Change", command=gun_change_callback)
        change_button.pack(side='left')
        
        self.gun_status_label = tk.Label(self.portal_gun_tab, text="", bg='#1e1e1e', fg='#28a745', font=('Arial', 10))
        self.gun_status_label.pack(pady=(0, 10))
        
        portal_frame = tk.Frame(self.portal_gun_tab, bg='#1e1e1e')
        portal_frame.pack(fill='x', padx=10, pady=10)
        
        portal_label = tk.Label(portal_frame, text="Custom Portal:", bg='#1e1e1e', fg='white')
        portal_label.pack(side='left', padx=(0, 5))
        
        self.portal_combobox = ttk.Combobox(portal_frame, values=[], width=25, state='readonly')
        self.portal_combobox.pack(side='left', padx=(0, 5))
        
        portal_change_button = ttk.Button(portal_frame, text="Change", command=portal_change_callback)
        portal_change_button.pack(side='left')
        
        self.portal_status_label = tk.Label(self.portal_gun_tab, text="", bg='#1e1e1e', fg='#28a745', font=('Arial', 10))
        self.portal_status_label.pack(pady=(0, 10))

        cube_frame = tk.Frame(self.portal_gun_tab, bg='#1e1e1e')
        cube_frame.pack(fill='x', padx=10, pady=10)

        cube_label = tk.Label(cube_frame, text="Companion Cube:", bg='#1e1e1e', fg='white')
        cube_label.pack(side='left', padx=(0, 5))

        self.cube_combobox = ttk.Combobox(cube_frame, values=[], width=25, state='readonly')
        self.cube_combobox.pack(side='left', padx=(0, 5))

        cube_change_button = ttk.Button(cube_frame, text="Change", command=cube_change_callback)
        cube_change_button.pack(side='left')

        self.cube_status_label = tk.Label(self.portal_gun_tab, text="", bg='#1e1e1e', fg='#28a745', font=('Arial', 10))
        self.cube_status_label.pack(pady=(0, 10))

        turret_frame = tk.Frame(self.portal_gun_tab, bg='#1e1e1e')
        turret_frame.pack(fill='x', padx=10, pady=10)

        turret_label = tk.Label(turret_frame, text="Turret:", bg='#1e1e1e', fg='white')
        turret_label.pack(side='left', padx=(0, 5))

        self.turret_combobox = ttk.Combobox(turret_frame, values=[], width=25, state='readonly')
        self.turret_combobox.pack(side='left', padx=(0, 5))

        turret_change_button = ttk.Button(turret_frame, text="Change", command=turret_change_callback)
        turret_change_button.pack(side='left')

        self.turret_status_label = tk.Label(self.portal_gun_tab, text="", bg='#1e1e1e', fg='#28a745', font=('Arial', 10))
        self.turret_status_label.pack(pady=(0, 10))

        chell_frame = tk.Frame(self.portal_gun_tab, bg='#1e1e1e')
        chell_frame.pack(fill='x', padx=10, pady=10)

        chell_label = tk.Label(chell_frame, text="Chell:", bg='#1e1e1e', fg='white')
        chell_label.pack(side='left', padx=(0, 5))

        self.chell_combobox = ttk.Combobox(chell_frame, values=[], width=25, state='readonly')
        self.chell_combobox.pack(side='left', padx=(0, 5))

        ttk.Button(chell_frame, text="Change", command=chell_change_callback).pack(side='left')

        self.chell_status_label = tk.Label(self.portal_gun_tab, text="", bg='#1e1e1e', fg='#28a745', font=('Arial', 10))
        self.chell_status_label.pack(pady=(0, 10))

        glados_frame = tk.Frame(self.portal_gun_tab, bg='#1e1e1e')
        glados_frame.pack(fill='x', padx=10, pady=10)

        glados_label = tk.Label(glados_frame, text="Glados:", bg='#1e1e1e', fg='white')
        glados_label.pack(side='left', padx=(0, 5))

        self.glados_combobox = ttk.Combobox(glados_frame, values=[], width=25, state='readonly')
        self.glados_combobox.pack(side='left', padx=(0, 5))

        ttk.Button(glados_frame, text="Change", command=glados_change_callback).pack(side='left')

        self.glados_status_label = tk.Label(self.portal_gun_tab, text="", bg='#1e1e1e', fg='#28a745', font=('Arial', 10))
        self.glados_status_label.pack(pady=(0, 10))

        return self.gun_model_combobox, self.portal_combobox, self.cube_combobox, self.turret_combobox, self.chell_combobox, self.glados_combobox, self.gun_status_label, self.portal_status_label, self.cube_status_label, self.turret_status_label, self.chell_status_label, self.glados_status_label
