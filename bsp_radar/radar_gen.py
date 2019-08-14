import struct


def get_poly(map_path):
    with open(map_path, "rb") as f:  # bsps are binary files
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
        print(len(vertices))
        print()
        print(length_verts)

        offset_edges = int.from_bytes(bytes1[96:100], byteorder='little', signed=False)
        length_edges = int.from_bytes(bytes1[100:104], byteorder='little', signed=False)
        print(length_edges)
        edges = list()
        max_index = 0
        for i in range(int(length_edges / 4)):  # texture information lump is 76 bytes large
            # (vert_1,) = struct.unpack('<h', (bytes1[offset_edges + 20 * i + 8:offset_edges + 20 * i + 10]))
            vert_1 = int.from_bytes(bytes1[offset_edges + 4 * i + 0:offset_edges + 4 * i + 2], byteorder='little', signed=False)
            vert_2 = int.from_bytes(bytes1[offset_edges + 4 * i + 2:offset_edges + 4 * i + 4], byteorder='little', signed=False)
            # (vert_2,) = struct.unpack('<h', (bytes1[offset_edges + 20 * i + 10:offset_edges + 20 * i + 12]))
            if vert_1 > max_index:
                max_index = vert_1
            if vert_2 > max_index:
                max_index = vert_2
            # if not int(vert_1/2) == vert_1/4:
            #     print("nub")
            #     return
            # try:
            edges.append([vertices[vert_1], vertices[vert_2]])
            # except:
            #     print(f"vert1: {vert_1} - vert2: {vert_2}")
        print(f"max_index: {max_index} - number of vertices: {length_verts / 12} - num_vert_byte: {length_verts}")
        # print(int(int.from_bytes(bytes1[104:108], byteorder='little', signed=False)/4))
        # return
        print(len(edges))

        offset_face_edges = int.from_bytes(bytes1[104:108], byteorder='little', signed=False)
        length_face_edges = int.from_bytes(bytes1[108:112], byteorder='little', signed=False)
        face_edges = list()
        for i in range(int(length_face_edges / 4)):  # texture information lump is 76 bytes large
            # (vert_1,) = struct.unpack('<h', (bytes1[offset_edges + 20 * i + 8:offset_edges + 20 * i + 10]))
            edge_index = int.from_bytes(bytes1[offset_face_edges + 4 * i + 0:offset_face_edges + 4 * i + 4], byteorder='little', signed=True)
            # print(edge_index)
            if edge_index > 0:
                face_edges.append([edges[abs(edge_index)][0], edges[abs(edge_index)][1]])
            elif edge_index < 0:
                face_edges.append([edges[abs(edge_index)][1], edges[abs(edge_index)][0]])
        print(len(face_edges))
        # print(face_edges)
        print()

        faces = list()
        max_face = 0
        min_idx = int(length_face_edges / 4)
        max_idx = 0
        for i in range(int(length_faces / 20)):  # texture information lump is 76 bytes large
            # get sum of flags / transform flag bit field to uint32
            first_edge = (bytes1[offset_faces + 20 * i + 4:offset_faces + 20 * i + 8])
            (num_edges,) = struct.unpack('<H', (bytes1[offset_faces + 20 * i + 8:offset_faces + 20 * i + 10]))
            first_edge = int.from_bytes(first_edge, byteorder='little', signed=True)
            next_edges = list()
            # print(first_edge)
            if first_edge+num_edges > max_face:
                max_face = first_edge+num_edges
            # fits = True
            print(first_edge)
            print(first_edge + num_edges)
            for j in range(num_edges):
                # n = i+1
                # if n > num_edges:
                #     n=0
                # print(face_edges[first_edge+i][0]== face_edges[first_edge+n][1])
                # if not (face_edges[first_edge+i+1][1]== face_edges[first_edge+n+1][0]):
                #     print("whoops")
                # print()
                # print(len(face_edges))
                # print(first_edge+j)
                if first_edge+j < min_idx:
                    print(first_edge+j)
                    min_idx = first_edge+j
                if first_edge+j > max_idx:
                    print(first_edge+j)
                    max_idx = first_edge+j
                if face_edges[first_edge+j][0] not in next_edges:
                    next_edges.append(face_edges[first_edge+j][0])
                if face_edges[first_edge + j][1] not in next_edges:
                    next_edges.append(face_edges[first_edge + j][1])
            faces.append(next_edges)
            # for face in face_edges:
            #     fits = True
            #     for idx, edge in enumerate(face):
            #         n = idx + 1
            #         if n >= len(face):
            #             n = 0
            #         if not (edge[0] == face[n][0]):
            #             fits = False
            #     # if fits:
            #     print(face)
        print(f"min_idx: {min_idx} - max_idx: {max_idx} - length: {int(length_face_edges / 4)}, {len(face_edges)}")
        # print(faces)
        return faces
