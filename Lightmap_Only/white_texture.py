from PIL import Image, WalImageFile
import os
import struct
import PIL.ImageOps
import math
# import numpy as np

def make_gs_lightmaps(pball_path, map_path, prefix_map):
    with open(pball_path+map_path, "rb") as f:  # bsps are binary files
        bytes1 = f.read()  # stores all bytes in bytes1 variable (named like that to not interfere with builtin names
        # get offset (position of entity block begin) and length of entity block -> see bsp quake 2 format documentation
        offset_faces = int.from_bytes(bytes1[56:60], byteorder='little', signed=False)
        length_faces = int.from_bytes(bytes1[60:64], byteorder='little', signed=False)

        offset_verts = int.from_bytes(bytes1[24:28], byteorder='little', signed=False)
        length_verts = int.from_bytes(bytes1[28:32], byteorder='little', signed=False)
        vertices = list()
        for i in range(int(length_verts / 12)):
            (vert_x,) = struct.unpack('<f', (bytes1[offset_verts + 12 * i + 0:offset_verts + 12 * i + 4]))
            (vert_y,) = struct.unpack('<f', (bytes1[offset_verts + 12 * i + 4:offset_verts + 12 * i + 8]))
            (vert_z,) = struct.unpack('<f', (bytes1[offset_verts + 12 * i + 8:offset_verts + 12 * i + 12]))
            vertices.append([vert_x, vert_y, vert_z])
            # print(f"{vert_x} - {vert_y} - {vert_z}")

        offset_edges = int.from_bytes(bytes1[96:100], byteorder='little', signed=False)
        length_edges = int.from_bytes(bytes1[100:104], byteorder='little', signed=False)
        edges = list()
        for i in range(int(length_edges / 4)):  # texture information lump is 76 bytes large
            vert_1 = int.from_bytes(bytes1[offset_edges + 4 * i + 0:offset_edges + 4 * i + 2], byteorder='little', signed=False)
            vert_2 = int.from_bytes(bytes1[offset_edges + 4 * i + 2:offset_edges + 4 * i + 4], byteorder='little', signed=False)
            edges.append([vertices[vert_1], vertices[vert_2]])

        offset_face_edges = int.from_bytes(bytes1[104:108], byteorder='little', signed=False)
        length_face_edges = int.from_bytes(bytes1[108:112], byteorder='little', signed=False)
        face_edges = list()
        for i in range(int(length_face_edges / 4)):  # texture information lump is 76 bytes large
            edge_index = int.from_bytes(bytes1[offset_face_edges + 4 * i + 0:offset_face_edges + 4 * i + 4], byteorder='little', signed=True)
            if edge_index > 0:
                face_edges.append([edges[abs(edge_index)][0], edges[abs(edge_index)][1]])
            elif edge_index < 0:
                face_edges.append([edges[abs(edge_index)][1], edges[abs(edge_index)][0]])

        offset_textures = int.from_bytes(bytes1[48:52], byteorder='little', signed=False)
        length_textures = int.from_bytes(bytes1[52:56], byteorder='little', signed=False)

        # texture_list = list()
        for i in range(int(length_textures/76)):
            tex = (bytes1[offset_textures+76*i+40:offset_textures+76*i+72])
            tex = [x for x in tex if x]
            tex_name = struct.pack("b" * len(tex), *tex).decode('ascii', "ignore")
            print(tex_name)
            # texture_list.append(tex_name)

        faces = list()
        # tex_ids = list()
        # texture_list_cleaned=list(dict.fromkeys(texture_list))
        #
        # average_colors=list()
        # for texture in texture_list_cleaned:
        #     color = (0, 0, 0)
        #     if os.path.isfile(pball_path+"/textures/"+texture+".png"):
        #         img = Image.open((pball_path+"/textures/"+texture+".png"))
        #         img2 = img.resize((1, 1))
        #
        #         color = img2.getpixel((0, 0))
        #
        #     elif os.path.isfile(pball_path+"/textures/"+texture+".jpg"):
        #         img = Image.open((pball_path+"/textures/"+texture+".jpg"))
        #         img.save("1.png")
        #         img2 = img.resize((1, 1))
        #         # break
        #
        #         color = img2.getpixel((0, 0))
        #         # print(f"texture: {texture} - color: {color}")
        #
        #     elif os.path.isfile(pball_path + "/textures/" + texture + ".tga"):
        #         img = Image.open((pball_path + "/textures/" + texture + ".tga"))
        #         img2 = img.resize((1, 1))
        #
        #         color = img2.getpixel((0, 0))
        #         # print(f"texture: {texture} - color: {color}")
        #
        #     elif os.path.isfile(pball_path+"/textures/"+texture+".wal"):
        #         with open("pb2e.pal", "r") as pal:
        #             conts = (pal.read().split("\n")[3:])
        #             conts = [b.split(" ") for b in conts]
        #             conts = [c for b in conts for c in b]
        #             conts.pop(len(conts)-1)
        #             conts=list(map(int, conts))
        #             img3 = WalImageFile.open((pball_path+"/textures/"+texture+".wal"))
        #             img3.putpalette(conts)
        #             img3=img3.convert("RGBA")
        #             print(img3.mode)
        #
        #             img2 = img3.resize((1, 1))
        #
        #             color = img2.getpixel((0, 0))
        #     print(f"texture: {texture} - color: {color}")
        #     color_rgb = color[:3]
        #     average_colors.append(color_rgb)
        u_axes = list()
        u_offsets = list()
        v_axes = list()
        v_offsets = list()

        for i in range(int(length_textures/76)):
            (u_x,) = struct.unpack('<f', (bytes1[offset_textures + 76 * i + 0:offset_textures + 76 * i + 4]))
            (u_y,) = struct.unpack('<f', (bytes1[offset_textures + 76 * i + 4:offset_textures + 76 * i + 8]))
            (u_z,) = struct.unpack('<f', (bytes1[offset_textures + 76 * i + 8:offset_textures + 76 * i + 12]))
            (u_offset,) = struct.unpack('<f', (bytes1[offset_textures + 76 * i + 12:offset_textures + 76 * i + 16]))
            (v_x,) = struct.unpack('<f', (bytes1[offset_textures + 76 * i + 16:offset_textures + 76 * i + 20]))
            (v_y,) = struct.unpack('<f', (bytes1[offset_textures + 76 * i + 20:offset_textures + 76 * i + 24]))
            (v_z,) = struct.unpack('<f', (bytes1[offset_textures + 76 * i + 24:offset_textures + 76 * i + 28]))
            (v_offset,) = struct.unpack('<f', (bytes1[offset_textures + 76 * i + 28:offset_textures + 76 * i + 32]))
            u_axes.append([u_x, u_y, u_z])
            u_offsets.append(u_offset)
            v_axes.append([v_x, v_y, v_z])
            v_offsets.append(v_offset)
            # for face in faces:
            #     for vertex in face:
            #         u = vertex[0] * u_x + vertex[1] * u_y + vertex[2] * u_z + u_offset
            # tex = (bytes1[offset_textures+76*i+40:offset_textures+76*i+72])
            # tex = [x for x in tex if x]
            # tex_name = struct.pack("b" * len(tex), *tex).decode('ascii', "ignore")
            # print(tex_name)
        print("u")
        print(u_axes)
        print("v")
        print(v_axes)
        print("u offsets")
        print(u_offsets)
        tex_indices = list()
        lightmap_offsets = list()
        min_u_list = list()
        max_u_list = list()
        min_v_list = list()
        max_v_list = list()
        lightmap_size = list()
        for i in range(int(length_faces / 20)):  # texture information lump is 76 bytes large
            # get sum of flags / transform flag bit field to uint32
            first_edge = (bytes1[offset_faces + 20 * i + 4:offset_faces + 20 * i + 8])
            (num_edges,) = struct.unpack('<H', (bytes1[offset_faces + 20 * i + 8:offset_faces + 20 * i + 10]))
            (tex_index,) = struct.unpack('<H', (bytes1[offset_faces + 20 * i + 10:offset_faces + 20 * i + 12]))
            lightmap_offset = int.from_bytes((bytes1[offset_faces + 20 * i + 13:offset_faces + 20 * i + 17]), byteorder='little', signed=False)
            tex_indices.append(tex_index)
            print(tex_index)
            # print(u_list[tex_index][0])
            lightmap_offsets.append(lightmap_offset)
            # tex_ids.append(texture_list_cleaned.index(texture_list[tex_index]))
            # print(tex_ids[len(tex_ids)-1])
            first_edge = int.from_bytes(first_edge, byteorder='little', signed=True)
            next_edges = list()
            u_list=list()
            v_list=list()
            for j in range(num_edges):
                if face_edges[first_edge+j][0] not in next_edges:
                    vertex = face_edges[first_edge+j][0]
                    print(vertex)
                    next_edges.append(vertex)
                    u_list.append(vertex[0] * u_axes[tex_index][0] + vertex[1] * u_axes[tex_index][1] + vertex[2] * u_axes[tex_index][2] + u_offsets[tex_index])
                    v_list.append(vertex[0] * v_axes[tex_index][0] + vertex[1] * v_axes[tex_index][1] + vertex[2] * v_axes[tex_index][2] + v_offsets[tex_index])
                if face_edges[first_edge + j][1] not in next_edges:
                    vertex = face_edges[first_edge + j][1]
                    next_edges.append(vertex)
                    u_list.append(vertex[0] * u_axes[tex_index][0] + vertex[1] * u_axes[tex_index][1] + vertex[2] * u_axes[tex_index][2] + u_offsets[tex_index])
                    v_list.append(vertex[0] * v_axes[tex_index][0] + vertex[1] * v_axes[tex_index][1] + vertex[2] * v_axes[tex_index][2] + v_offsets[tex_index])
            lightmap_width = math.ceil(max(u_list) / 16) - math.floor(min(u_list) / 16) + 1
            lightmap_height = math.ceil(max(v_list) / 16) - math.floor(min(v_list) / 16) + 1
            lightmap_size.append([lightmap_width, lightmap_height])
            # min_u_list.append(min(u_list))
            # max_u_list.append(max(u_list))
            # min_v_list.append(min(v_list))
            # max_v_list.append(max(v_list))

            faces.append(next_edges)
        offset_lightmaps = int.from_bytes(bytes1[64:68], byteorder='little', signed=False)
        length_lightmaps = int.from_bytes(bytes1[68:72], byteorder='little', signed=False)

        lightmaps = bytes1[offset_lightmaps:offset_lightmaps+length_lightmaps]
        print(len(lightmaps))
        print(length_lightmaps)
        past = 0
        graybytes=b""
        for j in range(int(len(lightmaps)/3)):
            x=lightmaps[3*j]
            y=lightmaps[3*j+1]
            z=lightmaps[3*j+2]
            gray=0.2989*x + 0.5870*y + 0.1140*z
            graybytes+=3*bytes([int(gray)])
            # print(f"{x}, {y}, {z} -> {gray}")
            # print(type(lightmaps[3*j+3]))
            # lightmaps=lightmaps[:3*j]+3*bytes([int(gray)])+lightmaps[3*j+3:]
        lightmaps=graybytes
        # for i in range(len(lightmap_size)):
        #     lightmap = lightmaps[past:past+lightmap_width*lightmap_height]
        #     # print(lightmap)
        #     past = past+lightmap_width*lightmap_height
        #     pixel_list = list()
        #     for j in range(int(len(lightmap)/3)):
        #         # print()
        #         # print(lightmap[3*j])
        #         x=lightmap[3*j]
        #         y=lightmap[3*j+1]
        #         z=lightmap[3*j+2]
        #         # x=struct.unpack('<B', lightmap[3*j])[0]
        #         # y=struct.unpack('<B', lightmap[3*j+1])[0]
        #         # z=struct.unpack('<B', lightmap[3*j+2])[0]
        #         gray=0.2989*x + 0.5870*y + 0.1140*z
        #         # print(gray)
        #         gray_bytes = bytes([int(gray)])
        #         lightmap=lightmap[:3*j]+3*gray_bytes+lightmap[3*j+3:]
        #         # print(f"{x}, {y}, {z} -> {gray}")
        #         # print(len(lightmap)==lightmap_height*lightmap_width)
        #         # pixel_list.append()
        #     # np.asarray(lightmap)#.reshape(lightmap_width, lightmap_height)
        #     lightmaps=lightmaps[:past]+lightmap+lightmaps[past+lightmap_width*lightmap_height:]
        #     # print(lightmaps)
        print(len(lightmaps))
        print(sum([w*h for w,h in lightmap_size]))
        # lightmaps = bytes1[offset_lightmaps:offset_lightmaps+length_lightmaps]
        bytes1=bytes1[:offset_lightmaps]+lightmaps+bytes1[offset_lightmaps+length_lightmaps:]
        with open(pball_path+'/'.join(map_path.split("/")[:len(map_path.split("/"))-1])+"/"+prefix_map+map_path.split("/")[len(map_path.split("/"))-1], "w+b") as g:  # bsps are binary files
            g.write(bytes1)


