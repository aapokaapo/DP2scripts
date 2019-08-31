from Lightmap_Only import white_texture as wt

if __name__ == '__main__':
    path_to_pball = "/home/lennart/paintball2/Paintball2-wine/pball"
    map_path = "/maps/wipa.bsp"
    white_texture_path = "/textures/tw-scripts"
    texture_name = "/white.png"
    texture_size = 16
    new_map_path = "/maps/light_kungfu.bsp"
    # Create white texture
    # wt.create_white_texture(path_to_pball+white_texture_path, texture_name, texture_size)
    #
    # # Change all texture paths and save edited map
    # wt.change_texture_paths(path_to_pball+map_path, "tw-scripts/white")
    # old_textures = wt.insert_to_texture_paths(path_to_pball+map_path, "twscripts/", "gs_", "gs_")
    # print(old_textures)
    # wt.create_grayscale_textures(path_to_pball, old_textures, "/textures/twscripts/", "gs_")

    wt.make_gs_lightmaps(path_to_pball, map_path, "gsl_")