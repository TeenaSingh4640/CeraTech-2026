"""
Add measurement overlays to visualization images
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch, FancyArrowPatch
from matplotlib.patches import ConnectionPatch
import cv2

def add_measurements_to_floorplan(scene_path, output_path):
    """Add dimension measurements to floorplan"""
    
    # Load annotation
    with open(f"{scene_path}/annotation_3d.json", 'r') as f:
        annotation = json.load(f)
    
    # Load bbox
    bbox_path = f"{scene_path}/bbox_3d.json"
    bboxes = []
    if os.path.exists(bbox_path):
        with open(bbox_path, 'r') as f:
            bboxes = json.load(f)
    
    # Get room dimensions from junctions
    junctions = annotation['junctions']
    if len(junctions) < 4:
        print(f"⚠️  Warning: Not enough junctions to determine dimensions")
        return
    
    # Extract room bounds
    x_coords = [j['coordinate'][0] for j in junctions]
    y_coords = [j['coordinate'][1] for j in junctions]
    z_coords = [j['coordinate'][2] for j in junctions]
    
    width = max(x_coords) - min(x_coords)
    depth = max(y_coords) - min(y_coords)
    height = max(z_coords) - min(z_coords)
    
    # Get room type from semantics
    room_type = "Room"
    if annotation.get('semantics'):
        for sem in annotation['semantics']:
            if 'type' in sem:
                room_type = sem['type'].title()
                break
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Room colors
    colors = {
        'Bedroom': '#FFE5E5',
        'Kitchen': '#E5F5FF',
        'Bathroom': '#E5FFE5',
        'Living_room': '#FFF5E5',
        'Living': '#FFF5E5'
    }
    
    # Draw room
    room_poly = Polygon([[0, 0], [width, 0], [width, depth], [0, depth]], 
                        facecolor=colors.get(room_type, '#F0F0F0'),
                        edgecolor='black', linewidth=3)
    ax.add_patch(room_poly)
    
    # Draw furniture bounding boxes
    for idx, bbox in enumerate(bboxes):
        center = bbox['centroid']
        coeffs = bbox['coeffs']
        x, y = center[0], center[1]
        w, d = coeffs[0]*2, coeffs[1]*2
        
        furniture_poly = Polygon([
            [x-w/2, y-d/2],
            [x+w/2, y-d/2],
            [x+w/2, y+d/2],
            [x-w/2, y+d/2]
        ], facecolor='#8B4513', edgecolor='black', linewidth=2, alpha=0.7)
        ax.add_patch(furniture_poly)
        
        # Add furniture label with background
        label_box = FancyBboxPatch((x-w/2, y+d/2+0.05), w, 0.25, 
                                   boxstyle="round,pad=0.05", 
                                   facecolor='white', edgecolor='black', 
                                   linewidth=1.5, alpha=0.9)
        ax.add_patch(label_box)
        
        # Handle both string IDs (like "bed_1") and numeric IDs (like 0, 1, 2)
        bbox_id = bbox['ID']
        if isinstance(bbox_id, str):
            name = bbox_id.split('_')[0].title()
        else:
            name = f"Object {bbox_id}"
        
        ax.text(x, y+d/2+0.175, name, 
                ha='center', va='center', fontsize=9, weight='bold')
        
        # Add furniture dimensions
        ax.text(x, y, f'{w:.2f}m × {d:.2f}m', 
                ha='center', va='center', fontsize=7, 
                color='white', weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
    
    # Add room dimension arrows and labels
    arrow_props = dict(arrowstyle='<->', lw=3, color='red', mutation_scale=20)
    
    # Width arrow (bottom)
    arrow_width = FancyArrowPatch((0, -0.4), (width, -0.4),
                                  **arrow_props)
    ax.add_patch(arrow_width)
    ax.text(width/2, -0.6, f'Width: {width:.2f}m', 
            ha='center', va='top', fontsize=14, weight='bold', color='red',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='red', linewidth=2))
    
    # Depth arrow (left)
    arrow_depth = FancyArrowPatch((-0.4, 0), (-0.4, depth),
                                  **arrow_props)
    ax.add_patch(arrow_depth)
    ax.text(-0.6, depth/2, f'Depth: {depth:.2f}m', 
            ha='right', va='center', fontsize=14, weight='bold', color='red',
            rotation=90,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='red', linewidth=2))
    
    # Height label (top right)
    height_text = f'Height: {height:.2f}m'
    ax.text(width+0.2, depth+0.2, height_text, 
            ha='left', va='bottom', fontsize=14, weight='bold', color='blue',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='blue', linewidth=2))
    
    # Area label (center bottom)
    area = width * depth
    area_text = f'Floor Area: {area:.2f} m²'
    ax.text(width/2, depth+0.5, area_text, 
            ha='center', va='bottom', fontsize=16, weight='bold', color='green',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='green', linewidth=2))
    
    # Volume label (center)
    volume = area * height
    volume_text = f'Volume: {volume:.1f} m³'
    ax.text(width/2, depth+0.8, volume_text, 
            ha='center', va='bottom', fontsize=14, weight='bold', color='purple',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='purple', linewidth=2))
    
    # Add scale indicator
    scale_x = width * 0.05
    scale_length = 1.0  # 1 meter scale
    ax.plot([scale_x, scale_x + scale_length], [depth * 0.05, depth * 0.05], 
            'k-', linewidth=4)
    ax.plot([scale_x, scale_x], [depth * 0.05 - 0.05, depth * 0.05 + 0.05], 
            'k-', linewidth=3)
    ax.plot([scale_x + scale_length, scale_x + scale_length], 
            [depth * 0.05 - 0.05, depth * 0.05 + 0.05], 'k-', linewidth=3)
    ax.text(scale_x + scale_length/2, depth * 0.05 - 0.15, '1.0m', 
            ha='center', va='top', fontsize=10, weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))
    
    # Add corner markers
    corner_size = 0.1
    for corner in [[0, 0], [width, 0], [width, depth], [0, depth]]:
        circle = plt.Circle(corner, corner_size, color='red', zorder=5)
        ax.add_patch(circle)
    
    # Set limits and styling
    margin = 1.2
    ax.set_xlim(-margin, width + margin)
    ax.set_ylim(-margin, depth + margin + 0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle='--')
    ax.set_xlabel('X-axis (meters)', fontsize=12, weight='bold')
    ax.set_ylabel('Y-axis (meters)', fontsize=12, weight='bold')
    ax.set_title(f'{room_type} - Detailed Measurements', 
                fontsize=18, weight='bold', pad=20)
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], color='red', linewidth=3, label='Dimensions'),
        plt.Rectangle((0, 0), 1, 1, fc='#8B4513', alpha=0.7, label='Furniture'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                   markersize=10, label='Corners')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Measurement overlay created: {output_path}")


def add_measurements_to_all_scenes():
    """Add measurement overlays to all scenes"""
    print("\n📏 Adding measurement overlays to all scenes...\n")
    
    scenes = []
    for i in range(4):
        scene_path = f"dummy_dataset/scene_{i:05d}"
        if os.path.exists(scene_path):
            scenes.append((i, scene_path))
    
    for scene_id, scene_path in scenes:
        print(f"📐 Processing scene {scene_id:05d}...")
        output_path = f"{scene_path}/floorplan_measurements.png"
        add_measurements_to_floorplan(scene_path, output_path)
    
    print(f"\n✅ All measurement overlays created!")
    print(f"📁 Files saved as: floorplan_measurements.png in each scene folder")


if __name__ == "__main__":
    add_measurements_to_all_scenes()
