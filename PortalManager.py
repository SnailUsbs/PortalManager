import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), 'Scripts'))
import CustomFiles
import UI
import Setup
import Maps
import SourceMods

SKIN_SLOTS = [
    {
        'label':    'Portal Gun Model/Texture',
        'subfolder': 'PortalGuns',
        'mod_type': 'Portal Gun Model/Texture',
        'combobox': 'gun_model_combobox',
        'status':   'gun_status_label',
        'removed_msg': 'Portal Gun mod removed',
    },
    {
        'label':    'Custom Portal',
        'subfolder': 'Portals',
        'mod_type': 'Portal',
        'combobox': 'portal_combobox',
        'status':   'portal_status_label',
        'removed_msg': 'Portal mod removed',
    },
    {
        'label':    'Companion Cube',
        'subfolder': 'CompanionCubes',
        'mod_type': 'CompanionCube',
        'combobox': 'cube_combobox',
        'status':   'cube_status_label',
        'removed_msg': 'Companion Cube mod removed',
    },
    {
        'label':    'Turret',
        'subfolder': 'Turrets',
        'mod_type': 'Turret',
        'combobox': 'turret_combobox',
        'status':   'turret_status_label',
        'removed_msg': 'Turret mod removed',
    },
    {
        'label':    'Chell',
        'subfolder': 'Chell',
        'mod_type': 'Chell',
        'combobox': 'chell_combobox',
        'status':   'chell_status_label',
        'removed_msg': 'Chell mod removed',
    },
    {
        'label':    'Glados',
        'subfolder': 'Glados',
        'mod_type': 'Glados',
        'combobox': 'glados_combobox',
        'status':   'glados_status_label',
        'removed_msg': 'Glados mod removed',
    },
    {
        'label':    'Beans',
        'subfolder': 'Beans',
        'mod_type': 'Beans',
        'combobox': 'beans_combobox',
        'status':   'beans_status_label',
        'removed_msg': 'Beans mod removed',
    },
    {
        'label':    'Incinerator',
        'subfolder': 'Incinerator',
        'mod_type': 'Incinerator',
        'combobox': 'incinerator_combobox',
        'status':   'incinerator_status_label',
        'removed_msg': 'Incinerator mod removed',
    },
]


