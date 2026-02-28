# How Structured3D Creates 3D Building Structures and Images

## Overview
The Structured3D pipeline transforms architectural 3D annotations into various visualizations including wireframes, textured meshes, layouts, and semantic floorplans.

---

## 🏗️ The Data Pipeline

### 1. **Input Data Structure**

Each building scene contains:
```
scene_00000/
├── annotation_3d.json          # 3D structure primitives
├── bbox_3d.json                # 3D bounding boxes for furniture
└── 2D_rendering/
    └── room_0/
        ├── panorama/
        │   ├── full/rgb_rawlight.png    # 360° panoramic image
        │   ├── camera_xyz.txt           # Camera position
        │   └── layout.txt               # Room boundary
        └── perspective/                  # Regular camera views
```

### 2. **3D Structure Representation**

The system uses **primitive-based 3D modeling**:

#### **Primitives** (Building Blocks):
- **Junctions**: 3D points (corners) `[x, y, z]`
- **Lines**: 3D line segments defined by point + direction
- **Planes**: Wall/floor/ceiling surfaces (normal vector + offset)

#### **Relationships** (How primitives connect):
- `planeLineMatrix`: Which lines belong to which planes
- `lineJunctionMatrix`: Which junctions belong to which lines
- `semantics`: What each structure is (room, door, window)

---

## 🎨 Visualization Methods

### **Method 1: Wireframe Visualization** (`visualize_3d.py --type wireframe`)

**How it works:**
```python
# 1. Extract 3D junction coordinates (corners)
junctions = [(x1,y1,z1), (x2,y2,z2), ...]

# 2. Find which junctions connect to form lines
junction_pairs = [[0,1], [1,2], [2,3], ...]  # Line segments

# 3. Identify special features
- Extract lines belonging to doors/windows
- Extract lines belonging to cuboid objects (furniture)
- Color them differently

# 4. Render with Open3D
- Create point cloud for junctions (corners)
- Create line set for edges
- Display in 3D viewer
```

**Result**: A 3D wireframe showing the skeleton structure of the building.

---

### **Method 2: Plane Visualization** (`visualize_3d.py --type plane`)

**How it works:**
```python
# 1. For each plane (wall/floor/ceiling):
   - Get lines belonging to this plane
   - Convert lines to vertices (corners)
   - Handle holes (doors/windows) by clipping polygons

# 2. Triangulation
   - Break down each polygon into triangles
   - Create mesh surfaces

# 3. Coloring options:
   - By Normal Direction: Color based on surface orientation
     * Red: East-facing walls
     * Green: North-facing walls
     * Blue: West-facing walls
   - By Manhattan Alignment: Color room groups
   - By Semantics: Color by room type/function

# 4. Render with Open3D
   - Create triangle mesh for each surface
   - Apply colors
   - Display filled 3D surfaces
```

**Result**: Solid colored 3D surfaces showing walls, floors, and ceilings.

---

### **Method 3: 3D Textured Mesh** (`visualize_mesh.py`)

**This is the most realistic visualization!**

**How it works:**

#### **Step 1: Panorama to Perspective Conversion**
```python
# Take 360° panoramic image (equirectangular projection)
# Convert sections to flat perspective textures for each wall

def E2P(panorama_image, corner_i, corner_j, wall_height):
    # Sample the panoramic image between two corners
    # Project spherical coordinates to flat plane
    # Result: Wall texture image
    return wall_texture
```

#### **Step 2: Build Wall Meshes**
```python
# For each wall between two corners:
1. Create 4 vertices (rectangle):
   - Bottom-left: corner_i at floor level
   - Bottom-right: corner_j at floor level
   - Top-left: corner_i at ceiling height
   - Top-right: corner_j at ceiling height

2. Create 2 triangles from rectangle:
   - Triangle 1: [0, 2, 1]  (bottom-left → top-left → bottom-right)
   - Triangle 2: [2, 0, 3]  (top-left → bottom-left → top-right)

3. Map texture coordinates (UV mapping):
   - (0,0) = bottom-left
   - (1,1) = top-right
```

#### **Step 3: Build Floor and Ceiling**
```python
# Floor/ceiling may be non-rectangular (L-shaped rooms, etc.)

1. Take floor corner vertices
2. Use Panda3D Triangulator to break into triangles
3. Sample floor texture from panorama (looking down)
4. Sample ceiling texture from panorama (looking up)
5. Duplicate floor vertices and lift to ceiling height
```

#### **Step 4: Merge and Create Water-Tight Mesh**
```python
# Combine all pieces:
all_vertices = walls_vertices + floor_vertices + ceiling_vertices
all_triangles = walls_triangles + floor_triangles + ceiling_triangles
all_textures = [wall1_tex, wall2_tex, ..., floor_tex, ceiling_tex]

# Create textured mesh
mesh = open3d.geometry.TriangleMesh(vertices, triangles)
mesh.texture = combined_texture_image
mesh.triangle_uvs = UV_coordinates  # How to map texture

# Display with texture
open3d.visualization.draw_geometries([mesh])
```

**Result**: Photorealistic 3D model with actual wall/floor textures from photos.

---

### **Method 4: 2D Layout Visualization** (`visualize_layout.py`)

#### **A. Panorama Layout**
```python
# 1. Read layout.txt (corner coordinates)
# 2. Project 3D corners to 2D panoramic image coordinates
# 3. Draw room boundary polygon on panorama
# 4. Display 360° image with room boundary overlay
```

