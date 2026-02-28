"""
STRUCTURAL QUANTITY ESTIMATION & COST ANALYSIS MODULE

Purpose: Detailed quantity takeoff and cost estimation for structural systems
Based on: Previous structural design calculations
Standards: IS 1200 (Method of Measurement), CPWD DSR 2023

Author: Advanced AI Structural Design Engine
Date: February 2026
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple, Any


class BuiltUpAreaCalculation:
    """
    Calculate built-up area per floor with deductions
    
    Methodology:
    - Gross Floor Area (GFA): Plot length × width
    - Carpet Area: Usable area (excludes walls, shafts)
    - Super Built-up Area: Includes common areas
    - FSI calculation per local regulations
    
    Assumptions:
    - External wall thickness: 230mm (9" masonry)
    - Internal wall thickness: 115mm (4.5" partition)
    - Core area (stairs, lifts, services): 8-12% of GFA
    - Efficiency ratio: 75-80% (carpet/GFA)
    """
    
    def __init__(self, plot_length: float, plot_width: float, num_floors: int,
                 building_type: str, column_grid: Dict):
        """
        Args:
            plot_length: Plot length in meters
            plot_width: Plot width in meters
            num_floors: Number of floors
            building_type: Commercial/Residential/Institutional
            column_grid: Dictionary with grid configuration
        """
        self.plot_length = plot_length
        self.plot_width = plot_width
        self.num_floors = num_floors
        self.building_type = building_type
        self.column_grid = column_grid
        
        # Constants based on building type
        self.core_percentage = {
            "Commercial": 0.12,      # 12% for lifts, stairs, toilets
            "Residential": 0.10,     # 10% for circulation
            "Institutional": 0.15    # 15% for labs, services
        }
        
        self.efficiency_ratio = {
            "Commercial": 0.77,      # 77% efficiency (corporate standard)
            "Residential": 0.80,     # 80% efficiency
            "Institutional": 0.75    # 75% efficiency
        }
    
    def calculate_areas(self) -> Dict[str, Any]:
        """
        Calculate all area components
        
        Returns:
            Dictionary with area breakdown
        """
        # 1. Gross Floor Area (GFA)
        gfa_per_floor = self.plot_length * self.plot_width
        total_gfa = gfa_per_floor * self.num_floors
        
        # 2. Core Area (stairs, lifts, services)
        core_percentage = self.core_percentage.get(self.building_type, 0.12)
        core_area_per_floor = gfa_per_floor * core_percentage
        total_core_area = core_area_per_floor * self.num_floors
        
        # 3. Column Area Deduction
        # Extract column sizes from grid
        num_columns = self.column_grid.get('total_columns', 40)
        # Average column size (considering taper from 700mm to 300mm)
        avg_column_size = (0.7 + 0.3) / 2  # 0.5m average
        column_area_per_floor = num_columns * (avg_column_size ** 2)
        total_column_area = column_area_per_floor * self.num_floors
        
        # 4. Carpet Area (usable area)
        efficiency = self.efficiency_ratio.get(self.building_type, 0.77)
        carpet_area_per_floor = gfa_per_floor * efficiency - core_area_per_floor
        total_carpet_area = carpet_area_per_floor * self.num_floors
        
        # 5. Circulation Area
        circulation_per_floor = gfa_per_floor - carpet_area_per_floor - core_area_per_floor - column_area_per_floor
        total_circulation = circulation_per_floor * self.num_floors
        
        # 6. Super Built-up Area (includes common areas with loading factor)
        common_area_factor = 1.15  # 15% loading for common areas
        super_builtup_per_floor = carpet_area_per_floor * common_area_factor
        total_super_builtup = super_builtup_per_floor * self.num_floors
        
        # 7. Saleable Area (for commercial: ~85% of super built-up)
        saleable_factor = 0.85
        saleable_area_per_floor = super_builtup_per_floor * saleable_factor
        total_saleable = saleable_area_per_floor * self.num_floors
        
        # 8. FAR/FSI Consumption
        # Assuming plot FSI = 3.0 (typical urban limit)
        plot_area = self.plot_length * self.plot_width
        fsi_consumed = total_gfa / plot_area
        
        return {
            "gross_floor_area_per_floor_m2": round(gfa_per_floor, 2),
            "total_gross_floor_area_m2": round(total_gfa, 2),
            "carpet_area_per_floor_m2": round(carpet_area_per_floor, 2),
            "total_carpet_area_m2": round(total_carpet_area, 2),
            "core_area_per_floor_m2": round(core_area_per_floor, 2),
            "total_core_area_m2": round(total_core_area, 2),
            "circulation_area_per_floor_m2": round(circulation_per_floor, 2),
            "total_circulation_area_m2": round(total_circulation, 2),
            "column_area_per_floor_m2": round(column_area_per_floor, 2),
            "total_column_area_m2": round(total_column_area, 2),
            "super_builtup_per_floor_m2": round(super_builtup_per_floor, 2),
            "total_super_builtup_m2": round(total_super_builtup, 2),
            "saleable_area_per_floor_m2": round(saleable_area_per_floor, 2),
            "total_saleable_area_m2": round(total_saleable, 2),
            "efficiency_ratio": efficiency,
            "fsi_consumed": round(fsi_consumed, 2),
            "plot_area_m2": round(plot_area, 2),
            "assumptions": {
                "core_percentage": f"{core_percentage*100}%",
                "efficiency_ratio": f"{efficiency*100}%",
                "common_area_loading": "15%",
                "saleable_from_super_builtup": "85%"
            }
        }


class ConcreteVolumeEstimation:
    """
    Estimate total concrete volume for all structural elements
    
    Components:
    1. Columns (tapered from base to top)
    2. Beams (primary + secondary)
    3. Slabs (including drops if any)
    4. Shear walls (for lateral system)
    5. Foundation (raft/piled raft)
    
    Assumptions:
    - Floor height: 3.5m (commercial typical)
    - Shear wall thickness: 300mm (for dual system)
    - Foundation depth: 2.5m (average for piled raft)
    - Wastage: 5% (transport, spillage, over-excavation)
    """
    
    def __init__(self, plot_length: float, plot_width: float, num_floors: int,
                 column_sizes: List[Dict], beam_sections: Dict, slab_thickness: float,
                 lateral_system: str):
        """
        Args:
            plot_length: Building length (m)
            plot_width: Building width (m)
            num_floors: Number of floors
            column_sizes: List of column dimensions per floor
            beam_sections: Dictionary with beam dimensions
            slab_thickness: Slab thickness (m)
            lateral_system: Type of lateral system
        """
        self.plot_length = plot_length
        self.plot_width = plot_width
        self.num_floors = num_floors
        self.column_sizes = column_sizes
        self.beam_sections = beam_sections
        self.slab_thickness = slab_thickness
        self.lateral_system = lateral_system
        
        self.floor_height = 3.5  # meters
        self.wastage_factor = 1.05  # 5% wastage
    
    def calculate_column_volume(self) -> Dict[str, float]:
        """
        Calculate concrete volume for all columns
        
        Method:
        - Tapered columns: Use average cross-section
        - Volume = Σ(Area × Height) for all floors
        """
        total_volume = 0.0
        floor_wise_volume = []
        
        # Assuming 40 columns total (from 7×4 grid + edge columns)
        num_columns = 40
        
        for floor_idx in range(self.num_floors):
            # Get column size for this floor
            if floor_idx < len(self.column_sizes):
                col_size = self.column_sizes[floor_idx].get('size_m', 0.7 - floor_idx * 0.04)
            else:
                col_size = 0.3  # minimum 300mm
            
            # Column area
            col_area = col_size * col_size
            
            # Volume for this floor
            floor_volume = num_columns * col_area * self.floor_height
            total_volume += floor_volume
            
            floor_wise_volume.append({
                "floor": floor_idx + 1,
                "column_size_m": round(col_size, 3),
                "volume_m3": round(floor_volume, 2)
            })
        
        # Apply wastage
        total_volume_with_wastage = total_volume * self.wastage_factor
        
        return {
            "total_column_volume_m3": round(total_volume, 2),
            "with_wastage_m3": round(total_volume_with_wastage, 2),
            "floor_wise": floor_wise_volume,
            "assumptions": {
                "num_columns": num_columns,
                "floor_height_m": self.floor_height,
                "wastage_factor": f"{(self.wastage_factor-1)*100}%"
            }
        }
    
    def calculate_beam_volume(self) -> Dict[str, float]:
        """
        Calculate concrete volume for all beams
        
        Types:
        - Primary beams (along grid lines)
        - Secondary beams (perpendicular)
        
        Method:
        - Total length = Grid perimeter × floors
        - Volume = Length × Width × Depth
        """
        # Beam dimensions (from structural design)
        beam_width = self.beam_sections.get('width_m', 0.25)  # 250mm
        beam_depth = self.beam_sections.get('depth_m', 0.30)  # 300mm
        beam_area = beam_width * beam_depth
        
        # Calculate total beam length per floor
        # Primary beams (7 bays × 4 spans + 4 bays × 7 spans)
        primary_length_per_floor = (7 * self.plot_length / 7 * 4) + (4 * self.plot_width / 4 * 7)
        # Simplified: perimeter-based
        primary_length_per_floor = 2 * (self.plot_length + self.plot_width)
        
        # Secondary beams (internal grid)
        # 6 internal longitudinal + 3 internal transverse
        secondary_length_per_floor = (6 * self.plot_length) + (3 * self.plot_width)
        
        total_length_per_floor = primary_length_per_floor + secondary_length_per_floor
        total_length_all_floors = total_length_per_floor * self.num_floors
        
        # Volume calculation
        total_volume = total_length_all_floors * beam_area
        total_volume_with_wastage = total_volume * self.wastage_factor
        
        return {
            "beam_width_m": beam_width,
            "beam_depth_m": beam_depth,
            "beam_cross_section_m2": round(beam_area, 4),
            "primary_beam_length_per_floor_m": round(primary_length_per_floor, 2),
            "secondary_beam_length_per_floor_m": round(secondary_length_per_floor, 2),
            "total_beam_length_per_floor_m": round(total_length_per_floor, 2),
            "total_beam_length_all_floors_m": round(total_length_all_floors, 2),
            "total_beam_volume_m3": round(total_volume, 2),
            "with_wastage_m3": round(total_volume_with_wastage, 2),
            "assumptions": {
                "grid_configuration": "7×4 bays",
                "wastage_factor": f"{(self.wastage_factor-1)*100}%"
            }
        }
    
    def calculate_slab_volume(self) -> Dict[str, float]:
        """
        Calculate concrete volume for all slabs
        
        Method:
        - Slab area = Plot length × width
        - Volume = Area × Thickness × Number of floors
        - Deduction: Column area (already calculated)
        """
        # Slab area per floor
        gross_slab_area = self.plot_length * self.plot_width
        
        # Deduct column area (40 columns × average size²)
        avg_column_size = 0.5  # 500mm average
        column_deduction = 40 * (avg_column_size ** 2)
        
        net_slab_area_per_floor = gross_slab_area - column_deduction
        total_slab_area = net_slab_area_per_floor * self.num_floors
        
        # Volume
        total_volume = total_slab_area * self.slab_thickness
        total_volume_with_wastage = total_volume * self.wastage_factor
        
        return {
            "slab_thickness_m": self.slab_thickness,
            "gross_slab_area_per_floor_m2": round(gross_slab_area, 2),
            "column_deduction_per_floor_m2": round(column_deduction, 2),
            "net_slab_area_per_floor_m2": round(net_slab_area_per_floor, 2),
            "total_slab_area_m2": round(total_slab_area, 2),
            "total_slab_volume_m3": round(total_volume, 2),
            "with_wastage_m3": round(total_volume_with_wastage, 2),
            "assumptions": {
                "column_deduction": "40 columns × 0.5m²",
                "wastage_factor": f"{(self.wastage_factor-1)*100}%"
            }
        }
    
    def calculate_shear_wall_volume(self) -> Dict[str, float]:
        """
        Calculate concrete volume for shear walls (if dual system)
        
        Assumptions:
        - Shear wall thickness: 300mm
        - Shear wall length: 20% of perimeter (typical for dual systems)
        - Height: Full building height
        """
        if "dual" not in self.lateral_system.lower():
            return {
                "shear_wall_volume_m3": 0.0,
                "note": "No shear walls (frame system)"
            }
        
        # Shear wall parameters
        wall_thickness = 0.30  # 300mm
        total_height = self.num_floors * self.floor_height
        perimeter = 2 * (self.plot_length + self.plot_width)
        
        # Typical shear wall length: 20% of perimeter
        total_wall_length = perimeter * 0.20
        
        # Volume
        total_volume = total_wall_length * wall_thickness * total_height
        total_volume_with_wastage = total_volume * self.wastage_factor
        
        return {
            "shear_wall_thickness_m": wall_thickness,
            "total_shear_wall_length_m": round(total_wall_length, 2),
            "building_height_m": round(total_height, 2),
            "total_shear_wall_volume_m3": round(total_volume, 2),
            "with_wastage_m3": round(total_volume_with_wastage, 2),
            "assumptions": {
                "wall_length_percentage": "20% of perimeter",
                "wall_thickness": "300mm",
                "wastage_factor": f"{(self.wastage_factor-1)*100}%"
            }
        }
    
    def calculate_foundation_volume(self) -> Dict[str, float]:
        """
        Calculate concrete volume for foundation
        
        Assumptions:
        - Piled raft foundation (for medium-rise)
        - Raft thickness: 1.0m (heavily loaded)
        - Piles: 40 columns × 1 pile each
        - Pile diameter: 600mm
        - Pile depth: 15m (typical for sand/clay)
        """
        # Raft foundation
        raft_area = self.plot_length * self.plot_width
        raft_thickness = 1.0  # 1m thick raft
        raft_volume = raft_area * raft_thickness
        
        # Piles
        num_piles = 40  # One under each column
        pile_diameter = 0.6  # 600mm
        pile_depth = 15.0  # 15m
        pile_area = 3.14159 * (pile_diameter / 2) ** 2
        pile_volume = num_piles * pile_area * pile_depth
        
        # Pile caps (one per pile)
        pile_cap_size = 1.5  # 1.5m × 1.5m
        pile_cap_depth = 0.8  # 800mm
        pile_cap_volume = num_piles * (pile_cap_size ** 2) * pile_cap_depth
        
        # Total foundation volume
        total_volume = raft_volume + pile_volume + pile_cap_volume
        total_volume_with_wastage = total_volume * 1.10  # 10% wastage for foundation
        
        return {
            "raft_foundation": {
                "area_m2": round(raft_area, 2),
                "thickness_m": raft_thickness,
                "volume_m3": round(raft_volume, 2)
            },
            "piles": {
                "number_of_piles": num_piles,
                "pile_diameter_m": pile_diameter,
                "pile_depth_m": pile_depth,
                "total_pile_volume_m3": round(pile_volume, 2)
            },
            "pile_caps": {
                "number": num_piles,
                "cap_size_m": pile_cap_size,
                "cap_depth_m": pile_cap_depth,
                "total_cap_volume_m3": round(pile_cap_volume, 2)
            },
            "total_foundation_volume_m3": round(total_volume, 2),
            "with_wastage_m3": round(total_volume_with_wastage, 2),
            "assumptions": {
                "foundation_type": "Piled Raft",
                "raft_thickness": "1.0m",
                "pile_configuration": "1 pile per column",
                "wastage_factor": "10%"
            }
        }
    
    def calculate_total_concrete(self) -> Dict[str, Any]:
        """
        Calculate total concrete volume for entire structure
        """
        columns = self.calculate_column_volume()
        beams = self.calculate_beam_volume()
        slabs = self.calculate_slab_volume()
        shear_walls = self.calculate_shear_wall_volume()
        foundation = self.calculate_foundation_volume()
        
        # Total without wastage
        total_superstructure = (
            columns['total_column_volume_m3'] +
            beams['total_beam_volume_m3'] +
            slabs['total_slab_volume_m3'] +
            shear_walls.get('total_shear_wall_volume_m3', 0)
        )
        
        total_substructure = foundation['total_foundation_volume_m3']
        total_concrete = total_superstructure + total_substructure
        
        # Total with wastage
        total_with_wastage = (
            columns['with_wastage_m3'] +
            beams['with_wastage_m3'] +
            slabs['with_wastage_m3'] +
            shear_walls.get('with_wastage_m3', 0) +
            foundation['with_wastage_m3']
        )
        
        return {
            "columns": columns,
            "beams": beams,
            "slabs": slabs,
            "shear_walls": shear_walls,
            "foundation": foundation,
            "summary": {
                "total_column_volume_m3": round(columns['total_column_volume_m3'], 2),
                "total_beam_volume_m3": round(beams['total_beam_volume_m3'], 2),
                "total_slab_volume_m3": round(slabs['total_slab_volume_m3'], 2),
                "total_shear_wall_volume_m3": round(shear_walls.get('total_shear_wall_volume_m3', 0), 2),
                "total_superstructure_m3": round(total_superstructure, 2),
                "total_substructure_m3": round(total_substructure, 2),
                "total_concrete_volume_m3": round(total_concrete, 2),
                "total_with_wastage_m3": round(total_with_wastage, 2),
                "percentage_breakdown": {
                    "columns": f"{(columns['total_column_volume_m3']/total_concrete*100):.1f}%",
                    "beams": f"{(beams['total_beam_volume_m3']/total_concrete*100):.1f}%",
                    "slabs": f"{(slabs['total_slab_volume_m3']/total_concrete*100):.1f}%",
                    "shear_walls": f"{(shear_walls.get('total_shear_wall_volume_m3', 0)/total_concrete*100):.1f}%",
                    "foundation": f"{(foundation['total_foundation_volume_m3']/total_concrete*100):.1f}%"
                }
            }
        }


class SteelReinforcementEstimation:
    """
    Estimate steel reinforcement requirement
    
    Method: Reinforcement ratio method
    
    Typical Ratios (% of concrete volume):
    - Columns: 2.0-2.5% (by volume) → ~160-200 kg/m³
    - Beams: 1.5-2.0% → ~120-160 kg/m³
    - Slabs: 1.0-1.2% → ~80-95 kg/m³
    - Shear walls: 0.5-0.8% → ~40-65 kg/m³
    - Foundation: 1.0-1.5% → ~80-120 kg/m³
    
    Assumptions:
    - Steel density: 7850 kg/m³
    - Wastage: 8% (cutting, lapping, site wastage)
    - Lap length factor: 1.10 (10% extra for laps)
    """
    
    def __init__(self, concrete_volumes: Dict, material_grade: str = "Fe 500"):
        """
        Args:
            concrete_volumes: Dictionary with concrete volumes
            material_grade: Steel grade (Fe 415, Fe 500, Fe 550)
        """
        self.concrete_volumes = concrete_volumes
        self.material_grade = material_grade
        
        self.steel_density = 7850  # kg/m³
        self.wastage_factor = 1.08  # 8% wastage
        self.lap_factor = 1.10  # 10% for laps
        
        # Reinforcement ratios (kg per m³ of concrete)
        self.reinforcement_ratios = {
            "columns": 180,     # kg/m³ (2.3% by volume)
            "beams": 140,       # kg/m³ (1.8% by volume)
            "slabs": 90,        # kg/m³ (1.15% by volume)
            "shear_walls": 55,  # kg/m³ (0.7% by volume)
            "foundation": 100   # kg/m³ (1.3% by volume)
        }
    
    def calculate_steel_requirement(self) -> Dict[str, Any]:
        """
        Calculate total steel requirement
        """
        # Extract concrete volumes
        col_vol = self.concrete_volumes['columns']['total_column_volume_m3']
        beam_vol = self.concrete_volumes['beams']['total_beam_volume_m3']
        slab_vol = self.concrete_volumes['slabs']['total_slab_volume_m3']
        wall_vol = self.concrete_volumes['shear_walls'].get('total_shear_wall_volume_m3', 0)
        found_vol = self.concrete_volumes['foundation']['total_foundation_volume_m3']
        
        # Calculate steel for each component (basic)
        steel_columns = col_vol * self.reinforcement_ratios['columns']
        steel_beams = beam_vol * self.reinforcement_ratios['beams']
        steel_slabs = slab_vol * self.reinforcement_ratios['slabs']
        steel_walls = wall_vol * self.reinforcement_ratios['shear_walls']
        steel_foundation = found_vol * self.reinforcement_ratios['foundation']
        
        # Total basic steel
        total_basic_steel = steel_columns + steel_beams + steel_slabs + steel_walls + steel_foundation
        
        # Apply lap factor
        total_with_laps = total_basic_steel * self.lap_factor
        
        # Apply wastage
        total_with_wastage = total_with_laps * self.wastage_factor
        
        # Steel breakdown by diameter (typical distribution)
        diameter_distribution = {
            "8mm": 0.10,   # 10% - stirrups, distribution bars
            "10mm": 0.15,  # 15% - slab bars, secondary stirrups
            "12mm": 0.20,  # 20% - slab main bars, small beams
            "16mm": 0.25,  # 25% - beam main bars, column ties
            "20mm": 0.20,  # 20% - large beam bars, small column bars
            "25mm": 0.10   # 10% - column main bars
        }
        
        steel_by_diameter = {}
        for dia, percentage in diameter_distribution.items():
            steel_by_diameter[dia] = round(total_with_wastage * percentage, 2)
        
        return {
            "reinforcement_ratios_kg_per_m3": self.reinforcement_ratios,
            "steel_by_component": {
                "columns_kg": round(steel_columns, 2),
                "beams_kg": round(steel_beams, 2),
                "slabs_kg": round(steel_slabs, 2),
                "shear_walls_kg": round(steel_walls, 2),
                "foundation_kg": round(steel_foundation, 2)
            },
            "total_basic_steel_kg": round(total_basic_steel, 2),
            "total_basic_steel_tonnes": round(total_basic_steel / 1000, 2),
            "with_laps_kg": round(total_with_laps, 2),
            "with_laps_tonnes": round(total_with_laps / 1000, 2),
            "with_wastage_kg": round(total_with_wastage, 2),
            "with_wastage_tonnes": round(total_with_wastage / 1000, 2),
            "steel_by_diameter_kg": steel_by_diameter,
            "material_grade": self.material_grade,
            "assumptions": {
                "lap_factor": f"{(self.lap_factor-1)*100}%",
                "wastage_factor": f"{(self.wastage_factor-1)*100}%",
                "steel_density": f"{self.steel_density} kg/m³",
                "typical_distribution": "8mm to 25mm bars"
            }
        }


class FormworkAreaEstimation:
    """
    Estimate formwork area for all structural components
    
    Formwork Types:
    - Column formwork: 4 sides
    - Beam formwork: 3 sides (bottom + 2 sides)
    - Slab formwork: Bottom only
    - Shear wall formwork: 2 sides
    
    Assumptions:
    - Formwork reuse: 6-8 times (aluminum formwork)
    - Edge forms: Additional 15% for edges, openings
    """
    
    def __init__(self, concrete_volumes: Dict, num_floors: int, floor_height: float = 3.5):
        """
        Args:
            concrete_volumes: Dictionary with concrete volumes and dimensions
            num_floors: Number of floors
            floor_height: Floor-to-floor height (m)
        """
        self.concrete_volumes = concrete_volumes
        self.num_floors = num_floors
        self.floor_height = floor_height
        
        self.edge_form_factor = 1.15  # 15% extra for edges
        self.formwork_reuse = 7  # 7 times average
    
    def calculate_formwork_area(self) -> Dict[str, Any]:
        """
        Calculate total formwork area
        """
        # 1. Column Formwork (4 sides × perimeter × height)
        # Assuming tapered columns, use average size
        avg_column_size = 0.5  # 500mm average
        num_columns = 40
        column_perimeter = 4 * avg_column_size
        column_height_per_floor = self.floor_height
        
        column_formwork_per_floor = num_columns * column_perimeter * column_height_per_floor
        total_column_formwork = column_formwork_per_floor * self.num_floors
        
        # 2. Beam Formwork (3 sides: bottom + 2 sides)
        beam_width = 0.25  # 250mm
        beam_depth = 0.30  # 300mm
        beam_length_per_floor = self.concrete_volumes['beams']['total_beam_length_per_floor_m']
        
        # Formwork area = (width + 2×depth) × length
        beam_formwork_perimeter = beam_width + 2 * beam_depth
        beam_formwork_per_floor = beam_formwork_perimeter * beam_length_per_floor
        total_beam_formwork = beam_formwork_per_floor * self.num_floors
        
        # 3. Slab Formwork (bottom surface only)
        slab_area_per_floor = self.concrete_volumes['slabs']['net_slab_area_per_floor_m2']
        total_slab_formwork = slab_area_per_floor * self.num_floors
        
        # 4. Shear Wall Formwork (both sides)
        wall_length = self.concrete_volumes['shear_walls'].get('total_shear_wall_length_m', 0)
        wall_height = self.num_floors * self.floor_height
        shear_wall_formwork = 0
        if wall_length > 0:
            shear_wall_formwork = 2 * wall_length * wall_height
        
        # 5. Foundation Formwork (edges of raft + pile caps)
        foundation_info = self.concrete_volumes['foundation']
        raft_area = foundation_info['raft_foundation']['area_m2']
        raft_perimeter = 2 * (self.concrete_volumes['slabs']['gross_slab_area_per_floor_m2'] ** 0.5 * 2)  # approximate
        raft_thickness = foundation_info['raft_foundation']['thickness_m']
        raft_formwork = raft_perimeter * raft_thickness
        
        # Pile caps (4 sides each)
        num_pile_caps = foundation_info['pile_caps']['number']
        pile_cap_size = foundation_info['pile_caps']['cap_size_m']
        pile_cap_depth = foundation_info['pile_caps']['cap_depth_m']
        pile_cap_formwork = num_pile_caps * 4 * pile_cap_size * pile_cap_depth
        
        foundation_formwork = raft_formwork + pile_cap_formwork
        
        # Total formwork
        total_formwork_basic = (
            total_column_formwork +
            total_beam_formwork +
            total_slab_formwork +
            shear_wall_formwork +
            foundation_formwork
        )
        
        # Apply edge form factor
        total_formwork_with_edges = total_formwork_basic * self.edge_form_factor
        
        # Actual formwork required (considering reuse)
        actual_formwork_required = total_formwork_with_edges / self.formwork_reuse
        
        return {
            "formwork_by_component_m2": {
                "columns": round(total_column_formwork, 2),
                "beams": round(total_beam_formwork, 2),
                "slabs": round(total_slab_formwork, 2),
                "shear_walls": round(shear_wall_formwork, 2),
                "foundation": round(foundation_formwork, 2)
            },
            "total_formwork_basic_m2": round(total_formwork_basic, 2),
            "total_formwork_with_edges_m2": round(total_formwork_with_edges, 2),
            "actual_formwork_required_m2": round(actual_formwork_required, 2),
            "formwork_reuse_factor": self.formwork_reuse,
            "percentage_breakdown": {
                "columns": f"{(total_column_formwork/total_formwork_basic*100):.1f}%",
                "beams": f"{(total_beam_formwork/total_formwork_basic*100):.1f}%",
                "slabs": f"{(total_slab_formwork/total_formwork_basic*100):.1f}%",
                "shear_walls": f"{(shear_wall_formwork/total_formwork_basic*100 if total_formwork_basic > 0 else 0):.1f}%",
                "foundation": f"{(foundation_formwork/total_formwork_basic*100):.1f}%"
            },
            "assumptions": {
                "edge_form_factor": f"{(self.edge_form_factor-1)*100}%",
                "formwork_reuse": f"{self.formwork_reuse} times",
                "formwork_type": "Aluminum/Steel formwork system"
            }
        }


class CostEstimation:
    """
    Rough cost breakdown - Structure vs Finishing
    
    Cost Components:
    STRUCTURE (55-60%):
    - Concrete: M30 @ ₹7,500/m³, M50 @ ₹9,500/m³
    - Steel: Fe 500 @ ₹65,000/tonne
    - Formwork: ₹350/m² (aluminum, amortized)
    - Labor: 30% of material
    
    FINISHING (25-30%):
    - Flooring: ₹800/m²
    - Plastering: ₹150/m²
    - Painting: ₹80/m²
    - False ceiling: ₹200/m²
    - Doors/Windows: ₹1,200/m²
    
    MEP (15-20%):
    - HVAC, Electrical, Plumbing, Fire
    
    Assumptions:
    - Rates: Feb 2026, Tier 1 city (Mumbai/Delhi)
    - GST excluded
    - Contingency: 10%
    """
    
    def __init__(self, concrete_volumes: Dict, steel_requirement: Dict,
                 formwork_area: Dict, built_up_areas: Dict, location: str = "Mumbai"):
        """
        Args:
            concrete_volumes: Concrete volume breakdown
            steel_requirement: Steel quantity
            formwork_area: Formwork area
            built_up_areas: Built-up area calculations
            location: City for rate adjustment
        """
        self.concrete_volumes = concrete_volumes
        self.steel_requirement = steel_requirement
        self.formwork_area = formwork_area
        self.built_up_areas = built_up_areas
        self.location = location
        
        # Rates (INR) - Feb 2026
        self.rates = {
            "concrete_m30_per_m3": 7500,
            "concrete_m50_per_m3": 9500,
            "steel_fe500_per_tonne": 65000,
            "formwork_per_m2": 350,
            "labor_percentage": 0.30,
            "flooring_per_m2": 800,
            "plastering_per_m2": 150,
            "painting_per_m2": 80,
            "false_ceiling_per_m2": 200,
            "doors_windows_per_m2": 1200,
            "mep_percentage": 0.18,  # 18% of subtotal
            "contingency_percentage": 0.10  # 10%
        }
    
    def calculate_structure_cost(self) -> Dict[str, Any]:
        """
        Calculate structural cost components
        """
        summary = self.concrete_volumes['summary']
        
        # Concrete cost (mixed grades)
        # Columns: M50, Rest: M30
        col_volume = summary['total_column_volume_m3']
        other_volume = (summary['total_concrete_volume_m3'] - col_volume)
        
        concrete_cost_columns = col_volume * self.rates['concrete_m50_per_m3']
        concrete_cost_others = other_volume * self.rates['concrete_m30_per_m3']
        total_concrete_cost = concrete_cost_columns + concrete_cost_others
        
        # Steel cost
        steel_tonnes = self.steel_requirement['with_wastage_tonnes']
        steel_cost = steel_tonnes * self.rates['steel_fe500_per_tonne']
        
        # Formwork cost
        formwork_area = self.formwork_area['actual_formwork_required_m2']
        formwork_cost = formwork_area * self.rates['formwork_per_m2']
        
        # Material subtotal
        material_subtotal = total_concrete_cost + steel_cost + formwork_cost
        
        # Labor cost (30% of material)
        labor_cost = material_subtotal * self.rates['labor_percentage']
        
        # Total structure cost
        total_structure_cost = material_subtotal + labor_cost
        
        return {
            "concrete_cost_inr": {
                "columns_m50": round(concrete_cost_columns, 2),
                "others_m30": round(concrete_cost_others, 2),
                "total": round(total_concrete_cost, 2)
            },
            "steel_cost_inr": round(steel_cost, 2),
            "formwork_cost_inr": round(formwork_cost, 2),
            "material_subtotal_inr": round(material_subtotal, 2),
            "labor_cost_inr": round(labor_cost, 2),
            "total_structure_cost_inr": round(total_structure_cost, 2),
            "cost_breakdown_percentage": {
                "concrete": f"{(total_concrete_cost/total_structure_cost*100):.1f}%",
                "steel": f"{(steel_cost/total_structure_cost*100):.1f}%",
                "formwork": f"{(formwork_cost/total_structure_cost*100):.1f}%",
                "labor": f"{(labor_cost/total_structure_cost*100):.1f}%"
            }
        }
    
    def calculate_finishing_cost(self) -> Dict[str, Any]:
        """
        Calculate finishing cost components
        """
        # Use total built-up area for finishing
        total_area = self.built_up_areas['total_gross_floor_area_m2']
        
        # Flooring (all floors)
        flooring_cost = total_area * self.rates['flooring_per_m2']
        
        # Plastering (walls - assume 25% of floor area as wall area)
        wall_area = total_area * 0.25
        plastering_cost = wall_area * self.rates['plastering_per_m2']
        
        # Painting (walls + ceiling - 30% of floor area)
        painting_area = total_area * 0.30
        painting_cost = painting_area * self.rates['painting_per_m2']
        
        # False ceiling (80% of floor area)
        ceiling_area = total_area * 0.80
        ceiling_cost = ceiling_area * self.rates['false_ceiling_per_m2']
        
        # Doors/Windows (15% of floor area equivalent)
        door_window_area = total_area * 0.15
        door_window_cost = door_window_area * self.rates['doors_windows_per_m2']
        
        # Total finishing cost
        total_finishing_cost = (
            flooring_cost +
            plastering_cost +
            painting_cost +
            ceiling_cost +
            door_window_cost
        )
        
        return {
            "flooring_cost_inr": round(flooring_cost, 2),
            "plastering_cost_inr": round(plastering_cost, 2),
            "painting_cost_inr": round(painting_cost, 2),
            "false_ceiling_cost_inr": round(ceiling_cost, 2),
            "doors_windows_cost_inr": round(door_window_cost, 2),
            "total_finishing_cost_inr": round(total_finishing_cost, 2),
            "cost_breakdown_percentage": {
                "flooring": f"{(flooring_cost/total_finishing_cost*100):.1f}%",
                "plastering": f"{(plastering_cost/total_finishing_cost*100):.1f}%",
                "painting": f"{(painting_cost/total_finishing_cost*100):.1f}%",
                "ceiling": f"{(ceiling_cost/total_finishing_cost*100):.1f}%",
                "doors_windows": f"{(door_window_cost/total_finishing_cost*100):.1f}%"
            }
        }
    
    def calculate_total_cost(self) -> Dict[str, Any]:
        """
        Calculate complete project cost
        """
        structure_cost_data = self.calculate_structure_cost()
        finishing_cost_data = self.calculate_finishing_cost()
        
        structure_cost = structure_cost_data['total_structure_cost_inr']
        finishing_cost = finishing_cost_data['total_finishing_cost_inr']
        
        # Subtotal
        subtotal = structure_cost + finishing_cost
        
        # MEP cost (18% of subtotal)
        mep_cost = subtotal * self.rates['mep_percentage']
        
        # Subtotal with MEP
        subtotal_with_mep = subtotal + mep_cost
        
        # Contingency (10%)
        contingency = subtotal_with_mep * self.rates['contingency_percentage']
        
        # Grand total
        grand_total = subtotal_with_mep + contingency
        
        # Cost per square meter
        total_area = self.built_up_areas['total_gross_floor_area_m2']
        cost_per_m2 = grand_total / total_area if total_area > 0 else 0
        
        return {
            "structure_cost": structure_cost_data,
            "finishing_cost": finishing_cost_data,
            "mep_cost_inr": round(mep_cost, 2),
            "contingency_inr": round(contingency, 2),
            "project_cost_summary": {
                "structure_cost_inr": round(structure_cost, 2),
                "finishing_cost_inr": round(finishing_cost, 2),
                "mep_cost_inr": round(mep_cost, 2),
                "subtotal_inr": round(subtotal_with_mep, 2),
                "contingency_inr": round(contingency, 2),
                "grand_total_inr": round(grand_total, 2),
                "grand_total_million_inr": round(grand_total / 1000000, 2),
                "cost_per_m2_inr": round(cost_per_m2, 2)
            },
            "percentage_distribution": {
                "structure": f"{(structure_cost/grand_total*100):.1f}%",
                "finishing": f"{(finishing_cost/grand_total*100):.1f}%",
                "mep": f"{(mep_cost/grand_total*100):.1f}%",
                "contingency": f"{(contingency/grand_total*100):.1f}%"
            },
            "benchmarks": {
                "typical_structure_percentage": "55-60%",
                "typical_finishing_percentage": "25-30%",
                "typical_mep_percentage": "15-20%",
                "actual_structure": f"{(structure_cost/grand_total*100):.1f}%",
                "actual_finishing": f"{(finishing_cost/grand_total*100):.1f}%",
                "actual_mep": f"{(mep_cost/grand_total*100):.1f}%"
            }
        }


class CostDriverAnalysis:
    """
    Identify major cost drivers and optimization opportunities
    """
    
    def __init__(self, quantity_data: Dict, cost_data: Dict):
        """
        Args:
            quantity_data: All quantity calculations
            cost_data: Cost breakdown
        """
        self.quantity_data = quantity_data
        self.cost_data = cost_data
    
    def identify_cost_drivers(self) -> Dict[str, Any]:
        """
        Analyze and rank cost drivers
        """
        cost_summary = self.cost_data['project_cost_summary']
        structure_cost = self.cost_data['structure_cost']
        
        # Extract individual cost components
        concrete_cost = structure_cost['concrete_cost_inr']['total']
        steel_cost = structure_cost['steel_cost_inr']
        formwork_cost = structure_cost['formwork_cost_inr']
        labor_cost = structure_cost['labor_cost_inr']
        finishing_cost = cost_summary['finishing_cost_inr']
        mep_cost = cost_summary['mep_cost_inr']
        
        grand_total = cost_summary['grand_total_inr']
        
        # Rank cost drivers
        cost_drivers = [
            {
                "component": "Concrete",
                "cost_inr": concrete_cost,
                "percentage": round(concrete_cost / grand_total * 100, 1),
                "impact": "CRITICAL"
            },
            {
                "component": "Steel Reinforcement",
                "cost_inr": steel_cost,
                "percentage": round(steel_cost / grand_total * 100, 1),
                "impact": "CRITICAL"
            },
            {
                "component": "Finishing",
                "cost_inr": finishing_cost,
                "percentage": round(finishing_cost / grand_total * 100, 1),
                "impact": "HIGH"
            },
            {
                "component": "MEP Systems",
                "cost_inr": mep_cost,
                "percentage": round(mep_cost / grand_total * 100, 1),
                "impact": "HIGH"
            },
            {
                "component": "Labor",
                "cost_inr": labor_cost,
                "percentage": round(labor_cost / grand_total * 100, 1),
                "impact": "MEDIUM"
            },
            {
                "component": "Formwork",
                "cost_inr": formwork_cost,
                "percentage": round(formwork_cost / grand_total * 100, 1),
                "impact": "MEDIUM"
            }
        ]
        
        # Sort by percentage
        cost_drivers_sorted = sorted(cost_drivers, key=lambda x: x['percentage'], reverse=True)
        
        return {
            "ranked_cost_drivers": cost_drivers_sorted,
            "top_3_drivers": {
                "driver_1": cost_drivers_sorted[0],
                "driver_2": cost_drivers_sorted[1],
                "driver_3": cost_drivers_sorted[2],
                "combined_percentage": sum([d['percentage'] for d in cost_drivers_sorted[:3]])
            },
            "optimization_focus": "Top 3 drivers account for majority of costs"
        }
    
    def suggest_optimizations(self) -> Dict[str, Any]:
        """
        Suggest optimization strategies for material efficiency
        """
        optimizations = [
            {
                "category": "Concrete Optimization",
                "strategies": [
                    {
                        "strategy": "Use fly ash replacement (30%)",
                        "savings_percentage": "15-20%",
                        "impact": "₹ saving on concrete cost",
                        "implementation": "Replace 30% cement with GGBS/fly ash",
                        "payback": "Immediate",
                        "sustainability": "Reduces CO2 by 30%"
                    },
                    {
                        "strategy": "Optimize slab thickness",
                        "savings_percentage": "10-15%",
                        "impact": "Reduce concrete volume by 10%",
                        "implementation": "Use post-tensioning for longer spans",
                        "payback": "3-6 months",
                        "sustainability": "Lower embodied carbon"
                    },
                    {
                        "strategy": "Use high-strength concrete selectively",
                        "savings_percentage": "8-12%",
                        "impact": "Reduce column sizes",
                        "implementation": "M60 in lower floors only",
                        "payback": "Immediate (area gained)",
                        "sustainability": "Less material, smaller footprint"
                    }
                ],
                "potential_savings_inr": round(self.cost_data['structure_cost']['concrete_cost_inr']['total'] * 0.15, 2),
                "priority": "CRITICAL"
            },
            {
                "category": "Steel Optimization",
                "strategies": [
                    {
                        "strategy": "Use Fe 550 in columns",
                        "savings_percentage": "12-15%",
                        "impact": "18% less steel by weight",
                        "implementation": "Switch to higher grade",
                        "payback": "Immediate",
                        "sustainability": "Lower steel consumption"
                    },
                    {
                        "strategy": "Optimize reinforcement detailing",
                        "savings_percentage": "8-10%",
                        "impact": "Reduce wastage and laps",
                        "implementation": "Bar bending schedule optimization",
                        "payback": "Immediate",
                        "sustainability": "Less waste"
                    },
                    {
                        "strategy": "Use welded wire mesh in slabs",
                        "savings_percentage": "5-8%",
                        "impact": "Faster installation, less wastage",
                        "implementation": "Replace conventional bars",
                        "payback": "1-2 months (labor savings)",
                        "sustainability": "Prefabricated, less site waste"
                    }
                ],
                "potential_savings_inr": round(self.cost_data['structure_cost']['steel_cost_inr'] * 0.12, 2),
                "priority": "CRITICAL"
            },
            {
                "category": "Formwork Optimization",
                "strategies": [
                    {
                        "strategy": "Aluminum formwork system",
                        "savings_percentage": "20-25%",
                        "impact": "80+ reuses vs 6-8 for timber",
                        "implementation": "Use modern formwork",
                        "payback": "4-6 floors",
                        "sustainability": "Reusability"
                    },
                    {
                        "strategy": "Standardize member sizes",
                        "savings_percentage": "10-15%",
                        "impact": "Maximize formwork reuse",
                        "implementation": "Use 3-4 column sizes only",
                        "payback": "Immediate",
                        "sustainability": "Less fabrication"
                    },
                    {
                        "strategy": "Jump formwork for core",
                        "savings_percentage": "15-20%",
                        "impact": "Faster construction",
                        "implementation": "Self-climbing system",
                        "payback": "3-4 floors",
                        "sustainability": "Safer, faster"
                    }
                ],
                "potential_savings_inr": round(self.cost_data['structure_cost']['formwork_cost_inr'] * 0.20, 2),
                "priority": "HIGH"
            },
            {
                "category": "Design Optimization",
                "strategies": [
                    {
                        "strategy": "Optimize grid spacing",
                        "savings_percentage": "8-12%",
                        "impact": "Reduce beam/column count",
                        "implementation": "7.5-9m spans for commercial",
                        "payback": "Design stage (no extra cost)",
                        "sustainability": "Less material overall"
                    },
                    {
                        "strategy": "Use flat slab system",
                        "savings_percentage": "10-15%",
                        "impact": "Eliminate beams, reduce height",
                        "implementation": "Flat slab with drop panels",
                        "payback": "Immediate (area gained)",
                        "sustainability": "Faster construction"
                    },
                    {
                        "strategy": "Precast elements",
                        "savings_percentage": "15-20%",
                        "impact": "Reduce site labor, faster",
                        "implementation": "Precast stairs, facades",
                        "payback": "5-6 months",
                        "sustainability": "Factory quality control"
                    }
                ],
                "potential_savings_inr": round(self.cost_data['project_cost_summary']['grand_total_inr'] * 0.10, 2),
                "priority": "HIGH"
            },
            {
                "category": "Construction Methodology",
                "strategies": [
                    {
                        "strategy": "Early strength concrete",
                        "savings_percentage": "Time savings",
                        "impact": "Formwork removal in 3 days vs 7",
                        "implementation": "Accelerators/admixtures",
                        "payback": "1-2 months (faster cycle)",
                        "sustainability": "Faster construction"
                    },
                    {
                        "strategy": "Ready-mix concrete",
                        "savings_percentage": "Quality + speed",
                        "impact": "Consistent quality, no site batching",
                        "implementation": "Use RMC for all concrete",
                        "payback": "Immediate",
                        "sustainability": "Better quality control"
                    },
                    {
                        "strategy": "Prefabricated rebar",
                        "savings_percentage": "8-10%",
                        "impact": "Reduce site labor and wastage",
                        "implementation": "Factory-cut and bent",
                        "payback": "Immediate",
                        "sustainability": "Less site waste"
                    }
                ],
                "potential_savings_inr": round(self.cost_data['structure_cost']['labor_cost_inr'] * 0.15, 2),
                "priority": "MEDIUM"
            }
        ]
        
        # Calculate total optimization potential
        total_optimization_potential = sum([opt['potential_savings_inr'] for opt in optimizations])
        grand_total = self.cost_data['project_cost_summary']['grand_total_inr']
        
        return {
            "optimization_strategies": optimizations,
            "summary": {
                "total_optimization_potential_inr": round(total_optimization_potential, 2),
                "total_optimization_potential_million_inr": round(total_optimization_potential / 1000000, 2),
                "percentage_of_project_cost": round(total_optimization_potential / grand_total * 100, 1),
                "implementation_priority": "Focus on Concrete and Steel (70% of savings)",
                "quick_wins": [
                    "Fly ash replacement (immediate, 15-20% concrete savings)",
                    "Fe 550 steel in columns (immediate, 12-15% steel savings)",
                    "Aluminum formwork (payback in 4-6 floors)"
                ],
                "strategic_initiatives": [
                    "Flat slab system (10-15% overall savings)",
                    "Precast elements (15-20% labor + time savings)",
                    "Optimize grid to 7.5-9m spans (8-12% savings)"
                ]
            }
        }


def run_quantity_cost_estimation(
    plot_length: float = 50.0,
    plot_width: float = 30.0,
    num_floors: int = 10,
    building_type: str = "Commercial",
    location: str = "Mumbai",
    structural_system: Dict = None
) -> Dict[str, Any]:
    """
    Run complete quantity and cost estimation
    
    Args:
        plot_length: Plot length in meters
        plot_width: Plot width in meters
        num_floors: Number of floors
        building_type: Building type
        location: Location for rate adjustment
        structural_system: Structural system from previous analysis
    
    Returns:
        Complete quantity and cost report
    """
    print("\n" + "="*80)
    print("STRUCTURAL QUANTITY ESTIMATION & COST ANALYSIS")
    print("="*80)
    
    # Default structural system if not provided
    if structural_system is None:
        structural_system = {
            'grid': {
                'num_bays_x': 7,
                'num_bays_y': 4,
                'total_columns': 40
            },
            'columns': [{'floor': i, 'size_m': 0.7 - i*0.04} for i in range(num_floors)],
            'beams': {'width_m': 0.25, 'depth_m': 0.30},
            'slab': {'thickness_m': 0.30},
            'lateral_system': 'Dual System (Frame + Shear Walls)'
        }
    
    # 1. Built-up Area Calculation
    print("\n[1/6] Calculating built-up areas...")
    area_calc = BuiltUpAreaCalculation(
        plot_length, plot_width, num_floors, building_type,
        structural_system['grid']
    )
    built_up_areas = area_calc.calculate_areas()
    print(f"   └─ Gross Floor Area: {built_up_areas['total_gross_floor_area_m2']:,.0f} m²")
    print(f"   └─ Carpet Area: {built_up_areas['total_carpet_area_m2']:,.0f} m²")
    print(f"   └─ Saleable Area: {built_up_areas['total_saleable_area_m2']:,.0f} m²")
    
    # 2. Concrete Volume Estimation
    print("\n[2/6] Calculating concrete volumes...")
    concrete_calc = ConcreteVolumeEstimation(
        plot_length, plot_width, num_floors,
        structural_system['columns'],
        structural_system['beams'],
        structural_system['slab']['thickness_m'],
        structural_system['lateral_system']
    )
    concrete_volumes = concrete_calc.calculate_total_concrete()
    total_concrete = concrete_volumes['summary']['total_with_wastage_m3']
    print(f"   └─ Total Concrete: {total_concrete:,.0f} m³")
    print(f"   └─ Columns: {concrete_volumes['summary']['total_column_volume_m3']:,.0f} m³")
    print(f"   └─ Slabs: {concrete_volumes['summary']['total_slab_volume_m3']:,.0f} m³")
    
    # 3. Steel Reinforcement Estimation
    print("\n[3/6] Calculating steel reinforcement...")
    steel_calc = SteelReinforcementEstimation(concrete_volumes, "Fe 500")
    steel_requirement = steel_calc.calculate_steel_requirement()
    total_steel = steel_requirement['with_wastage_tonnes']
    print(f"   └─ Total Steel: {total_steel:,.0f} tonnes")
    print(f"   └─ Steel Intensity: {total_steel*1000/total_concrete:.0f} kg/m³ concrete")
    
    # 4. Formwork Area Estimation
    print("\n[4/6] Calculating formwork areas...")
    formwork_calc = FormworkAreaEstimation(concrete_volumes, num_floors)
    formwork_area = formwork_calc.calculate_formwork_area()
    total_formwork = formwork_area['actual_formwork_required_m2']
    print(f"   └─ Total Formwork: {total_formwork:,.0f} m²")
    print(f"   └─ Formwork Intensity: {formwork_area['total_formwork_basic_m2']/total_concrete:.1f} m²/m³")
    
    # 5. Cost Estimation
    print("\n[5/6] Calculating project costs...")
    cost_calc = CostEstimation(
        concrete_volumes, steel_requirement, formwork_area,
        built_up_areas, location
    )
    cost_data = cost_calc.calculate_total_cost()
    grand_total = cost_data['project_cost_summary']['grand_total_million_inr']
    cost_per_m2 = cost_data['project_cost_summary']['cost_per_m2_inr']
    print(f"   └─ Total Project Cost: ₹{grand_total:.2f} Million")
    print(f"   └─ Cost per m²: ₹{cost_per_m2:,.0f}/m²")
    
    # 6. Cost Driver Analysis
    print("\n[6/6] Analyzing cost drivers and optimizations...")
    driver_analysis = CostDriverAnalysis(
        {
            'areas': built_up_areas,
            'concrete': concrete_volumes,
            'steel': steel_requirement,
            'formwork': formwork_area
        },
        cost_data
    )
    cost_drivers = driver_analysis.identify_cost_drivers()
    optimizations = driver_analysis.suggest_optimizations()
    optimization_potential = optimizations['summary']['total_optimization_potential_million_inr']
    print(f"   └─ Top Cost Driver: {cost_drivers['top_3_drivers']['driver_1']['component']}")
    print(f"   └─ Optimization Potential: ₹{optimization_potential:.2f} Million")
    
    # Compile complete report
    complete_report = {
        "project_parameters": {
            "plot_length_m": plot_length,
            "plot_width_m": plot_width,
            "num_floors": num_floors,
            "building_type": building_type,
            "location": location,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "1_built_up_areas": built_up_areas,
        "2_concrete_volumes": concrete_volumes,
        "3_steel_requirement": steel_requirement,
        "4_formwork_area": formwork_area,
        "5_cost_estimation": cost_data,
        "6_cost_drivers": cost_drivers,
        "7_optimization_strategies": optimizations
    }
    
    # Print executive summary
    print("\n" + "="*80)
    print("EXECUTIVE SUMMARY")
    print("="*80)
    print(f"\nPROJECT: {building_type} Building ({num_floors} floors)")
    print(f"LOCATION: {location}")
    print(f"PLOT SIZE: {plot_length}m × {plot_width}m")
    print(f"\nAREAS:")
    print(f"  • Gross Floor Area:     {built_up_areas['total_gross_floor_area_m2']:>12,.0f} m²")
    print(f"  • Carpet Area:          {built_up_areas['total_carpet_area_m2']:>12,.0f} m²")
    print(f"  • Saleable Area:        {built_up_areas['total_saleable_area_m2']:>12,.0f} m²")
    print(f"\nQUANTITIES:")
    print(f"  • Total Concrete:       {total_concrete:>12,.0f} m³")
    print(f"  • Total Steel:          {total_steel:>12,.0f} tonnes")
    print(f"  • Total Formwork:       {total_formwork:>12,.0f} m²")
    print(f"\nCOSTS:")
    print(f"  • Structure Cost:       ₹{cost_data['project_cost_summary']['structure_cost_inr']/1000000:>11.2f} Million")
    print(f"  • Finishing Cost:       ₹{cost_data['project_cost_summary']['finishing_cost_inr']/1000000:>11.2f} Million")
    print(f"  • MEP Cost:             ₹{cost_data['project_cost_summary']['mep_cost_inr']/1000000:>11.2f} Million")
    print(f"  • TOTAL COST:           ₹{grand_total:>11.2f} Million")
    print(f"  • Cost per m²:          ₹{cost_per_m2:>11,.0f}/m²")
    print(f"\nOPTIMIZATION:")
    print(f"  • Potential Savings:    ₹{optimization_potential:>11.2f} Million ({optimization_potential/grand_total*100:.0f}% of total)")
    print(f"  • Top 3 Cost Drivers:   {cost_drivers['top_3_drivers']['combined_percentage']:.0f}% of total cost")
    print("="*80)
    
    return complete_report


# Main execution
if __name__ == "__main__":
    # Run with default parameters
    report = run_quantity_cost_estimation()
    
    # Save report to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quantity_cost_estimation_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Complete report saved to: {filename}")
    print(f"✓ File size: {len(json.dumps(report, indent=2))/1024:.1f} KB")
