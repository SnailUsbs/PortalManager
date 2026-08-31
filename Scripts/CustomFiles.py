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
    return os.path.join(_resolve_portal_subdir(portal_dir_path), 'PortalManager')


def get_custom_folder_path(portal_dir_path):
    return os.path.join(_resolve_portal_subdir(portal_dir_path), 'custom')


def get_mod_folders(portal_manager_path, subfolder):
    if not portal_manager_path:
        return []
    path = os.path.join(portal_manager_path, subfolder)
    if not os.path.exists(path):
        return []
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]


def get_active_mod(custom_folder_path, mod_type):
    if not custom_folder_path or not os.path.exists(custom_folder_path):
        return None
    for folder in os.listdir(custom_folder_path):
        if not os.path.isdir(os.path.join(custom_folder_path, folder)):
            continue
        pm_info_path = os.path.join(custom_folder_path, folder, 'PMInfo.txt')
        if os.path.exists(pm_info_path):
            try:
                with open(pm_info_path, 'r') as f:
                    if any(line.strip() == f'- Mod Type: {mod_type}' for line in f):
                        return folder
            except Exception:
                pass
    return None


def get_portal_gun_folders(portal_manager_path):
    return get_mod_folders(portal_manager_path, 'PortalGuns')

def get_portal_folders(portal_manager_path):
    return get_mod_folders(portal_manager_path, 'Portals')

def get_companion_cube_folders(portal_manager_path):
    return get_mod_folders(portal_manager_path, 'CompanionCubes')

def get_turret_folders(portal_manager_path):
    return get_mod_folders(portal_manager_path, 'Turrets')

def get_chell_folders(portal_manager_path):
    return get_mod_folders(portal_manager_path, 'Chell')

def get_glados_folders(portal_manager_path):
    return get_mod_folders(portal_manager_path, 'Glados')

def get_beans_folders(portal_manager_path):
    return get_mod_folders(portal_manager_path, 'Beans')

def get_incinerator_folders(portal_manager_path):
    return get_mod_folders(portal_manager_path, 'Incinerator')


def get_active_portal_gun_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, 'Portal Gun Model/Texture')

def get_active_portal_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, 'Portal')

def get_active_companion_cube_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, 'CompanionCube')

def get_active_turret_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, 'Turret')

def get_active_chell_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, 'Chell')

def get_active_glados_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, 'Glados')

def get_active_beans_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, 'Beans')

def get_active_incinerator_mod(custom_folder_path):
    return get_active_mod(custom_folder_path, 'Incinerator')


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


def create_pm_info_file(folder_path, mod_type='Portal Gun Model/Texture'):
    pm_info_path = os.path.join(folder_path, 'PMInfo.txt')
    if not os.path.exists(pm_info_path):
        with open(pm_info_path, 'w') as f:
            f.write(f'- Mod Type: {mod_type}\n')
