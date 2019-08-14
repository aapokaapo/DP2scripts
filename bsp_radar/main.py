from shapely.geometry import LineString, Polygon
from bsp_radar import radar_gen as rg

l = LineString([[1,0.5,0.5],[3,0.5,0.5]])
p = Polygon([[1.2,0.0,0.],[2.2,1.0,0.],[2.8,0.5,1.]])
print(l.intersection(p))
#LINESTRING Z (1.7 0.5 0.25, 2.8 0.5 1)
l = LineString([[1,0.5,0.5],[3,0.5,0.5]])
p = Polygon([[1.2,0.0,100],[2.2,1.0,100],[2.8,0.5,200]])
print(l.intersection(p))
#LINESTRING Z (1.7 0.5 0.25, 2.8 0.5 1)

# l = LineString([[100,1000],[0,-1000]])
# p = Polygon([[1.2,0.0],[2.2,1.0],[2.8,0.5]])
# print(l.intersection(p))
# #LINESTRING (1.7 0.5, 2.8 0.5)

path_to_pball = "/home/lennart/paintball2/Paintball2-wine/pball"
map_path = "/maps/hca_fort.bsp"

if __name__ == '__main__':
    faces = rg.get_poly(path_to_pball+map_path)
    # edge_list_xz = list()
    # for face in faces:
    #     verts = list()
    #     for edge in face:
    #         for vert in edge:
    #             if vert not in verts:
    #                 vert = [vert[0], vert[2], vert[1]]
    #                 verts.append(vert)
    #     edge_list_xz.append(verts)
    # edge_list_yz = list()
    # for face in faces:
    #     verts = list()
    #     for edge in face:
    #         for vert in edge:
    #             if vert not in verts:
    #                 vert = [vert[1], vert[2], vert[0]]
    #                 verts.append(vert)
    #     edge_list_yz.append(verts)
    print(faces)
    edge_list_xz = faces
    distance_list=list()
    bads = 0
    goods = 0
    for i in range(-2,5):
        inner_list=list()
        for k in range(-2,-1):
            print("k= "+str(k))
            l = LineString([[100*i, 1000, 10*k], [100*i, -1000, 10*k]])
            intersections = list()
            for idx, edge in enumerate(edge_list_xz):
                p = Polygon(edge)
                try:
                    if not str(l.intersection(p)) == "GEOMETRYCOLLECTION EMPTY":
                        intersections.append(l.intersection((p)).coords[0][1])
                    goods += 1

                except:
                    print(edge)
                    bads += 1
                    pass
                    pp2 = p.buffer(0)
                    if pp2.is_valid and p.is_valid:
                        if not (str(pp2)== "POLYGON EMPTY") and not len(pp2.interiors)==0:
                            exterior=(pp2.exterior.coords[:])
                            p=Polygon(exterior)
                            if not str(l.intersection(p)) == "GEOMETRYCOLLECTION EMPTY":
                                intersections.append(l.intersection((p)).coords[0][1])

                            interior=(pp2.interiors[0].coords[:])
                            p=Polygon(interior)
                            if not str(l.intersection(p)) == "GEOMETRYCOLLECTION EMPTY":
                                intersections.append(l.intersection((p)).coords[0][1])
            intersections.sort()
            dist=0
            for f in range(int(len(intersections)/2)):
                dist+=intersections[2*f+1] - intersections[2*f]
            print(dist)
            inner_list.append(dist)
        distance_list.append(inner_list)
    print(distance_list)
    print(bads)
    print(goods)