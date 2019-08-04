from transparent_map import flag_changing as fc

if __name__ == '__main__':
    path_to_pball = "/home/lennart/paintball2/Paintball2-wine/pball"
    map_path = "/maps/hca_fort.bsp"

    flags = {"light": 1,
             "slick": 2,
             "sky": 4,
             "warp": 8,
             "trans33": 16,
             "trans66": 32,
             "flowing": 64,
             "nodraw": 128,
             "hint": 256,
             "skip": 512}

    fc.list_flags(path_to_pball + map_path)
    fc.set_flags(path_to_pball+map_path, flags["trans33"], path_to_pball+"/maps/trans_hca_fort.bsp")
