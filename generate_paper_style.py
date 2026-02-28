"""
Generate paper-style visualizations with graph representation and semantic color-coded floorplans
Similar to LIFULL HOME's database / research paper format
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import networkx as nx

# Load data
with open('dummy_dataset/scene_00000/annotation_3d.json', 'r') as f:
    annos = json.load(f)

with open('dummy_dataset/scene_00000/bbox_3d.json', 'r') as f:
    bboxes = json.load(f)

# Extract junctions
junctions = np.array([j['coordinate'] for j in annos['junctions']])

# Room type colors (matching research paper style)
ROOM_COLORS = {
    'living room': '#8B4513',    # Brown
    'dining room': '#D2691E',    # Light brown
    'kitchen': '#FF00FF',        # Magenta
    'bedroom': '#FFA500',        # Orange
    'bathroom': '#808080',       # Gray
    'laundry room': '#FFFF00',   # Yellow
    'corridor': '#2E8B57',       # Dark green
    'closet': '#0000FF',         # Blue
    'balcony': '#00FFFF',        # Cyan
    'unknown': '#FF0000'         # Red
}

# Furniture type colors
FURNITURE_COLORS = {
    'table': '#8B4513',
    'chair': '#D2691E', 
    'sofa': '#CD853F',
    'bed': '#DEB887',
    'cabinet': '#F4A460'
}

print("=" * 80)
print("GENERATING RESEARCH PAPER STYLE VISUALIZATIONS")
print("=" * 80)

# ============================================================================
# STYLE 1: Graph Representation with Colored Nodes
# ============================================================================

def generate_graph_representation():
    """Generate graph with colored nodes representing room types"""
    print("\n📊 Generating GRAPH REPRESENTATION...")
    
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
    
    # Create graph
    G = nx.Graph()
    
    # Get floor junctions for layout
    floor_junctions = junctions[junctions[:, 2] < 0.1][:4]
    
    # Add nodes for each room corner
    node_positions = {}
    node_colors = []
    node_types = []
    
    for i, junction in enumerate(floor_junctions):
        node_id = f"j{i}"
        G.add_node(node_id)
        node_positions[node_id] = (junction[0], junction[1])
        
        # Assign room type based on position
        if i == 0:
            node_types.append('living room')
            node_colors.append(ROOM_COLORS['living room'])
        elif i == 1:
            node_types.append('bedroom')
            node_colors.append(ROOM_COLORS['bedroom'])
        elif i == 2:
            node_types.append('kitchen')
            node_colors.append(ROOM_COLORS['kitchen'])
        else:
            node_types.append('bathroom')
            node_colors.append(ROOM_COLORS['bathroom'])
    
    # Add center node for living room
    center = floor_junctions.mean(axis=0)
    G.add_node("center")
    node_positions["center"] = (center[0], center[1])
    node_colors.append(ROOM_COLORS['living room'])
    node_types.append('living room')
    
    # Add edges (connections between rooms)
    edges = [
        ("j0", "j1"), ("j1", "j2"), ("j2", "j3"), ("j3", "j0"),
        ("center", "j0"), ("center", "j1"), ("center", "j2"), ("center", "j3")
    ]
    G.add_edges_from(edges)
    
    # Draw graph
    nx.draw_networkx_edges(G, node_positions, width=2, alpha=0.6, edge_color='black', ax=ax)
    
    # Draw nodes with colors
    nx.draw_networkx_nodes(G, node_positions, node_color=node_colors, 
                          node_size=1000, alpha=0.9, ax=ax)
    
    # Add labels
    labels = {node: node_types[i].split()[0].capitalize() 
             for i, node in enumerate(G.nodes())}
    nx.draw_networkx_labels(G, node_positions, labels, font_size=8, 
                           font_weight='bold', font_color='white', ax=ax)
    
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Graph Representation\n(Room Connectivity)', fontsize=12, weight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('dummy_dataset/scene_00000/graph_representation.png', dpi=150, bbox_inches='tight', facecolor='white')
    print(f"   ✅ Saved: graph_representation.png")
    plt.close()


# ============================================================================
# STYLE 2: Semantic Floorplan with Color-Coded Rooms
# ============================================================================

def generate_semantic_floorplan():
    """Generate colored floorplan like research papers"""
    print("\n🏠 Generating SEMANTIC FLOORPLAN...")
    
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
    
    # Get floor boundary
    floor_junctions = junctions[junctions[:, 2] < 0.1]
    center = floor_junctions.mean(axis=0)
    angles = np.arctan2(floor_junctions[:, 1] - center[1], 
                       floor_junctions[:, 0] - center[0])
    sorted_idx = np.argsort(angles)
    floor_sorted = floor_junctions[sorted_idx]
    
    # Draw main room (living room) - fill entire floor
    floor_closed = np.vstack([floor_sorted, floor_sorted[0]])
    ax.fill(floor_closed[:, 0], floor_closed[:, 1], 
           color=ROOM_COLORS['living room'], alpha=0.8, edgecolor='black', linewidth=2)
    
    # Add room label
    ax.text(2.5, 2.0, 'Living room', ha='center', va='center', 
           fontsize=14, weight='bold', color='white')
    
    # Draw furniture as colored rectangles
    furniture_labels = ['Table', 'Shelf', 'Chair']
    furniture_colors_list = ['#8B4513', '#D2691E', '#CD853F']
    
    for i, bbox in enumerate(bboxes):
        centroid = np.array(bbox['centroid'])
        coeffs = np.array(bbox['coeffs'])
        basis = np.array(bbox['basis'])
        
        # Get corners
        corners_2d = []
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                offset = dx * coeffs[0] * basis[0][:2] + dy * coeffs[1] * basis[1][:2]
                corners_2d.append(centroid[:2] + offset)
        corners_2d = np.array(corners_2d)
        
        # Draw furniture with specific color
        from matplotlib.patches import Polygon
        poly = Polygon(corners_2d[[0, 1, 3, 2]], 
                      facecolor=furniture_colors_list[i], alpha=0.9, 
                      edgecolor='black', linewidth=1.5)
        ax.add_patch(poly)
        
        # Add label
        if i < len(furniture_labels):
            ax.text(centroid[0], centroid[1], furniture_labels[i], 
                   ha='center', va='center', fontsize=8, weight='bold', color='white')
    
    # Draw window if present
    if len(junctions) > 8:
        window_center = junctions[8:12].mean(axis=0)
        window_rect = Rectangle((window_center[0]-0.5, window_center[1]-0.1), 
                                1.0, 0.2, facecolor=ROOM_COLORS['balcony'], 
                                alpha=0.8, edgecolor='black', linewidth=2)
        ax.add_patch(window_rect)
        ax.text(window_center[0], window_center[1], 'Window', 
               ha='center', va='center', fontsize=7, weight='bold')
    
    # Draw outer boundary
    ax.plot(floor_closed[:, 0], floor_closed[:, 1], 'k-', linewidth=3)
    
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Semantic Floorplan\n(Color-coded by Room Type)', 
                fontsize=12, weight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('dummy_dataset/scene_00000/semantic_floorplan.png', dpi=150, 
               bbox_inches='tight', facecolor='white')
    print(f"   ✅ Saved: semantic_floorplan.png")
    plt.close()


# ============================================================================
# STYLE 3: Combined Paper-Style Layout (Graph + Floorplan Side-by-Side)
# ============================================================================

def generate_paper_style_combined():
    """Generate combined visualization like in research papers"""
    print("\n📄 Generating PAPER-STYLE COMBINED VIEW...")
    
    fig = plt.figure(figsize=(16, 7), facecolor='white')
    
    # LEFT: Graph representation
    ax1 = plt.subplot(1, 2, 1)
    
    # Create graph
    G = nx.Graph()
    floor_junctions = junctions[junctions[:, 2] < 0.1][:4]
    
    node_positions = {}
    node_colors = []
    node_labels_dict = {}
    
    # Add room nodes
    room_types = ['Living\nroom', 'Bedroom', 'Kitchen', 'Bath']
    room_color_keys = ['living room', 'bedroom', 'kitchen', 'bathroom']
    
    for i, junction in enumerate(floor_junctions):
        node_id = f"r{i}"
        G.add_node(node_id)
        node_positions[node_id] = (junction[0], junction[1])
        node_colors.append(ROOM_COLORS[room_color_keys[i]])
        node_labels_dict[node_id] = room_types[i]
    
    # Add center node
    center = floor_junctions.mean(axis=0)
    G.add_node("c")
    node_positions["c"] = (center[0], center[1])
    node_colors.append(ROOM_COLORS['living room'])
    node_labels_dict["c"] = "Main"
    
    # Add furniture nodes
    for i, bbox in enumerate(bboxes):
        node_id = f"f{i}"
        centroid = bbox['centroid']
        G.add_node(node_id)
        node_positions[node_id] = (centroid[0], centroid[1])
        node_colors.append('#CD853F')
        node_labels_dict[node_id] = f"Obj{i+1}"
    
    # Add edges
    edges = [
        ("r0", "r1"), ("r1", "r2"), ("r2", "r3"), ("r3", "r0"),
        ("c", "r0"), ("c", "r1"), ("c", "r2"), ("c", "r3"),
        ("c", "f0"), ("c", "f1"), ("c", "f2")
    ]
    G.add_edges_from(edges)
    
    # Draw
    nx.draw_networkx_edges(G, node_positions, width=2, alpha=0.5, edge_color='black', ax=ax1)
    nx.draw_networkx_nodes(G, node_positions, node_color=node_colors, 
                          node_size=800, alpha=0.9, ax=ax1)
    nx.draw_networkx_labels(G, node_positions, node_labels_dict, font_size=7, 
                           font_weight='bold', font_color='white', ax=ax1)
    
    ax1.set_xlim(-0.5, 5.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Graph Representation', fontsize=14, weight='bold', pad=15)
    
    # RIGHT: Semantic floorplan
    ax2 = plt.subplot(1, 2, 2)
    
    # Get floor boundary
    floor_junctions = junctions[junctions[:, 2] < 0.1]
    center = floor_junctions.mean(axis=0)
    angles = np.arctan2(floor_junctions[:, 1] - center[1], 
                       floor_junctions[:, 0] - center[0])
    sorted_idx = np.argsort(angles)
    floor_sorted = floor_junctions[sorted_idx]
    floor_closed = np.vstack([floor_sorted, floor_sorted[0]])
    
    # Draw room
    ax2.fill(floor_closed[:, 0], floor_closed[:, 1], 
            color=ROOM_COLORS['living room'], alpha=0.85, edgecolor='black', linewidth=3)
    
    # Draw furniture
    furniture_colors_list = ['#8B4513', '#D2691E', '#CD853F']
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
                      facecolor=furniture_colors_list[i], alpha=0.9, 
                      edgecolor='black', linewidth=2)
        ax2.add_patch(poly)
    
    # Window
    if len(junctions) > 8:
        window_center = junctions[8:12].mean(axis=0)
        window_rect = Rectangle((window_center[0]-0.5, -0.05), 
                                1.0, 0.1, facecolor=ROOM_COLORS['balcony'], 
                                alpha=0.9, edgecolor='black', linewidth=2)
        ax2.add_patch(window_rect)
    
    ax2.plot(floor_closed[:, 0], floor_closed[:, 1], 'k-', linewidth=3)
    
    ax2.set_xlim(-0.5, 5.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('Semantic Floorplan', fontsize=14, weight='bold', pad=15)
    
    # Add legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, fc=ROOM_COLORS['living room'], ec='black', label='Living room'),
        plt.Rectangle((0, 0), 1, 1, fc=ROOM_COLORS['bedroom'], ec='black', label='Bedroom'),
        plt.Rectangle((0, 0), 1, 1, fc=ROOM_COLORS['kitchen'], ec='black', label='Kitchen'),
        plt.Rectangle((0, 0), 1, 1, fc=ROOM_COLORS['bathroom'], ec='black', label='Bathroom'),
        plt.Rectangle((0, 0), 1, 1, fc=ROOM_COLORS['balcony'], ec='black', label='Balcony/Window'),
        plt.Rectangle((0, 0), 1, 1, fc='#8B4513', ec='black', label='Furniture')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=6, 
              fontsize=10, frameon=True, fancybox=True)
    
    # Overall title
    fig.suptitle('5m × 4m × 2.5m Living Room - Research Paper Style Visualization', 
                fontsize=16, weight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0.06, 1, 0.96])
    plt.savefig('dummy_dataset/scene_00000/paper_style_combined.png', dpi=200, 
               bbox_inches='tight', facecolor='white')
    print(f"   ✅ Saved: paper_style_combined.png")
    plt.close()


# ============================================================================
# STYLE 4: Multi-Scene Layout (Like the Research Paper Grid)
# ============================================================================

def generate_research_grid_layout():
    """Generate grid layout showing multiple variations like in research papers"""
    print("\n📊 Generating RESEARCH GRID LAYOUT...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 14), facecolor='white')
    fig.suptitle('Structured3D - Room Variations\n(Research Paper Style)', 
                fontsize=16, weight='bold', y=0.98)
    
    # Get base floor plan
    floor_junctions = junctions[junctions[:, 2] < 0.1]
    center = floor_junctions.mean(axis=0)
    angles = np.arctan2(floor_junctions[:, 1] - center[1], 
                       floor_junctions[:, 0] - center[0])
    sorted_idx = np.argsort(angles)
    floor_sorted = floor_junctions[sorted_idx]
    floor_closed = np.vstack([floor_sorted, floor_sorted[0]])
    
    # Variation 1: Graph with many connections
    ax = axes[0, 0]
    G1 = nx.Graph()
    pos1 = {}
    colors1 = []
    for i in range(8):
        G1.add_node(i)
        angle = 2 * np.pi * i / 8
        pos1[i] = (2.5 + 1.5*np.cos(angle), 2.0 + 1.5*np.sin(angle))
        colors1.append(list(ROOM_COLORS.values())[i % len(ROOM_COLORS)])
    
    for i in range(8):
        for j in range(i+1, min(i+3, 8)):
            G1.add_edge(i, j)
    
    nx.draw_networkx_edges(G1, pos1, width=2, alpha=0.5, ax=ax)
    nx.draw_networkx_nodes(G1, pos1, node_color=colors1, node_size=600, alpha=0.9, ax=ax)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Variation 1: Multi-Room Graph', fontsize=12, weight='bold')
    
    # Variation 2: Semantic floorplan - main room
    ax = axes[0, 1]
    ax.fill(floor_closed[:, 0], floor_closed[:, 1], 
           color=ROOM_COLORS['living room'], alpha=0.85, edgecolor='black', linewidth=3)
    for i, bbox in enumerate(bboxes):
        centroid = np.array(bbox['centroid'])
        rect = Rectangle((centroid[0]-0.3, centroid[1]-0.3), 0.6, 0.6,
                        facecolor='#8B4513', edgecolor='black', linewidth=2)
        ax.add_patch(rect)
    ax.plot(floor_closed[:, 0], floor_closed[:, 1], 'k-', linewidth=3)
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Variation 2: Living Room + Furniture', fontsize=12, weight='bold')
    
    # Variation 3: Graph with fewer connections
    ax = axes[1, 0]
    G3 = nx.Graph()
    pos3 = {}
    colors3 = []
    room_positions = [(1, 1), (4, 1), (4, 3), (1, 3), (2.5, 2)]
    room_colors_keys = ['bedroom', 'kitchen', 'bathroom', 'closet', 'living room']
    
    for i, (x, y) in enumerate(room_positions):
        G3.add_node(i)
        pos3[i] = (x, y)
        colors3.append(ROOM_COLORS[room_colors_keys[i]])
    
    G3.add_edges_from([(0,1), (1,2), (2,3), (3,0), (4,0), (4,1), (4,2), (4,3)])
    
    nx.draw_networkx_edges(G3, pos3, width=2, alpha=0.5, ax=ax)
    nx.draw_networkx_nodes(G3, pos3, node_color=colors3, node_size=800, alpha=0.9, ax=ax)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Variation 3: Multi-Room Layout', fontsize=12, weight='bold')
    
    # Variation 4: Multi-room semantic floorplan
    ax = axes[1, 1]
    # Divide room into sections
    sections = [
        ([0, 2.5], [0, 2], ROOM_COLORS['bedroom']),
        ([2.5, 5], [0, 2], ROOM_COLORS['kitchen']),
        ([0, 2.5], [2, 4], ROOM_COLORS['bathroom']),
        ([2.5, 5], [2, 4], ROOM_COLORS['living room'])
    ]
    
    for (x_range, y_range, color) in sections:
        rect = Rectangle((x_range[0], y_range[0]), 
                        x_range[1]-x_range[0], y_range[1]-y_range[0],
                        facecolor=color, alpha=0.85, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
    
    ax.plot(floor_closed[:, 0], floor_closed[:, 1], 'k-', linewidth=3)
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Variation 4: Four-Room Apartment', fontsize=12, weight='bold')
    
    # Add legend
    legend_elements = [
        plt.Rectangle((0,0), 1, 1, fc=ROOM_COLORS['living room'], ec='black', label='Living room'),
        plt.Rectangle((0,0), 1, 1, fc=ROOM_COLORS['bedroom'], ec='black', label='Bedroom'),
        plt.Rectangle((0,0), 1, 1, fc=ROOM_COLORS['kitchen'], ec='black', label='Kitchen'),
        plt.Rectangle((0,0), 1, 1, fc=ROOM_COLORS['bathroom'], ec='black', label='Bathroom'),
        plt.Rectangle((0,0), 1, 1, fc=ROOM_COLORS['closet'], ec='black', label='Closet'),
        plt.Rectangle((0,0), 1, 1, fc=ROOM_COLORS['corridor'], ec='black', label='Corridor')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=6, 
              fontsize=11, frameon=True, fancybox=True)
    
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig('dummy_dataset/scene_00000/research_grid_layout.png', dpi=200, 
               bbox_inches='tight', facecolor='white')
    print(f"   ✅ Saved: research_grid_layout.png")
    plt.close()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    generate_graph_representation()
    generate_semantic_floorplan()
    generate_paper_style_combined()
    generate_research_grid_layout()
    
    print("\n" + "=" * 80)
    print("✅ ALL RESEARCH PAPER STYLE VISUALIZATIONS GENERATED!")
    print("=" * 80)
    print("\nGenerated files:")
    print("   📄 graph_representation.png      - Node/edge graph showing connectivity")
    print("   📄 semantic_floorplan.png         - Color-coded room layout")
    print("   📄 paper_style_combined.png       - Graph + Floorplan side-by-side")
    print("   📄 research_grid_layout.png       - Multi-scene grid (like research papers)")
    print("\n" + "=" * 80)
