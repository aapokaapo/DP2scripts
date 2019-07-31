from PIL import Image
import os
import struct

def create_white_texture(path, name, size) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
    img = Image.new('RGB', (size, size), (255, 255, 255))
    img.save(path+name, "PNG")
    print("saved that image")


def change_texture_paths(map_path, tex_path) -> None:
    b = tex_path.encode()
    c = b"\x00"*(32-len(b))
    tex_bytes = b+c
    print(type(b))
    print(tex_bytes)
    with open(map_path, "rb") as f:  # bsps are binary files
        bytes1 = f.read() # stores all bytes in bytes1 variable (named like that to not interfere with builtin names
        # get offset (position of entity block begin) and length of entity block -> see bsp quake 2 format documentation
        offset = int.from_bytes(bytes1[48:52], byteorder='little', signed=False)
        length = int.from_bytes(bytes1[52:56], byteorder='little', signed=False)
        print(len(bytes1))
        for i in range(int(length/76)):
            a = (bytes1[offset+76*i+40:offset+76*i+72])
            a = [x for x in a if x]
            # try:
            # print(len(a))
            # print(a)
            # a.decode("ascii", "ignore")
            # print(struct.pack("b" * len(a), *a).decode('ascii', "ignore"))

            bytes1 = bytes1[:offset+76*i+40]+tex_bytes+bytes1[offset + 76 * i + 72:]
            a = (bytes1[offset+76*i+40:offset+76*i+72])
            a = [x for x in a if x]
            # print(struct.pack("b" * len(a), *a).decode('ascii', "ignore"))
            # bytes1[offset + 76 * i + 40:offset + 76 * i + 72] = bytes(tex_bytes)
            # except:
                # hg = 0
        # 60- 72
        with open("/home/lennart/paintball2/Paintball2-wine/pball/maps/light_wipa.bsp", "w+b") as g:  # bsps are binary files
            g.write(bytes1)
        print(length)
        read_textures("/home/lennart/paintball2/Paintball2-wine/pball/maps/light_wipa.bsp", tex_path)
    print()


def read_textures(map_path, tex_path) -> None:
    with open(map_path, "rb") as f:  # bsps are binary files
        bytes1 = f.read() # stores all bytes in bytes1 variable (named like that to not interfere with builtin names
        # get offset (position of entity block begin) and length of entity block -> see bsp quake 2 format documentation
        offset = int.from_bytes(bytes1[48:52], byteorder='little', signed=False)
        length = int.from_bytes(bytes1[52:56], byteorder='little', signed=False)
        for i in range(int(length/76)):
            a = (bytes1[offset+76*i+40:offset+76*i+72])
            a = [x for x in a if x]
            print(struct.pack("b" * len(a), *a).decode('ascii', "ignore"))
        print(offset)
        print(length)
    print()