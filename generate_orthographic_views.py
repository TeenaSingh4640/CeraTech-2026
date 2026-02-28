"""
Generate Top View (Bird's Eye), Front View, and Side View images of the dummy room
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle
import cv2

# Load the 3D annotations
with open('dummy_dataset/scene_00000/annotation_3d.json', 'r') as f:
    annos = json.load(f)

# Load bounding boxes (furniture)
with open('dummy_dataset/scene_00000/bbox_3d.json', 'r') as f:
    bboxes = json.load(f)

# Extract junctions (corner points)
junctions = np.array([j['coordinate'] for j in annos['junctions']])

print("=" * 70)
print("GENERATING ORTHOGRAPHIC VIEWS OF DUMMY ROOM")
print("=" * 70)
print(f"\nRoom has {len(junctions)} junctions (corners)")
print(f"Room has {len(bboxes)} furniture objects")

# ===========================================================================
# TOP VIEW (Bird's Eye View - Looking Down from Above)
# ===========================================================================

def generate_top_view():
    """Generate top-down view (X-Y plane, looking down Z-axis)"""
    print("\n📐 Generating TOP VIEW (Bird's Eye)...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Get floor and ceiling junctions
    floor_junctions = junctions[junctions[:, 2] < 0.1]  # Z near 0
    ceiling_junctions = junctions[junctions[:, 2] > 2.0]  # Z near ceiling
    
    # Draw floor outline
    if len(floor_junctions) > 0:
        # Sort by angle to get proper polygon
        center = floor_junctions.mean(axis=0)
        angles = np.arctan2(floor_junctions[:, 1] - center[1], 
                           floor_junctions[:, 0] - center[0])
        sorted_idx = np.argsort(angles)
        floor_sorted = floor_junctions[sorted_idx]
        
        # Close the polygon
        floor_closed = np.vstack([floor_sorted, floor_sorted[0]])
        
        # Draw room outline
        ax.fill(floor_closed[:, 0], floor_closed[:, 1], 
                color='lightblue', alpha=0.3, edgecolor='blue', linewidth=2, label='Room')
        ax.plot(floor_closed[:, 0], floor_closed[:, 1], 'b-', linewidth=2)
    
    # Draw corners as points
    ax.scatter(floor_junctions[:, 0], floor_junctions[:, 1], 
              c='red', s=100, marker='o', zorder=5, label='Corners')
    
    # Draw furniture bounding boxes (top view)
    for i, bbox in enumerate(bboxes):
        centroid = np.array(bbox['centroid'])
        coeffs = np.array(bbox['coeffs'])
        basis = np.array(bbox['basis'])
        
        # Get corners of bounding box in 2D (X-Y plane)
        corners_2d = []
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                offset = dx * coeffs[0] * basis[0][:2] + dy * coeffs[1] * basis[1][:2]
                corners_2d.append(centroid[:2] + offset)
        corners_2d = np.array(corners_2d)
        
        # Draw bounding box
        from matplotlib.patches import Polygon
        poly = Polygon(corners_2d[[0, 1, 3, 2]], 
                      facecolor='orange', alpha=0.5, 
                      edgecolor='darkorange', linewidth=2)
        ax.add_patch(poly)
        
        # Label
        ax.text(centroid[0], centroid[1], f'Obj{i+1}', 
               ha='center', va='center', fontsize=10, weight='bold')
    
    # Window (from semantics)
    window_junctions = junctions[8:12]  # Window junctions
    if len(window_junctions) > 0:
        window_center = window_junctions.mean(axis=0)
        ax.scatter(window_center[0], window_center[1], 
                  c='cyan', s=200, marker='s', label='Window', zorder=4)
    
    # Formatting
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (meters)', fontsize=12)
    ax.set_ylabel('Y (meters)', fontsize=12)
    ax.set_title('TOP VIEW (Bird\'s Eye View)\n5m × 4m Living Room', fontsize=14, weight='bold')
    ax.legend(loc='upper right')
    
    # Add compass
    ax.annotate('N', xy=(5.2, 4.2), fontsize=16, weight='bold', color='red')
    ax.arrow(5.2, 3.8, 0, 0.3, head_width=0.1, head_length=0.1, fc='red', ec='red')
    
    # Save
    plt.tight_layout()
    output_path = 'dummy_dataset/scene_00000/top_view.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✅ Saved: {output_path}")
    plt.close()


# ===========================================================================
# FRONT VIEW (Looking at South Wall - along Y-axis)
# ===========================================================================

def generate_front_view():
    """Generate front view (X-Z plane, looking along Y-axis)"""
    print("\n📐 Generating FRONT VIEW (South Wall)...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Project junctions onto X-Z plane
    front_junctions = junctions[:, [0, 2]]  # X and Z coordinates
    
    # Get floor and ceiling edges
    floor_x = front_junctions[front_junctions[:, 1] < 0.1, 0]
    ceiling_x = front_junctions[front_junctions[:, 1] > 2.0, 0]
    
    if len(floor_x) > 0:
        floor_x = np.sort(floor_x)
        ceiling_x = np.sort(ceiling_x)
        
        # Draw room outline
        room_outline = np.array([
            [floor_x[0], 0],
            [floor_x[-1], 0],
            [ceiling_x[-1], 2.5],
            [ceiling_x[0], 2.5],
            [floor_x[0], 0]
        ])
        
        ax.fill(room_outline[:, 0], room_outline[:, 1], 
                color='lightblue', alpha=0.3, edgecolor='blue', linewidth=2)
        ax.plot(room_outline[:, 0], room_outline[:, 1], 'b-', linewidth=2)
    
    # Draw floor line
    ax.plot([0, 5], [0, 0], 'brown', linewidth=3, label='Floor')
    
    # Draw ceiling line
    ax.plot([0, 5], [2.5, 2.5], 'gray', linewidth=3, label='Ceiling')
    
    # Draw window (on front wall)
    window_junctions = junctions[8:12]
    if len(window_junctions) > 0:
        window_x = window_junctions[:, 0]
        window_z = window_junctions[:, 2]
        x_min, x_max = window_x.min(), window_x.max()
        z_min, z_max = window_z.min(), window_z.max()
        
        window_rect = Rectangle((x_min, z_min), x_max - x_min, z_max - z_min,
                                facecolor='cyan', alpha=0.5, 
                                edgecolor='blue', linewidth=2, label='Window')
        ax.add_patch(window_rect)
    
    # Draw furniture (projected onto front view)
    for i, bbox in enumerate(bboxes):
        centroid = np.array(bbox['centroid'])
        coeffs = np.array(bbox['coeffs'])
        
        # Simple box representation (X and Z)
        x_min = centroid[0] - coeffs[0]
        x_max = centroid[0] + coeffs[0]
        z_min = centroid[2] - coeffs[2]
        z_max = centroid[2] + coeffs[2]
        
        furniture_rect = Rectangle((x_min, z_min), x_max - x_min, z_max - z_min,
                                   facecolor='orange', alpha=0.5,
                                   edgecolor='darkorange', linewidth=2)
        ax.add_patch(furniture_rect)
        
        ax.text(centroid[0], z_max + 0.1, f'Obj{i+1}', 
               ha='center', fontsize=9, weight='bold')
    
    # Formatting
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.2, 3.0)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (meters) - Width', fontsize=12)
    ax.set_ylabel('Z (meters) - Height', fontsize=12)
    ax.set_title('FRONT VIEW (Looking at South Wall)\n5m wide × 2.5m high', 
                fontsize=14, weight='bold')
    ax.legend(loc='upper right')
    
    # Save
    plt.tight_layout()
    output_path = 'dummy_dataset/scene_00000/front_view.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✅ Saved: {output_path}")
    plt.close()


# ===========================================================================
# SIDE VIEW (Looking at East Wall - along X-axis)
# ===========================================================================

def generate_side_view():
    """Generate side view (Y-Z plane, looking along X-axis)"""
    print("\n📐 Generating SIDE VIEW (East Wall)...")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Project junctions onto Y-Z plane
    side_junctions = junctions[:, [1, 2]]  # Y and Z coordinates
    
    # Get floor and ceiling edges
    floor_y = side_junctions[side_junctions[:, 1] < 0.1, 0]
    ceiling_y = side_junctions[side_junctions[:, 1] > 2.0, 0]
    
    if len(floor_y) > 0:
        floor_y = np.sort(floor_y)
        ceiling_y = np.sort(ceiling_y)
        
        # Draw room outline
        room_outline = np.array([
            [floor_y[0], 0],
            [floor_y[-1], 0],
            [ceiling_y[-1], 2.5],
            [ceiling_y[0], 2.5],
            [floor_y[0], 0]
        ])
        
        ax.fill(room_outline[:, 0], room_outline[:, 1], 
                color='lightblue', alpha=0.3, edgecolor='blue', linewidth=2)
        ax.plot(room_outline[:, 0], room_outline[:, 1], 'b-', linewidth=2)
    
    # Draw floor line
    ax.plot([0, 4], [0, 0], 'brown', linewidth=3, label='Floor')
    
    # Draw ceiling line
    ax.plot([0, 4], [2.5, 2.5], 'gray', linewidth=3, label='Ceiling')
    
    # Draw furniture (projected onto side view)
    for i, bbox in enumerate(bboxes):
        centroid = np.array(bbox['centroid'])
        coeffs = np.array(bbox['coeffs'])
        
        # Simple box representation (Y and Z)
        y_min = centroid[1] - coeffs[1]
        y_max = centroid[1] + coeffs[1]
        z_min = centroid[2] - coeffs[2]
        z_max = centroid[2] + coeffs[2]
        
        furniture_rect = Rectangle((y_min, z_min), y_max - y_min, z_max - z_min,
                                   facecolor='orange', alpha=0.5,
                                   edgecolor='darkorange', linewidth=2)
        ax.add_patch(furniture_rect)
        
        ax.text(centroid[1], z_max + 0.1, f'Obj{i+1}', 
               ha='center', fontsize=9, weight='bold')
    
    # Formatting
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.2, 3.0)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Y (meters) - Depth', fontsize=12)
    ax.set_ylabel('Z (meters) - Height', fontsize=12)
    ax.set_title('SIDE VIEW (Looking at East Wall)\n4m deep × 2.5m high', 
                fontsize=14, weight='bold')
    ax.legend(loc='upper right')
    
    # Save
    plt.tight_layout()
    output_path = 'dummy_dataset/scene_00000/side_view.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✅ Saved: {output_path}")
    plt.close()


# ===========================================================================
# COMBINED VIEW (All three views in one image)
# ===========================================================================

def generate_combined_view():
    """Generate a combined image with all three orthographic views"""
    print("\n📐 Generating COMBINED VIEW (All three projections)...")
    
    fig = plt.figure(figsize=(16, 10))
    
    # Top View (Top)
    ax1 = plt.subplot(2, 2, 1)
    ax1.set_title('TOP VIEW (Bird\'s Eye)', fontsize=12, weight='bold')
    
    floor_junctions = junctions[junctions[:, 2] < 0.1]
    if len(floor_junctions) > 0:
        center = floor_junctions.mean(axis=0)
        angles = np.arctan2(floor_junctions[:, 1] - center[1], 
                           floor_junctions[:, 0] - center[0])
        sorted_idx = np.argsort(angles)
        floor_sorted = floor_junctions[sorted_idx]
        floor_closed = np.vstack([floor_sorted, floor_sorted[0]])
        
        ax1.fill(floor_closed[:, 0], floor_closed[:, 1], 
                color='lightblue', alpha=0.3, edgecolor='blue', linewidth=2)
        ax1.scatter(floor_junctions[:, 0], floor_junctions[:, 1], 
                   c='red', s=80, marker='o', zorder=5)
    
    for i, bbox in enumerate(bboxes):
        centroid = np.array(bbox['centroid'])
        coeffs = np.array(bbox['coeffs'])
        basis = np.array(bbox['basis'])
        
        corners_2d = []
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                offset = dx * coeffs[0] * basis[0][:2] + dy * coeffs[1] * basis[1][:2]
                corners_2d.append(centroid[:2] + offset)
        corners_2d = np.array(corners_2d)
        
        from matplotlib.patches import Polygon
        poly = Polygon(corners_2d[[0, 1, 3, 2]], 
                      facecolor='orange', alpha=0.5, edgecolor='darkorange', linewidth=1.5)
        ax1.add_patch(poly)
    
    ax1.set_xlim(-0.5, 5.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    
    # Front View (Bottom Left)
    ax2 = plt.subplot(2, 2, 3)
    ax2.set_title('FRONT VIEW (South Wall)', fontsize=12, weight='bold')
    
    ax2.plot([0, 5], [0, 0], 'brown', linewidth=2)
    ax2.plot([0, 5], [2.5, 2.5], 'gray', linewidth=2)
    ax2.plot([0, 0], [0, 2.5], 'blue', linewidth=2)
    ax2.plot([5, 5], [0, 2.5], 'blue', linewidth=2)
    
    for i, bbox in enumerate(bboxes):
        centroid = np.array(bbox['centroid'])
        coeffs = np.array(bbox['coeffs'])
        x_min = centroid[0] - coeffs[0]
        x_max = centroid[0] + coeffs[0]
        z_min = centroid[2] - coeffs[2]
        z_max = centroid[2] + coeffs[2]
        
        furniture_rect = Rectangle((x_min, z_min), x_max - x_min, z_max - z_min,
                                   facecolor='orange', alpha=0.5,
                                   edgecolor='darkorange', linewidth=1.5)
        ax2.add_patch(furniture_rect)
    
    ax2.set_xlim(-0.5, 5.5)
    ax2.set_ylim(-0.2, 3.0)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('X (m) - Width')
    ax2.set_ylabel('Z (m) - Height')
    
    # Side View (Bottom Right)
    ax3 = plt.subplot(2, 2, 4)
    ax3.set_title('SIDE VIEW (East Wall)', fontsize=12, weight='bold')
    
    ax3.plot([0, 4], [0, 0], 'brown', linewidth=2)
    ax3.plot([0, 4], [2.5, 2.5], 'gray', linewidth=2)
    ax3.plot([0, 0], [0, 2.5], 'blue', linewidth=2)
    ax3.plot([4, 4], [0, 2.5], 'blue', linewidth=2)
    
    for i, bbox in enumerate(bboxes):
        centroid = np.array(bbox['centroid'])
        coeffs = np.array(bbox['coeffs'])
        y_min = centroid[1] - coeffs[1]
        y_max = centroid[1] + coeffs[1]
        z_min = centroid[2] - coeffs[2]
        z_max = centroid[2] + coeffs[2]
        
        furniture_rect = Rectangle((y_min, z_min), y_max - y_min, z_max - z_min,
                                   facecolor='orange', alpha=0.5,
                                   edgecolor='darkorange', linewidth=1.5)
        ax3.add_patch(furniture_rect)
    
    ax3.set_xlim(-0.5, 4.5)
    ax3.set_ylim(-0.2, 3.0)
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlabel('Y (m) - Depth')
    ax3.set_ylabel('Z (m) - Height')
    
    # 3D Isometric View (Top Right) - simplified
    ax4 = plt.subplot(2, 2, 2, projection='3d')
    ax4.set_title('3D ISOMETRIC VIEW', fontsize=12, weight='bold')
    
    # Draw room edges
    floor = junctions[junctions[:, 2] < 0.1]
    ceiling = junctions[junctions[:, 2] > 2.0]
    
    if len(floor) > 0:
        center = floor.mean(axis=0)
        angles = np.arctan2(floor[:, 1] - center[1], floor[:, 0] - center[0])
        sorted_idx = np.argsort(angles)
        floor_sorted = floor[sorted_idx]
        ceiling_sorted = ceiling[sorted_idx]
        
        # Draw floor and ceiling
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        floor_poly = [[floor_sorted[i] for i in range(len(floor_sorted))]]
        ceiling_poly = [[ceiling_sorted[i] for i in range(len(ceiling_sorted))]]
        
        ax4.add_collection3d(Poly3DCollection(floor_poly, alpha=0.2, 
                                             facecolor='brown', edgecolor='black'))
        ax4.add_collection3d(Poly3DCollection(ceiling_poly, alpha=0.2, 
                                             facecolor='gray', edgecolor='black'))
        
        # Draw vertical edges
        for i in range(len(floor_sorted)):
            ax4.plot([floor_sorted[i, 0], ceiling_sorted[i, 0]],
                    [floor_sorted[i, 1], ceiling_sorted[i, 1]],
                    [floor_sorted[i, 2], ceiling_sorted[i, 2]], 'b-', linewidth=1)
    
    # Draw furniture as wireframe boxes
    for bbox in bboxes:
        centroid = np.array(bbox['centroid'])
        coeffs = np.array(bbox['coeffs'])
        
        # Simple box
        x = [centroid[0] - coeffs[0], centroid[0] + coeffs[0]]
        y = [centroid[1] - coeffs[1], centroid[1] + coeffs[1]]
        z = [centroid[2] - coeffs[2], centroid[2] + coeffs[2]]
        
        for i in range(2):
            for j in range(2):
                ax4.plot([x[0], x[1]], [y[i], y[i]], [z[j], z[j]], 'orange', linewidth=2)
                ax4.plot([x[i], x[i]], [y[0], y[1]], [z[j], z[j]], 'orange', linewidth=2)
                ax4.plot([x[i], x[i]], [y[j], y[j]], [z[0], z[1]], 'orange', linewidth=2)
    
    ax4.set_xlabel('X (m)')
    ax4.set_ylabel('Y (m)')
    ax4.set_zlabel('Z (m)')
    ax4.set_xlim(0, 5)
    ax4.set_ylim(0, 4)
    ax4.set_zlim(0, 2.5)
    
    # Overall title
    fig.suptitle('ORTHOGRAPHIC PROJECTIONS - 5m × 4m × 2.5m Living Room', 
                fontsize=16, weight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    output_path = 'dummy_dataset/scene_00000/combined_views.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✅ Saved: {output_path}")
    plt.close()


# ===========================================================================
# MAIN EXECUTION
# ===========================================================================

if __name__ == "__main__":
    # Generate all views
    generate_top_view()
    generate_front_view()
    generate_side_view()
    generate_combined_view()
    
    print("\n" + "=" * 70)
    print("✅ ALL ORTHOGRAPHIC VIEWS GENERATED!")
    print("=" * 70)
    print("\nGenerated files:")
    print("   📄 dummy_dataset/scene_00000/top_view.png")
    print("   📄 dummy_dataset/scene_00000/front_view.png")
    print("   📄 dummy_dataset/scene_00000/side_view.png")
    print("   📄 dummy_dataset/scene_00000/combined_views.png (all in one)")
    print("\nYou can view these images with any image viewer!")
    print("=" * 70)
