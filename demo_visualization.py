"""
Demo Script: Understanding Structured3D Visualization Concepts
This script demonstrates how the visualization tools work without needing the full dataset
"""

import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("=" * 70)
print("STRUCTURED3D VISUALIZATION DEMO")
print("=" * 70)
print("\nThis demo shows how the visualization tools create 3D structures")
print("from geometric primitives (junctions, lines, planes)\n")

# ============================================================================
# DEMO 1: Creating a Simple Room from Junctions and Lines
# ============================================================================

def demo_1_wireframe():
    """Demonstrate wireframe visualization concept"""
    print("\n" + "=" * 70)
    print("DEMO 1: WIREFRAME VISUALIZATION")
    print("=" * 70)
    print("\nA wireframe is created from:")
    print("  1. Junctions (3D corner points)")
    print("  2. Lines connecting these junctions")
    
    # Define a simple rectangular room (4m x 3m x 2.5m high)
    # Floor corners
    floor_junctions = np.array([
        [0.0, 0.0, 0.0],  # Junction 0: Bottom-left-front
        [4.0, 0.0, 0.0],  # Junction 1: Bottom-right-front
        [4.0, 3.0, 0.0],  # Junction 2: Bottom-right-back
        [0.0, 3.0, 0.0],  # Junction 3: Bottom-left-back
    ])
    
    # Ceiling corners (2.5m high)
    ceiling_junctions = floor_junctions.copy()
    ceiling_junctions[:, 2] = 2.5  # Lift to ceiling height
    
    # Combine all junctions
    all_junctions = np.vstack([floor_junctions, ceiling_junctions])
    
    print(f"\nJunctions created: {len(all_junctions)} points")
    print("Floor corners:", floor_junctions.shape)
    print("Ceiling corners:", ceiling_junctions.shape)
    
    # Define line segments (which junctions connect)
    lines = [
        # Floor edges
        [0, 1], [1, 2], [2, 3], [3, 0],
        # Ceiling edges  
        [4, 5], [5, 6], [6, 7], [7, 4],
        # Vertical edges (walls)
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]
    
    print(f"Line segments created: {len(lines)} edges")
    
    # Create Open3D LineSet for visualization
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(all_junctions)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    
    # Color the lines
    colors = [[0.2, 0.6, 0.9] for _ in range(len(lines))]  # Blue lines
    line_set.colors = o3d.utility.Vector3dVector(colors)
    
    # Create junction points
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(all_junctions)
    point_cloud.paint_uniform_color([1.0, 0.3, 0.3])  # Red points
    
    print("\n✅ Wireframe created!")
    print("Visualizing... (Close window to continue)")
    
    o3d.visualization.draw_geometries(
        [line_set, point_cloud],
        window_name="Demo 1: Wireframe Visualization",
        width=1024,
        height=768
    )


# ============================================================================
# DEMO 2: Creating Solid Planes (Walls, Floor, Ceiling)
# ============================================================================

