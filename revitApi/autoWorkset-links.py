from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI import *

import clr
clr.AddReference("RevitServices")

import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

wsCol = FilteredWorksetCollector(doc)
ws = wsCol.OfKind(WorksetKind.UserWorkset).ToWorksets()

# Functions
def GetWorkset(name):
	for w in ws:
		if w.Name == name:
			return w.Id.IntegerValue

def GetElem(singleCategory):
	col = FilteredElementCollector(doc)
	return col.OfCategory(singleCategory).WhereElementIsNotElementType().ToElements()

def GetElems(multiCategory):
	col = FilteredElementCollector(doc)
	return col.WherePasses(multiCategory).WhereElementIsNotElementType().ToElements()

t = Transaction(doc, "Transaction Name")
t.Start()

# Workset: Links
links = GetElem(BuiltInCategory.OST_RvtLinks)

for l in links:
	name = l
	param = l.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if "-ARC-" in l.Name and ("COR" in l.Name == False) and ("INT" in l.Name == False):
		param.Set(GetWorkset("Links-ARC"))
    
    elif "-BDR-" in l.Name:
	param.Set(GetWorkset("Links-ARC (BKE-INT)"))
    
'''
    elif "-BDR-" in l.Name:
		param.Set(GetWorkset("Links-MEP (BDR)"))
	elif "-BEL-" in l.Name:
		param.Set(GetWorkset("Links-MEP (BEL)"))
	elif "-BFS-" in l.Name:
		param.Set(GetWorkset("Links-MEP (BFS)"))
	elif "-BME-" in l.Name:
		param.Set(GetWorkset("Links-MEP (BME)"))
	elif "-BPL-" in l.Name:
		param.Set(GetWorkset("Links-MEP (BPL)"))
	elif "-MDE-" in l.Name:
		param.Set(GetWorkset("Links-MEP (MDE)"))
	elif "-STR-" in l.Name:
		param.Set(GetWorkset("Links-STR"))
	elif "-CUW-" in l.Name:
		param.Set(GetWorkset("Links-Curtain Wall"))		
	elif "-CEL-" in l.Name:
		param.Set(GetWorkset("Links-Ceiling"))
	elif "-STE-" in l.Name:
		param.Set(GetWorkset("Links-Site"))
	elif "-BTG-" in l.Name:
		param.Set(GetWorkset("Links-MEP (BTG)"))
	elif "-ELV-" in l.Name:
		param.Set(GetWorkset("Links-MEP (ELV)"))
	elif "-ICT-" in l.Name:
		param.Set(GetWorkset("Links-MEP (ICT)"))
	elif "-LTE-" in l.Name:
		param.Set(GetWorkset("Links-MEP (LTE)"))
	elif "-BAL-" in l.Name:
		param.Set(GetWorkset("Links-Clash Balls"))
'''
print ("Workset: Links done!")

t.Commit()

print ("Well done!")
