from Lightmap_Only import white_texture as wt

if __name__ == '__main__':
    path_to_pball = "/home/lennart/paintball2/Paintball2-wine/pball"
    white_texture_path = "/textures/tw-scripts"
    texture_name = "/white.png"
    texture_size = 16
    map_path = "/maps/wipa.bsp"
    new_map_path = "/maps/light_kungfu.bsp"
    # Create white texture
    wt.create_white_texture(path_to_pball+white_texture_path, texture_name, texture_size)

    # Change all texture paths and save edited map
    wt.change_texture_paths(path_to_pball+map_path, "tw-scripts/white")