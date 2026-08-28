import os
import shutil


def _resolve_portal_subdir(portal_dir_path):
    candidate = os.path.join(portal_dir_path, 'portal')
    if os.path.isdir(candidate):
        return candidate

    if os.path.basename(portal_dir_path).lower() == 'portal':
        return portal_dir_path

    return candidate


def get_portal_manager_path(portal_dir_path):
    portal_subdir = _resolve_portal_subdir(portal_dir_path)
    return os.path.join(portal_subdir, 'PortalManager')


def get_portal_gun_folders(portal_manager_path):
    if portal_manager_path and os.path.exists(portal_manager_path):
        portal_gun_path = os.path.join(portal_manager_path, 'PortalGuns')
        if os.path.exists(portal_gun_path):
            folders = [f for f in os.listdir(portal_gun_path) 
                      if os.path.isdir(os.path.join(portal_gun_path, f))]
            return folders
    return []


def get_portal_folders(portal_manager_path):
    if portal_manager_path and os.path.exists(portal_manager_path):
        portals_path = os.path.join(portal_manager_path, 'Portals')
        if os.path.exists(portals_path):
            folders = [f for f in os.listdir(portals_path) 
                      if os.path.isdir(os.path.join(portals_path, f))]
            return folders
    return []


def get_custom_folder_path(portal_dir_path):
    portal_subdir = _resolve_portal_subdir(portal_dir_path)
    return os.path.join(portal_subdir, 'custom')


def get_active_mod(custom_folder_path, mod_type):
    if not custom_folder_path or not os.path.exists(custom_folder_path):
        return None
    
    subfolders = [f for f in os.listdir(custom_folder_path) 
                  if os.path.isdir(os.path.join(custom_folder_path, f))]
    
    for folder in subfolders:
        pm_info_path = os.path.join(custom_folder_path, folder, 'PMInfo.txt')
        if os.path.exists(pm_info_path):
            try:
                with open(pm_info_path, 'r') as f:
                    content = f.read()
                    if any(line.strip() == f'- Mod Type: {mod_type}' for line in content.splitlines()):
                        return folder
            except Exception:
                pass
    
    return None


def get_active_portal_gun_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, "Portal Gun Model/Texture")


def get_active_portal_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, "Portal")


def get_companion_cube_folders(portal_manager_path):
    if portal_manager_path and os.path.exists(portal_manager_path):
        cubes_path = os.path.join(portal_manager_path, 'CompanionCubes')
        if os.path.exists(cubes_path):
            folders = [f for f in os.listdir(cubes_path)
                      if os.path.isdir(os.path.join(cubes_path, f))]
            return folders
    return []


def get_active_companion_cube_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, "CompanionCube")


def get_turret_folders(portal_manager_path):
    if portal_manager_path and os.path.exists(portal_manager_path):
        turrets_path = os.path.join(portal_manager_path, 'Turrets')
        if os.path.exists(turrets_path):
            folders = [f for f in os.listdir(turrets_path)
                      if os.path.isdir(os.path.join(turrets_path, f))]
            return folders
    return []


def get_active_turret_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, "Turret")


def get_chell_folders(portal_manager_path):
    if portal_manager_path and os.path.exists(portal_manager_path):
        chell_path = os.path.join(portal_manager_path, 'Chell')
        if os.path.exists(chell_path):
            folders = [f for f in os.listdir(chell_path)
                      if os.path.isdir(os.path.join(chell_path, f))]
            return folders
    return []


def get_active_chell_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, "Chell")


def get_glados_folders(portal_manager_path):
    if portal_manager_path and os.path.exists(portal_manager_path):
        glados_path = os.path.join(portal_manager_path, 'Glados')
        if os.path.exists(glados_path):
            folders = [f for f in os.listdir(glados_path)
                      if os.path.isdir(os.path.join(glados_path, f))]
            return folders
    return []


def get_active_glados_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, "Glados")


def move_folder(source_path, dest_path):
    try:
        if os.path.exists(source_path):
            if os.path.exists(dest_path):
                if os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)
                else:
                    os.remove(dest_path)
            shutil.move(source_path, dest_path)
            return True
    except Exception:
        pass
    return False


def create_pm_info_file(folder_path, mod_type="Portal Gun Model/Texture"):
    pm_info_path = os.path.join(folder_path, 'PMInfo.txt')
    if not os.path.exists(pm_info_path):
        with open(pm_info_path, 'w') as f:
            f.write(f"- Mod Type: {mod_type}\n")
