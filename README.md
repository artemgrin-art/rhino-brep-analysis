# Rhino BREP Analysis Scripts

Python scripts for analyzing and processing Brep/Polysurface geometry in Rhinoceros 3D.

## 📋 Overview

Collection of scripts for:
- Surface type detection (cylinders, cones, planes, NURBS)
- Automatic line generation along surface axes
- Batch processing of multiple surfaces
- Geometric analysis and statistics

## 🎯 Key Learning

**CRITICAL: Always Explode Breps before analysis!**

```
BREP → Explode → Individual Surfaces → Accurate Analysis ✅
BREP → Direct Analysis → Unreliable Results ❌
```

### Why Explode?

1. **Type Detection**: `TryGetCylinder()` and `TryGetCone()` work reliably only on individual surfaces
2. **Parameter Access**: UV domains and face boundaries are more accurate
3. **Visual Control**: Can see and select each surface independently
4. **No Missing Geometry**: Complex forms properly separated

## 📁 Scripts

### 01_analyze_brep.py
Analyzes a Brep and counts surface types.

**Features:**
- Counts cylinders, cones, planes, NURBS
- Filters cylinders by diameter (>3.2mm threshold)
- Progress reporting for large models
- Summary statistics

**Usage:**
```
1. Select a Brep object
2. Run script
3. View statistics
```

### 02_check_surface.py
Detailed analysis of a single surface.

**Features:**
- Surface class identification
- Type detection (cylinder/cone/sphere/plane)
- Parameters (diameter, radius, angle, center)
- BoundingBox information
- NURBS parameters (degree, closed status)

**Usage:**
```
1. Select ONE surface
2. Run script
3. View detailed info
```

### 03_create_line_cylinder.py
Creates axis-aligned line on cylindrical surface.

**Features:**
- Line positioned exactly on cylinder axis
- Runs from edge to edge of face
- Uses UV parameter projection
- Green color coding

**Usage:**
```
1. Select cylindrical surface
2. Run script
3. Green line created along axis
```

### 04_batch_process_surfaces.py
Process multiple surfaces at once.

**Features:**
- Automatic type detection
- Creates lines for cylinders (green) and cones (red)
- Handles multiple selections
- Progress reporting

**Usage:**
```
1. Select multiple surfaces (use Shift)
2. Run script
3. Lines created automatically
```

## 🔧 Technical Details

### Surface Type Detection

```python
# Cylinder
is_cyl, cyl = surf.TryGetCylinder()
if is_cyl:
    diameter = cyl.Radius * 2
    axis = cyl.Axis
    center = cyl.Center

# Cone
is_cone, cone = surf.TryGetCone()
if is_cone:
    radius = cone.Radius
    angle = cone.AngleInDegrees
    apex = cone.ApexPoint
```

### Axis Projection Method

```python
# Get face boundaries
u_mid = (face.Domain(0).Min + face.Domain(0).Max) / 2
v_min = face.Domain(1).Min
v_max = face.Domain(1).Max

# Points at edges
p1 = face.PointAt(u_mid, v_min)
p2 = face.PointAt(u_mid, v_max)

# Project to cylinder axis
v1 = p1 - cyl_center
v2 = p2 - cyl_center

t1 = v1.X * axis.X + v1.Y * axis.Y + v1.Z * axis.Z
t2 = v2.X * axis.X + v2.Y * axis.Y + v2.Z * axis.Z

# Line endpoints on axis
start = cyl_center + axis * t1
end = cyl_center + axis * t2
```

## 📊 Workflow

### Recommended Process

```
1. IMPORT MODEL
   ↓
2. IF Brep → EXPLODE
   ↓
3. SELECT SURFACES (individually or in groups)
   ↓
4. RUN ANALYSIS SCRIPT
   ↓
5. CREATE LINES/POINTS
   ↓
6. EXPORT RESULTS
```

### Brep vs Individual Surfaces

| Aspect | Brep | Individual Surfaces |
|--------|------|---------------------|
| Type Detection | ❌ Unreliable | ✅ Accurate |
| Speed | ⚡ Fast | 🐢 Slower |
| Control | ❌ Limited | ✅ Full |
| Missing Geometry | ⚠️ Possible | ✅ None |
| **Recommendation** | ❌ Don't use | ✅ Always use |

## ⚙️ Requirements

- Rhinoceros 3D (version 6 or later)
- RhinoPython enabled
- Python 2.7 (IronPython in Rhino)

## 🚀 Installation

1. Download scripts from this repository
2. In Rhino, go to Tools → PythonScript → Edit
3. Open script file
4. Run with F5 or Run button

Or use via MCP (Model Context Protocol) integration with Claude.

## 📝 Notes

- All measurements in millimeters
- Tolerance: 0.01mm (Rhino default)
- Color coding:
  - 🟢 Green = Cylinder lines
  - 🔴 Red = Cone lines
  - 🔴 Red = Center points

## 🤝 Contributing

Created during Claude AI session for CAD automation workflow.

## 📄 License

Free to use and modify for personal and commercial projects.

## 📧 Contact

For questions or improvements, open an issue on GitHub.

---

**Remember:** Always Explode Breps before analysis! 🎯
