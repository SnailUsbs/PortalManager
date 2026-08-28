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
        self.gun_model_combobox, self.portal_combobox, self.cube_combobox, self.turret_combobox, self.chell_combobox, self.glados_combobox, self.gun_status_label, self.portal_status_label, self.cube_status_label, self.turret_status_label, self.chell_status_label, self.glados_status_label = self.ui.setup_portal_gun_tab(
            self.change_gun_model,
            self.change_portal,
            self.change_companion_cube,
            self.change_turret,
            self.change_chell,
            self.change_glados
        )
        
        self.maps_listbox = self.ui.setup_maps_tab(Maps.CUSTOM_MAPS, self.delete_map, self.add_custom_map)
        self.load_portal_path()
    
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
            dest = os.path.join(maps_dest, os.path.basename(bsp_file))
            shutil.move(bsp_file, dest)
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

        skin_types = {
            'Portal Gun Model/Texture': 'PortalGuns',
            'Custom Portal': 'Portals',
            'Companion Cube': 'CompanionCubes',
            'Turret': 'Turrets',
            'Chell': 'Chell',
            'Glados': 'Glados',
        }

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
                self.update_portal_gun_dropdown()
                self.update_portal_dropdown()
                self.update_companion_cube_dropdown()
                self.update_turret_dropdown()
                self.update_chell_dropdown()
                self.update_glados_dropdown()
            else:
                tk.messagebox.showerror("Error", f'Failed to add "{mod_name}". Make sure the folder exists.')

        btn_frame = tk.Frame(popup, bg='#1e1e1e')
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Confirm", command=on_confirm).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)
    
    def change_gun_model(self):
        selected_mod = self.gun_model_combobox.get()
        if not selected_mod:
            return

        active_mod = CustomFiles.get_active_portal_gun_mod(self.custom_folder_path)
        if selected_mod == 'NONE':
            if active_mod:
                source_path = os.path.join(self.custom_folder_path, active_mod)
                dest_path = os.path.join(self.portal_manager_path, 'PortalGuns', active_mod)
                CustomFiles.move_folder(source_path, dest_path)
                self.gun_status_label.config(text="Portal Gun mod removed")
            self.update_portal_gun_dropdown()
            return

        if active_mod:
            source_path = os.path.join(self.custom_folder_path, active_mod)
            dest_path = os.path.join(self.portal_manager_path, 'PortalGuns', active_mod)
            CustomFiles.move_folder(source_path, dest_path)
        
        source_path = os.path.join(self.portal_manager_path, 'PortalGuns', selected_mod)
        dest_path = os.path.join(self.custom_folder_path, selected_mod)
        if CustomFiles.move_folder(source_path, dest_path):
            CustomFiles.create_pm_info_file(dest_path)
            self.gun_status_label.config(text=f"{selected_mod} has been set as active")
        
        self.update_portal_gun_dropdown()
    
    def change_portal(self):
        selected_mod = self.portal_combobox.get()
        if not selected_mod:
            return

        active_mod = CustomFiles.get_active_portal_mod(self.custom_folder_path)
        if selected_mod == 'NONE':
            if active_mod:
                source_path = os.path.join(self.custom_folder_path, active_mod)
                dest_path = os.path.join(self.portal_manager_path, 'Portals', active_mod)
                CustomFiles.move_folder(source_path, dest_path)
                self.portal_status_label.config(text="Portal mod removed")
            self.update_portal_dropdown()
            return

        if active_mod:
            source_path = os.path.join(self.custom_folder_path, active_mod)
            dest_path = os.path.join(self.portal_manager_path, 'Portals', active_mod)
            CustomFiles.move_folder(source_path, dest_path)
        
        source_path = os.path.join(self.portal_manager_path, 'Portals', selected_mod)
        dest_path = os.path.join(self.custom_folder_path, selected_mod)
        if CustomFiles.move_folder(source_path, dest_path):
            CustomFiles.create_pm_info_file(dest_path, "Portal")
            self.portal_status_label.config(text=f"{selected_mod} has been set as active")
        
        self.update_portal_dropdown()
    
    def change_companion_cube(self):
        selected_mod = self.cube_combobox.get()
        if not selected_mod:
            return

        active_mod = CustomFiles.get_active_companion_cube_mod(self.custom_folder_path)
        if selected_mod == 'NONE':
            if active_mod:
                source_path = os.path.join(self.custom_folder_path, active_mod)
                dest_path = os.path.join(self.portal_manager_path, 'CompanionCubes', active_mod)
                CustomFiles.move_folder(source_path, dest_path)
                self.cube_status_label.config(text="Companion Cube mod removed")
            self.update_companion_cube_dropdown()
            return

        if active_mod:
            source_path = os.path.join(self.custom_folder_path, active_mod)
            dest_path = os.path.join(self.portal_manager_path, 'CompanionCubes', active_mod)
            CustomFiles.move_folder(source_path, dest_path)

        source_path = os.path.join(self.portal_manager_path, 'CompanionCubes', selected_mod)
        dest_path = os.path.join(self.custom_folder_path, selected_mod)
        if CustomFiles.move_folder(source_path, dest_path):
            CustomFiles.create_pm_info_file(dest_path, "CompanionCube")
            self.cube_status_label.config(text=f"{selected_mod} has been set as active")

        self.update_companion_cube_dropdown()

    def update_companion_cube_dropdown(self):
        if not hasattr(self, 'cube_combobox'):
            return

        folders = CustomFiles.get_companion_cube_folders(self.portal_manager_path)
        active_mod = CustomFiles.get_active_companion_cube_mod(self.custom_folder_path)

        if active_mod and active_mod not in folders:
            folders.append(active_mod)

        self.cube_combobox['values'] = ['NONE'] + folders

        if active_mod:
            self.cube_combobox.set(active_mod)
        else:
            self.cube_combobox.set('NONE')

    def change_turret(self):
        selected_mod = self.turret_combobox.get()
        if not selected_mod:
            return

        active_mod = CustomFiles.get_active_turret_mod(self.custom_folder_path)
        if selected_mod == 'NONE':
            if active_mod:
                source_path = os.path.join(self.custom_folder_path, active_mod)
                dest_path = os.path.join(self.portal_manager_path, 'Turrets', active_mod)
                CustomFiles.move_folder(source_path, dest_path)
                self.turret_status_label.config(text="Turret mod removed")
            self.update_turret_dropdown()
            return

        if active_mod:
            source_path = os.path.join(self.custom_folder_path, active_mod)
            dest_path = os.path.join(self.portal_manager_path, 'Turrets', active_mod)
            CustomFiles.move_folder(source_path, dest_path)

        source_path = os.path.join(self.portal_manager_path, 'Turrets', selected_mod)
        dest_path = os.path.join(self.custom_folder_path, selected_mod)
        if CustomFiles.move_folder(source_path, dest_path):
            CustomFiles.create_pm_info_file(dest_path, "Turret")
            self.turret_status_label.config(text=f"{selected_mod} has been set as active")

        self.update_turret_dropdown()

    def update_turret_dropdown(self):
        if not hasattr(self, 'turret_combobox'):
            return

        folders = CustomFiles.get_turret_folders(self.portal_manager_path)
        active_mod = CustomFiles.get_active_turret_mod(self.custom_folder_path)

        if active_mod and active_mod not in folders:
            folders.append(active_mod)

        self.turret_combobox['values'] = ['NONE'] + folders

        if active_mod:
            self.turret_combobox.set(active_mod)
        else:
            self.turret_combobox.set('NONE')

    def change_chell(self):
        selected_mod = self.chell_combobox.get()
        if not selected_mod:
            return

        active_mod = CustomFiles.get_active_chell_mod(self.custom_folder_path)
        if selected_mod == 'NONE':
            if active_mod:
                CustomFiles.move_folder(
                    os.path.join(self.custom_folder_path, active_mod),
                    os.path.join(self.portal_manager_path, 'Chell', active_mod)
                )
                self.chell_status_label.config(text="Chell mod removed")
            self.update_chell_dropdown()
            return

        if active_mod:
            CustomFiles.move_folder(
                os.path.join(self.custom_folder_path, active_mod),
                os.path.join(self.portal_manager_path, 'Chell', active_mod)
            )

        dest_path = os.path.join(self.custom_folder_path, selected_mod)
        if CustomFiles.move_folder(os.path.join(self.portal_manager_path, 'Chell', selected_mod), dest_path):
            CustomFiles.create_pm_info_file(dest_path, "Chell")
            self.chell_status_label.config(text=f"{selected_mod} has been set as active")

        self.update_chell_dropdown()

    def update_chell_dropdown(self):
        if not hasattr(self, 'chell_combobox'):
            return

        folders = CustomFiles.get_chell_folders(self.portal_manager_path)
        active_mod = CustomFiles.get_active_chell_mod(self.custom_folder_path)

        if active_mod and active_mod not in folders:
            folders.append(active_mod)

        self.chell_combobox['values'] = ['NONE'] + folders
        self.chell_combobox.set(active_mod if active_mod else 'NONE')

    def change_glados(self):
        selected_mod = self.glados_combobox.get()
        if not selected_mod:
            return

        active_mod = CustomFiles.get_active_glados_mod(self.custom_folder_path)
        if selected_mod == 'NONE':
            if active_mod:
                CustomFiles.move_folder(
                    os.path.join(self.custom_folder_path, active_mod),
                    os.path.join(self.portal_manager_path, 'Glados', active_mod)
                )
                self.glados_status_label.config(text="Glados mod removed")
            self.update_glados_dropdown()
            return

        if active_mod:
            CustomFiles.move_folder(
                os.path.join(self.custom_folder_path, active_mod),
                os.path.join(self.portal_manager_path, 'Glados', active_mod)
            )

        dest_path = os.path.join(self.custom_folder_path, selected_mod)
        if CustomFiles.move_folder(os.path.join(self.portal_manager_path, 'Glados', selected_mod), dest_path):
            CustomFiles.create_pm_info_file(dest_path, "Glados")
            self.glados_status_label.config(text=f"{selected_mod} has been set as active")

        self.update_glados_dropdown()

    def update_glados_dropdown(self):
        if not hasattr(self, 'glados_combobox'):
            return

        folders = CustomFiles.get_glados_folders(self.portal_manager_path)
        active_mod = CustomFiles.get_active_glados_mod(self.custom_folder_path)

        if active_mod and active_mod not in folders:
            folders.append(active_mod)

        self.glados_combobox['values'] = ['NONE'] + folders
        self.glados_combobox.set(active_mod if active_mod else 'NONE')

    def update_portal_gun_dropdown(self):
        if not hasattr(self, 'gun_model_combobox'):
            return
        folders = CustomFiles.get_portal_gun_folders(self.portal_manager_path)
        active_mod = CustomFiles.get_active_portal_gun_mod(self.custom_folder_path)
        if active_mod and active_mod not in folders:
            folders.append(active_mod)
        self.gun_model_combobox['values'] = ['NONE'] + folders
        if active_mod:
            self.gun_model_combobox.set(active_mod)
        else:
            self.gun_model_combobox.set('NONE')
    
    def update_portal_dropdown(self):
        if not hasattr(self, 'portal_combobox'):
            return
        folders = CustomFiles.get_portal_folders(self.portal_manager_path)
        active_mod = CustomFiles.get_active_portal_mod(self.custom_folder_path)
        if active_mod and active_mod not in folders:
            folders.append(active_mod)
        self.portal_combobox['values'] = ['NONE'] + folders
        if active_mod:
            self.portal_combobox.set(active_mod)
        else:
            self.portal_combobox.set('NONE')
    
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
        self.portal_manager_path = CustomFiles.get_portal_manager_path(portal_dir_path)
        self.custom_folder_path = CustomFiles.get_custom_folder_path(portal_dir_path)
        self.update_portal_gun_dropdown()
        self.update_portal_dropdown()
        self.update_companion_cube_dropdown()
        self.update_turret_dropdown()
        self.update_chell_dropdown()
        self.update_glados_dropdown()
    
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
