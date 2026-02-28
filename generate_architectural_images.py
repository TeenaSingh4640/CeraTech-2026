"""
AI Structural Design - Architectural Rendering Generator
Generates professional architectural visualizations including floor plans, elevations, and 3D views
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch, Arc
from PIL import Image, ImageDraw, ImageFont
import json
import sys
import os
from datetime import datetime

def generate_floor_plan(data, floor_num, output_path):
    """Generate detailed floor plan"""
    fig, ax = plt.subplots(figsize=(16, 12), facecolor='white')
    ax.set_aspect('equal')
    
    plot_l = data['plot_length']
    plot_w = data['plot_width']
    bay_size = 4.5 if data['building_type'] == 'Residential' else 6.0
    
    # Building footprint (80% of plot)
    building_l = plot_l * 0.8
    building_w = plot_w * 0.8
    offset_x = (plot_l - building_l) / 2
    offset_y = (plot_w - building_w) / 2
    
    # Draw plot boundary
    plot_rect = Rectangle((0, 0), plot_l, plot_w, linewidth=3, edgecolor='black', 
                           facecolor='#f0f0f0', linestyle='--', alpha=0.3)
    ax.add_patch(plot_rect)
    
    # Draw building outline with thick walls
    wall_thickness = 0.25
    building_rect = Rectangle((offset_x, offset_y), building_l, building_w, 
                               linewidth=6, edgecolor='black', facecolor='white')
    ax.add_patch(building_rect)
    
    # Draw structural grid (columns)
    num_cols_x = int(building_l / bay_size) + 1
    num_cols_y = int(building_w / bay_size) + 1
    
    for i in range(num_cols_x):
        for j in range(num_cols_y):
            col_x = offset_x + i * bay_size
            col_y = offset_y + j * bay_size
            if col_x <= offset_x + building_l and col_y <= offset_y + building_w:
                # Column (450mm x 450mm)
                col_size = 0.45
                column = Rectangle((col_x - col_size/2, col_y - col_size/2), 
                                  col_size, col_size, 
                                  facecolor='#2c3e50', edgecolor='black', linewidth=1.5)
                ax.add_patch(column)
                # Column label
                ax.text(col_x, col_y - 0.8, f'C{i+1}{j+1}', ha='center', va='top', 
                       fontsize=7, color='#2c3e50', fontweight='bold')
    
    # Draw grid lines
    for i in range(num_cols_x):
        x = offset_x + i * bay_size
        ax.plot([x, x], [offset_y, offset_y + building_w], 'b--', 
               linewidth=0.5, alpha=0.3)
        ax.text(x, offset_y - 1, f'{i*bay_size:.1f}m', ha='center', va='top', 
               fontsize=8, color='blue')
    
    for j in range(num_cols_y):
        y = offset_y + j * bay_size
        ax.plot([offset_x, offset_x + building_l], [y, y], 'b--', 
               linewidth=0.5, alpha=0.3)
        ax.text(offset_x - 1, y, f'{j*bay_size:.1f}m', ha='right', va='center', 
               fontsize=8, color='blue')
    
    # Draw rooms based on building type
    if data['building_type'] == 'Residential':
        # Typical residential floor plan
        # Core area (center 30%)
        core_x = offset_x + building_l * 0.35
        core_y = offset_y + building_w * 0.35
        core_w = building_l * 0.3
        core_h = building_w * 0.3
        
        # Service core (lifts + stairs)
        core_rect = FancyBboxPatch((core_x, core_y), core_w, core_h,
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#e74c3c', edgecolor='black', 
                                   linewidth=2, alpha=0.6)
        ax.add_patch(core_rect)
        ax.text(core_x + core_w/2, core_y + core_h/2, 'SERVICE\nCORE\n(Lifts+Stairs)', 
               ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Apartments around core
        apt_zones = [
            {'x': offset_x + 1, 'y': offset_y + 1, 'w': building_l*0.3, 'h': building_w*0.3, 'label': 'APT 1\n2BHK'},
            {'x': offset_x + building_l*0.65, 'y': offset_y + 1, 'w': building_l*0.3, 'h': building_w*0.3, 'label': 'APT 2\n2BHK'},
            {'x': offset_x + 1, 'y': offset_y + building_w*0.65, 'w': building_l*0.3, 'h': building_w*0.3, 'label': 'APT 3\n2BHK'},
            {'x': offset_x + building_l*0.65, 'y': offset_y + building_w*0.65, 'w': building_l*0.3, 'h': building_w*0.3, 'label': 'APT 4\n2BHK'},
        ]
        
        for apt in apt_zones:
            apt_rect = Rectangle((apt['x'], apt['y']), apt['w'], apt['h'],
                                facecolor='#3498db', edgecolor='black', 
                                linewidth=1.5, alpha=0.4)
            ax.add_patch(apt_rect)
            ax.text(apt['x'] + apt['w']/2, apt['y'] + apt['h']/2, apt['label'],
                   ha='center', va='center', fontsize=9, fontweight='bold')
    
    else:  # Commercial/Institutional
        # Open plan with core
        core_x = offset_x + building_l * 0.4
        core_y = offset_y + building_w * 0.4
        core_w = building_l * 0.2
        core_h = building_w * 0.2
        
        core_rect = FancyBboxPatch((core_x, core_y), core_w, core_h,
                                   boxstyle="round,pad=0.1",
                                   facecolor='#e67e22', edgecolor='black',
                                   linewidth=2, alpha=0.6)
        ax.add_patch(core_rect)
        ax.text(core_x + core_w/2, core_y + core_h/2, 'CORE\n(Vert. Circ.)',
               ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Open office area
        office_rect = Rectangle((offset_x + 1, offset_y + 1), 
                                building_l - 2, building_w - 2,
                                facecolor='#9b59b6', edgecolor='black',
                                linewidth=1.5, alpha=0.2)
        ax.add_patch(office_rect)
        ax.text(offset_x + building_l/2, offset_y + building_w/2 + building_w*0.3,
               'OPEN PLAN OFFICE SPACE',
               ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Draw entrance
    entrance_w = 4
    entrance_rect = Rectangle((offset_x + building_l/2 - entrance_w/2, offset_y - 0.1),
                              entrance_w, 0.1, facecolor='#27ae60', 
                              edgecolor='black', linewidth=2)
    ax.add_patch(entrance_rect)
    ax.text(offset_x + building_l/2, offset_y - 1.5, '▼ MAIN ENTRANCE',
           ha='center', va='top', fontsize=11, fontweight='bold', color='#27ae60')
    
    # Add dimensions
    ax.annotate('', xy=(plot_l, -3), xytext=(0, -3),
                arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    ax.text(plot_l/2, -3.5, f'PLOT LENGTH = {plot_l:.1f}m',
           ha='center', va='top', fontsize=10, color='red', fontweight='bold')
    
    ax.annotate('', xy=(-3, plot_w), xytext=(-3, 0),
                arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    ax.text(-3.5, plot_w/2, f'PLOT WIDTH = {plot_w:.1f}m',
           ha='center', va='center', fontsize=10, color='red', 
           fontweight='bold', rotation=90)
    
    # Title and info
    title = f"FLOOR PLAN - {data['building_type'].upper()} BUILDING\n"
    title += f"Floor {floor_num} | Location: {data['location']} | Scale: 1:100"
    ax.text(plot_l/2, plot_w + 3, title, ha='center', va='bottom',
           fontsize=14, fontweight='bold', color='#2c3e50')
    
    # Legend
    legend_x = plot_l + 2
    legend_y = plot_w - 5
    ax.text(legend_x, legend_y, 'LEGEND:', fontsize=10, fontweight='bold')
    legend_items = [
        ('Column (450×450mm)', '#2c3e50'),
        ('Service Core', '#e74c3c' if data['building_type'] == 'Residential' else '#e67e22'),
        ('Occupied Space', '#3498db' if data['building_type'] == 'Residential' else '#9b59b6'),
        ('Plot Boundary', '#f0f0f0'),
    ]
    for i, (label, color) in enumerate(legend_items):
        y = legend_y - (i+1)*1.2
        legend_rect = Rectangle((legend_x, y), 0.8, 0.8, facecolor=color, 
                               edgecolor='black', linewidth=1)
        ax.add_patch(legend_rect)
        ax.text(legend_x + 1.2, y + 0.4, label, va='center', fontsize=8)
    
    # Project info box
    info_y = 5
    info_text = f"Project: {data['building_type']} Building\n"
    info_text += f"Floors: {data['num_floors']} | Bay: {bay_size}m×{bay_size}m\n"
    info_text += f"Climate: {data['climate_zone']} | Seismic: Zone {data['seismic_zone']}"
    ax.text(legend_x, info_y, info_text, fontsize=8, 
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_xlim(-5, plot_l + 15)
    ax.set_ylim(-5, plot_w + 5)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Floor plan saved: {output_path}")

def generate_elevation(data, output_path):
    """Generate building elevation view"""
    fig, ax = plt.subplots(figsize=(18, 10), facecolor='white')
    
    building_l = data['plot_length'] * 0.8
    floor_height = 3.5
    total_height = data['num_floors'] * floor_height
    ground_level = 2
    
    # Sky
    sky = Rectangle((0, ground_level + total_height), building_l * 1.5, 15,
                    facecolor='#87CEEB', alpha=0.3)
    ax.add_patch(sky)
    
    # Ground
    ground = Rectangle((0, 0), building_l * 1.5, ground_level,
                       facecolor='#8B7355', alpha=0.3)
    ax.add_patch(ground)
    
    # Building mass
    building = Rectangle((5, ground_level), building_l, total_height,
                         facecolor='#ecf0f1', edgecolor='black', linewidth=3)
    ax.add_patch(building)
    
    # Draw floors
    for i in range(data['num_floors'] + 1):
        y = ground_level + i * floor_height
        ax.plot([5, 5 + building_l], [y, y], 'k-', linewidth=2)
        if i < data['num_floors']:
            # Floor label
            ax.text(3, y + floor_height/2, f'FL {i+1}', ha='right', va='center',
                   fontsize=9, fontweight='bold')
    
    # Windows - different patterns based on building type
    if data['building_type'] == 'Residential':
        # Punched windows for residential
        window_w = 1.5
        window_h = 1.8
        for floor in range(data['num_floors']):
            y = ground_level + floor * floor_height + (floor_height - window_h) / 2
            for col in range(int(building_l / 4)):
                x = 5 + col * 4 + 1.5
                if x + window_w < 5 + building_l:
                    window = Rectangle((x, y), window_w, window_h,
                                      facecolor='#3498db', edgecolor='black',
                                      linewidth=1, alpha=0.7)
                    ax.add_patch(window)
    else:
        # Curtain wall for commercial
        for floor in range(data['num_floors']):
            y = ground_level + floor * floor_height + 0.2
            curtain = Rectangle((5.5, y), building_l - 1, floor_height - 0.4,
                               facecolor='#5dade2', edgecolor='#34495e',
                               linewidth=1.5, alpha=0.5)
            ax.add_patch(curtain)
            # Mullions
            for i in range(int(building_l / 2)):
                x = 5.5 + i * 2
                ax.plot([x, x], [y, y + floor_height - 0.4], 'k-', linewidth=0.8)
    
    # Entrance
    entrance_y = ground_level
    entrance = Rectangle((5 + building_l/2 - 3, entrance_y), 6, floor_height * 1.5,
                         facecolor='#2c3e50', edgecolor='black', linewidth=2)
    ax.add_patch(entrance)
    ax.text(5 + building_l/2, entrance_y + floor_height * 0.8, 'ENTRANCE',
           ha='center', va='center', fontsize=10, fontweight='bold',
           color='white')
    
    # Parapet
    parapet = Rectangle((5, ground_level + total_height), building_l, 0.8,
                       facecolor='#7f8c8d', edgecolor='black', linewidth=2)
    ax.add_patch(parapet)
    
    # Height dimensions
    ax.annotate('', xy=(building_l + 8, ground_level + total_height), 
               xytext=(building_l + 8, ground_level),
               arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    ax.text(building_l + 9, ground_level + total_height/2,
           f'H = {total_height:.1f}m\n({data["num_floors"]} floors)',
           ha='left', va='center', fontsize=10, color='red', fontweight='bold')
    
    # Width dimension
    ax.annotate('', xy=(5 + building_l, ground_level - 1), xytext=(5, ground_level - 1),
               arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    ax.text(5 + building_l/2, ground_level - 1.5, f'W = {building_l:.1f}m',
           ha='center', va='top', fontsize=10, color='red', fontweight='bold')
    
    # Title
    title = f"FRONT ELEVATION - {data['building_type'].upper()} BUILDING\n"
    title += f"Location: {data['location']} | Style: {data['architectural_style']} | Scale: 1:200"
    ax.text(building_l/2 + 5, total_height + ground_level + 3, title,
           ha='center', va='bottom', fontsize=14, fontweight='bold', color='#2c3e50')
    
    ax.set_xlim(0, building_l + 20)
    ax.set_ylim(0, total_height + ground_level + 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Elevation saved: {output_path}")

def generate_3d_view(data, output_path):
    """Generate 3D isometric view"""
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    building_l = data['plot_length'] * 0.8
    building_w = data['plot_width'] * 0.8
    building_h = data['num_floors'] * 3.5
    
    # Building vertices
    vertices = np.array([
        [0, 0, 0], [building_l, 0, 0], [building_l, building_w, 0], [0, building_w, 0],  # Base
        [0, 0, building_h], [building_l, 0, building_h], [building_l, building_w, building_h], [0, building_w, building_h]  # Top
    ])
    
    # Define the 6 faces
    faces = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back
        [vertices[3], vertices[0], vertices[4], vertices[7]],  # Left
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top
        [vertices[0], vertices[1], vertices[2], vertices[3]]   # Bottom
    ]
    
    # Colors for each face
    facecolors = ['#bdc3c7', '#95a5a6', '#7f8c8d', '#bdc3c7', '#34495e', '#2c3e50']
    
    # Create the collection
    poly = Poly3DCollection(faces, alpha=0.8, facecolors=facecolors, 
                            edgecolors='black', linewidths=2)
    ax.add_collection3d(poly)
    
    # Draw floors
    for i in range(1, data['num_floors']):
        z = i * 3.5
        floor_vertices = [
            [0, 0, z], [building_l, 0, z], [building_l, building_w, z], [0, building_w, z]
        ]
        floor_face = [floor_vertices]
        floor_poly = Poly3DCollection(floor_face, alpha=0.3, facecolors='none',
                                     edgecolors='blue', linewidths=1, linestyles='--')
        ax.add_collection3d(floor_poly)
    
    # Draw structural grid (columns)
    bay_size = 4.5 if data['building_type'] == 'Residential' else 6.0
    num_cols_x = int(building_l / bay_size) + 1
    num_cols_y = int(building_w / bay_size) + 1
    
    for i in range(num_cols_x):
        for j in range(num_cols_y):
            x = i * bay_size
            y = j * bay_size
            if x <= building_l and y <= building_w:
                ax.plot([x, x], [y, y], [0, building_h], 'r-', linewidth=2, alpha=0.7)
    
    # Ground plane
    xx, yy = np.meshgrid([-5, building_l+5], [-5, building_w+5])
    zz = np.zeros_like(xx)
    ax.plot_surface(xx, yy, zz, alpha=0.2, color='green')
    
    # Labels
    ax.text(building_l/2, -5, building_h + 5, 
           f'{data["building_type"].upper()} BUILDING - 3D VIEW\n{data["location"]}',
           ha='center', fontsize=14, fontweight='bold', color='#2c3e50')
    
    ax.set_xlabel('Length (m)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Width (m)', fontsize=10, fontweight='bold')
    ax.set_zlabel('Height (m)', fontsize=10, fontweight='bold')
    
    ax.set_xlim([-5, building_l + 5])
    ax.set_ylim([-5, building_w + 5])
    ax.set_zlim([0, building_h + 10])
    
    ax.view_init(elev=25, azim=45)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 3D view saved: {output_path}")

def generate_site_plan(data, output_path):
    """Generate site plan"""
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
    ax.set_aspect('equal')
    
    plot_l = data['plot_length']
    plot_w = data['plot_width']
    building_l = plot_l * 0.8
    building_w = plot_w * 0.8
    offset_x = (plot_l - building_l) / 2
    offset_y = (plot_w - building_w) / 2
    
    # Plot boundary
    plot_rect = Rectangle((0, 0), plot_l, plot_w, linewidth=4, 
                          edgecolor='red', facecolor='#90EE90', alpha=0.2)
    ax.add_patch(plot_rect)
    
    # Building footprint
    building_rect = Rectangle((offset_x, offset_y), building_l, building_w,
                              facecolor='#95a5a6', edgecolor='black', linewidth=3)
    ax.add_patch(building_rect)
    ax.text(offset_x + building_l/2, offset_y + building_w/2, 'BUILDING\nFOOTPRINT',
           ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # Setbacks
    for side, coords in [
        ('FRONT SETBACK', (plot_l/2, offset_y/2)),
        ('REAR SETBACK', (plot_l/2, offset_y + building_w + offset_y/2)),
        ('LEFT SETBACK', (offset_x/2, plot_w/2)),
        ('RIGHT SETBACK', (offset_x + building_l + offset_x/2, plot_w/2))
    ]:
        ax.text(coords[0], coords[1], side, ha='center', va='center',
               fontsize=9, fontweight='bold', color='#27ae60',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Landscaping
    for _ in range(8):
        tree_x = np.random.uniform(1, plot_l-1)
        tree_y = np.random.uniform(1, plot_w-1)
        if not (offset_x < tree_x < offset_x + building_l and 
               offset_y < tree_y < offset_y + building_w):
            tree = Circle((tree_x, tree_y), 0.8, facecolor='#27ae60', 
                         edgecolor='#229954', linewidth=1.5, alpha=0.6)
            ax.add_patch(tree)
    
    # Access road
    road = Rectangle((0, -2), plot_l, 2, facecolor='#34495e', alpha=0.5)
    ax.add_patch(road)
    ax.text(plot_l/2, -1, 'ACCESS ROAD', ha='center', va='center',
           fontsize=12, fontweight='bold', color='white')
    
    # North arrow
    arrow_x, arrow_y = plot_l - 3, plot_w - 3
    ax.arrow(arrow_x, arrow_y, 0, 2, head_width=0.5, head_length=0.3,
            fc='red', ec='red', linewidth=2)
    ax.text(arrow_x, arrow_y + 2.5, 'N', ha='center', va='bottom',
           fontsize=14, fontweight='bold', color='red')
    
    # Dimensions
    ax.text(plot_l/2, plot_w + 1.5, f'{plot_l:.1f}m', ha='center', va='bottom',
           fontsize=11, fontweight='bold', color='red')
    ax.text(-1.5, plot_w/2, f'{plot_w:.1f}m', ha='right', va='center',
           fontsize=11, fontweight='bold', color='red', rotation=90)
    
    # Title
    title = f"SITE PLAN - {data['location'].upper()}\n"
    title += f"{data['building_type']} Building | Plot Area: {plot_l*plot_w:.1f} m²"
    ax.text(plot_l/2, plot_w + 3, title, ha='center', va='bottom',
           fontsize=14, fontweight='bold', color='#2c3e50')
    
    ax.set_xlim(-3, plot_l + 3)
    ax.set_ylim(-4, plot_w + 5)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Site plan saved: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_architectural_images.py <design_data.json>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Create output directory
    output_dir = f"exports/design_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n🎨 Generating Architectural Renderings...\n")
    
    # Generate all views
    generate_site_plan(data, f"{output_dir}/01_site_plan.png")
    generate_floor_plan(data, 1, f"{output_dir}/02_ground_floor_plan.png")
    generate_floor_plan(data, 5, f"{output_dir}/03_typical_floor_plan.png")
    generate_elevation(data, f"{output_dir}/04_front_elevation.png")
    generate_3d_view(data, f"{output_dir}/05_3d_isometric_view.png")
    
    print(f"\n✅ All renderings generated successfully!")
    print(f"📁 Output directory: {output_dir}\n")
    
    # Return output directory path
    print(f"OUTPUT_DIR:{output_dir}")

if __name__ == "__main__":
    main()
