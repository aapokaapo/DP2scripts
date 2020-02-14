def get_header(map_path):
    header = {}
    with open(map_path+".bsp", "rb") as f:
        bytes1 = f.read()
        header["map_version"] = int.from_bytes(bytes1[32:36], byteorder='little', signed=False)
from bsp_hacking.Q2Bsp import Q2BSP
def only_current_portal(map_path):
    italy = Q2BSP(map_path+".bsp")
    with open(map_path+".bsp", "rb") as f:  # bsps are binary files
        bytes1 = f.read() # stores all bytes in bytes1 variable (named like that to not interfere with builtin names
        # get offset (position of entity block begin) and length of entity block -> see bsp quake 2 format documentation
        offset_vis = int.from_bytes(bytes1[32:36], byteorder='little', signed=False)
        length_vis = int.from_bytes(bytes1[36:40], byteorder='little', signed=False)
        n_clusters = int.from_bytes(bytes1[offset_vis:offset_vis+4], byteorder='little', signed=False)
        print(n_clusters)
        print(length_vis)
        pvs_offsets = list()
        phs_offsets = list()
        for i in range(n_clusters):
            pvs_offset = int.from_bytes(bytes1[offset_vis+4+8*i:offset_vis+4+8*i+4], byteorder='little', signed=False)
            pvs_offsets.append(pvs_offset)
            phs_offset = int.from_bytes(bytes1[offset_vis+4+8*i+4:offset_vis+4+8*i+8], byteorder='little', signed=False)
            phs_offsets.append(phs_offset)
        pvs_data = bytes1[offset_vis+pvs_offsets[0]:offset_vis+phs_offsets[0]]
        phs_data = bytes1[offset_vis+phs_offsets[0]:offset_vis+length_vis]
        len_pre_pvs=(8*n_clusters+4)
        len_post_pvs=length_vis - phs_offsets[0]
        print(offset_vis+length_vis)
        import math
        print(math.ceil(n_clusters/8.0))
        for i in range(10):
            print(pvs_offsets[i+1]-pvs_offsets[i])
        print(pvs_offsets[n_clusters-1])
        print(phs_offsets[0])
        bytes_per_pvs = math.ceil(n_clusters/8.0)
        new_pvs = b""
        new_pvs += (1).to_bytes(1, byteorder='little')
        print(bytes_per_pvs)
        print(math.ceil((n_clusters-1)/8.0))
        new_pvs += bytes(1) + (bytes_per_pvs-math.ceil((0)/8.0)).to_bytes(1, byteorder='little')
        pvs_offsets[0]=4+n_clusters*8
        for i in range(1,n_clusters-1):
            pvs_offsets[i]= 4+n_clusters*8+3+5*(i-1)
            exp=(i-int(i/8.0)*8)
            before = math.floor(i/8.0)
            after= bytes_per_pvs-math.ceil(i/8.0)
            mid=(2**exp).to_bytes(1, byteorder='little')
            insert_before = bytes(1)+ (before).to_bytes(1, byteorder='little')
            insert_after = bytes(1) + (after).to_bytes(1, byteorder='little')
            new_pvs+=insert_before+mid+insert_after
        pvs_offsets[n_clusters-1]= 4+n_clusters*8+3+5*(n_clusters-2)
        for i in range(len(phs_offsets)):
            phs_offsets[i]=phs_offsets[i]-(pvs_offsets[n_clusters-1]+3)
        new_pvs += bytes(1)+ (math.floor((n_clusters-1)/8.0)).to_bytes(1, byteorder='little')
        new_pvs += (2**(n_clusters-1-int((n_clusters-1)/8.0)*8)).to_bytes(1, byteorder='little')
        new_len_vis = len_pre_pvs+phs_offsets[0]+len_post_pvs
        sublump = b""
        sublump+=(n_clusters).to_bytes(4, byteorder='little')
        for i in range(n_clusters):
            sublump+=pvs_offsets[i].to_bytes(4, byteorder='little')
            sublump+=phs_offsets[i].to_bytes(4, byteorder='little')
        new_header=bytes1[:8]+new_len_vis.to_bytes(4, byteorder='little')
        vis_len_diff = length_vis-new_len_vis
        print(vis_len_diff)
        print()
        for i in range(19):
            offset = int.from_bytes(bytes1[(i+1)*8:(i+1)*8+4], byteorder='little', signed=False)
            if offset > offset_vis and not i == 3:
                print(i)
                offset-=vis_len_diff
            new_header+=offset.to_bytes(4, byteorder='little')
            new_header+=bytes1[(i+1)*8+4:(i+1)*8+8]
        new_bytes = new_header+ bytes1[160:offset_vis]+sublump+new_pvs+phs_data+bytes1[offset_vis+length_vis:]
        italy.binary_lumps[4]=b""
        italy.binary_lumps[4]+=sublump+new_pvs+phs_data
        italy.update_lump_sizes()
        italy.save_map("_rofl2")
        with open(map_path+"_lol"+".bsp", 'w+b') as g:
            g.write(new_bytes)