class PortalManager:
    def __init__(self, root):
        self.config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        self.config_file = os.path.join(self.config_dir, 'PMConfig.txt')
        self.portal_manager_path = None
        self.custom_folder_path = None
        os.makedirs(self.config_dir, exist_ok=True)
        self.ui = UI.UI(root)
        self.root = root
        self.portal_path_entry = self.ui.setup_game_tab(
            self.browse_portal_path,
            self.save_current_path,
            self.start_game,
            self.add_skin_mod
        )

        skin_callbacks = [lambda s=slot: self.change_skin(s) for slot in SKIN_SLOTS]
        widgets = self.ui.setup_portal_gun_tab(*skin_callbacks)

        comboboxes = widgets[:8]
        status_labels = widgets[8:]
        for slot, combobox, status in zip(SKIN_SLOTS, comboboxes, status_labels):
            setattr(self, slot['combobox'], combobox)
            setattr(self, slot['status'], status)

        self.maps_listbox = self.ui.setup_maps_tab(Maps.CUSTOM_MAPS, self.delete_map, self.add_custom_map, self.open_maps_folder)
        self.sourcemods_listbox = self.ui.setup_sourcemods_tab(self.delete_sourcemod, self.open_sourcemods_folder, self.add_sourcemod, self.toggle_portal1_filter)
        self.load_portal_path()

    def change_skin(self, slot):
        combobox = getattr(self, slot['combobox'])
        status_label = getattr(self, slot['status'])
        selected_mod = combobox.get()
        if not selected_mod:
            return

        active_mod = CustomFiles.get_active_mod(self.custom_folder_path, slot['mod_type'])

        if selected_mod == 'NONE':
            if active_mod:
                CustomFiles.move_folder(
                    os.path.join(self.custom_folder_path, active_mod),
                    os.path.join(self.portal_manager_path, slot['subfolder'], active_mod)
                )
                status_label.config(text=slot['removed_msg'])
            self.update_skin_dropdown(slot)
            return

        if active_mod:
            CustomFiles.move_folder(
                os.path.join(self.custom_folder_path, active_mod),
                os.path.join(self.portal_manager_path, slot['subfolder'], active_mod)
            )

        dest_path = os.path.join(self.custom_folder_path, selected_mod)
        if CustomFiles.move_folder(os.path.join(self.portal_manager_path, slot['subfolder'], selected_mod), dest_path):
            CustomFiles.create_pm_info_file(dest_path, slot['mod_type'])
            status_label.config(text=f"{selected_mod} has been set as active")

        self.update_skin_dropdown(slot)

    def update_skin_dropdown(self, slot):
        combobox = getattr(self, slot['combobox'], None)
        if not combobox:
            return
        folders = CustomFiles.get_mod_folders(self.portal_manager_path, slot['subfolder'])
        active_mod = CustomFiles.get_active_mod(self.custom_folder_path, slot['mod_type'])
        if active_mod and active_mod not in folders:
            folders.append(active_mod)
        combobox['values'] = ['NONE'] + folders
        combobox.set(active_mod if active_mod else 'NONE')

    def update_all_skin_dropdowns(self):
        for slot in SKIN_SLOTS:
            self.update_skin_dropdown(slot)

    def open_maps_folder(self):
        if not self.portal_path_entry.get():
            tk.messagebox.showwarning("No Path Set", "Please set your Portal 1 path first.")
            return
        path = os.path.join(self.portal_path_entry.get(), 'portal', 'maps')
        os.makedirs(path, exist_ok=True)
        subprocess.Popen(['xdg-open', path])

    def add_custom_map(self):
        if not self.portal_path_entry.get():
            tk.messagebox.showwarning("No Path Set", "Please set your Portal 1 path first.")
            return

        portal_dir_path = self.portal_path_entry.get()
        maps_dest = os.path.join(portal_dir_path, 'portal', 'maps')
        materials_dest = os.path.join(portal_dir_path, 'portal', 'materials')

        popup = tk.Toplevel(self.root)
        popup.title("Add Custom Map")
        popup.configure(bg='#1e1e1e')
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="What are you adding?", bg='#1e1e1e', fg='white',
                 font=('Arial', 11), padx=20, pady=10).pack()

        btn_frame = tk.Frame(popup, bg='#1e1e1e')
        btn_frame.pack(pady=10, padx=20)

        def pick_file():
            popup.destroy()
            bsp_file = filedialog.askopenfilename(
                title="Select .bsp file",
                filetypes=[("BSP files", "*.bsp")]
            )
            if not bsp_file:
                return
            self._install_map_bsp(bsp_file, maps_dest, portal_dir_path)

        def pick_folder():
            popup.destroy()
            folder = filedialog.askdirectory(title="Select map mod folder")
            if not folder:
                return
            self._install_map_folder(folder, maps_dest, materials_dest, portal_dir_path)

        ttk.Button(btn_frame, text=".bsp File", style='Blue.TButton', command=pick_file).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Folder", style='Blue.TButton', command=pick_folder).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def _install_map_bsp(self, bsp_file, maps_dest, portal_dir_path):
        try:
            os.makedirs(maps_dest, exist_ok=True)
            shutil.move(bsp_file, os.path.join(maps_dest, os.path.basename(bsp_file)))
            Maps.scan_custom_maps(portal_dir_path)
            self.ui.refresh_maps_list(Maps.CUSTOM_MAPS)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to install map: {e}")

    def _install_map_folder(self, folder, maps_dest, materials_dest, portal_dir_path):
        try:
            os.makedirs(maps_dest, exist_ok=True)
            bsp_found = False
            for root, dirs, files in os.walk(folder):
                for filename in files:
                    if filename.endswith('.bsp'):
                        shutil.move(os.path.join(root, filename), os.path.join(maps_dest, filename))
                        bsp_found = True

            if not bsp_found:
                tk.messagebox.showwarning("No BSP Found", "No .bsp file was found in the selected folder.")
                return

            src_materials = os.path.join(folder, 'materials')
            if os.path.isdir(src_materials):
                os.makedirs(materials_dest, exist_ok=True)
                for item in os.listdir(src_materials):
                    s = os.path.join(src_materials, item)
                    d = os.path.join(materials_dest, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)

            Maps.scan_custom_maps(portal_dir_path)
            self.ui.refresh_maps_list(Maps.CUSTOM_MAPS)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to install map: {e}")

    def toggle_portal1_filter(self):
        if self.ui.portal1_filter_var.get():
            self.ui.refresh_sourcemods_list(SourceMods.get_portal1_mods(self.portal_path_entry.get()))
        else:
            self.ui.refresh_sourcemods_list(SourceMods.SOURCEMODS)

    def add_sourcemod(self):
        if not self.portal_path_entry.get():
            tk.messagebox.showwarning("No Path Set", "Please set your Portal 1 path first.")
            return
        folder = filedialog.askdirectory(title="Select SourceMod folder")
        if not folder:
            return
        if SourceMods.add_sourcemod(self.portal_path_entry.get(), folder):
            self.ui.refresh_sourcemods_list(SourceMods.SOURCEMODS)
        else:
            tk.messagebox.showerror("Error", "Failed to add SourceMod.")

    def open_sourcemods_folder(self):
        if not self.portal_path_entry.get():
            tk.messagebox.showwarning("No Path Set", "Please set your Portal 1 path first.")
            return
        subprocess.Popen(['xdg-open', Setup.get_sourcemods_path(self.portal_path_entry.get())])

    def delete_sourcemod(self, mod_name):
        if not self.portal_path_entry.get():
            return
        SourceMods.delete_sourcemod(self.portal_path_entry.get(), mod_name)
        self.ui.refresh_sourcemods_list(SourceMods.SOURCEMODS)

    def delete_map(self, map_name):
        if not self.portal_path_entry.get():
            return
        portal_dir_path = self.portal_path_entry.get()
        bsp_path = os.path.join(portal_dir_path, 'portal', 'maps', f'{map_name}.bsp')
        if os.path.exists(bsp_path):
            os.remove(bsp_path)
        Maps.scan_custom_maps(portal_dir_path)
        self.ui.refresh_maps_list(Maps.CUSTOM_MAPS)

    def start_game(self):
        subprocess.Popen(['xdg-open', 'steam://rungameid/400'])

    def add_skin_mod(self):
        if not self.portal_manager_path:
            tk.messagebox.showwarning("No Path Set", "Please set your Portal 1 path first.")
            return

        skin_types = {slot['label']: slot['subfolder'] for slot in SKIN_SLOTS}

        popup = tk.Toplevel(self.root)
        popup.title("Select Skin Type")
        popup.configure(bg='#1e1e1e')
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Select the skin type for your mod:", bg='#1e1e1e', fg='white',
                 font=('Arial', 11), padx=20, pady=10).pack()

        selected_type = tk.StringVar(value=list(skin_types.keys())[0])

        for label in skin_types:
            tk.Radiobutton(popup, text=label, variable=selected_type, value=label,
                           bg='#1e1e1e', fg='white', selectcolor='#3e3e3e',
                           activebackground='#1e1e1e', activeforeground='white').pack(anchor='w', padx=30)

        def on_confirm():
            skin_type = selected_type.get()
            popup.destroy()
            mod_folder = filedialog.askdirectory(title=f"Select your {skin_type} mod folder")
            if not mod_folder:
                return
            mod_name = os.path.basename(mod_folder)
            dest = os.path.join(self.portal_manager_path, skin_types[skin_type], mod_name)
            if CustomFiles.move_folder(mod_folder, dest):
                tk.messagebox.showinfo("Success", f'"{mod_name}" added to {skin_types[skin_type]}.')
                self.update_all_skin_dropdowns()
            else:
                tk.messagebox.showerror("Error", f'Failed to add "{mod_name}". Make sure the folder exists.')

        btn_frame = tk.Frame(popup, bg='#1e1e1e')
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Confirm", command=on_confirm).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def browse_portal_path(self):
        dir_path = filedialog.askdirectory(title="Select Portal 1 Game Directory")
        if dir_path:
            self.portal_path_entry.delete(0, tk.END)
            self.portal_path_entry.insert(0, dir_path)
            self.update_portal_manager_path(dir_path)

    def save_current_path(self):
        path = self.portal_path_entry.get()
        if path:
            self.save_portal_path(path)

    def save_portal_path(self, path):
        with open(self.config_file, 'w') as f:
            f.write(f"portal1_path={path}\n")

    def update_portal_manager_path(self, portal_dir_path):
        Setup.run_setup(portal_dir_path)
        Maps.scan_custom_maps(portal_dir_path)
        self.ui.refresh_maps_list(Maps.CUSTOM_MAPS)
        SourceMods.scan_sourcemods(portal_dir_path)
        self.ui.refresh_sourcemods_list(SourceMods.SOURCEMODS)
        self.portal_manager_path = CustomFiles.get_portal_manager_path(portal_dir_path)
        self.custom_folder_path = CustomFiles.get_custom_folder_path(portal_dir_path)
        self.update_all_skin_dropdowns()

    def load_portal_path(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                for line in f:
                    if line.startswith('portal1_path='):
                        path = line.split('=')[1].strip()
                        self.portal_path_entry.delete(0, tk.END)
                        self.portal_path_entry.insert(0, path)
                        self.update_portal_manager_path(path)
                        break

if __name__ == "__main__":
    root = tk.Tk()
    app = PortalManager(root)
    root.mainloop()
