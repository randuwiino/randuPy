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
# Only sets the workset of the placed instance of the link not the Workset inside Type Property
links = GetElem(BuiltInCategory.OST_RvtLinks)

for l in links:
	name = l
	param = l.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if "-ARC-" in l.Name:
		param.Set(GetWorkset("Links-ARC"))
	elif "-STR-" in l.Name:

t.Commit()
print ("Well done!")