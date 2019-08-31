import os
from Ent_Gen import entity_generator as ent_gen

if __name__ == '__main__':
    log_name = "DM1.txt" # Name of condump file
    path = "/home/lennart/paintball2/Paintball2-wine/pball"
    loc_path="/home/lennart/paintball2/Paintball2-wine/locs/"
    map = "/maps/italy" # map_name path relative to path variable above
    mapname = "italy" # map_name name to search for inside of log
    message_attachment = "\\n- TW-DM Version" # Attachment to worldspawn message (map_name loading message)

    # TODO: get existing spawns from map.ent or .bsp
    # TODO: get modified spawns from log
    # TODO: modify .loc to remove unsuccessfully placed spawns and to match exact spawn position

    # if os.path.isfile(path+map+".ent"):
    #     old_spawns = ent_gen.get_spawns_from_ent(path+map+".ent")
    spawns, remove_spawns, keys = ent_gen.get_spawns_from_log(path+"/"+log_name, mapname, loc_path)  # gets positions entered ingame and saved in log_name
    print(spawns)
    # print(spawns)
    old_entities, is_ent = ent_gen.get_old_entities(path+map, message_attachment, remove_spawns, loc_path, mapname, keys) # gets and edits preexisting entities

    ent_gen.save_ent(old_entities, spawns, path+map+".ent")  # combines and saves old and new entities
