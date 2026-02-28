# 🏠 Dummy Dataset for Testing Structured3D Visualizations

## Overview

This lightweight dummy dataset lets you test all Structured3D visualization scripts **without downloading the massive real dataset** (which is hundreds of GB). Perfect for learning how the system works on a laptop!

## 📦 What's Included

```
dummy_dataset/
└── scene_00000/
    ├── annotation_3d.json          # 3D structure (5m x 4m x 2.5m room)
    ├── bbox_3d.json                # 3 furniture bounding boxes
    └── 2D_rendering/
        └── 0/                      # Room 0 (living room)
            ├── panorama/
            │   ├── full/           # With furniture
            │   │   ├── rgb_rawlight.png
            │   │   ├── semantic.png
            │   │   ├── instance.png
            │   │   ├── depth.png
            │   │   ├── normal.png
            │   │   └── albedo.png
            │   ├── empty/          # Without furniture
            │   │   └── rgb_rawlight.png
            │   ├── camera_xyz.txt
            │   └── layout.txt
            └── perspective/
                └── full/
                    └── 0/
                        ├── rgb_rawlight.png
                        ├── semantic.png
                        ├── instance.png
                        ├── depth.png
                        ├── normal.png
                        ├── albedo.png
                        ├── camera_pose.txt
                        └── layout.json
```

## 🎯 Dummy Scene Details

**Room Dimensions:**
- 5 meters × 4 meters × 2.5 meters high
- Simple rectangular living room
- 1 window on the south wall

**Furniture (3 objects):**
- Coffee table (0.6m × 0.6m × 0.4m)
- Bookshelf (1.0m × 0.5m × 0.8m)
- Chair (0.8m × 0.8m × 0.5m, rotated 30°)

**Camera Position:**
- Center of room: (2.5, 2.0, 1.25)

## 🚀 How to Use

### 1. Wireframe Visualization (3D structure skeleton)

```bash
cd Structured3D
python visualize_3d.py --path dummy_dataset --scene 0 --type wireframe
```

**Shows:** Blue lines and red corner points forming the room structure.

### 2. Floorplan Visualization (2D top-down view)

```bash
python visualize_3d.py --path dummy_dataset --scene 0 --type floorplan
```

**Shows:** 2D colored floorplan of the room layout.

### 3. Textured 3D Mesh (Photorealistic!)

```bash
python visualize_mesh.py --path dummy_dataset --scene 0 --room 0
```

**Shows:** 3D room with textured walls from panoramic image.

### 4. Panorama Layout (360° view with boundaries)

```bash
python visualize_layout.py --path dummy_dataset --scene 0 --type panorama
```

**Shows:** Panoramic image with room boundary overlay.

### 5. Perspective Layout (Regular camera view)

```bash
python visualize_layout.py --path dummy_dataset --scene 0 --type perspective
```

**Shows:** Regular camera view with layout annotations.

### 6. 3D Bounding Boxes (Furniture locations)

```bash
python visualize_bbox.py --path dummy_dataset --scene 0
```

**Shows:** Furniture bounding boxes projected onto images.

### 7. Semantic Floorplan (Colored by room type)

```bash
python visualize_floorplan.py --path dummy_dataset --scene 0
```

**Shows:** Floorplan with color-coded room types.

## ⚠️ Notes

### About PyMesh

**PyMesh is NOT required for most visualizations!**

