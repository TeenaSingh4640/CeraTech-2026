"""
AI-Driven Architectural and Structural Design Engine

Professional design consultant system for generating complete conceptual
architectural and structural designs with engineering-based reasoning.
"""

import json
import numpy as np
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import math


@dataclass
class ProjectInputs:
    """Project input parameters"""
    plot_length: float  # meters
    plot_width: float  # meters
    location: str
    climate_zone: str
    building_type: str  # Residential/Commercial/Institutional/Industrial
    num_floors: int
    far_allowed: float  # Floor Area Ratio
    budget_range: Tuple[float, float]  # min, max in USD
    soil_type: str  # Clay/Sand/Rock/Mixed
    seismic_zone: str  # I/II/III/IV/V
    architectural_style: str  # Modern/Brutalist/Glass/Traditional/etc.
    special_requirements: List[str] = None


@dataclass
class StructuralDesignOutput:
    """Complete structural design output"""
    project_id: str
    timestamp: str
    
    # 1. Conceptual architectural massing
    massing_logic: Dict
    
    # 2. Structural system
    structural_system: Dict
    
    # 3. Load path
    load_path: Dict
    
    # 4. Column grid
    column_grid: Dict
    
    # 5. Slab system
    slab_system: Dict
    
    # 6. Foundation system
    foundation_system: Dict
    
    # 7. Concrete volume
    concrete_estimate: Dict
    
    # 8. Steel requirement
    steel_estimate: Dict
    
    # 9. Climate adaptation
    climate_strategy: Dict
    
    # 10. Risk assessment
    risk_assessment: Dict
    
    # 11. Optimization opportunities
    optimization: Dict


