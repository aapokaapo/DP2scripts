from Ent_Gen import entity_generator as ent_gen

if __name__ == '__main__':
    log_name = "DM1.txt" # Name of condump file
    path = "path/to/pball"
    map = "/maps/italy" # map_name path relative to path variable above
    mapname = "italy" # map_name name to search for inside of log
    message_attachment = "\\n- TW-DM Version" # Attachment to worldspawn message (map_name loading message)

    spawns = ent_gen.get_spawns(path+"/"+log_name, mapname)  # gets positions entered ingame and saved in log_name
    old_entities = ent_gen.get_old_entities(path+map+".bsp", message_attachment) # gets and edits preexisting entities
    ent_gen.save_ent(old_entities, spawns, path+map+".ent")  # combines and saves old and new entities

