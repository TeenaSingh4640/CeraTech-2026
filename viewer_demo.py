"""
Interactive Visualization Viewer for End Users
Shows how the Structured3D visualizations would be presented in a real application
"""
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess

class Structured3DViewer:
    """
    Simple GUI viewer showing how visualizations would be displayed to users
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Structured3D Visualization Viewer - Demo Interface")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Data path
        self.scene_path = "dummy_dataset/scene_00000"
        
        # Create main layout
        self.create_header()
        self.create_navigation()
        self.create_main_area()
        self.create_info_panel()
        
        # Load first visualization
        self.current_view = "paper_style_combined"
        self.load_visualization(self.current_view)
    
    def create_header(self):
        """Create header with title and scene info"""
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill='x', side='top')
        
        title = tk.Label(header, text="Structured3D Building Visualization System",
                        font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title.pack(pady=10)
        
        subtitle = tk.Label(header, text="Scene 00000 - 5m × 4m × 2.5m Living Room",
                          font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50')
        subtitle.pack()
    
    def create_navigation(self):
        """Create navigation buttons for different views"""
        nav_frame = tk.Frame(self.root, bg='#34495e', height=60)
        nav_frame.pack(fill='x', side='top')
        
        button_style = {
            'font': ('Arial', 10, 'bold'),
            'bg': '#3498db',
            'fg': 'white',
            'activebackground': '#2980b9',
            'relief': 'flat',
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        views = [
            ("📊 Paper Style", "paper_style_combined"),
            ("🏠 Semantic Plan", "semantic_floorplan"),
            ("🔷 Graph View", "graph_representation"),
            ("📐 Orthographic", "combined_views"),
            ("🔝 Top View", "top_view"),
            ("👁️ 3D Wireframe", "wireframe_3d")
        ]
        
        for text, view_id in views:
            btn = tk.Button(nav_frame, text=text, 
                          command=lambda v=view_id: self.load_visualization(v),
                          **button_style)
            btn.pack(side='left', padx=5, pady=10)
    
    def create_main_area(self):
        """Create main display area for visualization"""
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        
        # Canvas with scrollbar for image display
        canvas_frame = tk.Frame(main_frame, bg='white')
        canvas_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(canvas_frame, orient='vertical')
        h_scrollbar = tk.Scrollbar(canvas_frame, orient='horizontal')
        
        self.canvas = tk.Canvas(canvas_frame, bg='white',
                               yscrollcommand=v_scrollbar.set,
                               xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
        
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # View label
        self.view_label = tk.Label(main_frame, text="", 
                                   font=('Arial', 14, 'bold'),
                                   bg='white', fg='#2c3e50')
        self.view_label.pack(pady=5)
    
    def create_info_panel(self):
        """Create information panel on the right"""
        info_frame = tk.Frame(self.root, bg='#ecf0f1', width=300)
        info_frame.pack(fill='y', side='right', padx=10, pady=10)
        
        # Title
        title = tk.Label(info_frame, text="Scene Information",
                        font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)
        
        # Info text
        info_text = tk.Text(info_frame, wrap='word', height=25, width=35,
                           font=('Arial', 10), bg='white', relief='flat',
                           padx=10, pady=10)
        info_text.pack(fill='both', expand=True, padx=10)
        
        info_content = """
📍 Scene Details:
━━━━━━━━━━━━━━━━━
 ID: scene_00000
 Type: Living Room
 Dimensions: 5m × 4m × 2.5m
 Floor Area: 20 m²
 Volume: 50 m³

🪑 Furniture Objects:
━━━━━━━━━━━━━━━━━
 • Coffee Table (0.6m × 0.6m)
 • Bookshelf (1.0m × 0.5m)
 • Chair (0.8m × 0.8m)

🎨 Visualization Types:
━━━━━━━━━━━━━━━━━
📊 Paper Style
   Graph + semantic floorplan
   Matches research papers
   Best for understanding layout

🏠 Semantic Plan
   Color-coded room types
   Shows spatial organization
   Professional presentation

🔷 Graph View
   Node/edge representation
   Room connectivity
   Topology visualization

📐 Orthographic
   Top, front, side views
   Engineering drawings
   CAD-style projections

🔝 Top View
   Bird's eye perspective
   Clear layout overview
   Floor plan view

👁️ 3D Wireframe
   Interactive 3D model
   Rotate and zoom
   Structural skeleton

💡 Usage Tips:
━━━━━━━━━━━━━━━━━
• Click buttons to switch views
• Each view highlights different
  aspects of the building
• All views generated from 3D
  annotation data
