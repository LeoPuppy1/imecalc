import re

patt1 = re.compile(r'(GRID\*\s*)(\d*)(\s*-?\d*\.?\d*)(\s*-?\d*\.?\d*)(\s*-?\d*\.?\d*)')
patt2 = re.compile(r'(GRID\*\s*)(\d*)(\s*-?\d*\.?\d*)(\s*-?\d*\.?\d*)')
patt3 = re.compile(r'\*\s*(-?\d*.?\d*)')
pattNL =  re.compile(r'^GRID\*')

#to add other types of element
tagDict = {'CQUAD4':4,'CTETRA':13,}
dofDict = {'u1':'1', 'u2':'2', 'u3':'3', 'u1 u2':'1, 2', 'u2 u3':'2, 3', 'u1 u3':'1, 3'}

def isNCardBDF(ln):
    m = pattNL.match(ln)
    if m:
#        print m.group()
        return True
    else:
        return False
def isECardBDF(ln):
    for eKey in tagDict.keys():
        s = r'^' + eKey
        pattEL = re.compile(s)
        m = pattEL.match(ln)
        if m:
            ECardBDF.ET = eKey
            return True
    return False

class NCardBDF:
        def __init__(self, tag, nodeIndex, xCoord, yCoord, zCoord):
            self.setValue(nodeIndex, xCoord, yCoord, zCoord)
            self.nTag = tag
            self.done = True
        def printInfo(self):
            print "%s, Node:%s, %s %s %s"%(self.nTag, self.nIndex, self.nX, self.nY, self.nZ)
        def setValue(self, nodeIndex, x, y, z):
            self.nIndex = nodeIndex
            self.nX = x
            self.nY = y
            self.nZ = z
        def getValue(self):
            return self.nTag, self.nX, self.nY, self.nZ
        def stringInterpret(self,strline):
            #m = pattNL.match(strline)
            #if m:
            try:
                flagCont=strline[-2]
            except IndexError, e:
                print "Index Error, there should be a * ... line after line .... *."
                return 2
            flagCont1=strline[0]
            if flagCont == r'*':
                m = patt2.match(strline)
                if m:
                    self.done = False
                    self.nIndex = int(m.group(2))
                    self.nX = float(m.group(3))
                    self.nY = float(m.group(4))
                    return self.done
                else:
                    pass
            if flagCont1 == r'*':
                m = patt3.match(strline)
                if m:
                    self.done = True
                    self.nZ = float(m.group(1))
                    return self.done
                else:
                    pass
            #else:
                #pass
        def convToInp(self):
            return '%09s,  %13s,  %13s,  %13s\n'%(self.nIndex, self.nX, self.nY, self.nZ)
        
#the Class ECard instance should be implemented after the call to isECard() func.

class ECardBDF:
    ET=''
    def __init__(self, tag, eIndex, pID, nIDlist):
        self.setValue(eIndex, pID, nIDlist)
        self.nTag = tag
        self.patt = r''
    def printInfo(self):
        nStr = r''
        for n in self.nlst:
            nStr = nStr + str(n) + ' '
        print "%s, Elm:%s, %s %s"%(self.nTag, self.nIndex, self.pID, nStr)
    def setValue(self, eIndex, pID, nIDlist):
        self.nIndex = eIndex
        self.pID = pID
        self.nlst = nIDlist
    def getValue(self):
        return self.nTag, self.nIndex, self.pID, self.nlst
    def stringInterpret(self,strline):
        if tagDict[ECardBDF.ET] == 4:
            self.patt = ECardBDF.ET + r'(\s+\d+)(\s+\d+)(\s+\d+)(\s+\d+)(\s+\d+)(\s+\d+)'
            p = re.compile(self.patt)
            m = p.match(strline)
            if m:
                self.nTag = ECardBDF.ET
                self.nIndex = int(m.group(1))
                self.pID = int(m.group(2))
                self.nLst = [int(m.group(n + 3)) for n in range(4)]
                return True
            else:
                print 'match failed'
                return False
        elif tagDict[ECardBDF.ET] == 13:
            self.patt = ECardBDF.ET + r'(\s+\d+)(\s+\d+)(\s+\d+)(\s+\d+)(\s+\d+)(\s+\d+)'
            p = re.compile(self.patt)
            m = p.match(strline)
            if m:
                self.nTag = ECardBDF.ET
                self.nIndex = int(m.group(1))
                self.pID = int(m.group(2))
                self.nLst = [int(m.group(n + 3)) for n in range(4)]
                return True
            else:
                print 'match failed'
                return False            
        else:
            #to add other types of element
            pass
    def convToInp(self):
        if tagDict[ECardBDF.ET] == 4:
            return '%s, %13s, %13s, %13s, %13s\n'%(self.nIndex, self.nLst[0], self.nLst[1], self.nLst[2], self.nLst[3])
        elif tagDict[ECardBDF.ET] == 13:
            return '%s, %13s, %13s, %13s, %13s\n'%(self.nIndex, self.nLst[0], self.nLst[1], self.nLst[2], self.nLst[3])
        else:
            #to add other types of element
            pass
