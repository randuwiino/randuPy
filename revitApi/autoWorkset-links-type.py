import clr
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI import *

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

t = Transaction(doc, "Transaction Name")
t.Start()

# Workset: Links
# Only sets the workset of the placed instance of the link not the Workset parameter inside Type Property
links = GetElem(BuiltInCategory.OST_RvtLinks)

for l in links:
	name = l
	param = l.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if "-ARC-" in l.Name:
		param.Set(GetWorkset("Links-ARC"))
	elif "-STR-" in l.Name:
		param.Set(GetWorkset("Links-STR"))
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
	elif "-BTG-" in l.Name:
		param.Set(GetWorkset("Links-MEP (BTG)"))
	elif "-ELV-" in l.Name:
		param.Set(GetWorkset("Links-MEP (ELV)"))
	elif "-ICT-" in l.Name:
		param.Set(GetWorkset("Links-MEP (ICT)"))
	elif "-LTE-" in l.Name:
		param.Set(GetWorkset("Links-MEP (LTE)"))
	elif "-CEL-" in l.Name:
		param.Set(GetWorkset("Links-Ceiling"))
	elif "-STE-" in l.Name:
		param.Set(GetWorkset("Links-Site"))
	elif "-BAL-" in l.Name:
		param.Set(GetWorkset("Links-Clash Balls"))
    
t.Commit()
print ("Well done!")