def create_inverted_textures(pball_path, old_texture_paths, new_dir, prefix_texture):
    if not os.path.exists(pball_path + new_dir):
        os.makedirs(pball_path + new_dir)

    for texture in old_texture_paths:
        image = Image.new('RGB', (2, 2), (255, 255, 255))
        if os.path.isfile(pball_path + "/textures/" + texture + ".png"):
            image = Image.open((pball_path + "/textures/" + texture + ".png"))
            # inverted_image = PIL.ImageOps.invert(img)
            # inverted_image.save(pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png", "PNG")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".jpg"):
            image = Image.open((pball_path + "/textures/" + texture + ".jpg"))
            # image = Image.open('your_image.png')

            # inverted_image = PIL.ImageOps.invert(img)
            # inverted_image.save(pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png", "PNG")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".tga"):
            image = Image.open((pball_path + "/textures/" + texture + ".tga"))
            # img=img.convert("RGB")
            # inverted_image = PIL.ImageOps.invert(img)
            # inverted_image.save(pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png", "PNG")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".wal"):
            with open("pb2e.pal", "r") as pal:
                conts = (pal.read().split("\n")[3:])
                conts = [b.split(" ") for b in conts]
                conts = [c for b in conts for c in b]
                conts.pop(len(conts) - 1)
                conts = list(map(int, conts))
                # print(conts)
                # print(len(conts))
                # print()
                # img = None
                img3 = WalImageFile.open((pball_path + "/textures/" + texture + ".wal"))
                img3.putpalette(conts)
                # img3.convert("RGBA")
                # img3.save("1.png")
                img3 = img3.convert("RGBA")
                print(img3.mode)
                r, g, b, a = img3.split()
                rgb_image = Image.merge('RGB', (r, g, b))

                inverted_image = PIL.ImageOps.invert(rgb_image)

                r2, g2, b2 = inverted_image.split()

                final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))

                final_transparent_image.save(
                    pball_path + new_dir + prefix_texture + texture.split("/")[len(texture.split("/")) - 1] + ".png",
                    "PNG")
            continue
            # print(f"ltexture: {texture} - color: {color}")
            # color_rgb = color[:3]
            # average_colors.append(color_rgb)
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            rgb_image = Image.merge('RGB', (r, g, b))

            inverted_image = PIL.ImageOps.invert(rgb_image)

            r2, g2, b2 = inverted_image.split()

            final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))

            final_transparent_image.save(
                pball_path + new_dir + prefix_texture + texture.split("/")[len(texture.split("/")) - 1] + ".png", "PNG")

        else:
            inverted_image = PIL.ImageOps.invert(image)
            inverted_image.save(
                pball_path + new_dir + prefix_texture + texture.split("/")[len(texture.split("/")) - 1] + ".png", "PNG")


