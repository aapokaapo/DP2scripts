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
    for lines in ent_lines:
        for line in lines:
            print(line)
        print()

def get_old_entities(path):
    print()

def remove_spawns(entities):
    print()

def worldspawn_to_dm(entities):
    print()

def save_ent(entities, path):
    print()