class NsetCardBDF:
    def __init__(self,setName, strNset):
        self.setValue(setName, strNset)
    def stringInterpret(self,strline):
        pass
    def setValue(self, setName, strNset):
        self.setName = setName
        self.strNset = strNset
    def printInp1(self):
        return '*NSET, NSET=%s\n\t%s\n'%(self.setName, self.strNset)
    @staticmethod
    def printInp2(setName,fN,lN):
        return '*NSET, NSET=%s,GENERATE\n%s,%s\n'%(setName, fN, lN)       
class EsetCardBDF:
    def __init__(self,setName,*eLst):
        self.setName = setName
        self.eLst = eLst
    def stringInterpret(self,strline):
        pass
    def printInp1(self):
        strElem = ''
        for n in self.eLst:
            strElem = strElem + str(n) + ", "
        return '*ELSET, ELSET=%s\n\t%s\n'%(self.setName, strElem)
    @staticmethod
    def printInp2(setName, fE,lE):
        return '*ELSET, ELSET=%s,GENERATE\n%s,%s\n'%(setName, fE, lE)   
class MatCardBDF:
    def __init__(self, matName, rou, *prop):
        self.setValue(matName, rou, *prop)
    def stringInterpret(self):
        pass
    def setValue(self, matName, rou, *prop):
        self.matName = matName
        self.rou = rou
        self.prop = prop
    def printInp(self):
        if len(self.prop) == 2:
            return '*MATERIAL,NAME=%s\n*ELASTIC\n\t%s,\t%s\n*Density\n%s\n'%(self.matName, self.prop[0], self.prop[1],self.rou)
class SolidSectCardBDF:
    def __init__(self,matName,eleSet):
        self.setValue( matName,eleSet)
    def stringInterpret(self):
        pass
    def setValue(self, matName,eleSet):
        self.matName = matName
        self.eleSet = eleSet        
    def printInp(self):
        return '*SOLID SECTION, MATERIAL = %s, ELSET = %s\n'%(self.matName, self.eleSet)
class BondCardBDF:
    def __init__(self, setNameB, dof):
        self.setValue(setNameB, dof)
    def stringInterpret(self):
        pass
    def setValue(self, setNameB, dof):
        self.setNameB = setNameB
        for ekey in dofDict.keys():
            if dof == ekey:
                self.dof = dofDict[ekey]
                return
        print 'invalid dof string'
    def printInp(self):
        return '*BOUNDARY\n%s, %s\n'%(self.setNameB, self.dof)
        
class LoadCardBDF:
    def __init__(self, setNameL, ldir, mag):
        self.setValue(setNameL, ldir, mag)
    def stringInterpret(self):
        pass
    def setValue(self, setNameL, ldir, mag):
        self.setNameL = setNameL
        if ldir == 'u1':
             self.ldir = '1'           
        elif ldir == 'u2':
            self.ldir = '2'
        elif ldir == 'u3':
            self.ldir = '3'
        else:
            print r'invalid value for load direction'
        self.mag =mag        
    def printInp(self):
        return '*CLOAD\n%s, %s, %s\n'%(self.setNameL, self.ldir, self.mag)

class OutputCardBDF:
    def __init__(self):
        pass
    def stringInterpret(self):
        pass
    @staticmethod
    def printInpU(nset):
        return '*NODE FILE,NSET=%s\nU\n'%(nset)
    @staticmethod
    def printInpS(eset):
        return '*EL FILE,ELSET=%s\nS\n'%(eset)
    @staticmethod
    def printInpE(eset):
        return '*EL FILE,ELSET=%s\nE\n'%(eset)

class StepCardBDF:
    def __init__(self):
        pass
    @staticmethod
    def printInp(atype, load, opt):
        return '*STEP\n%s%s%s*END STEP\n'%(atype,load,opt)
