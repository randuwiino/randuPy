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
	if "-STR-" in l.Name:
		param.Set(GetWorkset("Links-STR"))
    
t.Commit()
