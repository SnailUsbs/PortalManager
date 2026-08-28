import os

DEFAULT_MAPS = {
    "testchmb_a_00",
    "testchmb_a_01",
    "testchmb_a_02",
    "testchmb_a_03",
    "testchmb_a_04",
    "testchmb_a_05",
    "testchmb_a_06",
    "testchmb_a_07",
    "testchmb_a_08",
    "testchmb_a_09",
    "testchmb_a_10",
    "testchmb_a_11",
    "testchmb_a_13",
    "testchmb_a_14",
    "testchmb_a_15",
    "testchmb_a_08_advanced",
    "testchmb_a_09_advanced",
    "testchmb_a_10_advanced",
    "testchmb_a_11_advanced",
    "testchmb_a_13_advanced",
    "testchmb_a_14_advanced",
    "escape_00",
    "escape_01",
    "escape_02",
    "d2_coast_02",
    "background1",
    "background2",
}

CUSTOM_MAPS = []

def scan_custom_maps(portal_dir_path):
    global CUSTOM_MAPS
    CUSTOM_MAPS = []

    maps_path = os.path.join(portal_dir_path, 'portal', 'maps')
    if not os.path.exists(maps_path):
        return

    for filename in os.listdir(maps_path):
        if filename.endswith('.bsp'):
            map_name = filename[:-4]
            if map_name not in DEFAULT_MAPS:
                CUSTOM_MAPS.append(map_name)
