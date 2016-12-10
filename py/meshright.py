import os
import sys
sys.path.append("../bin")
import _meshright
'''
wrapper for raw cffi functions and data structures
'''


def MR_MemoryFree(obj):
    _meshright.lib.MR_MemoryFree(obj)


class MR_Node(object):
    def __init__(self):
        self._obj = _meshright.ffi.new('struct MR_Node_ *')

    def id(self):
        return self._obj.id

    def xyz(self):
        return self._obj.xyz


class MR_Elem(object):
    def __init__(self):
        self._obj = _meshright.ffi.new('struct MR_Elem_ *')

    def id(self):
        return self._obj.id

    def type(self):
        return self._obj.type

    def nodes(self):
        return self._obj.nodes


class MR_Array(object):
    def __init__(self):
        self._obj = None
        self._i = 0

    def __getitem__(self, i):
        return self._obj.array[i]

    def __len__(self):
        return self._obj.length

    def __del__(self):
        MR_MemoryFree(self._obj.array)

    def __iter__(self):
        return self

    def next(self):
        n = self.__len__()
        while self._i < n:
            value = self._obj.array[self._i]
            self._i += 1
            return value

        self._i = 0
        raise StopIteration()

    @property
    def obj(self):
        return self._obj


class MR_IntArray(MR_Array):
    def __init__(self):
        super(MR_IntArray, self).__init__()
        self._obj = _meshright.ffi.new('struct MR_IntArray_ *')


class MR_DoubleArray(MR_Array):
    def __init__(self):
        super(MR_DoubleArray, self).__init__()
        self._obj = _meshright.ffi.new('struct MR_DoubleArray_ *')


class MR_NodeArray(MR_Array):
    def __init__(self):
        super(MR_NodeArray, self).__init__()
        self._obj = _meshright.ffi.new('struct MR_NodeArray_ *')


class MR_ElemArray(MR_Array):
    def __init__(self):
        super(MR_ElemArray, self).__init__()
        self._obj = _meshright.ffi.new('struct MR_ElemArray_ *')


class MR_Point3D(object):
    def __init__(self):
        self._obj = _meshright.ffi.new('struct MR_Point3D_ *')

    @property
    def xyz(self):
        return self._obj.xyz

    @property
    def obj(self):
        return self._obj


def MR_LoadModel(filename):
    return _meshright.lib.MR_LoadModel(filename)


def MR_FreeModel():
    _meshright.lib.MR_FreeModel()


def MR_Mesh(jsonStr):
    return _meshright.lib.MR_Mesh(jsonStr)


def MR_Main(argc, argv):
    return _meshright.lib.MR_Main(argc, argv)


def MR_AskBRepEntities(ent_type, entities):
    assert isinstance(entities, MR_IntArray)
    rt = _meshright.lib.MR_AskBRepEntities(ent_type, entities.obj)
    return rt


def MR_AskBRepSubEntities(ent_type, ent_id, subent_type, entities):
    assert isinstance(entities, MR_IntArray)
    return _meshright.lib.MR_AskBRepSubEntities(ent_type, ent_id, subent_type,  entities.obj)


def MR_ASKEntityBoundaryBox(ent_type, ent_id, p1, p2):
    assert isinstance(p1, MR_Point3D)
    assert isinstance(p2, MR_Point3D)
    return _meshright.lib.MR_ASKEntityBoundaryBox(ent_type, ent_id, p1.obj, p2.obj)


def MR_AskFaceFacetes(face_id, nodes, normals, triangles):
    assert isinstance(nodes, MR_DoubleArray)
    assert isinstance(normals, MR_DoubleArray)
    assert isinstance(triangles, MR_IntArray)

    return _meshright.lib.MR_AskFaceFacetes(face_id, nodes.obj, normals.obj, triangles.obj)


def MR_AskFaceMesh(face_id, nodes, elems):
    assert isinstance(nodes, MR_NodeArray)
    assert isinstance(elems, MR_ElemArray)
    return _meshright.lib.MR_AskFaceMesh(face_id, nodes.obj, elems.obj)


def MR_AskPartMesh(part_id, nodes, elems):
    assert isinstance(nodes, MR_NodeArray)
    assert isinstance(elems, MR_ElemArray)
    return _meshright.lib.MR_AskPartMesh(part_id, nodes.obj, elems.obj)


def MR_IsLinear(type):
    return _meshright.lib.MR_IsLinear(type)


def MR_IsTria(type):
    return _meshright.lib.MR_IsTria(type)


def MR_IsQuad(type):
    return _meshright.lib.MR_IsQuad(type)

def MR_IsTetra(type):
    return _meshright.lib.MR_IsTetra(type)


def MR_IsPyramid(type):
    return _meshright.lib.MR_IsPyramid(type)


def MR_IsPrism(type):
    return _meshright.lib.MR_IsPrism(type)


def MR_IsHexa(type):
    return _meshright.lib.MR_IsHexa(type)


def MR_IsShell(type):
    return _meshright.lib.MR_IsShell(type)


def MR_IsSolid(type):
    return _meshright.lib.MR_IsSolid(type)


def MR_Is2ndOrder(type):
    return _meshright.lib.MR_Is2ndOrder(type)


def MR_Is1stOrder(type):
    return _meshright.lib.MR_Is1stOrder(type)


def MR_Type1st(type):
    return _meshright.lib.MR_Type1st(type)


def MR_Type2nd(type):
    return _meshright.lib.MR_Type2nd(type)


def MR_NodeNum(type):
    return _meshright.lib.MR_NodeNum(type)


def MR_EdgeNum(type):
    return _meshright.lib.MR_EdgeNum(type)


def MR_FaceNum(type):
    return _meshright.lib.MR_FaceNum(type)


def MR_Dim(type):
    return _meshright.lib.MR_Dim(type)


def MR_GetFaceVertex(type, fi, handles):
    return _meshright.lib.MR_GetFaceVertex(type, fi, handles)


def MR_GetEdgeLinkFaces(type, ei, faces):
    return _meshright.lib.MR_GetEdgeLinkFaces(type, ei, faces)


def MR_GetEdgeNodes(type, i, en):
    return _meshright.lib.MR_GetEdgeNodes(type, i, en)

def MR_PartMeshNodeNum(pid):
    return _meshright.lib.MR_PartMeshNodeNum(pid)

def MR_PartMeshElemNum(pid,type):
    return _meshright.lib.MR_PartMeshElemNum(pid,type)

def MR_PartMeshElemQuality(pid,criteria,low,up):
    wst = _meshright.ffi.new("double *")
    rt= _meshright.lib.MR_PartMeshElemQuality(pid,criteria,low,up,wst)
    return [rt,wst[0]]

if __name__ == '__main__':
    MR_LoadModel('/home/kang/models/cad2cae/simple/simple_cad2cae.json')
    ids = _meshright.ffi.new('struct MR_IntArray_*')
    MR_AskBRepEntities(1, ids)
    print ids.length
    print ids.array
    pass
