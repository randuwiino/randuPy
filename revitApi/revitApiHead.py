import clr
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.UI import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

wsCol = FilteredWorksetCollector(doc)
ws = wsCol.OfKind(WorksetKind.UserWorkset).ToWorksets()

#Functions
def GetWorkset(name):
	for w in ws:
		if w.Name == name:
			return w.Id.IntegerValue

def GetElem(singleCategory):
	col = FilteredElementCollector(doc)
	return col.OfCategory(singleCategory).WhereElementIsElementType().ToElements()

#Start Transactions
t = Transaction(doc, "Transaction Name")
t.Start()
links = GetElem(BuiltInCategory.OST_RvtLinks)

for l in links:
    name = l
    param = l.GetParameters("Name")
    if "-ARC-" in l.Name:
        param.Set(GetWorkset("Links-ARC"))

print ("Type Property Workset Succesfully Changed")
t.Commit()
print ("Well done!")