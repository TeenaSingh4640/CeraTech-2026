"""
AI ARCHITECTURAL RENDERING PROMPT GENERATOR
===========================================

Automatically generates photorealistic rendering prompts based on 
structural analysis parameters.

Usage:
    python generate_rendering_prompts.py
    
Output:
    - Console display of prompts
    - Text file with all variants
    - Ready for AI image generation tools

Author: Structural Design System
Date: February 26, 2026
"""

import json
from datetime import datetime
from typing import Dict, List


class RenderingPromptGenerator:
    """Generate architectural rendering prompts from structural data"""
    
    def __init__(self, 
                 num_floors: int = 10,
                 plot_length: float = 50.0,
                 plot_width: float = 30.0,
                 building_type: str = "commercial",
                 location: str = "Mumbai",
                 climate: str = "tropical coastal",
                 style: str = "contemporary modernist",
                 grid_x: float = 7.14,
                 grid_y: float = 7.50,
                 column_ground: int = 700,
                 column_top: int = 300):
        """
        Initialize prompt generator with building parameters
        
        Args:
            num_floors: Number of floors
            plot_length: Plot length in meters
            plot_width: Plot width in meters
            building_type: Type of building (commercial, residential, etc.)
            location: City/location name
            climate: Climate description
            style: Architectural style
            grid_x: Grid spacing in X direction (m)
            grid_y: Grid spacing in Y direction (m)
            column_ground: Ground floor column size (mm)
            column_top: Top floor column size (mm)
        """
        self.num_floors = num_floors
        self.plot_length = plot_length
        self.plot_width = plot_width
        self.building_type = building_type
        self.location = location
        self.climate = climate
        self.style = style
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.column_ground = column_ground
        self.column_top = column_top
        
        # Calculate derived parameters
        self.building_height = num_floors * 3.5  # Typical floor-to-floor
        self.num_bays_x = int(plot_length / grid_x)
        self.num_bays_y = int(plot_width / grid_y)
        
    def generate_base_prompt(self, 
                            view_type: str = "perspective",
                            lighting: str = "golden hour",
                            additional_features: str = "") -> str:
        """
        Generate base rendering prompt
        
        Args:
            view_type: Type of view (perspective, aerial, detail, street, night)
            lighting: Lighting condition
            additional_features: Additional features to include
            
        Returns:
            Complete rendering prompt string
        """
        
        # View-specific additions
        view_additions = {
            "perspective": f"professional architectural visualization from street level perspective, ",
            "aerial": f"aerial drone view from 100m height showing urban context, ",
            "detail": f"close-up architectural detail view showing material textures and junctions, ",
            "street": f"street level view at human eye height 1.6m, pedestrian perspective, ",
            "night": f"twilight blue hour view with interior lighting visible, ",
            "interior": f"interior view showing spatial quality and natural daylighting, ",
            "section": f"architectural section cutaway showing structural system, "
        }
        
        view_text = view_additions.get(view_type, "")
        
        # Build prompt
        prompt = f"""Ultra realistic architectural rendering of a {self.num_floors}-storey {self.building_type} building on a {self.plot_length}m × {self.plot_width}m site located in {self.climate} {self.location}, designed in {self.style} style, reinforced concrete structural frame visible with {self.grid_x}m × {self.grid_y}m bay spacing, realistic façade articulation with climate-responsive design, window grid aligned with {self.column_ground}mm structural columns at ground floor tapering to {self.column_top}mm at top, {view_text}{additional_features}professional architectural visualization, high detail, natural daylight, {lighting} lighting, photorealistic materials, 4K resolution"""
        
        return prompt.strip()
    
    def generate_all_variants(self) -> Dict[str, str]:
        """
        Generate all common rendering prompt variants
        
        Returns:
            Dictionary of prompt variants
        """
        prompts = {}
        
        # 1. Main perspective - golden hour
        prompts["01_Main_Perspective"] = self.generate_base_prompt(
            view_type="perspective",
            lighting="golden hour",
            additional_features="cantilevered balconies, glass curtain wall with aluminum mullions, deep overhangs for sun protection, vertical shading fins, dramatic shadows, "
        )
        
        # 2. Street level entry
        prompts["02_Street_Entry"] = self.generate_base_prompt(
            view_type="street",
            lighting="midday",
            additional_features="double-height ground floor lobby, human scale figures, tropical landscaping with palm trees, shaded entry plaza, "
        )
        
        # 3. Aerial contextual
        prompts["03_Aerial_Context"] = self.generate_base_prompt(
            view_type="aerial",
            lighting="afternoon",
            additional_features=f"{self.num_bays_x} × {self.num_bays_y} bay structural grid clearly visible, rooftop solar panels, surrounding urban development, "
        )
        
        # 4. Night/twilight
        prompts["04_Night_View"] = self.generate_base_prompt(
            view_type="night",
            lighting="blue hour",
            additional_features="warm interior office lighting visible through glazing, structural grid pattern emphasized by interior lights, dramatic dusk atmosphere, "
        )
        
        # 5. Façade detail
        prompts["05_Facade_Detail"] = self.generate_base_prompt(
            view_type="detail",
            lighting="overcast diffuse",
            additional_features=f"exposed concrete columns and beams, unitized curtain wall system, climate-responsive external louvers, {self.grid_x}m bay width clearly visible, high resolution material finishes, "
        )
        
        # 6. Interior typical floor
        prompts["06_Interior_Office"] = self.generate_base_prompt(
            view_type="interior",
            lighting="natural daylight",
            additional_features=f"typical office floor open plan layout, {self.column_ground}mm × {self.column_ground}mm columns integrated into design, floor-to-ceiling glazing, contemporary office furniture, "
        )
        
        # 7. Structural section
        prompts["07_Structural_Section"] = self.generate_base_prompt(
            view_type="section",
            lighting="technical lighting",
            additional_features=f"complete structural system visible, dual frame and shear wall system, columns stepping from {self.column_ground}mm to {self.column_top}mm, foundation system shown, technical detail with dimensions, "
        )
        
        # 8. Green features
        prompts["08_Green_Building"] = self.generate_base_prompt(
            view_type="perspective",
            lighting="bright sunny day",
            additional_features=f"vertical gardens on balconies aligned with {self.grid_x}m structural grid, rooftop solar panels, rainwater harvesting features, climate-responsive shading, lush tropical landscaping, sustainable architecture, "
        )
        
        return prompts
    
    def generate_negative_prompt(self) -> str:
        """Generate negative prompt to exclude unwanted elements"""
        return ("cartoon, anime, sketch, drawing, unrealistic proportions, distorted perspective, "
                "oversaturated colors, fantasy architecture, impossible structures, poor quality, "
                "blurry, low resolution,text, watermark, signature, out of frame")
    
    def format_for_midjourney(self, prompt: str, aspect_ratio: str = "16:9", quality: int = 2) -> str:
        """
        Format prompt for Midjourney with parameters
        
        Args:
            prompt: Base prompt text
            aspect_ratio: Image aspect ratio (16:9, 4:5, 1:1, etc.)
            quality: Quality setting (1 or 2)
            
        Returns:
            Midjourney-formatted prompt with parameters
        """
        return f"{prompt} --ar {aspect_ratio} --q {quality} --style raw --s 50"
    
    def format_for_dalle(self, prompt: str) -> str:
        """Format prompt for DALL-E (simpler, no parameters)"""
        # DALL-E works best with concise prompts
        return prompt[:4000]  # DALL-E has character limit
    
    def export_prompts(self, filename: str = None) -> str:
        """
        Export all prompts to text file
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Filename of exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rendering_prompts_{timestamp}.txt"
        
        prompts = self.generate_all_variants()
        negative = self.generate_negative_prompt()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ARCHITECTURAL RENDERING PROMPTS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Building: {self.num_floors}-storey {self.building_type}\n")
            f.write(f"Location: {self.location} ({self.climate})\n")
            f.write(f"Plot Size: {self.plot_length}m × {self.plot_width}m\n")
            f.write(f"Structural Grid: {self.grid_x}m × {self.grid_y}m\n")
            f.write(f"Style: {self.style}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("POSITIVE PROMPTS\n")
            f.write("=" * 80 + "\n\n")
            
            for name, prompt in prompts.items():
                f.write(f"{name}\n")
                f.write("-" * 80 + "\n")
                f.write(f"{prompt}\n\n")
                
                # Add Midjourney variant
                f.write("MIDJOURNEY FORMAT:\n")
                f.write(f"{self.format_for_midjourney(prompt)}\n\n")
                f.write("=" * 80 + "\n\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("NEGATIVE PROMPT (use with all)\n")
            f.write("=" * 80 + "\n")
            f.write(f"{negative}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
        
        return filename
    
    def display_summary(self):
        """Display prompt generation summary"""
        print("\n" + "=" * 80)
        print("RENDERING PROMPT GENERATOR - SUMMARY")
        print("=" * 80)
        print(f"\nBuilding Parameters:")
        print(f"  • Type: {self.building_type}")
        print(f"  • Floors: {self.num_floors} ({self.building_height}m height)")
        print(f"  • Plot: {self.plot_length}m × {self.plot_width}m")
        print(f"  • Location: {self.location} ({self.climate})")
        print(f"  • Style: {self.style}")
        print(f"\nStructural Parameters:")
        print(f"  • Grid: {self.grid_x}m × {self.grid_y}m")
        print(f"  • Bays: {self.num_bays_x} × {self.num_bays_y}")
        print(f"  • Columns: {self.column_ground}mm (ground) → {self.column_top}mm (top)")
        print(f"\nPrompt Variants Generated: 8")
        print(f"  1. Main Perspective (Golden Hour)")
        print(f"  2. Street Level Entry")
        print(f"  3. Aerial Contextual View")
        print(f"  4. Night/Twilight View")
        print(f"  5. Façade Detail Close-up")
        print(f"  6. Interior Office Space")
        print(f"  7. Structural Section Cutaway")
        print(f"  8. Green Building Features")
        print("\n" + "=" * 80 + "\n")


def load_from_structural_analysis(json_file: str) -> RenderingPromptGenerator:
    """
    Load building parameters from structural analysis JSON
    
    Args:
        json_file: Path to structural analysis JSON file
        
    Returns:
        RenderingPromptGenerator instance
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Extract parameters from JSON
        # Adjust these keys based on your JSON structure
        params = {
            'num_floors': data.get('project_parameters', {}).get('num_floors', 10),
            'plot_length': data.get('project_parameters', {}).get('plot_length', 50.0),
            'plot_width': data.get('project_parameters', {}).get('plot_width', 30.0),
            'building_type': data.get('project_parameters', {}).get('building_type', 'commercial'),
            'location': data.get('project_parameters', {}).get('location', 'Mumbai'),
            'style': 'contemporary modernist'
        }
        
        # Extract structural parameters if available
        if 'structural_grid' in data:
            params['grid_x'] = data['structural_grid'].get('span_x', 7.14)
            params['grid_y'] = data['structural_grid'].get('span_y', 7.50)
        
        if 'column_sizing' in data:
            floors = data['column_sizing'].get('floor_by_floor', [])
            if floors:
                params['column_ground'] = floors[0].get('column_size', 700)
                params['column_top'] = floors[-1].get('column_size', 300)
        
        return RenderingPromptGenerator(**params)
    
    except FileNotFoundError:
        print(f"Warning: Could not find {json_file}. Using default parameters.")
        return RenderingPromptGenerator()
    except Exception as e:
        print(f"Warning: Error loading JSON: {e}. Using default parameters.")
        return RenderingPromptGenerator()


