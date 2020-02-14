import math
import pydot
from scipy.spatial import distance


def insert_bmodel_to_leaf(model, italy):
    """
    find closest leaf to bmodel and increase that leaves' bbox to include that bmodel's faces
    :param model: object Model subclass of BSP containing center, origin, bbox
    :param italy: object BSP containing center and bbox
    :return: edited BSP object
    """
    centers = [x.center for x in italy.bsp_leaves]  # List of center of mass of all bsp leaves
    bbox_mins = [x.bbox_min for x in italy.bsp_leaves]  # List of all bbox mins of all bsp leaves
    bbox_maxs = [x.bbox_max for x in italy.bsp_leaves]  # List of all bbox maxs of all bsp leaves
    # List containing centers, leaf index in lump and distance outside of leaf bbox
    ordered_centers = list(map(list, zip(centers, list(range(len(centers))), [[0,0,0]]*len(centers))))
    ordered_bbox_mins = list(map(list, zip(bbox_mins, list(range(len(centers))))))  #2D List of bbox_mins and leaf index
    ordered_bbox_maxs = list(map(list, zip(bbox_maxs, list(range(len(centers))))))  # 2D list of bbox_maxs and leaf index

    a = len(ordered_centers) - 1  # to prevent index out of bounds exception
    while a >= 0:
        # Remove empty bbox info or centers (probably only if reading out didnt work or leaf has no face)
        if not ordered_centers[a][0] or not ordered_bbox_mins[a][0] or not ordered_bbox_maxs[a][0] or a >= 324:
            ordered_centers.pop(a)
            ordered_bbox_mins.pop(a)
            ordered_bbox_maxs.pop(a)
            a -= 1
            continue
        # Store distance to bbox mins or maxs in ordered_centers: pos if higher than maxs, neg if lower than mins
        for i in range(3):
            if ordered_bbox_maxs[a][0][i] < model.bbox_max[i]:
                ordered_centers[a][2][i] = model.bbox_max[i] - ordered_bbox_maxs[a][0][i]
            elif model.bbox_min[i] < ordered_bbox_mins[a][0][i]:
                ordered_centers[a][2][i] = ordered_bbox_mins[a][0][i] - model.bbox_min[i]
        # Replace leaf center by euclidean distance to model
        else:
            for k in range(3):
                ordered_centers[a][0][k] -= model.center[k]
            ordered_centers[a][0] = math.sqrt(sum([x ** 2 for x in ordered_centers[a][0]]))
        # Move down one index - looping reverse because pop() removes element in between and shifts all elements behind
        a -= 1
    # Abort if there is not a single distance calculated because bad input data etc
    if not [x[0] for x in ordered_centers]:
        print("No distance model to leaf calculation possible")
        return italy, None
    # print(f"centers sorted: {sorted(ordered_centers)}")
    print(f"min distance: {sorted(ordered_centers)[0][0]} with bbox deriv {sorted(ordered_centers)[0][2]}")
    here_faces = list(range(model.first_face, model.first_face + model.num_faces))
    #
    # # Set boundary box of nearest leaf to wide enough for covering the inserted bmodel face or to min/max possible
    # for i in range(3):
    #     # italy.bsp_leaves[sorted(ordered_centers)[0][1]].bbox_min[i] += math.ceil(sorted(ordered_centers)[0][2][i])
    #     italy.bsp_leaves[sorted(ordered_centers)[0][1]].bbox_min[i] = -2**15
    # for i in range(3):
    #     # italy.bsp_leaves[sorted(ordered_centers)[0][1]].bbox_max[i] += math.ceil(sorted(ordered_centers)[0][2][i])
    #     italy.bsp_leaves[sorted(ordered_centers)[0][1]].bbox_max[i] = 2**15-1
    # Insert model faces to closest bsp leaf
    italy.insert_leaf_faces(here_faces,
                            italy.bsp_leaves[sorted(ordered_centers)[0][1]].first_leaf_face + italy.bsp_leaves[
                                sorted(ordered_centers)[0][1]].num_leaf_faces - 1)
    return italy, sorted(ordered_centers)


def get_node(graph, index_old, index_new, bsp, min_dist_idx):
    if index_new < 0:
        node_old = pydot.Node(str(index_old))
        node_new = pydot.Node(str(index_new)+
                              f"\n{bsp.bsp_leaves[index_new].first_leaf_face}\n{bsp.bsp_leaves[index_new].num_leaf_faces}"
                              f"\n{distance.euclidean(bsp.models[1].center, bsp.bsp_leaves[index_new].center) if bsp.bsp_leaves[index_new].center else None}"
                              f"\n{bsp.bsp_leaves[index_new].cluster}",
                              style="filled", fillcolor=f"{'blue' if not abs(index_new)==min_dist_idx else 'yellow'}", shape="box")
        graph.add_node(node_old)
        graph.add_node(node_new)
        graph.add_edge(pydot.Edge(node_old, node_new))
        return graph
    edge = pydot.Edge(f"{index_old}", str(index_new))
    graph.add_edge(edge)
    graph = get_node(graph, index_new, bsp.nodes[index_new].front_child, bsp, min_dist_idx)
    graph = get_node(graph, index_new, bsp.nodes[index_new].back_child, bsp, min_dist_idx)

    return graph


def plot_bsp_tree(italy, distances):
    for idx, node in enumerate(italy.nodes):
        print(f"idx: {idx} - front child: {node.front_child} - back child: {node.back_child}\n"
              f"first face: {node.first_face} - num_faces: {node.num_faces}")
    print(distances)
    graph = pydot.Dot(graph_type='graph')
    graph = get_node(graph, 0, italy.nodes[0].front_child, italy, distances[0][1])
    graph = get_node(graph, 0, italy.nodes[0].back_child, italy, distances[0][1])
    # for i in range(4):
    # edge = pydot.Edge("hi", "lol")
    # graph.add_edge(edge)
    # edge = pydot.Edge("lol", "hi")
    # graph.add_edge(edge)

    # for i in range(4):
    #     node_b = pydot.Node(f"Node B", style="filled", fillcolor="green", shape="box")
    #     node_c = pydot.Node(f"Node C", style="filled", fillcolor="#0000ff")
    #     node_d = pydot.Node(f"Node D", style="filled", fillcolor="#976856")
    #
    #     # ok, now we add the nodes to the graph
    #     graph.add_node(node_b)
    #     graph.add_node(node_b)
    #     graph.add_node(node_c)
    #     graph.add_node(node_d)
    #     graph.add_node(node_d)
    #
    #     graph.add_edge(pydot.Edge(node_b, node_c))

    graph.write_png('plot.png')
    print(len(italy.nodes))
    print(len(italy.bsp_leaves))
    print(len(italy.faces))
    print(min([x.num_leaf_faces for x in italy.bsp_leaves]))
    print(max([x.num_leaf_faces for x in italy.bsp_leaves]))
    print(distances)
    print(italy.n_clusters)
    print("done")




