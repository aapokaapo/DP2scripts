from vis_fooling import vis_editing as vis

if __name__ == '__main__':
    path = "/home/lennart/paintball2/Paintball2-wine/pball"
    map = "/maps/italy" # map_name path relative to path variable above

    vis.only_current_portal(path+map)