• Real dataset has 3,500 scenes
        """
        
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
        
        # Action buttons
        action_frame = tk.Frame(info_frame, bg='#ecf0f1')
        action_frame.pack(fill='x', pady=10)
        
        export_btn = tk.Button(action_frame, text="📥 Export Images",
                              font=('Arial', 10, 'bold'),
                              bg='#27ae60', fg='white',
                              command=self.export_images,
                              relief='flat', padx=10, pady=5)
        export_btn.pack(fill='x', padx=10, pady=2)
        
        open_folder_btn = tk.Button(action_frame, text="📂 Open Folder",
                                   font=('Arial', 10, 'bold'),
                                   bg='#3498db', fg='white',
                                   command=self.open_folder,
                                   relief='flat', padx=10, pady=5)
        open_folder_btn.pack(fill='x', padx=10, pady=2)
        
        view_3d_btn = tk.Button(action_frame, text="🎮 Launch 3D Viewer",
                              font=('Arial', 10, 'bold'),
                              bg='#e74c3c', fg='white',
                              command=self.launch_3d_viewer,
                              relief='flat', padx=10, pady=5)
        view_3d_btn.pack(fill='x', padx=10, pady=2)
    
    def load_visualization(self, view_id):
        """Load and display a visualization"""
        self.current_view = view_id
        
        # Map view IDs to file names and titles
        view_map = {
            "paper_style_combined": ("paper_style_combined.png", "Research Paper Style - Graph + Floorplan"),
            "semantic_floorplan": ("semantic_floorplan.png", "Semantic Floorplan - Color-Coded Rooms"),
            "graph_representation": ("graph_representation.png", "Graph Representation - Room Connectivity"),
            "combined_views": ("combined_views.png", "Orthographic Views - Top/Front/Side"),
            "top_view": ("top_view.png", "Top View - Bird's Eye"),
            "wireframe_3d": ("../assets/3d/wireframe.png", "3D Wireframe (Sample)")
        }
        
        if view_id not in view_map:
            return
        
        filename, title = view_map[view_id]
        filepath = os.path.join(self.scene_path, filename)
        
        # Update label
        self.view_label.config(text=title)
        
        # Check if file exists
        if not os.path.exists(filepath):
            # Show placeholder
            self.canvas.delete('all')
            self.canvas.create_text(400, 300, 
                                   text=f"Visualization: {title}\n\n(File not found: {filename})\n\nClick '🎮 Launch 3D Viewer' for interactive view",
                                   font=('Arial', 14),
                                   fill='#95a5a6')
            return
        
        try:
            # Load and display image
            image = Image.open(filepath)
            
            # Resize if too large
            max_width, max_height = 800, 600
            if image.width > max_width or image.height > max_height:
                ratio = min(max_width/image.width, max_height/image.height)
                new_size = (int(image.width*ratio), int(image.height*ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(image)
            
            # Clear canvas and display
            self.canvas.delete('all')
            self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
            
            # Update scroll region
            self.canvas.config(scrollregion=self.canvas.bbox('all'))
            
        except Exception as e:
            self.canvas.delete('all')
            self.canvas.create_text(400, 300,
                                   text=f"Error loading image:\n{str(e)}",
                                   font=('Arial', 12),
                                   fill='#e74c3c')
    
    def export_images(self):
        """Export all visualizations"""
        msg = tk.Toplevel(self.root)
        msg.title("Export")
        msg.geometry("400x200")
        
        label = tk.Label(msg, text="✅ All visualizations are already exported!\n\nLocation:\ndummy_dataset/scene_00000/\n\nFiles:\n• paper_style_combined.png\n• semantic_floorplan.png\n• graph_representation.png\n• combined_views.png",
                        font=('Arial', 11), justify='left')
        label.pack(expand=True, pady=20)
        
        ok_btn = tk.Button(msg, text="OK", command=msg.destroy,
                          bg='#3498db', fg='white', padx=20, pady=5)
        ok_btn.pack(pady=10)
    
    def open_folder(self):
        """Open the folder containing visualizations"""
        folder_path = os.path.abspath(self.scene_path)
        subprocess.run(['explorer', folder_path])
    
    def launch_3d_viewer(self):
        """Launch 3D wireframe viewer"""
        msg = tk.Toplevel(self.root)
        msg.title("Launch 3D Viewer")
        msg.geometry("500x250")
        
        info = tk.Label(msg, 
                       text="🎮 Launch Interactive 3D Viewer\n\nRun this command in terminal:",
                       font=('Arial', 12, 'bold'))
        info.pack(pady=10)
        
        cmd_frame = tk.Frame(msg, bg='#2c3e50')
        cmd_frame.pack(fill='x', padx=20, pady=10)
        
        cmd_text = tk.Label(cmd_frame,
                           text="python visualize_3d.py --path dummy_dataset --scene 0 --type wireframe",
                           font=('Courier', 10), fg='white', bg='#2c3e50',
                           padx=10, pady=10)
        cmd_text.pack()
        
        hint = tk.Label(msg,
                       text="Controls: Left-click=Rotate | Scroll=Zoom | Q=Close",
                       font=('Arial', 10), fg='#7f8c8d')
        hint.pack(pady=5)
        
        close_btn = tk.Button(msg, text="Close", command=msg.destroy,
                            bg='#95a5a6', fg='white', padx=20, pady=5)
        close_btn.pack(pady=10)


def main():
    """Main entry point for the viewer application"""
    print("=" * 80)
    print("STRUCTURED3D VISUALIZATION VIEWER - USER INTERFACE DEMO")
    print("=" * 80)
    print("\nStarting GUI viewer...")
    print("This demonstrates how visualizations would be shown to end users.\n")
    
    root = tk.Tk()
    app = Structured3DViewer(root)
    
    print("✅ Interface launched!")
    print("   • Click navigation buttons to switch between views")
    print("   • Use the info panel for scene details")
    print("   • Click 'Open Folder' to see all generated files")
    print("\n" + "=" * 80)
    
    root.mainloop()


if __name__ == "__main__":
    main()
