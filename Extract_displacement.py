# -*- coding: utf-8 -*-

# Define a new node set to extract displacement(U2) from ODB with python script

# Created by Chen Li, Beijing Jiaotong Universtity, 2022/2/11
#     Email: chen_li@bjtu.edu.cn

from abaqus import *
from abaqusConstants import *
from odbAccess import *

# Open the ODB File, Creat an output file
resultPath = 'G:/Project09/2.5m/Airload/Thickness/100/'
odbPath = resultPath + 'Job-airload.odb'
odb = session.openOdb(odbPath)
resultName = resultPath + 'DispU2.txt'
#resultfile = open(resultName, 'w')

# Define a new node set
assembly = odb.rootAssembly
nodeLabel = ()
for instanceName in assembly.instances.keys():
    if 'BEAM-MID' in instanceName:
        nodeLabel = nodeLabel + ((instanceName, (113,)),)
    elif 'BEAM-SIDE' in instanceName:
        nodeLabel = nodeLabel + ((instanceName, (165,)),)

nodeset = assembly.NodeSetFromNodeLabels(name = 'MidspanNodeSet', nodeLabels = (nodeLabel))

# Define steps, frames, fieldoutput
fieldoutput1 = odb.steps['Step-gravity'].frames[-1].fieldOutputs['U']
fieldoutput2 = odb.steps['Step-airload'].frames[-1].fieldOutputs['U']

# Extract displacement
disp1 = fieldoutput1.getSubset(region = nodeset, position = NODAL)
disp2 = fieldoutput2.getSubset(region = nodeset, position = NODAL)

for i in range(len(nodeLabel)):
    dispU2Gra = disp1.values[i].data[1]
    instance = disp1.values[i].instance.name
    # resultfile.write('%d %s Step-airload U2 %s'%(i, nodeLabel[i][0], dispU2Air))
    print '%d %s Step-gravity U2 %s'%(i, instance, dispU2Gra)

for i in range(len(nodeLabel)):
    dispU2Air = disp2.values[i].data[1]
    instance = disp2.values[i].instance.name
    # resultfile.write('%d %s Step-airload U2 %s'%(i, nodeLabel[i][0], dispU2Air))
    print '%d %s Step-airload U2 %s'%(i, instance, dispU2Air)