def demo_2_planes():
    """Demonstrate plane visualization with colored surfaces"""
    print("\n" + "=" * 70)
    print("DEMO 2: PLANE VISUALIZATION (Solid Surfaces)")
    print("=" * 70)
    print("\nPlanes are created by:")
    print("  1. Defining surface vertices")
    print("  2. Triangulating the surface")
    print("  3. Creating triangle mesh")
    print("  4. Coloring by surface type or orientation")
    
    # Same room dimensions
    room_meshes = []
    
    # --- FLOOR ---
    floor_vertices = np.array([
        [0.0, 0.0, 0.0],
        [4.0, 0.0, 0.0],
        [4.0, 3.0, 0.0],
        [0.0, 3.0, 0.0],
    ])
    floor_triangles = np.array([[0, 1, 2], [0, 2, 3]])  # Two triangles
    
    floor_mesh = o3d.geometry.TriangleMesh()
    floor_mesh.vertices = o3d.utility.Vector3dVector(floor_vertices)
    floor_mesh.triangles = o3d.utility.Vector3iVector(floor_triangles)
    floor_mesh.paint_uniform_color([0.7, 0.7, 0.7])  # Gray floor
    floor_mesh.compute_vertex_normals()
    room_meshes.append(floor_mesh)
    
    # --- CEILING ---
    ceiling_vertices = floor_vertices.copy()
    ceiling_vertices[:, 2] = 2.5
    ceiling_triangles = np.array([[0, 2, 1], [0, 3, 2]])  # Flipped normals
    
    ceiling_mesh = o3d.geometry.TriangleMesh()
    ceiling_mesh.vertices = o3d.utility.Vector3dVector(ceiling_vertices)
    ceiling_mesh.triangles = o3d.utility.Vector3iVector(ceiling_triangles)
    ceiling_mesh.paint_uniform_color([0.9, 0.9, 0.9])  # Light gray ceiling
    ceiling_mesh.compute_vertex_normals()
    room_meshes.append(ceiling_mesh)
    
    # --- WALLS (4 walls with different colors based on orientation) ---
    # Wall colors: North=Red, South=Blue, East=Green, West=Yellow
    walls_data = [
        # [v1, v2, v3, v4], color, name
        ([[0,0,0], [4,0,0], [4,0,2.5], [0,0,2.5]], [1.0, 0.3, 0.3], "South (Red)"),
        ([[4,0,0], [4,3,0], [4,3,2.5], [4,0,2.5]], [0.3, 1.0, 0.3], "East (Green)"),
        ([[4,3,0], [0,3,0], [0,3,2.5], [4,3,2.5]], [0.3, 0.3, 1.0], "North (Blue)"),
        ([[0,3,0], [0,0,0], [0,0,2.5], [0,3,2.5]], [1.0, 1.0, 0.3], "West (Yellow)"),
    ]
    
    for vertices, color, name in walls_data:
        wall_vertices = np.array(vertices)
        wall_triangles = np.array([[0, 1, 2], [0, 2, 3]])
        
        wall_mesh = o3d.geometry.TriangleMesh()
        wall_mesh.vertices = o3d.utility.Vector3dVector(wall_vertices)
        wall_mesh.triangles = o3d.utility.Vector3iVector(wall_triangles)
        wall_mesh.paint_uniform_color(color)
        wall_mesh.compute_vertex_normals()
        room_meshes.append(wall_mesh)
    
    print(f"\n✅ Created {len(room_meshes)} plane meshes:")
    print("   - 1 Floor (gray)")
    print("   - 1 Ceiling (light gray)")
    print("   - 4 Walls colored by orientation")
    print("\nVisualization shows different colors for different surface orientations")
    print("(This is the 'color by normal' mode in visualize_3d.py)")
    print("\nVisualizing... (Close window to continue)")
    
    o3d.visualization.draw_geometries(
        room_meshes,
        window_name="Demo 2: Plane Visualization with Colors",
        width=1024,
        height=768
    )


# ============================================================================
# DEMO 3: Understanding Texture Mapping
# ============================================================================

