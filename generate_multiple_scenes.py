"""
Generate multiple dummy scenes with different room types
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import cv2

def create_bedroom_scene():
    """Create a bedroom scene (4m x 4.5m x 2.8m)"""
    # Bedroom: 4m wide x 4.5m deep x 2.8m high
    w, d, h = 4.0, 4.5, 2.8
    
    # 8 corners of the room
    junctions = [
        {"coordinate": [0, 0, 0]},      # 0: bottom-left-floor
        {"coordinate": [w, 0, 0]},      # 1: bottom-right-floor
        {"coordinate": [w, d, 0]},      # 2: top-right-floor
        {"coordinate": [0, d, 0]},      # 3: top-left-floor
        {"coordinate": [0, 0, h]},      # 4: bottom-left-ceiling
        {"coordinate": [w, 0, h]},      # 5: bottom-right-ceiling
        {"coordinate": [w, d, h]},      # 6: top-right-ceiling
        {"coordinate": [0, d, h]},      # 7: top-left-ceiling
        # Window junction
        {"coordinate": [1.0, 0, 1.0]},  # 8
        {"coordinate": [3.0, 0, 1.0]},  # 9
        {"coordinate": [3.0, 0, 2.3]},  # 10
        {"coordinate": [1.0, 0, 2.3]},  # 11
    ]
    
    annotation = {
        "junctions": junctions,
        "lines": [],
        "planes": [],
        "semantics": []
    }
    
    # Floor (plane 0)
    annotation["planes"].append({"normal": [0, 0, 1], "offset": 0})
    annotation["lines"].extend([
        {"point": [0, 1]},  # 0
        {"point": [1, 2]},  # 1
        {"point": [2, 3]},  # 2
        {"point": [3, 0]},  # 3
    ])
    
    # Ceiling (plane 1)
    annotation["planes"].append({"normal": [0, 0, -1], "offset": h})
    annotation["lines"].extend([
        {"point": [4, 5]},  # 4
        {"point": [5, 6]},  # 5
        {"point": [6, 7]},  # 6
        {"point": [7, 4]},  # 7
    ])
    
    # South wall with window (plane 2)
    annotation["planes"].append({"normal": [0, 1, 0], "offset": 0})
    annotation["lines"].extend([
        {"point": [0, 4]},  # 8
        {"point": [4, 5]},  # 9
        {"point": [5, 1]},  # 10
        {"point": [1, 0]},  # 11
        {"point": [8, 9]},  # 12
        {"point": [9, 10]}, # 13
        {"point": [10, 11]},# 14
        {"point": [11, 8]}, # 15
    ])
    
    # North wall (plane 3)
    annotation["planes"].append({"normal": [0, -1, 0], "offset": d})
    annotation["lines"].extend([
        {"point": [2, 6]},  # 16
        {"point": [6, 7]},  # 17
        {"point": [7, 3]},  # 18
        {"point": [3, 2]},  # 19
    ])
    
    # West wall (plane 4)
    annotation["planes"].append({"normal": [1, 0, 0], "offset": 0})
    annotation["lines"].extend([
        {"point": [0, 3]},  # 20
        {"point": [3, 7]},  # 21
        {"point": [7, 4]},  # 22
        {"point": [4, 0]},  # 23
    ])
    
    # East wall (plane 5)
    annotation["planes"].append({"normal": [-1, 0, 0], "offset": w})
    annotation["lines"].extend([
        {"point": [1, 5]},  # 24
        {"point": [5, 6]},  # 25
        {"point": [6, 2]},  # 26
        {"point": [2, 1]},  # 27
    ])
    
    # Window (plane 6)
    annotation["planes"].append({"normal": [0, 1, 0], "offset": 0})
    
    # Semantics
    annotation["semantics"] = [
        {"type": "bedroom", "planeID": [0, 1, 2, 3, 4, 5]},
        {"type": "window", "planeID": [6]}
    ]
    
    # Create bounding boxes for bedroom furniture
    bboxes = [
        # Bed (2.0m x 1.6m x 0.6m height)
        {
            "ID": "bed_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [1.0, 0.8, 0.3],  # half extents
            "centroid": [2.0, 3.0, 0.3]
        },
        # Nightstand (0.5m x 0.5m x 0.5m)
        {
            "ID": "nightstand_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.25, 0.25, 0.25],
            "centroid": [3.5, 3.5, 0.25]
        },
        # Wardrobe (1.5m x 0.6m x 2.0m)
        {
            "ID": "wardrobe_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.75, 0.3, 1.0],
            "centroid": [0.75, 0.6, 1.0]
        },
        # Desk (1.2m x 0.6m x 0.75m)
        {
            "ID": "desk_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.6, 0.3, 0.375],
            "centroid": [3.2, 0.6, 0.375]
        }
    ]
    
    return annotation, bboxes, "bedroom", (w, d, h)


def create_kitchen_scene():
    """Create a kitchen scene (5m x 3.5m x 2.6m)"""
    w, d, h = 5.0, 3.5, 2.6
    
    # 8 corners
    junctions = [
        {"coordinate": [0, 0, 0]},      # 0
        {"coordinate": [w, 0, 0]},      # 1
        {"coordinate": [w, d, 0]},      # 2
        {"coordinate": [0, d, 0]},      # 3
        {"coordinate": [0, 0, h]},      # 4
        {"coordinate": [w, 0, h]},      # 5
        {"coordinate": [w, d, h]},      # 6
        {"coordinate": [0, d, h]},      # 7
    ]
    
    annotation = {
        "junctions": junctions,
        "lines": [],
        "planes": [],
        "semantics": []
    }
    
    # Similar structure to bedroom (simplified)
    annotation["planes"] = [
        {"normal": [0, 0, 1], "offset": 0},      # floor
        {"normal": [0, 0, -1], "offset": h},     # ceiling
        {"normal": [0, 1, 0], "offset": 0},      # south
        {"normal": [0, -1, 0], "offset": d},     # north
        {"normal": [1, 0, 0], "offset": 0},      # west
        {"normal": [-1, 0, 0], "offset": w},     # east
    ]
    
    # Basic lines
    for i in range(4):
        annotation["lines"].append({"point": [i, (i+1)%4]})
    for i in range(4):
        annotation["lines"].append({"point": [i+4, ((i+1)%4)+4]})
    for i in range(4):
        annotation["lines"].append({"point": [i, i+4]})
    
    annotation["semantics"] = [
        {"type": "kitchen", "planeID": [0, 1, 2, 3, 4, 5]}
    ]
    
    bboxes = [
        # Counter (2.5m x 0.6m x 0.9m)
        {
            "ID": "counter_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [1.25, 0.3, 0.45],
            "centroid": [1.25, 0.5, 0.45]
        },
        # Refrigerator (0.8m x 0.8m x 1.8m)
        {
            "ID": "refrigerator_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.4, 0.4, 0.9],
            "centroid": [4.5, 0.6, 0.9]
        },
        # Table (1.2m x 0.8m x 0.75m)
        {
            "ID": "table_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.6, 0.4, 0.375],
            "centroid": [2.5, 2.5, 0.375]
        },
        # Stove (0.6m x 0.6m x 0.9m)
        {
            "ID": "stove_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.3, 0.3, 0.45],
            "centroid": [3.0, 0.5, 0.45]
        }
    ]
    
    return annotation, bboxes, "kitchen", (w, d, h)


def create_bathroom_scene():
    """Create a bathroom scene (3m x 2.5m x 2.4m)"""
    w, d, h = 3.0, 2.5, 2.4
    
    junctions = [
        {"coordinate": [0, 0, 0]},      # 0
        {"coordinate": [w, 0, 0]},      # 1
        {"coordinate": [w, d, 0]},      # 2
        {"coordinate": [0, d, 0]},      # 3
        {"coordinate": [0, 0, h]},      # 4
        {"coordinate": [w, 0, h]},      # 5
        {"coordinate": [w, d, h]},      # 6
        {"coordinate": [0, d, h]},      # 7
    ]
    
    annotation = {
        "junctions": junctions,
        "lines": [],
        "planes": [],
        "semantics": []
    }
    
    annotation["planes"] = [
        {"normal": [0, 0, 1], "offset": 0},
        {"normal": [0, 0, -1], "offset": h},
        {"normal": [0, 1, 0], "offset": 0},
        {"normal": [0, -1, 0], "offset": d},
        {"normal": [1, 0, 0], "offset": 0},
        {"normal": [-1, 0, 0], "offset": w},
    ]
    
    for i in range(4):
        annotation["lines"].append({"point": [i, (i+1)%4]})
    for i in range(4):
        annotation["lines"].append({"point": [i+4, ((i+1)%4)+4]})
    for i in range(4):
        annotation["lines"].append({"point": [i, i+4]})
    
    annotation["semantics"] = [
        {"type": "bathroom", "planeID": [0, 1, 2, 3, 4, 5]}
    ]
    
    bboxes = [
        # Sink (0.6m x 0.5m x 0.85m)
        {
            "ID": "sink_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.3, 0.25, 0.425],
            "centroid": [0.5, 0.4, 0.425]
        },
        # Toilet (0.5m x 0.7m x 0.75m)
        {
            "ID": "toilet_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.25, 0.35, 0.375],
            "centroid": [2.5, 0.5, 0.375]
        },
        # Bathtub (1.6m x 0.7m x 0.6m)
        {
            "ID": "bathtub_1",
            "basis": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "coeffs": [0.8, 0.35, 0.3],
            "centroid": [1.5, 2.0, 0.3]
        }
    ]
    
    return annotation, bboxes, "bathroom", (w, d, h)


def generate_scene_visualizations(scene_id, annotation, bboxes, room_type, dimensions):
    """Generate all visualizations for a scene"""
    output_dir = f"dummy_dataset/scene_{scene_id:05d}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save JSON files
    with open(f"{output_dir}/annotation_3d.json", 'w') as f:
        json.dump(annotation, f, indent=2)
    
    with open(f"{output_dir}/bbox_3d.json", 'w') as f:
        json.dump(bboxes, f, indent=2)
    
    # Generate semantic floorplan
    generate_semantic_floorplan(output_dir, annotation, bboxes, room_type, dimensions)
    
    # Generate top view
    generate_top_view(output_dir, annotation, bboxes, dimensions)
    
    # Generate stats
    return {
        "scene_id": f"{scene_id:05d}",
        "room_type": room_type,
        "dimensions": dimensions,
        "objects": len(bboxes),
        "area": dimensions[0] * dimensions[1]
    }


def generate_semantic_floorplan(output_dir, annotation, bboxes, room_type, dimensions):
    """Generate semantic floorplan"""
    w, d, h = dimensions
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Room colors
    colors = {
        'bedroom': '#FFE5E5',
        'kitchen': '#E5F5FF',
        'bathroom': '#E5FFE5',
        'living_room': '#FFF5E5'
    }
    
    # Draw room
    room_poly = Polygon([[0, 0], [w, 0], [w, d], [0, d]], 
                        facecolor=colors.get(room_type, '#F0F0F0'),
                        edgecolor='black', linewidth=2)
    ax.add_patch(room_poly)
    
    # Draw furniture bounding boxes
    for bbox in bboxes:
        center = bbox['centroid']
        coeffs = bbox['coeffs']
        x, y = center[0], center[1]
        width, depth = coeffs[0]*2, coeffs[1]*2
        
        furniture_poly = Polygon([
            [x-width/2, y-depth/2],
            [x+width/2, y-depth/2],
            [x+width/2, y+depth/2],
            [x-width/2, y+depth/2]
        ], facecolor='#8B4513', edgecolor='black', linewidth=1.5, alpha=0.7)
        ax.add_patch(furniture_poly)
        
        # Label
        ax.text(x, y, bbox['ID'].split('_')[0], 
                ha='center', va='center', fontsize=8, color='white', weight='bold')
    
    ax.set_xlim(-0.5, w+0.5)
    ax.set_ylim(-0.5, d+0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Width (m)', fontsize=12)
    ax.set_ylabel('Depth (m)', fontsize=12)
    ax.set_title(f'Semantic Floorplan - {room_type.title()}', fontsize=14, weight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/semantic_floorplan.png', dpi=150, bbox_inches='tight')
    plt.close()


def generate_top_view(output_dir, annotation, bboxes, dimensions):
    """Generate top view"""
    w, d, h = dimensions
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Draw room outline
    ax.plot([0, w, w, 0, 0], [0, 0, d, d, 0], 'k-', linewidth=2)
    
    # Draw furniture
    for bbox in bboxes:
        center = bbox['centroid']
        coeffs = bbox['coeffs']
        x, y = center[0], center[1]
        width, depth = coeffs[0]*2, coeffs[1]*2
        
        rect = plt.Rectangle((x-width/2, y-depth/2), width, depth,
                             facecolor='brown', edgecolor='black', linewidth=1.5, alpha=0.6)
        ax.add_patch(rect)
    
    ax.set_xlim(-0.5, w+0.5)
    ax.set_ylim(-0.5, d+0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('Top View', fontsize=14, weight='bold')
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_view.png', dpi=150, bbox_inches='tight')
    plt.close()


def main():
    """Generate all scenes"""
    print("🏗️  Generating multiple room scenes...")
    
    scenes = [
        create_bedroom_scene(),
        create_kitchen_scene(),
        create_bathroom_scene()
    ]
    
    stats = []
    for idx, (annotation, bboxes, room_type, dimensions) in enumerate(scenes, 1):
        print(f"\n📐 Creating scene {idx:05d} ({room_type})...")
        scene_stats = generate_scene_visualizations(idx, annotation, bboxes, room_type, dimensions)
        stats.append(scene_stats)
        print(f"   ✅ {room_type.title()}: {dimensions[0]}m × {dimensions[1]}m × {dimensions[2]}m")
        print(f"   📦 Objects: {len(bboxes)}")
    
    # Save summary
    with open('dummy_dataset/scenes_summary.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print("\n✅ All scenes generated successfully!")
    print(f"📁 Output: dummy_dataset/scene_00001/, scene_00002/, scene_00003/")
    print(f"📊 Summary: dummy_dataset/scenes_summary.json")

if __name__ == "__main__":
    main()
