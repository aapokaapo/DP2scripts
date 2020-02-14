from bsp_hacking.Q2Bsp import *
from bsp_hacking.bsp_helper import *


if __name__ == '__main__':
    path = "/home/lennart/paintball2/Paintball2-wine/pball/maps/bombsaway.bsp"
    italy = Q2BSP(path)
    italy, distances = insert_bmodel_to_leaf(italy.models[1], italy)
    plot_bsp_tree(italy, distances)

    print("hi")

    for i in range(10):
        print(italy.nodes[i].first_face)
        print(italy.nodes[i].first_face+italy.nodes[i].num_faces)

    # for i in range(len(italy.nodes)-1):
    #     print(italy.nodes[i].first_face+italy.nodes[i].num_faces-1 < italy.nodes[i+1].first_face)
    # for j in range(19):
    #     print(italy.lump_sizes[italy.lump_order[j]])
    # print(f"len faces: {len(italy.faces)} - faces: {italy.faces}")
    # insert_index = 4
    # print(f"models: {[x.center for x in italy.models]}")
    # mcount = list()
    # for idx, model in enumerate(italy.models[1:]):
    #     italy = insert_bmodel_to_leaf(model, italy)
    # # all_faces = [x.num_faces for x in italy.models]
    # # non_worldspawn_faces = [x.num_faces for x in italy.models[1:]]
    # # italy.faces.extend(italy.faces[italy.models[1].first_face:])
    # # italy.models[0].num_faces = sum(all_faces)
    # # for i in range(1, len(italy.models)):
    # #     italy.models[i].first_face+=sum(non_worldspawn_faces)
    # # for model in italy.models:
    # #     print(f"center: {model.center} - origin: {model.origin}")
    # # for i in range(1, len(italy.models)):
    # #     italy.models[i].first_face=0
    # #     italy.models[i].num_faces=0
    for h in range(len(italy.bsp_leaves)):
        italy.bsp_leaves[h].bbox_min=[-2**15]*3
        italy.bsp_leaves[h].bbox_max = [2**15-1]*3
    # for j in range(19):
    #     print(italy.lump_sizes[italy.lump_order[j]])
    # print(f"num models: {len(italy.models)}\n models: {[x.first_face for x in italy.models]}- mcount {mcount}")
    # numbered_texture("hi123.png", "-lol ")
    # print(f"len faces: {len(italy.faces)} - faces: {italy.faces}")
    # # for i in range(len(italy.tex_infos)):
    # #     italy.tex_infos[i].set_texture_name("pball/trigger")
    # for i in range(len(italy.bsp_leaves)):
    #     italy.bsp_leaves[i].first_leaf_face = 0
    #     italy.bsp_leaves[i].num_leaf_faces = len(italy.bsp_leaves)
    # for face in italy.faces[italy.models[1].first_face:]:
    #     print(face.texture_info)
    #     print(italy.tex_infos[face.texture_info].get_texture_name())
    # for face in italy.faces[italy.models[0].first_face:italy.models[0].first_face+italy.models[0].num_faces]:
    #     print(italy.tex_infos[face.texture_info].get_texture_name())
    # for i in range(italy.models[1].first_face,italy.models[len(italy.models)-1].first_face+italy.models[len(italy.models)-1].num_faces):
    #     print(f"i: {i} - first edge: {italy.faces[i-515].first_edge}")
    #     italy.faces[i-italy.models[1].first_face].first_edge=italy.faces[i].first_edge
    #     italy.faces[i-italy.models[1].first_face].num_edges=italy.faces[i].num_edges
    #     print(f"i: {i} - first edge: {italy.faces[i - 515].first_edge}")
    # # italy.models = [italy.models[0]]
    italy.update_lump_sizes()
    italy.save_map(path, "2")
    # for idx, model in enumerate(italy.models):
    #     print(f"model {idx}: min face index: {model.first_face} - max face index: {model.first_face+model.num_faces-1}")
    # print(f"max leaf face: {max(italy.leaf_faces)}")
    # print(f"num clusters: {len(italy.clusters)}")
    print("done")