from Ent_Gen import entity_generator as ent_gen

if __name__ == '__main__':
    log_name = "DM1.txt"
    path = "/home/lennart/paintball2/Paintball2-wine/pball"
    map = "/beta/duck_fix_b6"
    mapname = "duck_fix_b6"
    spawns = ent_gen.get_spawns(path+"/"+log_name, mapname)
    # old_entities = ent_gen.get_old_entities(map)
    # new_entities = ent_gen.remove_spawns(old_entities)
    # new_entities_dm = ent_gen.worldspawn_to_dm(new_entities)
    # ent_gen.save_ent(new_entities_dm, path+"/maps"+map+".ent")