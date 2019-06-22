from DP2RadarGen.Brush import Brush as Brush

if __name__ == '__main__':
    path = "maps/construction_final.map"
    with open(path, 'r') as file:
        brushes = list()
        currentBrush = list()
        isBrush = False
        firstBracket = True
        for line in file:
            if line.startswith("{"):
                if firstBracket:
                    firstBracket = False
                else:
                    print("here")
                    isBrush = True
            if isBrush and not firstBracket:
                # print(line)
                currentBrush.append(line)
            if line.startswith("}"):
                print("!")
                isBrush = False
                brushes.append(currentBrush)
                currentBrush = list()
    print(len(brushes))
    print(len(brushes[0]))
    cleanBrushes = list()
    for i, brush in enumerate(brushes):
        cleanBrush = list()
        for idx, line in enumerate(brush[1:-1]):
            if line.startswith("(") and not "pball/hint" in line and not "pball/clip" in line:
                print(f"big idx: {i}, small idx: {idx}, line: {line}")
                cleanBrush.append(line)
        if not len(cleanBrush)==0:
            cleanBrushes.append(cleanBrush)
        cleanBrush = list()
    brush_list = list()
    for brush in cleanBrushes:
        brush_list.append(Brush(brush))
    for brush in brush_list:
        print("-----")
        for plane in brush.brush:
            print(plane)