def main():
    """Main execution function"""
    
    print("\n" + "=" * 80)
    print("AI ARCHITECTURAL RENDERING PROMPT GENERATOR")
    print("=" * 80)
    print("\nGenerating prompts based on structural analysis results...")
    
    # Try to load from structural analysis JSON
    json_file = "complete_structural_analysis_20260226_141951.json"
    
    # Create generator
    generator = load_from_structural_analysis(json_file)
    
    # Display summary
    generator.display_summary()
    
    # Generate all variants
    print("Generating prompt variants...")
    prompts = generator.generate_all_variants()
    
    # Display first prompt as example
    print("\n" + "=" * 80)
    print("EXAMPLE: Main Perspective View (Golden Hour)")
    print("=" * 80)
    print(f"\n{prompts['01_Main_Perspective']}\n")
    
    print("\nMIDJOURNEY FORMAT:")
    print(generator.format_for_midjourney(prompts['01_Main_Perspective']))
    print("\n" + "-" * 80)
    
    # Export to file
    print("\nExporting all prompts to file...")
    filename = generator.export_prompts()
    print(f"✓ Exported to: {filename}")
    
    # Display negative prompt
    print("\n" + "=" * 80)
    print("NEGATIVE PROMPT (use with all renderings)")
    print("=" * 80)
    print(f"\n{generator.generate_negative_prompt()}\n")
    
    print("=" * 80)
    print("READY TO USE!")
    print("=" * 80)
    print("\nNext Steps:")
    print("  1. Copy prompts from generated text file")
    print("  2. Paste into AI image generation tool:")
    print("     • Midjourney (use Midjourney format)")
    print("     • DALL-E (use standard format)")
    print("     • Stable Diffusion (use standard format)")
    print("  3. Or use with 3D rendering software:")
    print("     • Revit + Enscape")
    print("     • SketchUp + V-Ray")
    print("     • 3ds Max + Corona")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
