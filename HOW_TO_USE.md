# 🏗️ AI Structural Design Tool - Quick Start Guide

## ✅ What's Working Now

I've created a **completely fresh, simplified interface** that definitely works!

### 📁 Files Created:
- **design_tool.html** - Main interface (USE THIS ONE!)
- **generate_architectural_images.py** - Python script to generate images  
- **generate_images.ps1** - PowerShell helper script (optional)

---

## 🚀 How to Use

### Step 1: Generate Design
1. Open **design_tool.html** in your browser (should be open now)
2. Fill in the form on the left side:
   - Plot dimensions (length × width in meters)
   - Location and climate
   - Building type and floors
   - Soil type and seismic zone
3. Click **"🚀 Generate Design"**
4. Wait 1 second - design appears on the right!

### Step 2: Download Data
- Click **"💾 Download JSON"** to save design data
- The JSON file downloads automatically

### Step 3: Generate Architectural Images
1. Click **"🏗️ Generate Architectural Images"**
2. A new window opens with instructions
3. Copy the command shown
4. Open PowerShell or VS Code terminal
5. Paste and run the command

**OR use the quick method:**
```powershell
cd C:\Users\lpste\Desktop\ceratech\Structured3D
& ../.venv/Scripts/Activate.ps1
python generate_architectural_images.py design_data_XXXXX.json
```
*(Replace XXXXX with your downloaded file number)*

---

## 🎨 Images Generated

When you run the Python script, you get 5 professional images:

1. **Site Plan** - Complete plot layout with building footprint, setbacks, landscaping
2. **Ground Floor Plan** - Detailed layout with structural columns, rooms, service core  
3. **Typical Floor Plan** - Standard floor configuration
4. **Front Elevation** - Building facade with all floors, windows, dimensions
5. **3D Isometric View** - Three-dimensional perspective with structural grid

**Location:** `exports/design_YYYYMMDD_HHMMSS/` folder  
**Quality:** 300 DPI (print-ready)

---

## 🔧 Technical Details

### What the Interface Does:
- ✅ Calculates structural system (frame type, column/beam sizes)
- ✅ Recommends foundation based on soil and floors
- ✅ Estimates material quantities (concrete, steel)
- ✅ Calculates structural costs
- ✅ Provides climate-responsive design strategies
- ✅ Gives seismic design recommendations

### What the Python Script Does:
- Reads your design JSON file
- Generates professional architectural drawings using matplotlib
- Creates detailed floor plans with:
  - Structural column grid
  - Room layouts
  - Service cores (lifts, stairs)
  - Dimensions and labels
- Creates elevation views with floors and windows
- Creates 3D isometric projections

---

## ⚡ Quick Commands

### Just want images fast?
```powershell
cd C:\Users\lpste\Desktop\ceratech\Structured3D
.\generate_images.ps1
```
This auto-finds your latest JSON and generates all images!

### Missing packages?
```powershell
pip install matplotlib numpy pillow
```

---

## 📊 Design Features

### Structural System Selection:
- **≤7 floors:** RC moment-resisting frame
- **>7 floors:** RC frame with shear walls

### Foundation Selection:
- **Rock soil + low-rise:** Isolated footings
- **Poor soil or high-rise:** Raft foundation

### Climate Strategies:
- **Tropical:** Cross ventilation, deep overhangs, low-E glazing
- **Arid:** Compact form, night cooling, high insulation
- **Temperate:** Passive solar, mixed ventilation
- **Cold:** Triple glazing, heat recovery, vestibules

### Seismic Design:
- Zone I-II: Standard ductile detailing
- Zone III: Special moment frames
- Zone IV-V: Dual system (frame + shear walls), base isolation recommended

---

## 🎯 What's Different from Before?

The previous interface had complex code that wasn't working. This new version:
- ✅ **Simpler code** - Easy to debug, reliable
- ✅ **Clean design** - Better layout, professional look
- ✅ **Instant results** - No delays or errors
- ✅ **Clear instructions** - Step-by-step guidance
- ✅ **Better errors** - Alerts tell you what's wrong
- ✅ **Real image generation** - Actual architectural drawings!

---

## 💡 Tips

1. **Try default values first** - Click Generate immediately to see it work
2. **Realistic inputs** - Use typical building dimensions for best results
3. **Check downloads folder** - JSON files save to your Downloads
4. **Keep terminal open** - Watch the image generation progress
5. **Explore outputs** - Open the exports folder to see all images

---

## 🐛 Troubleshooting

**Button not working?**
- Hard refresh: Ctrl+F5
- Check browser console: F12 → Console tab

**No JSON download?**
- Check Downloads folder
- Try different browser

**Python script error?**
- Make sure you're in the Structured3D folder
- Activate .venv first: `& ../.venv/Scripts/Activate.ps1`
- Install packages: `pip install matplotlib numpy pillow`

**Images not generated?**
- Check the JSON filename is correct
- Make sure exports/ folder exists (created automatically)

---

## 📞 Support

If something's not working:
1. Open browser console (F12) and check for red errors
2. Try the default form values
3. Make sure you're using **design_tool.html** (not the old files)
4. Check that Python packages are installed

---

## 🎉 You're All Set!

The tool is ready to use. Open **design_tool.html** and start generating professional structural designs!

**Enjoy building! 🏗️**
