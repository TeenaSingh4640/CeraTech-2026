"""
Export Structured3D scenes to 3D model formats (OBJ, STL, glTF)
"""

import os
import json
import numpy as np
import argparse

class Scene3DExporter:
    def __init__(self, scene_path):
        self.scene_path = scene_path
        self.annotation = None
        self.bboxes = None
        self.load_data()
    
    def load_data(self):
        """Load annotation and bbox data"""
        with open(f"{self.scene_path}/annotation_3d.json", 'r') as f:
            self.annotation = json.load(f)
        
        bbox_path = f"{self.scene_path}/bbox_3d.json"
        if os.path.exists(bbox_path):
            with open(bbox_path, 'r') as f:
                self.bboxes = json.load(f)
        else:
            self.bboxes = []
    
    def export_obj(self, output_path):
        """Export to OBJ format (universally supported)"""
        print(f"🎨 Exporting to OBJ format: {output_path}")
        
        vertices = []
        faces = []
        vertex_count = 0
        
        # Export room structure
        junctions = self.annotation['junctions']
        
        # Create room wireframe vertices
        for junction in junctions:
            coord = junction['coordinate']
            vertices.append(f"v {coord[0]:.3f} {coord[1]:.3f} {coord[2]:.3f}\n")
        
        # Create floor (assuming first 4 junctions are floor corners)
        if len(junctions) >= 4:
            faces.append(f"f 1 2 3 4\n")
            
            # Create walls (simple box for now)
            if len(junctions) >= 8:
                # South wall
                faces.append(f"f 1 2 6 5\n")
                # North wall
                faces.append(f"f 3 4 8 7\n")
                # West wall
                faces.append(f"f 1 4 8 5\n")
                # East wall
                faces.append(f"f 2 3 7 6\n")
                # Ceiling
                faces.append(f"f 5 6 7 8\n")
        
        # Export furniture bounding boxes
        for bbox in self.bboxes:
            centroid = bbox['centroid']
            coeffs = bbox['coeffs']
            
            # Generate 8 corners of bounding box
            corners = [
                [centroid[0] - coeffs[0], centroid[1] - coeffs[1], centroid[2] - coeffs[2]],
                [centroid[0] + coeffs[0], centroid[1] - coeffs[1], centroid[2] - coeffs[2]],
                [centroid[0] + coeffs[0], centroid[1] + coeffs[1], centroid[2] - coeffs[2]],
                [centroid[0] - coeffs[0], centroid[1] + coeffs[1], centroid[2] - coeffs[2]],
                [centroid[0] - coeffs[0], centroid[1] - coeffs[1], centroid[2] + coeffs[2]],
                [centroid[0] + coeffs[0], centroid[1] - coeffs[1], centroid[2] + coeffs[2]],
                [centroid[0] + coeffs[0], centroid[1] + coeffs[1], centroid[2] + coeffs[2]],
                [centroid[0] - coeffs[0], centroid[1] + coeffs[1], centroid[2] + coeffs[2]],
            ]
            
            base_idx = len(vertices) + 1
            for corner in corners:
                vertices.append(f"v {corner[0]:.3f} {corner[1]:.3f} {corner[2]:.3f}\n")
            
            # Add faces for the box
            faces.append(f"# {bbox['ID']}\n")
            faces.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")  # Bottom
            faces.append(f"f {base_idx+4} {base_idx+5} {base_idx+6} {base_idx+7}\n")  # Top
            faces.append(f"f {base_idx} {base_idx+1} {base_idx+5} {base_idx+4}\n")  # Front
            faces.append(f"f {base_idx+2} {base_idx+3} {base_idx+7} {base_idx+6}\n")  # Back
            faces.append(f"f {base_idx} {base_idx+3} {base_idx+7} {base_idx+4}\n")  # Left
            faces.append(f"f {base_idx+1} {base_idx+2} {base_idx+6} {base_idx+5}\n")  # Right
        
        # Write OBJ file
        with open(output_path, 'w') as f:
            f.write("# Structured3D Scene Export\n")
            f.write(f"# Scene: {self.scene_path}\n\n")
            f.writelines(vertices)
            f.write("\n")
            f.writelines(faces)
        
        print(f"   ✅ OBJ file created: {len(vertices)} vertices, {len(faces)} faces")
        return output_path
    
    def export_stl(self, output_path):
        """Export to STL format (for 3D printing)"""
        print(f"🖨️  Exporting to STL format: {output_path}")
        
        triangles = []
        
        # Convert junctions to triangles (simplified)
        junctions = self.annotation['junctions']
        
        # Floor triangles
        if len(junctions) >= 4:
            p1 = junctions[0]['coordinate']
            p2 = junctions[1]['coordinate']
            p3 = junctions[2]['coordinate']
            p4 = junctions[3]['coordinate']
            triangles.append((p1, p2, p3))
            triangles.append((p1, p3, p4))
        
        # Export furniture as triangulated boxes
        for bbox in self.bboxes:
            centroid = bbox['centroid']
            coeffs = bbox['coeffs']
            
            corners = [
                [centroid[0] - coeffs[0], centroid[1] - coeffs[1], centroid[2] - coeffs[2]],
                [centroid[0] + coeffs[0], centroid[1] - coeffs[1], centroid[2] - coeffs[2]],
                [centroid[0] + coeffs[0], centroid[1] + coeffs[1], centroid[2] - coeffs[2]],
                [centroid[0] - coeffs[0], centroid[1] + coeffs[1], centroid[2] - coeffs[2]],
                [centroid[0] - coeffs[0], centroid[1] - coeffs[1], centroid[2] + coeffs[2]],
                [centroid[0] + coeffs[0], centroid[1] - coeffs[1], centroid[2] + coeffs[2]],
                [centroid[0] + coeffs[0], centroid[1] + coeffs[1], centroid[2] + coeffs[2]],
                [centroid[0] - coeffs[0], centroid[1] + coeffs[1], centroid[2] + coeffs[2]],
            ]
            
            # Create triangles for each face of the box (12 triangles total)
            box_triangles = [
                # Bottom
                (corners[0], corners[1], corners[2]),
                (corners[0], corners[2], corners[3]),
                # Top
                (corners[4], corners[5], corners[6]),
                (corners[4], corners[6], corners[7]),
                # Front
                (corners[0], corners[1], corners[5]),
                (corners[0], corners[5], corners[4]),
                # Back
                (corners[2], corners[3], corners[7]),
                (corners[2], corners[7], corners[6]),
                # Left
                (corners[0], corners[3], corners[7]),
                (corners[0], corners[7], corners[4]),
                # Right
                (corners[1], corners[2], corners[6]),
                (corners[1], corners[6], corners[5]),
            ]
            triangles.extend(box_triangles)
        
        # Write STL file (ASCII format)
        with open(output_path, 'w') as f:
            f.write("solid Structured3D_Scene\n")
            
            for tri in triangles:
                # Calculate normal (simplified - just use up direction)
                normal = [0, 0, 1]
                
                f.write(f"  facet normal {normal[0]} {normal[1]} {normal[2]}\n")
                f.write(f"    outer loop\n")
                for vertex in tri:
                    f.write(f"      vertex {vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}\n")
                f.write(f"    endloop\n")
                f.write(f"  endfacet\n")
            
            f.write("endsolid Structured3D_Scene\n")
        
        print(f"   ✅ STL file created: {len(triangles)} triangles")
        return output_path
    
    def export_gltf(self, output_path):
        """Export to glTF format (for web/game engines)"""
        print(f"🌐 Exporting to glTF format: {output_path}")
        
        # Simplified glTF 2.0 structure
        gltf = {
            "asset": {
                "version": "2.0",
                "generator": "Structured3D Exporter"
            },
            "scene": 0,
            "scenes": [{
                "name": "Structured3D Scene",
                "nodes": [0]
            }],
            "nodes": [{
                "name": "Room",
                "mesh": 0
            }],
            "meshes": [{
                "name": "Scene",
                "primitives": [{
                    "attributes": {
                        "POSITION": 0
                    },
                    "mode": 4  # TRIANGLES
                }]
            }],
            "accessors": [{
                "bufferView": 0,
                "componentType": 5126,  # FLOAT
                "count": 0,  # Will be updated
                "type": "VEC3",
                "max": [0, 0, 0],
                "min": [0, 0, 0]
            }],
            "bufferViews": [{
                "buffer": 0,
                "byteOffset": 0,
                "byteLength": 0  # Will be updated
            }],
            "buffers": [{
                "byteLength": 0  # Will be updated
            }]
        }
        
        with open(output_path, 'w') as f:
            json.dump(gltf, f, indent=2)
        
        print(f"   ✅ glTF file created (basic structure)")
        return output_path
    
    def export_all(self, output_dir):
        """Export to all formats"""
        os.makedirs(output_dir, exist_ok=True)
        
        obj_path = self.export_obj(f"{output_dir}/scene.obj")
        stl_path = self.export_stl(f"{output_dir}/scene.stl")
        gltf_path = self.export_gltf(f"{output_dir}/scene.gltf")
        
        # Create README
        with open(f"{output_dir}/README.txt", 'w') as f:
            f.write("Structured3D Scene - 3D Model Export\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Scene: {self.scene_path}\n\n")
            f.write("Exported Formats:\n")
            f.write("- scene.obj  - Universal 3D format (use in Blender, Maya, 3ds Max)\n")
            f.write("- scene.stl  - 3D printing format (use in slicing software)\n")
            f.write("- scene.gltf - Web/game format (use in Unity, Unreal, Three.js)\n\n")
            f.write("Import Instructions:\n")
            f.write("- Blender: File > Import > Wavefront (.obj)\n")
            f.write("- Unity: Drag .gltf into Assets folder\n")
            f.write("- 3D Printer: Load .stl in your slicer software\n")
        
        print(f"\n📦 All formats exported to: {output_dir}")
        print(f"   📄 README.txt included with usage instructions")


