from Ent_Gen import entity_generator as ent_gen

if __name__ == '__main__':
    log_name = "DM1.txt"
    path = "/home/lennart/paintball2/Paintball2-wine/pball"
    map = "/maps/hca_fort"
    mapname = "hca_fort"
    message_attachment = "\\n- TW-DM Version"
    spawns = ent_gen.get_spawns(path+"/"+log_name, mapname)
    old_entities = ent_gen.get_old_entities(path+map+".bsp", message_attachment)
    ent_gen.save_ent(old_entities, spawns, path+map+".ent")