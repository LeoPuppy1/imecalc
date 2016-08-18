import os
import sys
import filecmp
import platform
import unittest
sys.path.append(os.path.dirname(__file__))
import mr_model

if __name__ == '__main__':
    model = mr_model.MR_Model('E:/imecalc/example/testm1.sat')
    model.mesh('{"data":{"tasks": ["surfaceMesh","solidMesh"],"output":{"solidMesh":{"type":"fileAuto","name":"E:/imecalc/example/testm1.bdf"}}}}')
