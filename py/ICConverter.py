from InputDeckBDF import NCardBDF
from InputDeckBDF import isNCardBDF
from InputDeckBDF import ECardBDF
from InputDeckBDF import isECardBDF
from InputDeckBDF import NsetCardBDF
from InputDeckBDF import EsetCardBDF
from InputDeckBDF import LoadCardBDF
from InputDeckBDF import BondCardBDF
from InputDeckBDF import MatCardBDF
from InputDeckBDF import SolidSectCardBDF
from InputDeckBDF import StepCardBDF
from InputDeckBDF import OutputCardBDF
import os
import sys
import filecmp
import platform
import unittest
sys.path.append(os.path.dirname(__file__))
import mr_model
import xml.dom.minidom

#nc = NCard(r'GRID*',r'1', r'0', r'0', r'0')
#nc.printInfo()
#str1 = nc.convToInp()
#print str1
#f = open(r'E:\imecalc\py\sample.bdf', 'r')
f1 = open(r'testm.inp', 'w') ######overwrite the path if need
nc = NCardBDF(r'', 0, 0, 0, 0)
ec = ECardBDF(r'', 0, 0, [])
ns= NsetCardBDF(r'',r'')
lc =  LoadCardBDF(r'',r'u1',r'')
bc = BondCardBDF(r'',r'u1')
mc = MatCardBDF(r'',r'')
ssc = SolidSectCardBDF(r'',r'')
nq = []
eq = []
oq = []

nArg = len(sys.argv)
opt = sys.argv
docHelp = """
Option:
    --help: view mannual
    -x: (run the analysis) followed by xml file
    other:

version 1.1.0"""

#strJason = """{"data":{"tasks": ["surfaceMesh","solidMesh"],"output":{"solidMesh":{"type":"fileAuto","name":"yoke.bdf"}}}}"""

strJason = """{"data":{"tasks":["surfaceMesh", "solidMesh"],"output":{"solidMesh":{"type":"fileAuto","name":"testm.bdf"}},"options":{"surfaceMesh":{"meshSizePercentOfBBox":8.0,"elemType":"RTri"}}}}"""


def entry_user():
    s = True
    if nArg == 1:
		print docHelp
    elif opt[1] == '--help':
        print docHelp
    elif opt[1] == '-x':
        if opt[2] == '':
                print r'there should be a xml file to be input with'
                return
        strLd = ''
        strConstr = ''
        strOpt = ''
        xfile = opt[2]
        dom = xml.dom.minidom.parse(xfile)
        root = dom.documentElement
        t_geof = root.getElementsByTagName('geofile')
        print t_geof[0].firstChild.data + "<<<<"
        strGF = str(t_geof[0].firstChild.data)
        model = mr_model.MR_Model(strGF)
        model.mesh(strJason)
        #add some code to see if the file exists(TBD)
        f = open(r'..\example\testm.bdf', 'r')
        nq.append("*NODE, NSET=NAll\n")
        eq.append("*ELEMENT, ELSET=EALL, TYPE=C3D4\n")
        for eachL in f:
            #print "<<<"
            if isNCardBDF(eachL) or (not s):
                s = nc.stringInterpret(eachL)
                if  s == True:
                    str1 = nc.convToInp()
                    #print str1
                    nq.append(str1)
                else:
                    pass
            elif isECardBDF(eachL):
                    s1 = ec.stringInterpret(eachL)
                    if s1:
                        str1 = ec.convToInp()
                        eq.append(str1)
                    else:
                        print 'not match'
            else:
                pass
        nN = len(nq)
        nE = len(eq)

        t_ns1 = root.getElementsByTagName('nsetload')
        for n in t_ns1:
            ldir = n.getAttribute(r'dir')
            ldMag = n.getAttribute(r'mag')
            sName = n.getAttribute(r'name')
            strNset = n.firstChild.data
            ns.setValue(sName, strNset)
            oq.append(ns.printInp1())
            
            lc.setValue(sName, ldir, ldMag)
            strLd = strLd  + lc.printInp()
        #oq.append(NsetCardBDF.printInp2(r'NALL', 1, nN))
        #oq.append(EsetCardBDF.printInp2(r'EALL', 1, nE))
        t_nsb = root.getElementsByTagName('nsetbnd')
        for n in t_nsb:
            bdof = n.getAttribute(r'dof')
            bName = n.getAttribute(r'name')
            strNset = n.firstChild.data
            ns.setValue(bName, strNset)
            oq.append(ns.printInp1())

            bc.setValue(bName, bdof)
            strConstr = strConstr  + bc.printInp()
        oq.append(strConstr)

        t_mat = root.getElementsByTagName('mat')
        for m in t_mat:
            mType = m.getAttribute(r'type')
            #print 'mtype:%s'%mType
            if mType == r'elastic':
                t_name = m.getElementsByTagName('name')
                t_EX = m.getElementsByTagName('EX')
                t_NUXY = m.getElementsByTagName('NUXY')
                t_ROU = m.getElementsByTagName('ROU')
                mc.setValue(t_name[0].firstChild.data, t_ROU[0].firstChild.data,t_EX[0].firstChild.data,t_NUXY[0].firstChild.data)
                oq.append(mc.printInp())
            else:
                pass
        t_sldsec = root.getElementsByTagName('sldsect')
        for s in t_sldsec:
            t_matn = s.getElementsByTagName('matname')
            t_eset = s.getElementsByTagName('elset')
            if t_eset[0].firstChild.data == '-1':
                ssc.setValue(t_matn[0].firstChild.data, 'EALL')
            else:
                print 'invalid eleset for solidsection'
            oq.append(ssc.printInp())
        t_opt = root.getElementsByTagName('output')
        t_U = t_opt[0].getElementsByTagName('U')
        t_S = t_opt[0].getElementsByTagName('S')
        t_E = t_opt[0].getElementsByTagName('E')
        if t_U[0].firstChild.data == '1':
            strOpt = strOpt + OutputCardBDF.printInpU('NALL')
        if t_S[0].firstChild.data == '1':
            strOpt = strOpt + OutputCardBDF.printInpS('EALL')
        if t_E[0].firstChild.data == '1':
            strOpt = strOpt + OutputCardBDF.printInpE('EALL')
            
        oq.append(StepCardBDF.printInp('*static\n', strLd, strOpt))
        
        for i in range(nN):
            f1.write(nq.pop(0))
        for i in range(nE):
            f1.write(eq.pop(0))
        for i in range(len(oq)):
            f1.write(oq.pop(0))
        f.close()
        f1.close()
    else:
        print r'Please type "main.py --help" to view mannual'

if __name__ == '__main__':
    entry_user()
