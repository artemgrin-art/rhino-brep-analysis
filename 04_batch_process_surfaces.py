"""
BATCH PROCESS SURFACES
=======================
Process multiple selected surfaces at once:
- Detect surface type (cylinder/cone/other)
- Create axis-aligned lines for cylinders and cones
- Color coding: Green for cylinders, Red for cones

Features:
- Handles multiple surfaces in one run
- Automatic type detection
- Counts created lines
- Progress reporting

Usage:
1. Select multiple surfaces (use Shift to select multiple)
2. Run script
3. Lines created automatically for all valid surfaces

Author: Created during Claude session
Date: 2025-11-08
"""

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

print("="*80)
print("  BATCH SURFACE PROCESSING")
print("="*80)

sel = rs.SelectedObjects()

if not sel:
    print("\n❌ Nothing selected!")
else:
    print("\n✅ Selected: {} surfaces".format(len(sel)))
    
    lines_created = 0
    
    for idx, obj in enumerate(sel, 1):
        print("\n" + "-"*60)
        print("SURFACE #{}".format(idx))
        print("-"*60)
        
        t = rs.ObjectType(obj)
        
        if t == 8 or t == 16:
            geo = rs.coercebrep(obj) if t == 16 else rs.coercesurface(obj)
            
            if geo:
                # Get surface
                if t == 16 and hasattr(geo, 'Faces') and geo.Faces.Count > 0:
                    face = geo.Faces[0]
                    surf = face.UnderlyingSurface()
                else:
                    surf = geo
                    face = geo if hasattr(geo, 'PointAt') else None
                
                surf_type = surf.GetType().Name
                
                # Check types
                is_cyl, cyl = surf.TryGetCylinder()
                is_cone, cone = surf.TryGetCone()
                
                print("Type: {}".format(surf_type))
                
                if is_cone:
                    print("🔺 CONE!")
                    print("   R={:.1f}mm Angle={:.1f}°".format(
                        cone.Radius, cone.AngleInDegrees))
                    
                    # Face center
                    if face and hasattr(face, 'Domain'):
                        u = (face.Domain(0).Min + face.Domain(0).Max) / 2
                        v = (face.Domain(1).Min + face.Domain(1).Max) / 2
                        c = face.PointAt(u, v)
                    else:
                        c = cone.ApexPoint
                    
                    ax = cone.Axis
                    s = c - ax * 2.5
                    e = c + ax * 2.5
                    
                    ln = rs.AddLine(s, e)
                    if ln:
                        rs.ObjectColor(ln, [255, 0, 0])  # Red for cone
                        lines_created += 1
                        print("   ✅ RED line created")
                
                elif is_cyl:
                    diameter = cyl.Radius * 2
                    print("🔵 CYLINDER Ø{:.1f}mm".format(diameter))
                    
                    if face:
                        u_mid = (face.Domain(0).Min + face.Domain(0).Max) / 2
                        v_mid = (face.Domain(1).Min + face.Domain(1).Max) / 2
                        center = face.PointAt(u_mid, v_mid)
                        
                        axis = cyl.Axis
                        cyl_center = cyl.Center
                        
                        # Boundaries
                        v_min = face.Domain(1).Min
                        v_max = face.Domain(1).Max
                        
                        p1 = face.PointAt(u_mid, v_min)
                        p2 = face.PointAt(u_mid, v_max)
                        
                        # Project to axis
                        v1 = p1 - cyl_center
                        v2 = p2 - cyl_center
                        
                        t1 = v1.X * axis.X + v1.Y * axis.Y + v1.Z * axis.Z
                        t2 = v2.X * axis.X + v2.Y * axis.Y + v2.Z * axis.Z
                        
                        s = cyl_center + axis * t1
                        e = cyl_center + axis * t2
                        
                        ln = rs.AddLine(s, e)
                        if ln:
                            rs.ObjectColor(ln, [0, 255, 0])  # Green for cylinder
                            lines_created += 1
                            print("   ✅ GREEN line created")
                
                else:
                    print("❓ Other type")
    
    print("\n" + "="*80)
    print("✅ CREATED {} LINES".format(lines_created))
    print("="*80)

sc.doc.Views.Redraw()
