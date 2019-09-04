def only_current_portal(map_path):
    with open(map_path+".bsp", "rb") as f:  # bsps are binary files
        bytes1 = f.read() # stores all bytes in bytes1 variable (named like that to not interfere with builtin names
        # get offset (position of entity block begin) and length of entity block -> see bsp quake 2 format documentation
        offset_vis = int.from_bytes(bytes1[32:36], byteorder='little', signed=False)
        length_vis = int.from_bytes(bytes1[36:40], byteorder='little', signed=False)
        n_clusters = int.from_bytes(bytes1[offset_vis:offset_vis+4], byteorder='little', signed=False)
        print(n_clusters)