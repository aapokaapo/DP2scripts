import struct


def list_flags(map_path) -> None:
    """
    Sets a given flag for all brushes except skies (brushes with 'sky' in texture name)
    :param map_path: path of map to be changed
    :return: None
    """
    with open(map_path, "rb") as f:  # bsps are binary files
        bytes1 = f.read() # stores all bytes in bytes1 variable (named like that to not interfere with builtin names
        # get offset (position of entity block begin) and length of entity block -> see bsp quake 2 format documentation
        offset = int.from_bytes(bytes1[48:52], byteorder='little', signed=False)
        length = int.from_bytes(bytes1[52:56], byteorder='little', signed=False)

        for i in range(int(length/76)): # texture information lump is 76 bytes large
            # get sum of flags / transform flag bit field to uint32
            binary_flags = (bytes1[offset+76*i+32:offset+76*i+36])
            flags = int.from_bytes(binary_flags, byteorder='little', signed=False)

            # get texture name corresponding to current brush
            tex = (bytes1[offset + 76 * i + 40:offset + 76 * i + 72])
            if not flags == 0 and not flags == 2147483648:  # not 0 or negative 0 (sign bit set to 1)
                flag_list = list()
                for l in range(32):  # size of surface flag part
                    if not flags&2 ** l == 0:  # flag 2**l is in flag sum
                        flag_list.append(2**l)
                    if 2**l > flags:  # cannot be in flag sum anyway
                        break
                tex = tex.replace(b'\x00', b'')
                tex = struct.pack("b" * len(tex), *tex).decode('ascii', "ignore")
                print(f"flags: {flag_list} on texture {tex} with sum {flags}")


def set_flags(map_path, flag, output_name) -> None:
    """
    Sets a given flag for all brushes except skies (brushes with 'sky' in texture name)
    :param map_path: path of map to be changed
    :param flag: number of flag (must be 2**n)
    :param output_name: name of new file -> shouldn't overwrite old file for compatibility reasons
    :return: None
    """
    with open(map_path, "rb") as f:  # bsps are binary files
        bytes1 = f.read() # stores all bytes in bytes1 variable (named like that to not interfere with builtin names
        old_length = len(bytes1)
        # get offset (position of entity block begin) and length of entity block -> see bsp quake 2 format documentation
        offset = int.from_bytes(bytes1[48:52], byteorder='little', signed=False)
        length = int.from_bytes(bytes1[52:56], byteorder='little', signed=False)

        for i in range(int(length/76)): # texture information lump is 76 bytes large
            # get sum of flags / transform flag bit field to uint32
            binary_flags = (bytes1[offset+76*i+32:offset+76*i+36])
            flags = int.from_bytes(binary_flags, byteorder='little', signed=False)

            # get texture name corresponding to current brush
            tex = (bytes1[offset + 76 * i + 40:offset + 76 * i + 72])

            # set desired flag for every brush except skies if it isn't set already
            insert = struct.pack("<I", flags | flag)
            if b"sky" not in tex:
                bytes1 = bytes1[:offset+76*i+32]+insert+bytes1[offset + 76 * i + 36:]

        # save edited bytes as .bsp
        with open(output_name, "w+b") as g:  # bsps are binary files
            g.write(bytes1)
        print(f"new file length: {len(bytes1)}- old length: {old_length}- matching: {old_length==len(bytes1)}")
