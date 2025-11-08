"""
RHINO BREP ANALYSIS
===================
Analyzes a Brep/Polysurface and counts surface types:
- Cylinders (with diameter filtering)
- Cones
- Planes
- NURBS surfaces
- Other types

Usage:
1. Select a Brep object in Rhino
2. Run script
3. View statistics of surface types

Author: Created during Claude session
Date: 2025-11-08
"""

import rhinoscriptsyntax as rs
import Rhino

print("="*80)
print("  BREP ANALYSIS - SURFACE TYPE DETECTION")
print("="*80)

# Get selected Brep
sel = rs.SelectedObjects()

if not sel:
    print("\n❌ Nothing selected! Please select a Brep object.")
else:
    print("\n✅ Selected: {} objects".format(len(sel)))
    
    obj = sel[0]
    obj_type = rs.ObjectType(obj)
    
    print("Object type: {}".format(obj_type))
    
    if obj_type == 16:  # Brep
        geo = rs.coercebrep(obj)
        
        if geo and hasattr(geo, 'Faces'):
            total_faces = geo.Faces.Count
            print("\n📊 Total faces: {}".format(total_faces))
            
            # Counters
            cylinders = 0
            cones = 0
            planes = 0
            nurbs = 0
            others = 0
            
            cylinders_above_threshold = 0
            DIAMETER_THRESHOLD = 3.2  # mm
            
            print("\n⏳ Analyzing faces...")
            
            for face_idx in range(total_faces):
                face = geo.Faces[face_idx]
                surf = face.UnderlyingSurface()
                
                # Check surface types
                is_cyl, cyl = surf.TryGetCylinder()
                is_cone, cone = surf.TryGetCone()
                is_planar = face.IsPlanar()
                
                if is_cyl:
                    cylinders += 1
                    diameter = cyl.Radius * 2
                    if diameter > DIAMETER_THRESHOLD:
                        cylinders_above_threshold += 1
                
                elif is_cone:
                    cones += 1
                
                elif is_planar:
                    planes += 1
                
                elif surf.GetType().Name in ["NurbsSurface", "SumSurface", "RevSurface"]:
                    nurbs += 1
                
                else:
                    others += 1
                
                # Progress indicator
                if (face_idx + 1) % 100 == 0:
                    print("   Processed {} faces...".format(face_idx + 1))
            
            # Results
            print("\n" + "="*80)
            print("📊 RESULTS:")
            print("="*80)
            print("🔵 Cylinders: {}".format(cylinders))
            print("   └─ Ø>{:.1f}mm: {}".format(DIAMETER_THRESHOLD, cylinders_above_threshold))
            print("🔺 Cones: {}".format(cones))
            print("⬜ Planes: {}".format(planes))
            print("📐 NURBS: {}".format(nurbs))
            print("❓ Others: {}".format(others))
            print("="*80)
            print("✅ Total: {}".format(cylinders + cones + planes + nurbs + others))
    else:
        print("\n❌ Selected object is not a Brep!")

rs.Redraw()
