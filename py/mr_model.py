import os
import json

import meshright

class Facet(object):
    def __init__(self):
        self._node_ids = []
        self._normal = []

    @property
    def node_ids(self):
        return self._node_ids

    @node_ids.setter
    def node_ids(self, value):
        self._node_ids = value

    @property
    def normal(self):
        return self._normal

    @normal.setter
    def normal(self, value):
        self._normal = value


class MR_Model(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(MR_Model, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, json_fpath=None):
        self.load_json_file(json_fpath)

    def __del__(self):
        meshright.MR_FreeModel()

    def load_json_file(self, json_fpath):
        assert os.path.isfile(json_fpath)
        self._json_fpath = json_fpath
        meshright.MR_LoadModel(self._json_fpath)

    def get_entity_ids(self, ent_type):
        idarray = meshright.MR_IntArray()
        rt = meshright.MR_AskBRepEntities(ent_type, idarray)
        return [i for i in idarray]

    def get_vertex_ids(self):
        return self.get_entity_ids(0)

    def get_edge_ids(self):
        return self.get_entity_ids(1)

    def get_face_ids(self):
        return self.get_entity_ids(2)

    def get_part_ids(self):
        return self.get_entity_ids(3)

    def get_subentity_ids(self, ent_type, ent_id, subent_type):
        idarray = meshright.MR_IntArray()
        rt = meshright.MR_AskBRepSubEntities(ent_type, ent_id, subent_type, idarray)
        return [i for i in idarray]

    def mesh(self, json_str=None, json_file=None):
        if json_str:
            meshright.MR_Mesh(json_str)
        elif json_file:
            assert os.path.isfile(json_file)
            with open(json_file, 'r') as fp:
                meshright.MR_Mesh(fp.read())

    def get_bbox(self, ent_type, ent_id):
        p1 = meshright.MR_Point3D()
        p2 = meshright.MR_Point3D()
        meshright.MR_ASKEntityBoundaryBox(ent_type, ent_id, p1, p2)
        return [list(p1.xyz), list(p2.xyz)]

    def iter_face_facets(self, face_id):
        nodes = meshright.MR_DoubleArray()
        normals = meshright.MR_DoubleArray()
        triangles = meshright.MR_IntArray()
        meshright.MR_AskFaceFacetes(face_id, nodes, normals, triangles)

        num_trias = len(triangles)/3
        for i_tria in range(num_trias):
            inst_facet = Facet()
            inst_facet.node_ids = [triangles[3*i_tria+i] for i in [0, 1, 2]]
            inst_facet.normal = [normals[3*i_tria+i] for i in [0, 1, 2]]
            yield inst_facet

    def get_part_node_num(self, part_id):
       return meshright.MR_PartMeshNodeNum(part_id)

    def get_part_elem_num(self, part_id, type):
       return meshright.MR_PartMeshElemNum(part_id,type)

    def get_part_elem_num_by_criteria(self, part_id,criteria,low,up):
       return meshright.MR_PartMeshElemQuality(part_id,criteria,low,up)

def run_jsonfile(json_fpath, mesh_jsonstr=""):
    model = MR_Model(json_fpath=json_fpath)
    model.mesh(mesh_jsonstr)