def create_grayscale_textures(pball_path, old_texture_paths, new_dir, prefix_texture):
    if not os.path.exists(pball_path + new_dir):
        os.makedirs(pball_path + new_dir)

    for texture in old_texture_paths:
        image = Image.new('RGB', (2, 2), (255, 255, 255))
        if os.path.isfile(pball_path + "/textures/" + texture + ".png"):
            image = Image.open((pball_path + "/textures/" + texture + ".png"))
            # inverted_image = PIL.ImageOps.invert(img)
            # inverted_image.save(pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png", "PNG")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".jpg"):
            image = Image.open((pball_path + "/textures/" + texture + ".jpg"))
            # image = Image.open('your_image.png')

            # inverted_image = PIL.ImageOps.invert(img)
            # inverted_image.save(pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png", "PNG")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".tga"):
            image = Image.open((pball_path + "/textures/" + texture + ".tga"))
            # img=img.convert("RGB")
            # inverted_image = PIL.ImageOps.invert(img)
            # inverted_image.save(pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png", "PNG")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".wal"):
            with open("pb2e.pal", "r") as pal:
                conts = (pal.read().split("\n")[3:])
                conts = [b.split(" ") for b in conts]
                conts = [c for b in conts for c in b]
                conts.pop(len(conts) - 1)
                conts = list(map(int, conts))
                # print(conts)
                # print(len(conts))
                # print()
                # img = None
                img3 = WalImageFile.open((pball_path + "/textures/" + texture + ".wal"))
                img3.putpalette(conts)
                # img3.convert("RGBA")
                # img3.save("1.png")
                img3 = img3.convert("RGBA")
                final_transparent_image = img3.convert('LA')

                final_transparent_image.save(
                    pball_path + new_dir + prefix_texture + texture.split("/")[len(texture.split("/")) - 1] + ".png",
                    "PNG")
            continue
            # print(f"ltexture: {texture} - color: {color}")
            # color_rgb = color[:3]
            # average_colors.append(color_rgb)
        image=image.convert('LA')
        image.save(
            pball_path + new_dir + prefix_texture + texture.split("/")[len(texture.split("/")) - 1] + ".png", "PNG")