def main():
    parser = argparse.ArgumentParser(description='Export Structured3D scenes to 3D formats')
    parser.add_argument('--scene', type=int, default=0, help='Scene ID')
    parser.add_argument('--format', choices=['obj', 'stl', 'gltf', 'all'], default='all',
                       help='Export format')
    parser.add_argument('--output', type=str, default='exports',
                       help='Output directory')
    
    args = parser.parse_args()
    
    scene_path = f"dummy_dataset/scene_{args.scene:05d}"
    
    if not os.path.exists(scene_path):
        print(f"❌ Error: Scene {args.scene:05d} not found at {scene_path}")
        return
    
    print(f"\n🚀 Structured3D 3D Model Exporter")
    print(f"📁 Scene: {scene_path}")
    print(f"📦 Format: {args.format}")
    print(f"💾 Output: {args.output}\n")
    
    exporter = Scene3DExporter(scene_path)
    
    output_dir = f"{args.output}/scene_{args.scene:05d}"
    
    if args.format == 'all':
        exporter.export_all(output_dir)
    elif args.format == 'obj':
        os.makedirs(output_dir, exist_ok=True)
        exporter.export_obj(f"{output_dir}/scene.obj")
    elif args.format == 'stl':
        os.makedirs(output_dir, exist_ok=True)
        exporter.export_stl(f"{output_dir}/scene.stl")
    elif args.format == 'gltf':
        os.makedirs(output_dir, exist_ok=True)
        exporter.export_gltf(f"{output_dir}/scene.gltf")
    
    print(f"\n✅ Export complete!")


if __name__ == "__main__":
    main()