- ✅ Works without PyMesh: `wireframe`, `floorplan`, `mesh`, `layout`, `bbox`
- ⚠️ Limited without PyMesh: `plane` mode (can't handle complex holes like doors/windows)

If you see "Warning: pymesh not available" - that's OK! Most features work fine.

### File Size

The dummy dataset is **< 5 MB** compared to the real dataset's **hundreds of GB**.

- Annotation JSON files: ~10 KB
- Generated images: ~500 KB each
- Total: ~5 MB for complete test scene

## 🎨 Interactive Controls

When viewing 3D visualizations (Open3D windows):

- **Rotate:** Click and drag with left mouse button
- **Pan:** Click and drag with middle mouse button (or Ctrl + left mouse)
- **Zoom:** Scroll wheel (or right mouse button)
- **Reset view:** Press `R`
- **Close:** Press `Q` or close window

## 📝 Modifying the Dummy Data

Want to create your own test scene? Edit these files:

### Change Room Dimensions

Edit `dummy_dataset/scene_00000/annotation_3d.json`:
- Modify `junctions` array (corner coordinates)
- Update `lines` and `planes` accordingly

### Add More Furniture

Edit `dummy_dataset/scene_00000/bbox_3d.json`:
```json
{
  "ID": 3,
  "basis": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
  "coeffs": [width/2, depth/2, height/2],
  "centroid": [x, y, z]
}
```

### Regenerate Images

After modifying annotations, regenerate images:
```bash
python generate_dummy_images.py
python generate_perspective_images.py
```

## 🔧 Troubleshooting

### "No module named 'pymesh'"
**Solution:** Ignore it! Only needed for advanced plane visualization.

### "ModuleNotFoundError: No module named 'open3d'"
**Solution:** Install dependencies:
```bash
pip install open3d opencv-python matplotlib numpy shapely descartes panda3d
```

### Visualization window doesn't open
**Solution:** 
- Make sure you're in the `Structured3D` directory
- Check that dummy_dataset exists in current directory
- Try a different visualization mode

### "No such file or directory"
**Solution:** Make sure you run from the correct directory:
```bash
cd C:\Users\lpste\Desktop\ceratech\Structured3D
python visualize_3d.py --path dummy_dataset --scene 0 --type wireframe
```

## 🎓 Learning Path

**Recommended order for exploring:**

1. **Start with wireframe** - Understand the basic 3D structure
   ```bash
   python visualize_3d.py --path dummy_dataset --scene 0 --type wireframe
   ```

2. **View the floorplan** - See the 2D layout
   ```bash
   python visualize_3d.py --path dummy_dataset --scene 0 --type floorplan
   ```

3. **See the textured mesh** - Experience the photorealistic model
   ```bash
   python visualize_mesh.py --path dummy_dataset --scene 0 --room 0
   ```

4. **Explore layouts and bounding boxes**
   ```bash
   python visualize_layout.py --path dummy_dataset --scene 0 --type panorama
   python visualize_bbox.py --path dummy_dataset --scene 0
   ```

## 📊 Data Size Comparison

| Dataset | Scenes | Size | Use Case |
|---------|--------|------|----------|
| **Dummy** | 1 | ~5 MB | ✅ Testing, learning, development |
| **Sample** | 10 | ~5 GB | Development with variety |
| **Full** | 3,500 | ~1 TB | Research, training ML models |

## 🌟 Next Steps

Once you understand how it works with the dummy data:

1. **Request full dataset access:**
   - Fill form: https://forms.gle/LXg4bcjC2aEjrL9o8
   - Wait for approval (few days)
   - Download real scenes

2. **Use the same commands with real data:**
   ```bash
   python visualize_3d.py --path /path/to/real/dataset --scene 0 --type wireframe
   ```

3. **Explore 3,500 professional house designs** with:
   - Multiple rooms per house
   - Various lighting conditions
   - Different furniture configurations
   - Rich semantic annotations

## 💡 Tips

- **Fast iteration:** Dummy data loads instantly vs minutes for real scenes
- **Disk space:** Save hundreds of GB while learning
- **Debugging:** Test your modifications quickly
- **Understanding:** Learn the data structure without overwhelming complexity

## 📚 Additional Resources

- `HOW_IT_WORKS.md` - Detailed technical explanation
- `demo_visualization.py` - Interactive demonstrations
- Original README.md - Official documentation

---

**Created for easy testing and learning without the massive real dataset!**

Enjoy exploring Structured3D! 🏗️✨
