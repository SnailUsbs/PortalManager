import os
import shutil
import sys

sys.path.append(os.path.dirname(__file__))
import Setup

SOURCEMODS = []


def scan_sourcemods(portal_dir_path):
    global SOURCEMODS
    SOURCEMODS = []

    sourcemods_path = Setup.get_sourcemods_path(portal_dir_path)
    if not os.path.exists(sourcemods_path):
        return

    SOURCEMODS = [
        f for f in os.listdir(sourcemods_path)
        if os.path.isdir(os.path.join(sourcemods_path, f))
    ]


def get_steam_app_id(mod_folder_path):
    gameinfo_path = os.path.join(mod_folder_path, 'gameinfo.txt')
    if not os.path.exists(gameinfo_path):
        return None
    try:
        with open(gameinfo_path, 'r', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                if i == 21:
                    parts = line.split()
                    if len(parts) >= 2 and parts[0].lower() == 'steamappid':
                        return parts[1]
                    break
    except Exception:
        pass
    return None


def get_portal1_mods(portal_dir_path):
    sourcemods_path = Setup.get_sourcemods_path(portal_dir_path)
    if not os.path.exists(sourcemods_path):
        return []
    return [
        f for f in os.listdir(sourcemods_path)
        if os.path.isdir(os.path.join(sourcemods_path, f))
        and get_steam_app_id(os.path.join(sourcemods_path, f)) == '400'
    ]


def add_sourcemod(portal_dir_path, mod_folder):
    sourcemods_path = Setup.get_sourcemods_path(portal_dir_path)
    mod_name = os.path.basename(mod_folder)
    dest = os.path.join(sourcemods_path, mod_name)
    try:
        shutil.move(mod_folder, dest)
        scan_sourcemods(portal_dir_path)
        return True
    except Exception:
        return False


def delete_sourcemod(portal_dir_path, mod_name):
    sourcemods_path = Setup.get_sourcemods_path(portal_dir_path)
    mod_path = os.path.join(sourcemods_path, mod_name)
    if os.path.isdir(mod_path):
        shutil.rmtree(mod_path)
    scan_sourcemods(portal_dir_path)