def create_uni_textures(pball_path, old_texture_paths, new_dir, prefix_texture):
    average_colors = list()
    for texture in old_texture_paths:
        color = (0, 0, 0)
        if os.path.isfile(pball_path + "/textures/" + texture + ".png"):
            img = Image.open((pball_path + "/textures/" + texture + ".png"))
            img2 = img.resize((1, 1))

            color = img2.getpixel((0, 0))
            # print(f"texture: {texture} - color: {color}")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".jpg"):
            img = Image.open((pball_path + "/textures/" + texture + ".jpg"))
            img.save("1.png")
            img2 = img.resize((1, 1))
            # break

            color = img2.getpixel((0, 0))
            # print(f"texture: {texture} - color: {color}")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".tga"):
            img = Image.open((pball_path + "/textures/" + texture + ".tga"))
            img2 = img.resize((1, 1))

            color = img2.getpixel((0, 0))
            # print(f"texture: {texture} - color: {color}")

        elif os.path.isfile(pball_path + "/textures/" + texture + ".wal"):
            with open("pb2e.pal", "r") as pal:
                conts = (pal.read().split("\n")[3:])
                conts = [b.split(" ") for b in conts]
                conts = [c for b in conts for c in b]
                conts.pop(len(conts) - 1)
                conts = list(map(int, conts))
                # print(conts)
                # print(len(conts))
                # print()
                # img = None
                img3 = WalImageFile.open((pball_path + "/textures/" + texture + ".wal"))
                img3.putpalette(conts)
                # img3.convert("RGBA")
                # img3.save("1.png")
                img3 = img3.convert("RGBA")
                print(img3.mode)
                # img3.save("2.png")
                # img = Image.open("1.png")
                # plt.imshow(img)
                # plt.show()
                # img.load()
                # break

                img2 = img3.resize((1, 1))

                color = img2.getpixel((0, 0))
            print(f"ltexture: {texture} - color: {color}")
            # color_rgb = color[:3]
            # average_colors.append(color_rgb)
        if not os.path.exists(pball_path+new_dir):
            os.makedirs(pball_path+new_dir)
        print(color)
        if len(color) == 3:
            img = Image.new('RGB', (2, 2), color)
            img.save(pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png", "PNG")
            print("saved that image")
        elif len(color) == 4:
            img = Image.new('RGBA', (2, 2), color)
            img.save(pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png", "PNG")
            print("saved that image "+pball_path + new_dir+prefix_texture+ texture.split("/")[len(texture.split("/"))-1]+".png")


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
        with open("/home/lennart/paintball2/Paintball2-wine/pball/maps/wipa22.bsp", "w+b") as g:  # bsps are binary files
            g.write(bytes1)
        print(length)
        read_textures("/home/lennart/paintball2/Paintball2-wine/pball/maps/light_wipa.bsp", tex_path)
    print()


def insert_to_texture_paths(map_path, new_dir, prefix_texture, prefix_map):
    old_textures = list()
    with open(map_path, "rb") as f:  # bsps are binary files
        bytes1 = f.read() # stores all bytes in bytes1 variable (named like that to not interfere with builtin names
        # get offset (position of entity block begin) and length of entity block -> see bsp quake 2 format documentation
        offset = int.from_bytes(bytes1[48:52], byteorder='little', signed=False)
        length = int.from_bytes(bytes1[52:56], byteorder='little', signed=False)
        print(len(bytes1))
        for i in range(int(length/76)):
            a = (bytes1[offset+76*i+40:offset+76*i+72])
            (u_x,) = struct.unpack('<f', (bytes1[offset + 12 * i + 0:offset + 12 * i + 4]))
            (u_y,) = struct.unpack('<f', (bytes1[offset + 12 * i + 4:offset + 12 * i + 8]))
            (u_z,) = struct.unpack('<f', (bytes1[offset + 12 * i + 8:offset + 12 * i + 12]))
            (u_offset,) = struct.unpack('<f', (bytes1[offset + 12 * i + 12:offset + 12 * i + 16]))
            (v_x,) = struct.unpack('<f', (bytes1[offset + 12 * i + 16:offset + 12 * i + 20]))
            (v_y,) = struct.unpack('<f', (bytes1[offset + 12 * i + 24:offset + 12 * i + 28]))
            (v_z,) = struct.unpack('<f', (bytes1[offset + 12 * i + 28:offset + 12 * i + 32]))
            (v_offset,) = struct.unpack('<f', (bytes1[offset + 12 * i + 32:offset + 12 * i + 36]))

            a = [x for x in a if x]

            a=(struct.pack("b" * len(a), *a).decode('ascii', "ignore"))
            if a not in old_textures:
                old_textures.append(a)
            a = a.split("/")[len(a.split("/"))-1]
            tex_path = new_dir+prefix_texture+a
            b = tex_path.encode()
            c = b"\x00" * (32 - len(b))
            tex_bytes = b + c
            print(tex_bytes)
            print()

            bytes1 = bytes1[:offset+76*i+40]+tex_bytes+bytes1[offset + 76 * i + 72:]
        with open('/'.join(map_path.split("/")[:len(map_path.split("/"))-1])+"/"+prefix_map+map_path.split("/")[len(map_path.split("/"))-1], "w+b") as g:  # bsps are binary files
            g.write(bytes1)
        print(length)
        read_textures('/'.join(map_path.split("/")[:len(map_path.split("/"))-1])+"/"+prefix_map+map_path.split("/")[len(map_path.split("/"))-1], tex_path)
    return old_textures


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