#### **B. Perspective Layout**
```python
# 1. Read layout.json (visible + amodal boundaries)
# 2. Load RGB image + semantic segmentation
# 3. Draw visible boundaries (what camera sees)
# 4. Draw amodal boundaries (complete room shape including occluded parts)
```

---

### **Method 5: 3D Bounding Box Visualization** (`visualize_bbox.py`)

```python
# 1. Load bbox_3d.json - oriented bounding boxes for furniture
Each box has:
   - centroid: [x, y, z]  # Center position
   - basis: 3x3 rotation matrix  # Orientation
   - coeffs: [width, height, depth]  # Size

# 2. Project 3D boxes to 2D image plane
   - Use camera intrinsics + extrinsics
   - Get 8 corners of each box
   - Project to image coordinates

# 3. Draw boxes on image
   - Draw edges of box
   - Label with object class

# 4. Display image with overlaid boxes
```

---

### **Method 6: Semantic Floorplan** (`visualize_floorplan.py`)

```python
# 1. Create top-down 2D view of building
# 2. For each room:
   - Fill polygon with color based on room type
   - Red: Bedroom
   - Blue: Bathroom  
   - Green: Living room
   - Yellow: Kitchen
   - etc.

# 3. Overlay 2D projections of furniture bounding boxes
# 4. Add room labels
```

---

## 📐 Key Algorithms

### **1. Line-to-Vertex Conversion**
```
Input: Junction pairs [[0,1], [1,2], [2,3], [3,0]]
→ Order them into closed loop
→ Output: [0, 1, 2, 3] (vertices in order)
```

### **2. Polygon Clipping (for doors/windows)**
```
Wall polygon - Door polygon = Wall with hole
Uses Shapely library for geometric operations
```

### **3. Triangulation**
```
Complex polygon → Many triangles
Required because GPUs render triangles, not arbitrary polygons
```

### **4. UV Texture Mapping**
```
3D surface point (x,y,z) → 2D texture coordinate (u,v)
Maps each triangle vertex to position in texture image
```

---

## 🔧 Key Libraries Used

| Library | Purpose |
|---------|---------|
| **Open3D** | 3D geometry processing, rendering, visualization |
| **OpenCV** | Image processing, panorama remapping |
| **Matplotlib** | 2D plotting, floorplan rendering |
| **Shapely** | 2D polygon operations, clipping |
| **Panda3D** | Polygon triangulation |
| **NumPy** | Numerical computations |

---

## 🎯 Complete Workflow Example

```bash
# 1. Load building data
scene_path = "/path/to/scene_00000"
annotations = load("annotation_3d.json")  # Structure
panorama = load("panorama/rgb_rawlight.png")  # Texture

# 2. Extract geometry
junctions = annotations['junctions']  # 3D points
planes = annotations['planes']  # Surfaces
semantics = annotations['semantics']  # Room types

# 3. Build mesh
for each wall plane:
    corners = get_corners(plane)
    texture = sample_panorama(panorama, corners)
    mesh_wall = create_rectangle(corners, texture)

floor_mesh = triangulate_floor(floor_corners)
ceiling_mesh = triangulate_ceiling(ceiling_corners)

# 4. Combine and render
complete_mesh = merge(walls + floor + ceiling)
display_3d(complete_mesh)
```

---

## 💡 What Makes This Special

1. **Primitive-based representation**: Not just point clouds, but structured geometry (junctions, lines, planes)

2. **Manhattan world alignment**: Walls align to primary axes (N/S/E/W)

3. **Semantic annotations**: Every surface knows what it is (wall, door, bedroom, etc.)

4. **Photo-realistic textures**: Real photos mapped onto 3D geometry

5. **Multi-modal data**: Same scene has RGB, depth, normals, semantics, instance masks

6. **Water-tight meshes**: No gaps or holes, suitable for VR/AR applications

---

## 🚀 To Run Visualizations

```bash
# Wireframe (skeleton)
python visualize_3d.py --path /path/to/dataset --scene 0 --type wireframe

# Colored planes  
python visualize_3d.py --path /path/to/dataset --scene 0 --type plane

# Textured 3D mesh (photorealistic)
python visualize_mesh.py --path /path/to/dataset --scene 0 --room 0

# 2D layouts
python visualize_layout.py --path /path/to/dataset --scene 0 --type panorama

# Bounding boxes
python visualize_bbox.py --path /path/to/dataset --scene 0

# Semantic floorplan
python visualize_floorplan.py --path /path/to/dataset --scene 0
```

---

## 📊 Data Flow Diagram

```
Annotation JSON → Parse Primitives → Build Geometry → Apply Textures → Render
     ↓                    ↓                  ↓             ↓            ↓
  Junctions          Connect to         Create         Sample       Display
  Lines              form polygons      meshes        panorama      in 3D
  Planes             Handle holes       Triangulate   Extract        viewer
  Semantics          Clip doors         UV map        walls/floor
```

---

## 🎓 Educational Value

This project demonstrates:
- ✅ 3D computer graphics fundamentals
- ✅ Computational geometry algorithms  
- ✅ Texture mapping and UV coordinates
- ✅ Structure-from-annotations reconstruction
- ✅ Multi-view consistency (panorama + perspective)
- ✅ Semantic scene understanding
- ✅ Professional software engineering (modular, documented)

Perfect for learning computer vision, computer graphics, and 3D scene understanding!
