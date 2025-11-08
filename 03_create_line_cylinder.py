"""
CREATE LINE ON CYLINDER AXIS
=============================
Creates a line along the axis of a selected cylindrical surface.
The line runs from edge to edge of the surface, centered on the cylinder axis.

Features:
- Accurate axis projection using UV parameters
- Line positioned exactly within face boundaries
- Green color for cylinder lines (configurable)

Usage:
1. Select a cylindrical surface
2. Run script
3. Green line created along cylinder axis

Author: Created during Claude session
Date: 2025-11-08
"""

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

print("CREATE LINE ON CYLINDER AXIS")

sel = rs.SelectedObjects()

if not sel:
    print("❌ Nothing selected")
else:
    obj = sel[0]
    geo = rs.coercebrep(obj) if rs.ObjectType(obj) == 16 else rs.coercesurface(obj)
    
    if geo:
        # Get surface
        if rs.ObjectType(obj) == 16 and hasattr(geo, 'Faces'):
            face = geo.Faces[0]
            surf = face.UnderlyingSurface()
        else:
            surf = geo
            face = geo if hasattr(geo, 'PointAt') else None
        
        is_cyl, cyl = surf.TryGetCylinder()
        
        if is_cyl and face:
            diameter = cyl.Radius * 2
            print("\n✅ Cylinder Ø{:.1f}mm".format(diameter))
            print("   Center: ({:.0f}, {:.0f}, {:.0f})".format(
                cyl.Center.X, cyl.Center.Y, cyl.Center.Z))
            
            # Cylinder axis
            axis = cyl.Axis
            cyl_center = cyl.Center
            
            # Face boundaries in V direction (along axis)
            u_mid = (face.Domain(0).Min + face.Domain(0).Max) / 2
            v_min = face.Domain(1).Min
            v_max = face.Domain(1).Max
            
            # Points at face edges
            p1 = face.PointAt(u_mid, v_min)
            p2 = face.PointAt(u_mid, v_max)
            
            # Project onto cylinder axis
            v1 = p1 - cyl_center
            v2 = p2 - cyl_center
            
            # Projection parameters
            t1 = v1.X * axis.X + v1.Y * axis.Y + v1.Z * axis.Z
            t2 = v2.X * axis.X + v2.Y * axis.Y + v2.Z * axis.Z
            
            # Line along axis
            start = cyl_center + axis * t1
            end = cyl_center + axis * t2
            
            print("Start: ({:.0f}, {:.0f}, {:.0f})".format(start.X, start.Y, start.Z))
            print("End: ({:.0f}, {:.0f}, {:.0f})".format(end.X, end.Y, end.Z))
            
            # Create line
            ln = rs.AddLine(start, end)
            
            if ln:
                rs.ObjectColor(ln, [0, 255, 0])  # Green
                
                length = ((end.X - start.X)**2 + (end.Y - start.Y)**2 + (end.Z - start.Z)**2)**0.5
                
                print("\n✅ GREEN LINE CREATED!")
                print("   Length: {:.1f}mm".format(length))
                print("   (along cylinder axis)")
        else:
            print("\n❌ Not a cylinder or invalid face!")

sc.doc.Views.Redraw()
