"""
CHECK SELECTED SURFACE
======================
Detailed analysis of a single selected surface:
- Surface class (BrepFace, NurbsSurface, RevSurface, etc.)
- Type detection (Cylinder, Cone, Sphere, Plane)
- Parameters (diameter, radius, angle, center)
- BoundingBox information

Usage:
1. Select ONE surface in Rhino
2. Run script
3. View detailed surface information

Author: Created during Claude session
Date: 2025-11-08
"""

import rhinoscriptsyntax as rs
import Rhino

print("="*80)
print("  DETAILED SURFACE ANALYSIS")
print("="*80)

sel = rs.SelectedObjects()

if not sel:
    print("\n❌ Nothing selected!")
else:
    print("\n✅ Selected: {} object(s)".format(len(sel)))
    
    obj = sel[0]
    t = rs.ObjectType(obj)
    
    print("\n--- BASIC INFO ---")
    print("Object type: {}".format(t))
    
    if t == 8:
        print("Type name: Surface")
    elif t == 16:
        print("Type name: Brep")
    
    # Color
    color = rs.ObjectColor(obj)
    if color:
        print("Color: RGB({}, {}, {})".format(color.R, color.G, color.B))
    
    # Layer
    layer = rs.ObjectLayer(obj)
    print("Layer: {}".format(layer))
    
    if t == 8 or t == 16:
        geo = rs.coercebrep(obj) if t == 16 else rs.coercesurface(obj)
        
        if geo:
            print("\n--- GEOMETRY ---")
            
            # Get surface
            if t == 16 and hasattr(geo, 'Faces'):
                print("Faces in Brep: {}".format(geo.Faces.Count))
                face = geo.Faces[0]
                surf = face.UnderlyingSurface()
            else:
                surf = geo
                face = geo if hasattr(geo, 'PointAt') else None
            
            # Surface type
            surf_type = surf.GetType().Name
            print("Surface class: {}".format(surf_type))
            
            # BoundingBox
            bbox = surf.GetBoundingBox(True)
            print("\nBoundingBox:")
            print("  X: {:.1f} to {:.1f} (size {:.1f})".format(
                bbox.Min.X, bbox.Max.X, bbox.Max.X - bbox.Min.X))
            print("  Y: {:.1f} to {:.1f} (size {:.1f})".format(
                bbox.Min.Y, bbox.Max.Y, bbox.Max.Y - bbox.Min.Y))
            print("  Z: {:.1f} to {:.1f} (size {:.1f})".format(
                bbox.Min.Z, bbox.Max.Z, bbox.Max.Z - bbox.Min.Z))
            
            print("\n--- TYPE CHECK ---")
            
            # Cylinder
            is_cyl, cyl = surf.TryGetCylinder()
            if is_cyl:
                print("✅ CYLINDER")
                print("   Radius: {:.3f}mm".format(cyl.Radius))
                print("   Diameter: {:.3f}mm".format(cyl.Radius * 2))
                print("   Center: ({:.1f}, {:.1f}, {:.1f})".format(
                    cyl.Center.X, cyl.Center.Y, cyl.Center.Z))
            else:
                print("❌ NOT a cylinder")
            
            # Cone
            is_cone, cone = surf.TryGetCone()
            if is_cone:
                print("\n✅ CONE!")
                print("   Base radius: {:.3f}mm".format(cone.Radius))
                print("   Angle: {:.2f}°".format(cone.AngleInDegrees))
                print("   Apex: ({:.1f}, {:.1f}, {:.1f})".format(
                    cone.ApexPoint.X, cone.ApexPoint.Y, cone.ApexPoint.Z))
            else:
                print("❌ NOT a cone")
            
            # Sphere
            is_sphere, sphere = surf.TryGetSphere()
            if is_sphere:
                print("\n✅ SPHERE")
                print("   Radius: {:.3f}mm".format(sphere.Radius))
            else:
                print("❌ NOT a sphere")
            
            # Plane
            is_planar = face.IsPlanar() if face and hasattr(face, 'IsPlanar') else False
            if is_planar:
                print("\n✅ PLANE")
            else:
                print("❌ NOT a plane")
            
            # NURBS parameters
            if surf_type in ["NurbsSurface", "SumSurface", "RevSurface"]:
                print("\n--- NURBS PARAMETERS ---")
                print("Type: {}".format(surf_type))
                
                if hasattr(surf, 'IsClosed'):
                    print("Closed U: {}".format(surf.IsClosed(0)))
                    print("Closed V: {}".format(surf.IsClosed(1)))
                
                if hasattr(surf, 'Degree'):
                    print("Degree U: {}".format(surf.Degree(0)))
                    print("Degree V: {}".format(surf.Degree(1)))
            
            # Center of face
            if face and hasattr(face, 'Domain'):
                u = (face.Domain(0).Min + face.Domain(0).Max) / 2
                v = (face.Domain(1).Min + face.Domain(1).Max) / 2
                c = face.PointAt(u, v)
                
                print("\nFace center: ({:.0f}, {:.0f}, {:.0f})".format(c.X, c.Y, c.Z))
            
            print("\n" + "="*80)
            print("SUMMARY: ", end="")
            
            if is_cone:
                print("🔺 CONE")
            elif is_cyl:
                print("🔵 CYLINDER")
            elif is_planar:
                print("⬜ PLANE")
            else:
                print("❓ COMPLEX SURFACE ({})".format(surf_type))

rs.Redraw()
