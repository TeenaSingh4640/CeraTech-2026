# 🏗️ CeraTech Design Suite v2.0

**Professional Structural Design & Analysis Tool with AI Assistant**

A comprehensive web-based structural engineering platform that provides automated design calculations, 3D visualization, cost estimation, and architectural rendering capabilities for building projects.

---

## 🌟 Features

### 🎯 Core Features
- **Intelligent Design Calculator**: Automated structural design based on plot dimensions, FAR, and building parameters
- **Real-time Cost Estimation**: Instant calculation of concrete, steel, and total project costs
- **3D Visualization**: Interactive 3D building models and architectural views
- **AI Design Assistant**: Guided workflow with intelligent recommendations
- **Professional Dashboard**: Modern, responsive UI designed for engineering professionals

### 📊 Analysis Capabilities
- **Structural Analysis**: Complete structural system design and load calculations
- **Quantity Estimation**: Detailed material quantity takeoffs
- **Cost Breakdown**: Comprehensive cost analysis with material-wise breakdowns
- **Multiple Building Types**: Support for residential, commercial, and industrial projects
- **Soil Analysis**: Design optimization based on soil conditions

### 📐 Visualization Tools
- **6 Architectural Views**: Site Plan, Floor Plan, Elevation, Isometric, Structural Grid, Perspective
- **3D Model Export**: Export models in standard formats
- **Orthographic Projections**: Professional architectural drawings
- **Measurement Overlays**: Dimension annotations on drawings

### 📄 Export Options
- **JSON Export**: Complete design data in JSON format
- **PDF Reports**: Professional design reports (coming soon)
- **3D Models**: Export to CAD-compatible formats
- **Rendering Prompts**: AI-ready architectural visualization prompts


## 📁 Project Structure

```
Structured3D/
├── 🌐 Web Interface
│   ├── FINAL_WORKING.html           # Main application (Production)
│   ├── design_interface_v2.html     # Alternative interface
│   └── enhanced_viewer.html         # 3D model viewer
│
├── 🐍 Python Scripts
│   ├── structural_design_engine.py       # Core structural calculations
│   ├── structural_quantity_estimation.py # Material quantity estimation
│   ├── generate_architectural_images.py  # Image generation
│   ├── visualize_3d.py                   # 3D visualization
│   ├── export_3d_models.py               # 3D model export
│   ├── run_complete_structural_analysis.py # Full analysis pipeline
│   └── generate_rendering_prompts.py     # AI rendering prompts
│
├── 📊 Data & Exports
│   ├── complete_structural_analysis_*.json  # Analysis reports
│   ├── quantity_cost_estimation_*.json      # Cost estimates
│   ├── rendering_prompts_*.txt              # AI prompts
│   └── exports/                             # Generated models
│
├── 📚 Documentation
│   ├── README.md                         # This file
│   ├── HOW_TO_USE.md                     # Detailed user guide
│   ├── HOW_IT_WORKS.md                   # Technical documentation
│   ├── QUICKSTART.md                     # Quick reference
│   ├── STRUCTURAL_QUICK_REFERENCE.md     # Structural design guide
│   └── DESIGN_ENGINE_README.md           # Engine documentation
│
├── 🎨 Assets
│   ├── assets/3d/           # 3D models
│   ├── assets/bbox/         # Bounding box data
│   ├── assets/mesh/         # Mesh files
│   └── dummy_dataset/       # Sample data
│
└── 🔧 Utilities
    └── misc/                # Helper functions and utilities
```

---

## 🛠️ Technologies Used

### Frontend
- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with gradients, animations, responsive design
- **Vanilla JavaScript**: No framework dependencies, pure JS
- **Canvas API**: 2D drawing for architectural views
- **Font Awesome 6.4.0**: Professional iconography
- **Google Fonts (Inter)**: Clean, modern typography

### Backend & Processing
- **Python 3.x**: Core computational engine
- **NumPy**: Numerical computations
- **JSON**: Data exchange format
- **HTTP Server**: Built-in Python server for local development

### Design Principles
- **Responsive Design**: Mobile-first approach
- **Clean UI/UX**: Intuitive navigation and workflow
- **Professional Aesthetics**: Designed for engineering professionals
- **Performance Optimized**: Fast calculations and smooth animations

---

## 📊 Key Calculations

The design engine performs:

### Structural Calculations
- **Plot Area** = Length × Width
- **Built Area** = Plot Area × FAR
- **Concrete Volume** = (Built Area × 0.175 × 1.35) × 1.05 m³
- **Steel Weight** = (Built Area × 0.175 × 1.35) × 0.015 × 7850 kg

### Cost Estimation
- **Concrete Cost** = Volume × $175/m³
- **Steel Cost** = Weight × $1.35/kg
- **Total Cost** = Concrete Cost + Steel Cost

*Note: All calculations include safety factors and industry-standard multipliers*

---

## 🎨 Features in Detail

### AI Design Assistant
- Contextual suggestions based on project parameters
- Best practices recommendations
- Code compliance guidance
- Material optimization tips

### Professional Dashboard
- **Sidebar Navigation**: Quick access to all features
- **Stats Grid**: At-a-glance project metrics
- **Data Tables**: Detailed information presentation
- **Action Buttons**: Clear call-to-action elements

### 3D Visualization
- **Multiple Views**: 6 different architectural perspectives
- **Interactive Models**: Pan, zoom, rotate capabilities (in advanced scripts)
- **Measurement Tools**: Dimension annotations
- **Export Options**: Multiple format support

---

## 🚧 Roadmap

### Coming Soon
- ✅ PDF Export functionality
- ✅ Advanced 3D viewer with WebGL
- ✅ Cloud storage integration
- ✅ Multi-user collaboration
- ✅ Mobile app (iOS/Android)
- ✅ BIM integration
- ✅ Real-time cost database updates
- ✅ Machine learning-based optimization



[🌐 Live Demo](http://localhost:8000/Structured3D/FINAL_WORKING.html) | [📖 Documentation](HOW_TO_USE.md) | [🐛 Report Bug](https://github.com/TeenaSingh4640/CeraTech-2026/issues)

⭐ **Star this repo if you find it useful!** ⭐

</div>