def demo_3_texture_mapping():
    """Demonstrate texture mapping concept"""
    print("\n" + "=" * 70)
    print("DEMO 3: TEXTURE MAPPING CONCEPT")
    print("=" * 70)
    print("\nTexture mapping involves:")
    print("  1. Creating 3D geometry (mesh)")
    print("  2. Loading texture image")
    print("  3. Mapping texture coordinates (UV) to vertices")
    print("  4. Rendering textured surface")
    
    # Create a simple textured plane
    vertices = np.array([
        [0, 0, 0],
        [2, 0, 0],
        [2, 0, 2],
        [0, 0, 2],
    ])
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    
    # Create a simple procedural texture (checkerboard pattern)
    texture_size = 256
    texture = np.zeros((texture_size, texture_size, 3), dtype=np.uint8)
    
    # Create checkerboard
    square_size = 32
    for i in range(0, texture_size, square_size):
        for j in range(0, texture_size, square_size):
            if ((i // square_size) + (j // square_size)) % 2 == 0:
                texture[i:i+square_size, j:j+square_size] = [200, 200, 200]  # Light
            else:
                texture[i:i+square_size, j:j+square_size] = [50, 50, 50]     # Dark
    
    # UV coordinates (how texture maps to vertices)
    # Each vertex (x,y,z) maps to texture coordinate (u,v)
    # u,v range from 0 to 1
    uv_coords = np.array([
        [0.0, 0.0],  # Bottom-left vertex → bottom-left texture
        [1.0, 0.0],  # Bottom-right vertex → bottom-right texture
        [1.0, 1.0],  # Top-right vertex → top-right texture
        [0.0, 1.0],  # Top-left vertex → top-left texture
    ])
    
    # Create mesh
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    mesh.compute_vertex_normals()
    
    # Apply texture
    mesh.texture = o3d.geometry.Image(texture)
    triangle_uvs = uv_coords[triangles.flatten()]
    mesh.triangle_uvs = o3d.utility.Vector2dVector(triangle_uvs)
    
    print("\n✅ Textured plane created!")
    print(f"   Texture size: {texture_size}x{texture_size}")
    print("   UV mapping: Each vertex mapped to texture coordinates")
    print("\nThis is similar to how visualize_mesh.py samples")
    print("panoramic images to create wall textures!")
    print("\nVisualizing... (Close window to continue)")
    
    o3d.visualization.draw_geometries(
        [mesh],
        window_name="Demo 3: Texture Mapping",
        width=1024,
        height=768
    )


# ============================================================================
# DEMO 4: Visualizing the Data Structure
# ============================================================================

def demo_4_data_structure():
    """Show the hierarchical data structure"""
    print("\n" + "=" * 70)
    print("DEMO 4: DATA STRUCTURE OVERVIEW")
    print("=" * 70)
    
    print("\nStructured3D uses a hierarchical representation:")
    print()
    print("📐 PRIMITIVES (Building Blocks)")
    print("├── Junctions: 3D points [x, y, z]")
    print("│   Example: [2.5, 1.3, 0.0] (a corner point)")
    print("│")
    print("├── Lines: Line segments defined by point + direction")
    print("│   Example: point=[0,0,0], direction=[1,0,0] (horizontal line)")
    print("│")
    print("└── Planes: Surfaces defined by normal + offset")
    print("    Example: normal=[0,0,1], offset=0 (floor plane)")
    print()
    print("🔗 RELATIONSHIPS (How primitives connect)")
    print("├── planeLineMatrix[i,j]=1 means line_j is on plane_i")
    print("├── lineJunctionMatrix[i,j]=1 means junction_j is on line_i")
    print("└── semantics: assigns meaning (bedroom, door, window)")
    print()
    print("📦 HIGHER-LEVEL OBJECTS")
    print("├── Cuboids: groups of planes forming boxes")
    print("├── Manhattan: aligned plane groups")
    print("└── Bounding boxes: oriented boxes for furniture")
    print()
    print("🎨 VISUALIZATION DATA")
    print("├── Panoramic images (360° photos)")
    print("├── Perspective images (regular camera views)")
    print("├── Semantic labels (pixel-wise room/object types)")
    print("└── Depth maps, normal maps, instance masks")
    print()
    
    # Create a visual representation
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Simple room
    floor = np.array([[0,0,0], [3,0,0], [3,2,0], [0,2,0], [0,0,0]])
    ceiling = floor.copy()
    ceiling[:, 2] = 2.5
    
    # Plot floor and ceiling
    ax.plot(floor[:, 0], floor[:, 1], floor[:, 2], 'b-', linewidth=2, label='Floor')
    ax.plot(ceiling[:, 0], ceiling[:, 1], ceiling[:, 2], 'b-', linewidth=2, label='Ceiling')
    
    # Plot vertical edges
    for i in range(4):
        ax.plot([floor[i, 0], ceiling[i, 0]], 
                [floor[i, 1], ceiling[i, 1]], 
                [floor[i, 2], ceiling[i, 2]], 'b-', linewidth=2)
    
    # Plot junctions
    all_junctions = np.vstack([floor[:-1], ceiling[:-1]])
    ax.scatter(all_junctions[:, 0], all_junctions[:, 1], all_junctions[:, 2],
               c='red', s=100, marker='o', label='Junctions')
    
    # Add labels
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (height)')
    ax.set_title('3D Room Structure: Junctions + Lines + Planes')
    ax.legend()
    
    # Add annotations
    ax.text(1.5, 1, -0.3, 'FLOOR PLANE', ha='center', fontsize=10, weight='bold')
    ax.text(1.5, 1, 2.7, 'CEILING PLANE', ha='center', fontsize=10, weight='bold')
    ax.text(-0.3, 0, 1.25, 'WALL', rotation=90, va='center', fontsize=9)
    
    print("✅ Structure diagram displayed in matplotlib window")
    print("   Close the plot window to continue\n")
    
    plt.tight_layout()
    plt.show()


# ============================================================================
# DEMO 5: Show Example Commands
# ============================================================================

def demo_5_commands():
    """Show example commands for running the actual scripts"""
    print("\n" + "=" * 70)
    print("DEMO 5: HOW TO RUN THE ACTUAL VISUALIZATIONS")
    print("=" * 70)
    
    print("\n⚠️  To run the actual visualization scripts, you need:")
    print("   1. The Structured3D dataset (download from official source)")
    print("   2. Extract to a directory, e.g., C:\\data\\Structured3D")
    print()
    print("📝 Example commands:")
    print()
    print("# View wireframe structure")
    print('python visualize_3d.py --path C:\\data\\Structured3D --scene 0 --type wireframe')
    print()
    print("# View colored planes")
    print('python visualize_3d.py --path C:\\data\\Structured3D --scene 0 --type plane')
    print()
    print("# View 2D floorplan (top-down view)")
    print('python visualize_3d.py --path C:\\data\\Structured3D --scene 0 --type floorplan')
    print()
    print("# View photorealistic 3D mesh with textures")
    print('python visualize_mesh.py --path C:\\data\\Structured3D --scene 0 --room 0')
    print()
    print("# View panorama layout")
    print('python visualize_layout.py --path C:\\data\\Structured3D --scene 0 --type panorama')
    print()
    print("# View 3D bounding boxes")
    print('python visualize_bbox.py --path C:\\data\\Structured3D --scene 0')
    print()
    print("# View semantic floorplan")
    print('python visualize_floorplan.py --path C:\\data\\Structured3D --scene 0')
    print()
    print("📥 Get dataset access: https://forms.gle/LXg4bcjC2aEjrL9o8")
    print()


# ============================================================================
# MAIN DEMO RUNNER
# ============================================================================

def run_all_demos():
    """Run all demonstration visualizations"""
    print("\n" + "=" * 70)
    print("   STRUCTURED3D VISUALIZATION DEMONSTRATIONS")
    print("=" * 70)
    print("\nYou'll see 5 demonstrations explaining how the system works:")
    print("  1. Wireframe visualization (junctions + lines)")
    print("  2. Plane visualization (solid colored surfaces)")
    print("  3. Texture mapping (how photos map to 3D)")
    print("  4. Data structure overview")
    print("  5. Command examples")
    print("\n" + "=" * 70)
    input("\nPress ENTER to start the demos...")
    
    try:
        # Run demos sequentially
        demo_1_wireframe()
        demo_2_planes()
        demo_3_texture_mapping()
        demo_4_data_structure()
        demo_5_commands()
        
        print("\n" + "=" * 70)
        print("   ALL DEMOS COMPLETED!")
        print("=" * 70)
        print("\n✅ You now understand how Structured3D creates 3D structures!")
        print("\n📖 For detailed explanations, see: HOW_IT_WORKS.md")
        print("🚀 Ready to visualize real buildings once you get the dataset!")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("Make sure all dependencies are installed: open3d, matplotlib, numpy")


if __name__ == "__main__":
    run_all_demos()
