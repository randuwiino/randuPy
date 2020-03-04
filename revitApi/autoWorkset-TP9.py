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

# Workset: Shared Grids
grids = GetElem(BuiltInCategory.OST_Grids)
for g in grids:
	param = g.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	param.Set(GetWorkset("01_Shared_Grid"))
print ("Workset: Shared Grids done!")

# Workset: Shared Levels
levels = GetElem(BuiltInCategory.OST_Levels)
for l in levels:
	param = l.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	param.Set(GetWorkset("02_Shared_Level"))
print ("Workset: Shared Levels done!")

# Workset: Reference
categoryList_R_R_S_M = {BuiltInCategory.OST_CLines, BuiltInCategory.OST_VolumeOfInterest, BuiltInCategory.OST_Mass}
R_R_S_M_MultiFilter = List[BuiltInCategory](categoryList_R_R_S_M)
R_R_S_M_MultiFilter_Real = ElementMulticategoryFilter(R_R_S_M_MultiFilter)
refPlane_refLine_ScopeBox_Mass = GetElems(R_R_S_M_MultiFilter_Real)
for e in refPlane_refLine_ScopeBox_Mass:
	param = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	param.Set(GetWorkset("03_Reference"))
print ("Workset: Reference done!")

'''
# Workset: Travel Distance Railing
egress_Railings = GetElem(BuiltInCategory.OST_StairsRailing)
for r in egress_Railings:
	param = r.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if "FSI" in r.Name:
		param.Set(GetWorkset("Travel Distance Object"))
print ("Workset: Travel Distance Object (Railing) done!")

# Workset: Stacked Walls
stackWalls = GetElem(BuiltInCategory.OST_StackedWalls)
for e in stackWalls:
	param = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	param.Set(GetWorkset("Non-Structural Walls"))
print ("Workset: Non-Structural Walls (Stacked Walls) done!")
'''

# Workset: Walls
walls = GetElem(BuiltInCategory.OST_Walls)
for e in walls:
	param = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	
	if "STW-" in e.Name: #or e.LookupParameter("Structural").AsValueString() == "Yes":
		param.Set(GetWorkset("11_Structure"))
	else:
		param.Set(GetWorkset("10_Shell"))	
print ("Workset: Structural Walls & Non-Structural Wall done!")

# Workset： Column, Ramp, Beam, Roof
categoryList_C_R_R = {BuiltInCategory.OST_StructuralColumns, BuiltInCategory.OST_Ramps, BuiltInCategory.OST_Roofs, BuiltInCategory.OST_StructuralFraming}
C_R_R_MultiFilter = List[BuiltInCategory](categoryList_C_R_R)
C_R_R_MultiFilter_Real = ElementMulticategoryFilter(C_R_R_MultiFilter)
columns_Ramps_Roofs = GetElems(C_R_R_MultiFilter_Real)

for e in columns_Ramps_Roofs:
	param = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	param.Set(GetWorkset("11_Structure"))
print ("Workset: Structure done!")

# Workset: Floors
floors = GetElem(BuiltInCategory.OST_Floors)
for f in floors:
	param = f.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	
	if "SFL-" in f.Name:
		param.Set(GetWorkset("11_Structure"))
	else:
		param.Set(GetWorkset("22_Finish"))
print ("Workset: Structural Slab and Floor Finishes done!")

# Workset: Railing
railings = GetElem(BuiltInCategory.OST_Railings)
for r in railings:
	param = r.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	param.Set(GetWorkset("12_Core"))
print ("Workset: Core (Railing) done!")

# Workset: Stair Railing
stairRailings = GetElem(BuiltInCategory.OST_StairsRailing)
for r in stairRailings:
	param = r.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	param.Set(GetWorkset("12_Core"))
print ("Workset: Core (Stair Railing) done!")

# Workset: Stairs
stairs = GetElem(BuiltInCategory.OST_Stairs)
for s in stairs:
	param = s.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	param.Set(GetWorkset("12_Core"))
print ("Workset: Core (Stairs) done!")

'''
# Workset: Doors
doors = GetElem(BuiltInCategory.OST_Doors)
for d in doors:
	param = d.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	param.Set(GetWorkset("20_Interior"))
print ("Workset: Interior (Doors) done!")

# Workset: Windows
windows = GetElem(BuiltInCategory.OST_Windows)
for w in windows:
	param = d.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	param.Set(GetWorkset("20_Interior"))
print ("Workset: Interior (Windows) done!")
'''

# Workset: Door, Window, Room Separation Line, Shaft Opening
categoryList_General = {BuiltInCategory.OST_Doors, BuiltInCategory.OST_Windows, BuiltInCategory.OST_RoomSeparationLines, BuiltInCategory.OST_ShaftOpening}

general_MultiFilter = List[BuiltInCategory](categoryList_General)
general_MultiFilter_Real = ElementMulticategoryFilter(general_MultiFilter)
for e in GetElems(general_MultiFilter_Real):
	param = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	param.Set(GetWorkset("20_Interior"))
print ("Workset: Interior (Doors, Windows, Room Separation Lines and Shaft Opening) done!")

## Workset: Model Line 
modelLine = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).WhereElementIsNotElementType().ToElements()
for l in modelLine:
	if l.Name == "Model Lines":
		param = l.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		if param.IsReadOnly: continue
		param.Set(GetWorkset("20_Interior"))
print ("Workset: Interior (Model Lines) done!")

# Workset: Rooms
rooms = GetElem(BuiltInCategory.OST_Rooms)
for r in rooms:
	param = r.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	param.Set(GetWorkset("21_Room"))
print ("Workset: Room (Rooms) done!")

# Workset: Furnitures
furnitures = GetElem(BuiltInCategory.OST_Furniture)
for f in furnitures:
	param = f.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if "OTR-" in f.Name or "SIT-" in f.Name or "STG-" in f.Name or "BED-" in f.Name:
		param.Set(GetWorkset("Fixtures and Fittings"))
	elif "TBL-" in f.Name or "CHR-" in f.Name:
		param.Set(GetWorkset("30_Furniture"))
print ("Workset: Furniture (Furnitures) done!")

# Workset: Plumbing Fixtures
plumbingFixtures = GetElem(BuiltInCategory.OST_PlumbingFixtures)
for pf in plumbingFixtures:
	param = pf.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	#if "PLM-" in pf.Name:
	if param.IsReadOnly: continue
	param.Set(GetWorkset("31_Fixture"))
print ("Workset: Fixtures and Fittings (Plumbing Fixtures) done!")

## Workset: Specialty Equipment
specialEquip = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SpecialityEquipment).WhereElementIsNotElementType().ToElements()
for e in specialEquip:
	param = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
	if param.IsReadOnly: continue
	if "LFT-" in e.Name:
		param.Set(GetWorkset("32_Equipment"))
	else:
		param.Set(GetWorkset("31_Fixture"))
print ("Workset: Equipment (Specialty Equipment) done!")

t.Commit()

print ("Well done!")
