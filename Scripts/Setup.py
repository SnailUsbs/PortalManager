import os
import sys

sys.path.append(os.path.dirname(__file__))
import CustomFiles

SUBFOLDERS = ['PortalGuns', 'Portals', 'CompanionCubes', 'Turrets', 'Chell', 'Glados', 'Beans', 'Incinerator']


def get_sourcemods_path(portal_dir_path):
    steamapps = os.path.dirname(os.path.dirname(os.path.abspath(portal_dir_path)))
    return os.path.join(steamapps, 'sourcemods')


def run_setup(portal_dir_path):
    portal_manager_path = CustomFiles.get_portal_manager_path(portal_dir_path)
    custom_folder_path = CustomFiles.get_custom_folder_path(portal_dir_path)

    try:
        os.makedirs(portal_manager_path, exist_ok=True)
    except Exception:
        pass

    for subfolder in SUBFOLDERS:
        path = os.path.join(portal_manager_path, subfolder)
        try:
            os.makedirs(path, exist_ok=True)
        except Exception:
            pass

    try:
        os.makedirs(custom_folder_path, exist_ok=True)
    except Exception:
        pass

    try:
        os.makedirs(get_sourcemods_path(portal_dir_path), exist_ok=True)
    except Exception:
        pass
