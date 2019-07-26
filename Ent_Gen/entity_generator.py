def get_spawns(path, map):
    line_starts=["Location", "Old Position", "Position", "Angles", "_sun_angle"]
    lines = list()
    with open(path) as f:
        for line in f:
            # content = f.readlines()
            lines.append(line.replace("\n", ""))
    ent_lines = list()
    for idx, line in enumerate(lines):
        if map in line:
            matching = True
            linez = list()
            for i in range(1,5):
                if not lines[idx+i].startswith(line_starts[i-1]):
                    matching = False
            if matching:
                for i in range(5):
                    linez.append(lines[idx+i])
                ent_lines.append(linez)
    spawns = list()
    print(ent_lines)
    for lines in ent_lines:
        local_spawns = list()
        local_spawns.append('{')
        local_spawns.append('"teamnumber" "0"')
        local_spawns.append('"classname" "info_player_deathmatch"')

        id=lines[1].split(" ")[1].replace("'", "")
        rotation=round(float(lines[4].split(" ")[1]))+180
        coordinates = lines[3].split(" ")
        origin = [round(float(coordinates[i])) for i in range(1,4)]
        origin = f"{origin[0]} {origin[1]} {origin[2]}"
        print(f"id: {id}, rotation:{rotation}, origin: {origin}")
        local_spawns.append(f'"origin" "{origin}"')
        local_spawns.append(f'"angle" "{rotation}"')
        local_spawns.append(f'"_loc_id" "{id}"')
        local_spawns.append('}')
        spawns.append(local_spawns)
        for line in lines:
            print(line)
        print()
        print(spawns)
    return spawns


def get_old_entities(path, message_attachment):
    with open(path, "rb") as f:
        bytes1 = f.read()
        offset = int.from_bytes(bytes1[8:12], byteorder='little', signed=False)
        length = int.from_bytes(bytes1[12:16], byteorder='little', signed=False)
        lines = (bytes1[offset:offset+length-1].decode("ascii", "ignore"))
        lines = lines.split("\n")
        print(lines)
        print(len(lines))
        ents = list()
        localents = list()

        for i in range(len(lines)):
            localents.append(lines[i])
            if lines[i] == "}":
                ents.append(localents)
                localents = list()

        contains_gamemode = False
        for idx, line in enumerate(ents[0]):
            if line.startswith('"message"'):
                ents[0][idx] = line[0:len(line)-1] + message_attachment + '"'
            elif line.startswith('"gamemode"'):
                ents[0][idx] = line[0:12]+'1"'
                contains_gamemode = True
            elif line.startswith('"teamnumber"'):
                ents[0][idx] = ""
            elif line.startswith('"maxteams"'):
                ents[0][idx] = ""
            elif line.startswith('"team'):
                ents[0][idx] = ""
        if not contains_gamemode:
            ents[0].append(ents[0][len(ents[0])-1])
            ents[0][len(ents[0])-2] = '"gamemode" "1"'
        ents[0] = [x for x in ents[0] if x]
        ents = [x for x in ents if not '"classname" "info_player_deathmatch"' in x]
        print(ents)
        return ents


def save_ent(old_ents, new_ents, path):
    with open(path, "w") as f:
        for ent in old_ents:
            for line in ent:
                f.write(line+"\n")
        for ent in new_ents:
            for line in ent:
                f.write(line+"\n")