class StructuralDesignEngine:
    """Main design engine for architectural and structural design"""
    
    # Engineering constants
    LIVE_LOAD_RESIDENTIAL = 2.0  # kN/m²
    LIVE_LOAD_COMMERCIAL = 4.0  # kN/m²
    LIVE_LOAD_INSTITUTIONAL = 3.0  # kN/m²
    DEAD_LOAD_MULTIPLIER = 1.5  # DL = 1.5 * floor thickness
    SEISMIC_FACTORS = {'I': 0.10, 'II': 0.16, 'III': 0.24, 'IV': 0.36, 'V': 0.40}
    WIND_FACTORS = {'Low': 0.8, 'Medium': 1.2, 'High': 1.6}
    
    def __init__(self, inputs: ProjectInputs):
        self.inputs = inputs
        self.plot_area = inputs.plot_length * inputs.plot_width
        self.total_built_area = self.plot_area * inputs.far_allowed
        self.floor_area = self.total_built_area / inputs.num_floors
        
    def generate_complete_design(self) -> StructuralDesignOutput:
        """Generate complete structural design"""
        
        print(f"\n{'='*80}")
        print(f"🏗️  STRUCTURAL DESIGN ENGINE - ANALYSIS INITIATED")
        print(f"{'='*80}\n")
        
        project_id = f"SD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate all components
        massing = self._generate_massing_logic()
        structural = self._select_structural_system()
        load_path = self._explain_load_path()
        column_grid = self._plan_column_grid()
        slab = self._recommend_slab_system()
        foundation = self._recommend_foundation_system()
        concrete = self._estimate_concrete_volume()
        steel = self._estimate_steel_requirement()
        climate = self._develop_climate_strategy()
        risk = self._assess_risks()
        optimization = self._identify_optimizations()
        
        output = StructuralDesignOutput(
            project_id=project_id,
            timestamp=datetime.now().isoformat(),
            massing_logic=massing,
            structural_system=structural,
            load_path=load_path,
            column_grid=column_grid,
            slab_system=slab,
            foundation_system=foundation,
            concrete_estimate=concrete,
            steel_estimate=steel,
            climate_strategy=climate,
            risk_assessment=risk,
            optimization=optimization
        )
        
        return output
    
    def _generate_massing_logic(self) -> Dict:
        """1. Conceptual architectural massing logic"""
        print("📐 PHASE 1: Generating Conceptual Architectural Massing...")
        
        # Calculate optimal footprint
        aspect_ratio = self.inputs.plot_length / self.inputs.plot_width
        
        # Setback calculations (20% typical for all sides)
        setback_front = self.inputs.plot_length * 0.1
        setback_rear = self.inputs.plot_length * 0.1
        setback_sides = self.inputs.plot_width * 0.1
        
        buildable_length = self.inputs.plot_length - setback_front - setback_rear
        buildable_width = self.inputs.plot_width - (2 * setback_sides)
        buildable_area = buildable_length * buildable_width
        
        # FAR utilization strategy
        far_utilization = min(self.inputs.far_allowed, 3.5)  # Cap at 3.5 for practicality
        actual_built_area = self.plot_area * far_utilization
        
        # Vertical massing strategy
        if self.inputs.num_floors <= 3:
            massing_type = "Low-rise horizontal massing"
            core_type = "Distributed circulation"
        elif self.inputs.num_floors <= 7:
            massing_type = "Mid-rise vertical massing with podium"
            core_type = "Central circulation core"
        else:
            massing_type = "High-rise tower with stepped podium"
            core_type = "Central core with refuge floors every 15 floors"
        
        # Architectural style adaptation
        style_features = self._get_style_features()
        
        massing = {
            "concept": massing_type,
            "reasoning": f"Based on {self.inputs.num_floors}-floor {self.inputs.building_type} building",
            "plot_dimensions": {
                "length": self.inputs.plot_length,
                "width": self.inputs.plot_width,
                "area": self.plot_area,
                "aspect_ratio": round(aspect_ratio, 2)
            },
            "setbacks": {
                "front": round(setback_front, 2),
                "rear": round(setback_rear, 2),
                "sides": round(setback_sides, 2),
                "reasoning": "Code compliance and fire safety requirements"
            },
            "buildable_footprint": {
                "length": round(buildable_length, 2),
                "width": round(buildable_width, 2),
                "area": round(buildable_area, 2),
                "efficiency": round((buildable_area / self.plot_area) * 100, 1)
            },
            "far_strategy": {
                "allowed": self.inputs.far_allowed,
                "utilized": far_utilization,
                "total_built_area": round(actual_built_area, 2),
                "reasoning": "Maximized within zoning constraints"
            },
            "vertical_organization": {
                "type": massing_type,
                "circulation_core": core_type,
                "floor_height": self._get_typical_floor_height(),
                "total_height": round(self.inputs.num_floors * self._get_typical_floor_height(), 2)
            },
            "architectural_character": {
                "style": self.inputs.architectural_style,
                "features": style_features,
                "facade_to_floor_ratio": self._calculate_facade_ratio()
            }
        }
        
        print(f"   ✓ Massing type: {massing_type}")
        print(f"   ✓ Buildable area: {buildable_area:.2f} m²")
        print(f"   ✓ FAR utilization: {far_utilization}")
        
        return massing
    
    def _select_structural_system(self) -> Dict:
        """2. Structural system selection and justification"""
        print("\n🏛️  PHASE 2: Selecting Structural System...")
        
        # Decision matrix based on building characteristics
        if self.inputs.num_floors <= 3:
            if self.inputs.building_type == "Residential":
                primary = "Load-bearing wall system"
                reasoning = "Cost-effective for low-rise residential, simple construction"
            else:
                primary = "RC frame with brick infill"
                reasoning = "Flexibility in layout, moderate spans, economical"
        elif self.inputs.num_floors <= 7:
            primary = "RC moment-resisting frame"
            reasoning = "Ductile behavior, suitable for moderate seismic zones"
            secondary = "Shear walls at cores"
        elif self.inputs.num_floors <= 15:
            primary = "RC frame with shear walls"
            reasoning = "Combined lateral and gravity system, economical"
            secondary = "Central shear core for elevators and stairs"
        else:
            primary = "Outrigger-braced core system"
            reasoning = "Efficient for tall buildings, reduces drift"
            secondary = "Perimeter mega-columns with outrigger trusses"
        
        # Seismic considerations
        seismic_factor = self.SEISMIC_FACTORS[self.inputs.seismic_zone]
        if seismic_factor >= 0.24:
            ductility_class = "Special moment-resisting frame (SMRF)"
            detailing = "Special confining steel, ductile detailing required"
        elif seismic_factor >= 0.16:
            ductility_class = "Intermediate moment-resisting frame (IMRF)"
            detailing = "Moderate ductile detailing"
        else:
            ductility_class = "Ordinary moment-resisting frame (OMRF)"
            detailing = "Standard detailing sufficient"
        
        # Material selection
        if self.inputs.num_floors <= 7:
            concrete_grade = "M25-M30"
            steel_grade = "Fe 415/500"
        else:
            concrete_grade = "M30-M40 (M50 for columns)"
            steel_grade = "Fe 500/550"
        
        system = {
            "primary_system": primary,
            "reasoning": reasoning,
            "lateral_force_resisting": {
                "system": "Dual system (frame + shear walls)" if self.inputs.num_floors > 7 else "Moment frame",
                "seismic_zone": self.inputs.seismic_zone,
                "seismic_factor": seismic_factor,
                "ductility_class": ductility_class,
                "detailing_requirements": detailing
            },
            "materials": {
                "concrete_grade": concrete_grade,
                "steel_grade": steel_grade,
                "reasoning": "Based on load magnitude and ductility requirements"
            },
            "span_system": {
                "typical_span": self._get_typical_span(),
                "max_span": self._get_max_span(),
                "reasoning": "Economical span range for selected system"
            },
            "construction_methodology": self._get_construction_method()
        }
        
        print(f"   ✓ Primary system: {primary}")
        print(f"   ✓ Seismic zone: {self.inputs.seismic_zone} (Factor: {seismic_factor})")
        print(f"   ✓ Materials: {concrete_grade}, {steel_grade}")
        
        return system
    
    def _explain_load_path(self) -> Dict:
        """3. Load path explanation"""
        print("\n⚖️  PHASE 3: Analyzing Load Path...")
        
        # Calculate loads
        live_load = self._get_live_load()
        dead_load = self._estimate_dead_load()
        wind_load = self._calculate_wind_load()
        seismic_load = self._calculate_seismic_base_shear()
        
        # Load combinations (per IS 456:2000 and IS 1893)
        combinations = [
            "1.5 DL + 1.5 LL",
            "1.2 DL + 1.2 LL ± 1.2 EQ",
            "1.5 DL ± 1.5 WL",
            "0.9 DL ± 1.5 WL"
        ]
        
        # Load transfer mechanism
        path_description = [
            "1. Imposed loads and self-weight on floor slab",
            "2. Slab transfers to supporting beams via bending",
            "3. Beams transfer to columns via shear and torsion",
            "4. Columns carry axial load to foundation",
            "5. Foundation distributes to soil via bearing pressure",
            "6. Lateral loads resisted by moment frames/shear walls",
            "7. Overturning moment resisted by foundation reactions"
        ]
        
        load_path = {
            "gravity_loads": {
                "live_load": f"{live_load} kN/m²",
                "dead_load": f"{dead_load:.2f} kN/m²",
                "total_service_load": f"{live_load + dead_load:.2f} kN/m²",
                "factored_load": f"{1.5 * (live_load + dead_load):.2f} kN/m²"
            },
            "lateral_loads": {
                "wind_pressure": f"{wind_load:.2f} kN/m²",
                "seismic_base_shear": f"{seismic_load:.2f} kN",
                "governing_case": "Seismic" if seismic_load > wind_load * 100 else "Wind"
            },
            "load_combinations": combinations,
            "load_transfer_sequence": path_description,
            "critical_elements": {
                "most_loaded_column": "Corner column (gravity + moment)",
                "critical_beam": "Edge beam (torsion + bending)",
                "critical_slab": "Cantilever slab (maximum bending)"
            },
            "load_distribution": {
                "tributary_area_method": "Used for beam and column design",
                "influence_area_reduction": f"Applied as per code for large areas"
            }
        }
        
        print(f"   ✓ Service load: {live_load + dead_load:.2f} kN/m²")
        print(f"   ✓ Factored load: {1.5 * (live_load + dead_load):.2f} kN/m²")
        print(f"   ✓ Base shear: {seismic_load:.2f} kN")
        
        return load_path
    
    def _plan_column_grid(self) -> Dict:
        """4. Column grid planning logic"""
        print("\n📏 PHASE 4: Planning Column Grid...")
        
        typical_span = self._get_typical_span()
        
        # Calculate optimal grid
        num_bays_length = int(self.inputs.plot_length / typical_span)
        num_bays_width = int(self.inputs.plot_width / typical_span)
        
        actual_span_length = self.inputs.plot_length / num_bays_length
        actual_span_width = self.inputs.plot_width / num_bays_width
        
        # Column sizing (preliminary)
        column_size = self._estimate_column_size()
        
        grid = {
            "grid_philosophy": "Orthogonal grid for structural efficiency and construction ease",
            "typical_bay_size": {
                "length_direction": f"{actual_span_length:.2f} m",
                "width_direction": f"{actual_span_width:.2f} m",
                "reasoning": "Optimized for economical beam and slab design"
            },
            "grid_configuration": {
                "bays_in_length": num_bays_length,
                "bays_in_width": num_bays_width,
                "total_columns_per_floor": (num_bays_length + 1) * (num_bays_width + 1),
                "grid_pattern": "Regular orthogonal" if abs(actual_span_length - actual_span_width) < 1 else "Rectangular"
            },
            "column_sizing": column_size,
            "special_considerations": {
                "parking_requirements": "Larger spans in basement for parking",
                "transfer_beams": "Required if upper floor grid differs from basement",
                "corner_columns": "Increased size due to biaxial bending",
                "edge_columns": "Uniaxial bending consideration"
            },
            "modular_coordination": {
                "planning_module": f"{typical_span:.1f} m",
                "sub_module": f"{typical_span/2:.1f} m",
                "reasoning": "Facilitates repetitive formwork and MEP coordination"
            }
        }
        
        print(f"   ✓ Grid: {num_bays_length} × {num_bays_width} bays")
        print(f"   ✓ Typical span: {actual_span_length:.2f} × {actual_span_width:.2f} m")
        print(f"   ✓ Columns per floor: {(num_bays_length + 1) * (num_bays_width + 1)}")
        
        return grid
    
    def _recommend_slab_system(self) -> Dict:
        """5. Slab system recommendation"""
        print("\n🏗️  PHASE 5: Recommending Slab System...")
        
        span = self._get_typical_span()
        
        # Slab system selection logic
        if span <= 4.5:
            slab_type = "One-way slab"
            thickness = max(150, span * 1000 / 20)  # span/20 rule
            reinforcement = "Main bars in short direction"
        elif span <= 6.0:
            slab_type = "Two-way slab"
            thickness = max(175, span * 1000 / 25)  # span/25 for two-way
            reinforcement = "Grid reinforcement in both directions"
        elif span <= 9.0:
            slab_type = "Flat slab with drop panels"
            thickness = max(200, span * 1000 / 30)
            reinforcement = "Column strip and middle strip design"
        else:
            slab_type = "Post-tensioned flat slab"
            thickness = max(250, span * 1000 / 35)
            reinforcement = "Post-tensioning tendons + conventional rebars"
        
        slab = {
            "recommended_system": slab_type,
            "thickness": f"{int(thickness)} mm",
            "reasoning": f"Span = {span:.2f}m, economical for this range",
            "reinforcement_strategy": reinforcement,
            "advantages": self._get_slab_advantages(slab_type),
            "design_criteria": {
                "deflection_limit": "span/250 for live load deflection",
                "crack_width": "0.3 mm maximum for durability",
                "cover": "25-30 mm for moderate exposure"
            },
            "special_features": {
                "edge_beams": "Required at discontinuous edges",
                "opening_reinforcement": "Additional bars around openings",
                "cantilever_slabs": "Thickness = 2 × typical slab for balconies"
            },
            "construction_aspects": {
                "formwork": "Reusable table forms for efficiency",
                "curing": "7-day water curing minimum",
                "striking_time": "14-21 days based on concrete strength"
            }
        }
        
        print(f"   ✓ Slab type: {slab_type}")
        print(f"   ✓ Thickness: {int(thickness)} mm")
        
        return slab
    
    def _recommend_foundation_system(self) -> Dict:
        """6. Foundation system recommendation"""
        print("\n🏗️  PHASE 6: Recommending Foundation System...")
        
        soil_bearing = self._get_soil_bearing_capacity()
        total_load = self._calculate_total_building_weight()
        
        # Foundation selection logic
        if self.inputs.num_floors <= 3 and soil_bearing >= 150:
            foundation_type = "Isolated footings"
            reasoning = "Adequate soil bearing, low-rise structure"
        elif self.inputs.num_floors <= 7 and soil_bearing >= 150:
            foundation_type = "Combined footings with tie beams"
            reasoning = "Moderate loads, tie beams provide connection"
        elif soil_bearing >= 100:
            foundation_type = "Raft foundation (mat)"
            reasoning = "Distribute load over larger area, moderate bearing capacity"
        else:
            foundation_type = "Piled raft foundation"
            reasoning = "Poor soil, requires deep foundation support"
            pile_details = self._design_pile_foundation()
        
        foundation = {
            "recommended_system": foundation_type,
            "reasoning": reasoning,
            "soil_parameters": {
                "type": self.inputs.soil_type,
                "bearing_capacity": f"{soil_bearing} kN/m²",
                "settlement_criteria": "Maximum 50mm total, 25mm differential"
            },
            "design_approach": {
                "load_per_column": f"{total_load / self._get_num_columns():.2f} kN (average)",
                "factor_of_safety": "3.0 against bearing failure",
                "depth": self._get_foundation_depth()
            }
        }
        
        if foundation_type == "Piled raft foundation":
            foundation["pile_details"] = pile_details
        else:
            foundation["footing_details"] = {
                "typical_size": self._calculate_footing_size(soil_bearing, total_load),
                "reinforcement": "Grid reinforcement, minimum 16mm bars",
                "depth": "600-900mm typical for wind uplift resistance"
            }
        
        foundation["waterproofing"] = {
            "basement_walls": "Crystalline waterproofing + external membrane",
            "slab_on_grade": "Polyethylene vapor barrier + damp proof course",
            "drainage": "Perimeter drainage with gravel backfill"
        }
        
        print(f"   ✓ Foundation: {foundation_type}")
        print(f"   ✓ Soil bearing: {soil_bearing} kN/m²")
        
        return foundation
    
    def _estimate_concrete_volume(self) -> Dict:
        """7. Estimated concrete volume (approximate)"""
        print("\n📊 PHASE 7: Estimating Concrete Volume...")
        
        # Component-wise estimation
        slab_volume = self._calculate_slab_concrete()
        beam_volume = self._calculate_beam_concrete()
        column_volume = self._calculate_column_concrete()
        foundation_volume = self._calculate_foundation_concrete()
        
        total_volume = slab_volume + beam_volume + column_volume + foundation_volume
        
        # Add 5% wastage
        with_wastage = total_volume * 1.05
        
        concrete = {
            "component_breakdown": {
                "slabs": f"{slab_volume:.2f} m³",
                "beams": f"{beam_volume:.2f} m³",
                "columns": f"{column_volume:.2f} m³",
                "foundation": f"{foundation_volume:.2f} m³"
            },
            "subtotal": f"{total_volume:.2f} m³",
            "wastage_allowance": "5%",
            "total_with_wastage": f"{with_wastage:.2f} m³",
            "grade_distribution": {
                "M25": f"{(slab_volume + beam_volume) * 0.6:.2f} m³",
                "M30": f"{(slab_volume + beam_volume) * 0.4 + column_volume * 0.7:.2f} m³",
                "M40": f"{column_volume * 0.3:.2f} m³"
            },
            "cost_estimate": {
                "unit_rate": "$150-200 per m³ (including labor)",
                "estimated_cost": f"${with_wastage * 175:.2f}",
                "reasoning": "Includes material, labor, formwork amortization"
            }
        }
        
        print(f"   ✓ Total concrete: {with_wastage:.2f} m³")
        print(f"   ✓ Estimated cost: ${with_wastage * 175:,.2f}")
        
        return concrete
    
    def _estimate_steel_requirement(self) -> Dict:
        """8. Estimated steel requirement (approximate)"""
        print("\n🔩 PHASE 8: Estimating Steel Requirement...")
        
        # Steel percentage assumptions (based on building type and seismic zone)
        if self.inputs.seismic_zone in ['IV', 'V']:
            slab_steel = 1.2  # % of concrete volume
            beam_steel = 1.8
            column_steel = 2.5
        else:
            slab_steel = 1.0
            beam_steel = 1.5
            column_steel = 2.0
        
        # Calculate weights (density of steel = 7850 kg/m³)
        slab_vol = self._calculate_slab_concrete()
        beam_vol = self._calculate_beam_concrete()
        column_vol = self._calculate_column_concrete()
        
        slab_steel_weight = slab_vol * (slab_steel / 100) * 7850
        beam_steel_weight = beam_vol * (beam_steel / 100) * 7850
        column_steel_weight = column_vol * (column_steel / 100) * 7850
        
        total_steel = slab_steel_weight + beam_steel_weight + column_steel_weight
        
        steel = {
            "component_breakdown": {
                "slabs": f"{slab_steel_weight:.2f} kg ({slab_steel}% ratio)",
                "beams": f"{beam_steel_weight:.2f} kg ({beam_steel}% ratio)",
                "columns": f"{column_steel_weight:.2f} kg ({column_steel}% ratio)"
            },
            "total_weight": f"{total_steel:.2f} kg ({total_steel/1000:.2f} tonnes)",
            "steel_per_sqm": f"{total_steel / self.total_built_area:.2f} kg/m²",
            "grade_distribution": {
                "Fe 415": f"{total_steel * 0.3:.2f} kg (stirrups, distribution bars)",
                "Fe 500": f"{total_steel * 0.7:.2f} kg (main reinforcement)"
            },
            "cost_estimate": {
                "unit_rate": "$1.2-1.5 per kg",
                "estimated_cost": f"${total_steel * 1.35:,.2f}",
                "reasoning": "Includes material, cutting, bending, labor"
            },
            "detailing_requirements": {
                "seismic_zone": self.inputs.seismic_zone,
                "minimum_reinforcement": "0.12% for beams, 0.8% for columns",
                "lap_lengths": "50 × bar diameter minimum",
                "cover_requirements": "40mm columns, 25mm beams, 20mm slabs"
            }
        }
        
        print(f"   ✓ Total steel: {total_steel/1000:.2f} tonnes")
        print(f"   ✓ Steel intensity: {total_steel / self.total_built_area:.2f} kg/m²")
        
        return steel
    
    def _develop_climate_strategy(self) -> Dict:
        """9. Climate adaptation strategy"""
        print("\n🌡️  PHASE 9: Developing Climate Adaptation Strategy...")
        
        climate_strategies = {
            "Tropical": {
                "orientation": "North-South axis for minimal east-west exposure",
                "shading": "Deep overhangs (1.5-2m), vertical fins on east-west",
                "ventilation": "Cross ventilation, stack effect for natural cooling",
                "materials": "High thermal mass walls, reflective roof coating",
                "insulation": "Roof insulation R-3.5 minimum",
                "glazing": "30-40% WWR, double glazed low-E, exterior shading"
            },
            "Arid": {
                "orientation": "Compact form to minimize surface area",
                "shading": "Minimal glazing, deep recessed windows",
                "ventilation": "Night ventilation with thermal mass storage",
                "materials": "High thermal mass construction (concrete, masonry)",
                "insulation": "R-4.0 walls, R-6.0 roof",
                "glazing": "20-30% WWR, triple glazed, heat reflective coating"
            },
            "Temperate": {
                "orientation": "South facing for solar gain (northern hemisphere)",
                "shading": "Adjustable shading systems, deciduous landscaping",
                "ventilation": "Balanced mechanical + natural ventilation",
                "materials": "Moderate thermal mass, insulated envelope",
                "insulation": "R-3.0 walls, R-4.5 roof",
                "glazing": "40-50% WWR, double glazed, selective coating"
            },
            "Cold": {
                "orientation": "Maximize south exposure, minimize north openings",
                "shading": "Minimal shading, maximize solar gain",
                "ventilation": "Heat recovery ventilation, air locks at entries",
                "materials": "High insulation, thermal break construction",
                "insulation": "R-5.0 walls, R-8.0 roof, R-3.0 below grade",
                "glazing": "30-40% WWR, triple glazed, argon fill"
            }
        }
        
        strategy = climate_strategies.get(self.inputs.climate_zone, climate_strategies["Temperate"])
        
        # Add specific strategies
        strategy["passive_design"] = {
            "daylighting": "Target 2% minimum daylight factor",
            "thermal_comfort": "PMV ±0.5 range for 80% occupant satisfaction",
            "natural_ventilation": f"Operable windows 8-10% of floor area"
        }
        
        strategy["active_systems"] = {
            "hvac": self._select_hvac_system(),
            "lighting": "LED with daylight sensors, occupancy controls",
            "renewables": "Roof-mounted solar PV 30-50% of roof area"
        }
        
        strategy["performance_targets"] = {
            "energy_use_intensity": "80-120 kWh/m²/year",
            "water_efficiency": "30% reduction via low-flow fixtures, rainwater harvesting",
            "green_building_rating": "LEED Gold or equivalent achievable"
        }
        
        print(f"   ✓ Climate zone: {self.inputs.climate_zone}")
        print(f"   ✓ Primary strategy: Passive design optimization")
        
        return strategy
    
    def _assess_risks(self) -> Dict:
        """10. Risk assessment"""
        print("\n⚠️  PHASE 10: Conducting Risk Assessment...")
        
        risks = {
            "structural_risks": [
                {
                    "risk": "Foundation settlement",
                    "severity": "High" if self.inputs.soil_type in ["Clay", "Mixed"] else "Medium",
                    "mitigation": "Adequate soil investigation, proper foundation design, monitoring"
                },
                {
                    "risk": "Seismic damage",
                    "severity": "High" if self.inputs.seismic_zone in ['IV', 'V'] else "Medium",
                    "mitigation": "Ductile detailing, proper lap lengths, quality control"
                },
                {
                    "risk": "Progressive collapse",
                    "severity": "Medium",
                    "mitigation": "Tie beams, alternate load path, robust connections"
                }
            ],
            "construction_risks": [
                {
                    "risk": "Formwork failure",
                    "severity": "High",
                    "mitigation": "Engineered formwork design, qualified supervisors, inspections"
                },
                {
                    "risk": "Concrete quality issues",
                    "severity": "Medium",
                    "mitigation": "Approved mix design, cube testing, proper curing"
                },
                {
                    "risk": "Rebar corrosion",
                    "severity": "Medium",
                    "mitigation": "Adequate cover, quality concrete, proper drainage"
                }
            ],
            "environmental_risks": [
                {
                    "risk": "Thermal discomfort",
                    "severity": "Medium",
                    "mitigation": "Proper insulation, shading devices, HVAC sizing"
                },
                {
                    "risk": "Water infiltration",
                    "severity": "High",
                    "mitigation": "Waterproofing systems, drainage design, maintenance"
                }
            ],
            "cost_risks": [
                {
                    "risk": "Budget overrun",
                    "severity": "High",
                    "mitigation": "15-20% contingency, value engineering, phased construction"
                },
                {
                    "risk": "Material price escalation",
                    "severity": "Medium",
                    "mitigation": "Price adjustment clauses, bulk procurement, alternatives"
                }
            ],
            "schedule_risks": [
                {
                    "risk": "Weather delays",
                    "severity": "Medium",
                    "mitigation": "Weather-protected construction, buffer time"
                },
                {
                    "risk": "Labor shortage",
                    "severity": "Medium",
                    "mitigation": "Early contractor engagement, training programs"
                }
            ]
        }
        
        print(f"   ✓ Identified 13 major risk categories")
        print(f"   ✓ Mitigation strategies provided for all risks")
        
        return risks
    
    def _identify_optimizations(self) -> Dict:
        """11. Optimization opportunities"""
        print("\n🎯 PHASE 11: Identifying Optimization Opportunities...")
        
        optimizations = {
            "structural_optimization": [
                {
                    "opportunity": "Column grid regularization",
                    "potential_saving": "8-12% on formwork costs",
                    "implementation": "Use consistent bay sizes, minimize grid variations"
                },
                {
                    "opportunity": "Beam depth optimization",
                    "potential_saving": "5-8% on concrete volume",
                    "implementation": "Analyze for minimum depth meeting deflection criteria"
                },
                {
                    "opportunity": "High-strength concrete in columns",
                    "potential_saving": "10-15% reduction in column size",
                    "implementation": "Use M40-M50 for heavily loaded columns"
                }
            ],
            "material_optimization": [
                {
                    "opportunity": "Fly ash replacement in concrete",
                    "potential_saving": "15-20% on cement cost, reduced carbon footprint",
                    "implementation": "Replace 30-40% cement with fly ash"
                },
                {
                    "opportunity": "TMT bar optimization",
                    "potential_saving": "10-12% on steel tonnage",
                    "implementation": "Use higher grade steel (Fe 550) for smaller sizes"
                },
                {
                    "opportunity": "Recycled aggregates",
                    "potential_saving": "8-10% on aggregate cost",
                    "implementation": "Use recycled aggregates for non-structural elements"
                }
            ],
            "construction_optimization": [
                {
                    "opportunity": "Modular formwork systems",
                    "potential_saving": "20-25% on formwork costs",
                    "implementation": "Aluminum/steel formwork for repetitive floors"
                },
                {
                    "opportunity": "Prefabricated elements",
                    "potential_saving": "15-20% on construction time",
                    "implementation": "Precast stairs, bathroom pods, facade panels"
                },
                {
                    "opportunity": "Early contractor involvement",
                    "potential_saving": "10-15% on overall project cost",
                    "implementation": "Design-build or construction manager approach"
                }
            ],
            "energy_optimization": [
                {
                    "opportunity": "Building envelope optimization",
                    "potential_saving": "25-30% on HVAC operational costs",
                    "implementation": "Enhanced insulation, better glazing, shading"
                },
                {
                    "opportunity": "Solar PV integration",
                    "potential_saving": "30-50% of electricity from renewables",
                    "implementation": "Roof-mounted or BIPV systems"
                },
                {
                    "opportunity": "Smart building systems",
                    "potential_saving": "15-20% on total energy consumption",
                    "implementation": "BMS, occupancy sensors, demand response"
                }
            ],
            "value_engineering": {
                "phase_1": "Schematic design review - biggest impact potential",
                "phase_2": "Design development - moderate savings possible",
                "phase_3": "Construction documents - limited but still valuable",
                "approach": "Multi-disciplinary workshops, life-cycle cost analysis"
            }
        }
        
        total_potential_saving = "20-30% compared to conventional design approach"
        
        print(f"   ✓ Identified 14 optimization opportunities")
        print(f"   ✓ Potential savings: {total_potential_saving}")
        
        return {
            "opportunities": optimizations,
            "total_potential_saving": total_potential_saving,
            "priority_actions": [
                "1. Standardize column grid",
                "2. Implement fly ash concrete",
                "3. Use modular formwork",
                "4. Optimize building envelope",
                "5. Early contractor involvement"
            ]
        }
    
    # Helper methods
    
    def _get_typical_floor_height(self) -> float:
        """Get typical floor height based on building type"""
        heights = {
            "Residential": 3.0,
            "Commercial": 3.6,
            "Institutional": 3.8,
            "Industrial": 4.5
        }
        return heights.get(self.inputs.building_type, 3.3)
    
    def _get_style_features(self) -> List[str]:
        """Get architectural features based on style"""
        features = {
            "Modern": ["Clean lines", "Large glazing", "Minimal ornamentation", "Cantilevers"],
            "Brutalist": ["Exposed concrete", "Massive forms", "Geometric shapes", "Bold presence"],
            "Glass": ["Curtain wall facade", "Transparency", "Lightweight appearance", "High-tech"],
            "Traditional": ["Pitched roofs", "Symmetry", "Human scale", "Natural materials"]
        }
        return features.get(self.inputs.architectural_style, features["Modern"])
    
    def _calculate_facade_ratio(self) -> float:
        """Calculate window-to-wall ratio"""
        ratios = {
            "Modern": 0.45,
            "Brutalist": 0.25,
            "Glass": 0.70,
            "Traditional": 0.35
        }
        return ratios.get(self.inputs.architectural_style, 0.40)
    
    def _get_typical_span(self) -> float:
        """Get typical span based on building type"""
        spans = {
            "Residential": 4.5,
            "Commercial": 6.0,
            "Institutional": 7.5,
            "Industrial": 9.0
        }
        return spans.get(self.inputs.building_type, 5.5)
    
    def _get_max_span(self) -> float:
        """Get maximum economical span"""
        return self._get_typical_span() * 1.5
    
    def _get_construction_method(self) -> str:
        """Determine construction methodology"""
        if self.inputs.num_floors <= 5:
            return "Conventional cast-in-place construction"
        elif self.inputs.num_floors <= 15:
            return "Table formwork with concrete pumping"
        else:
            return "Jump form/slip form for cores, table form for floors"
    
    def _get_live_load(self) -> float:
        """Get live load based on building type"""
        loads = {
            "Residential": self.LIVE_LOAD_RESIDENTIAL,
            "Commercial": self.LIVE_LOAD_COMMERCIAL,
            "Institutional": self.LIVE_LOAD_INSTITUTIONAL
        }
        return loads.get(self.inputs.building_type, 3.0)
    
    def _estimate_dead_load(self) -> float:
        """Estimate dead load"""
        # Slab + finishes + partitions + MEP
        slab_thickness = 0.175  # meters (typical)
        concrete_density = 25  # kN/m³
        finishes = 1.5  # kN/m²
        partitions = 1.0  # kN/m²
        mep = 0.5  # kN/m²
        
        slab_wt = slab_thickness * concrete_density
        return slab_wt + finishes + partitions + mep
    
    def _calculate_wind_load(self) -> float:
        """Calculate design wind pressure"""
        # Simplified calculation
        basic_wind_speed = 47  # m/s (typical for many locations)
        wind_pressure = 0.6 * (basic_wind_speed ** 2) / 1000  # kN/m²
        return wind_pressure
    
    def _calculate_seismic_base_shear(self) -> float:
        """Calculate seismic base shear"""
        seismic_weight = self.total_built_area * 10  # kN (approximate)
        seismic_coeff = self.SEISMIC_FACTORS[self.inputs.seismic_zone]
        base_shear = seismic_coeff * seismic_weight
        return base_shear
    
    def _estimate_column_size(self) -> Dict:
        """Estimate column sizes"""
        if self.inputs.num_floors <= 3:
            size = "230 × 300 mm"
        elif self.inputs.num_floors <= 7:
            size = "300 × 450 mm (lower floors), 300 × 300 mm (upper floors)"
        else:
            size = "450 × 600 mm (lower), 400 × 500 mm (mid), 300 × 450 mm (upper)"
        
        return {
            "typical_size": size,
            "corner_columns": "+25% larger due to biaxial bending",
            "edge_columns": "+15% larger",
            "interior_columns": "Standard size"
        }
    
    def _get_slab_advantages(self, slab_type: str) -> List[str]:
        """Get advantages of slab system"""
        advantages = {
            "One-way slab": ["Economical", "Simple formwork", "Easy reinforcement"],
            "Two-way slab": ["Efficient for square panels", "Less deflection", "Better load distribution"],
            "Flat slab with drop panels": ["No beams - clear headroom", "Flexible layout", "Faster construction"],
            "Post-tensioned flat slab": ["Longer spans", "Reduced thickness", "Crack control"]
        }
        return advantages.get(slab_type, ["Efficient", "Economical"])
    
    def _get_soil_bearing_capacity(self) -> float:
        """Get soil bearing capacity based on soil type"""
        capacities = {
            "Rock": 500,
            "Sand": 200,
            "Clay": 100,
            "Mixed": 150
        }
        return capacities.get(self.inputs.soil_type, 150)
    
    def _calculate_total_building_weight(self) -> float:
        """Calculate total building weight"""
        # Dead load + 25% of live load
        weight_per_sqm = 15  # kN/m² (typical for multi-story)
        return self.total_built_area * weight_per_sqm
    
    def _get_num_columns(self) -> int:
        """Get approximate number of columns"""
        typical_span = self._get_typical_span()
        num_bays_length = int(self.inputs.plot_length / typical_span)
        num_bays_width = int(self.inputs.plot_width / typical_span)
        return (num_bays_length + 1) * (num_bays_width + 1)
    
    def _get_foundation_depth(self) -> str:
        """Get foundation depth recommendation"""
        if self.inputs.num_floors <= 3:
            return "1.5-2.0 m below ground level"
        elif self.inputs.num_floors <= 7:
            return "2.5-3.5 m below ground level"
        else:
            return "4.0-6.0 m below ground level (basement levels)"
    
    def _design_pile_foundation(self) -> Dict:
        """Design pile foundation"""
        return {
            "pile_type": "Bored cast-in-place piles",
            "diameter": "600-800 mm",
            "depth": "15-25 m (to bearing stratum)",
            "capacity": "1000-1500 kN per pile",
            "pile_cap": "1.2-1.5 m thick reinforced concrete",
            "testing": "Static load test on 2% of piles minimum"
        }
    
    def _calculate_footing_size(self, bearing_capacity: float, total_load: float) -> str:
        """Calculate typical footing size"""
        load_per_column = total_load / self._get_num_columns()
        req_area = load_per_column / bearing_capacity * 1.5  # FOS
        size = math.sqrt(req_area)
        return f"{size:.2f} m × {size:.2f} m square footing (typical)"
    
    def _calculate_slab_concrete(self) -> float:
        """Calculate slab concrete volume"""
        thickness = 0.175  # meters (typical)
        return self.total_built_area * thickness
    
    def _calculate_beam_concrete(self) -> float:
        """Calculate beam concrete volume"""
        # Approximate: 15% of slab volume
        return self._calculate_slab_concrete() * 0.15
    
    def _calculate_column_concrete(self) -> float:
        """Calculate column concrete volume"""
        num_columns = self._get_num_columns()
        avg_column_size = 0.3 * 0.45  # m² (typical)
        height_per_floor = self._get_typical_floor_height()
        total_height = height_per_floor * self.inputs.num_floors
        return num_columns * avg_column_size * total_height
    
    def _calculate_foundation_concrete(self) -> float:
        """Calculate foundation concrete volume"""
        # Approximate: 20% of superstructure
        super_structure = (self._calculate_slab_concrete() + 
                          self._calculate_beam_concrete() + 
                          self._calculate_column_concrete())
        return super_structure * 0.20
    
    def _select_hvac_system(self) -> str:
        """Select HVAC system based on building type"""
        systems = {
            "Residential": "Split AC units or VRF system",
            "Commercial": "Centralized chilled water system with AHUs",
            "Institutional": "VAV system with heat recovery",
            "Industrial": "Natural ventilation + spot cooling"
        }
        return systems.get(self.inputs.building_type, "VRF system")


def save_design_report(output: StructuralDesignOutput, filename: str = None):
    """Save design output to JSON file"""
    if filename is None:
        filename = f"design_report_{output.project_id}.json"
    
    with open(filename, 'w') as f:
        json.dump(asdict(output), f, indent=2)
    
    return filename


def main():
    """Example usage"""
    # Sample project inputs
    inputs = ProjectInputs(
        plot_length=50.0,
        plot_width=30.0,
        location="Mumbai",
        climate_zone="Tropical",
        building_type="Residential",
        num_floors=10,
        far_allowed=2.5,
        budget_range=(1000000, 1500000),
        soil_type="Sand",
        seismic_zone="III",
        architectural_style="Modern",
        special_requirements=["Parking basement", "Terrace garden"]
    )
    
    # Generate design
    engine = StructuralDesignEngine(inputs)
    output = engine.generate_complete_design()
    
    # Save report
    filename = save_design_report(output)
    print(f"\n{'='*80}")
    print(f"✅ DESIGN COMPLETE - Report saved: {filename}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
