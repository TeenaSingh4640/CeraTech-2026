"""
COMPREHENSIVE STRUCTURAL SYSTEM ANALYSIS - PART 2

Continuation of detailed engineering analysis covering:
5. Lateral load resisting system design
6. Seismic design considerations
7. Wind load analysis
8. Detailed load calculations
9. Material grade selection
10. Structural optimization strategies
"""

import numpy as np
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class LateralLoadResistingSystem:
    """Detailed lateral force resisting system design"""
    
    def __init__(self, num_floors: int, floor_height: float, building_length: float,
                 building_width: float, seismic_zone: str, building_type: str):
        self.num_floors = num_floors
        self.floor_height = floor_height
        self.building_length = building_length
        self.building_width = building_width
        self.total_height = num_floors * floor_height
        self.seismic_zone = seismic_zone
        self.building_type = building_type
    
    def design_lateral_system(self) -> Dict:
        """
        5. LATERAL LOAD RESISTING SYSTEM (SHEAR WALLS / MOMENT FRAMES / BRACING)
        
        Design per IS 1893:2016 for seismic loads
        System selection based on height, seismic zone, and architectural requirements
        """
        
        print("\n" + "="*100)
        print("5. LATERAL LOAD RESISTING SYSTEM DESIGN")
        print("="*100)
        
        # ==================== SYSTEM SELECTION LOGIC ====================
        
        # Height-based system selection
        if self.total_height <= 12:  # Low-rise
            primary_system = "Moment-Resisting Frame (MRF)"
            system_description = "Ductile frame with rigid beam-column connections"
            system_code = "SMRF/IMRF/OMRF based on seismic zone"
        elif self.total_height <= 40:  # Mid-rise
            primary_system = "Dual System (Frame + Shear Walls)"
            system_description = "Frame resists 25%, shear walls resist 75% of lateral loads"
            system_code = "Dual system per IS 1893 Cl 7.2"
        else:  # High-rise
            primary_system = "Core-Outrigger System"
            system_description = "Central core with outrigger trusses to perimeter columns"
            system_code = "Advanced system requiring detailed dynamic analysis"
        
        # Seismic zone factor (IS 1893 Table 3)
        zone_factors = {"I": 0.10, "II": 0.16, "III": 0.24, "IV": 0.36, "V": 0.40}
        Z = zone_factors[self.seismic_zone]
        
        # Importance factor (IS 1893 Table 8)
        importance_factors = {
            "Residential": 1.0,
            "Commercial": 1.0,
            "Institutional": 1.5,
            "Industrial": 1.0
        }
        I = importance_factors.get(self.building_type, 1.0)
        
        # Response reduction factor (IS 1893 Table 9)
        if "SMRF" in system_code or self.seismic_zone in ["IV", "V"]:
            R = 5.0  # Special moment-resisting frame
            ductility_class = "Special (DCH - High Ductility)"
        elif self.seismic_zone == "III":
            R = 4.0  # Intermediate
            ductility_class = "Intermediate (DCM - Medium Ductility)"
        else:
            R = 3.0  # Ordinary
            ductility_class = "Ordinary (DCL - Low Ductility)"
        
        # ==================== MOMENT FRAME DESIGN ====================
        
        if "Frame" in primary_system or "Dual" in primary_system:
            # Beam-column connection design
            connection_type = "Ductile detailing with confined joints"
            
            # Beam reinforcement provisions
            beam_provisions = {
                "top_steel": "Continuous over supports",
                "bottom_steel": "At least 50% of top steel throughout",
                "stirrups_spacing": "d/4 spacing in 2d length from face of support",
                "confinement": "Closely spaced hoops in joint region",
                "lap_splicing": "Avoid laps in potential plastic hinge zones"
            }
            
            # Column reinforcement provisions
            column_provisions = {
                "longitudinal_steel": "Min 0.8%, max 6% of gross area",
                "ties_spacing": "≤ least of (0.25×column_size, 8×dia_main_bar, 300mm)",
                "confinement_length": "Greater of (D, L/6, 450mm) from joint face",
                "splice_location": "Only in middle third of column height",
                "special_detailing": "135° hooks for ties in SMRF"
            }
            
            # Strong column - weak beam criterion
            strong_column_weak_beam = "ΣMc ≥ 1.2 × ΣMb (cl 7.4.2 of IS 1893)"
            
            frame_design = {
                "system_type": "Moment-Resisting Frame",
                "ductility_class": ductility_class,
                "response_reduction_factor_R": R,
                "connection_type": connection_type,
                "beam_detailing": beam_provisions,
                "column_detailing": column_provisions,
                "design_philosophy": strong_column_weak_beam,
                "drift_limit": "0.004 × storey height (per IS 1893 Cl 7.11.1)"
            }
        else:
            frame_design = {"note": "Frame not part of primary lateral system"}
        
        # ==================== SHEAR WALL DESIGN ====================
        
        if "Dual" in primary_system or "Shear Wall" in primary_system:
            # Shear wall configuration
            wall_thickness = max(150, self.total_height // 25)  # mm
            
            # Location of shear walls
            wall_locations = [
                "Core walls around staircases and elevators",
                "Walls at building periphery for torsion resistance",
                "L-shaped or C-shaped walls at corners for biaxial resistance",
                "Coupled walls with connecting beams for energy dissipation"
            ]
            
            # Shear wall length calculation
            # Approximate: Total wall length ≈ 1.5-2.5% of floor area
            total_floor_area = self.building_length * self.building_width
            wall_length_min = 0.015 * total_floor_area  # m (1.5%)
            wall_length_max = 0.025 * total_floor_area  # m (2.5%)
            
            # Reinforcement requirements (IS 13920:2016)
            wall_reinforcement = {
                "vertical_steel": "0.25% minimum (both faces)",
                "horizontal_steel": "0.25% minimum (both faces)",
                "bar_spacing": "≤ lesser of (300mm, 3×wall_thickness)",
                "boundary_elements": "Required when edge compression > 0.2fck",
                "boundary_confinement": "Same as special confinement for columns",
                "coupling_beams": "Diagonal reinforcement for high shear demand"
            }
            
            # Aspect ratio check
            wall_aspect_ratio = self.total_height / wall_thickness  # Should be reasonable
            
            if wall_aspect_ratio > 10:
                wall_behavior = "Slender wall - flexure dominant"
            else:
                wall_behavior = "Squat wall - shear dominant"
            
            # Shear capacity check
            # τc = V / (d × t)
            # For M25 concrete, τc,max = 3.1 N/mm² per IS 456
            
            shear_wall_design = {
                "wall_thickness": f"{wall_thickness} mm",
                "required_wall_length": f"{wall_length_min:.1f} - {wall_length_max:.1f} m total",
                "locations": wall_locations,
                "reinforcement": wall_reinforcement,
                "wall_behavior": wall_behavior,
                "aspect_ratio": f"{wall_aspect_ratio:.1f}",
                "design_code": "IS 13920:2016 for ductile detailing",
                "coupling": "Couple shear walls with deep beams for redundancy",
                "force_distribution": "75% of lateral loads resisted by walls in dual system"
            }
        else:
            shear_wall_design = {"note": "Shear walls not required for this height"}
        
        # ==================== BRACING SYSTEM (if applicable) ====================
        
        if "Industrial" in self.building_type or self.total_height > 50:
            # Bracing types
            bracing_options = {
                "concentric_bracing": {
                    "types": ["X-bracing", "Chevron bracing", "Single diagonal"],
                    "advantages": "Simple, economical, effective",
                    "disadvantages": "Yielding causes strength degradation",
                    "R_factor": "4.0 for SCBF (special concentrically braced frame)"
                },
                "eccentric_bracing": {
                    "types": ["Link beams with bracing"],
                    "advantages": "Superior energy dissipation, stable hysteresis",
                    "disadvantages": "Complex detailing",
                    "R_factor": "5.0 for SEBF"
                },
                "buckling_restrained_bracing": {
                    "types": ["BRB with steel core in concrete casing"],
                    "advantages": "Excellent seismic performance, no buckling",
                    "disadvantages": "Higher cost",
                    "R_factor": "6.0-8.0"
                }
            }
            
            bracing_design = {
                "recommendation": "Consider bracing for industrial or super-tall buildings",
                "options": bracing_options,
                "typical_application": "Infill braced frames in selected bays"
            }
        else:
            bracing_design = {"note": "Bracing not typical for RC buildings of this configuration"}
        
        # ==================== DIAPHRAGM ACTION ====================
        
        diaphragm = {
            "floor_slab_role": "Acts as horizontal diaphragm to transfer lateral loads",
            "requirements": [
                "Slab acts as deep beam spanning between shear walls/frames",
                "In-plane rigidity >> out-of-plane stiffness of vertical elements",
                "Chord reinforcement at edges parallel to lateral force",
                "Collector/drag beams to transfer forces to vertical elements",
                "Continuous load path from roof to foundation"
            ],
            "design_check": "In-plane shear stress v = V / (A_gross) < τc",
            "detailing": "Provide edge zone reinforcement as chord steel"
        }
        
        # ==================== TORSIONAL CONSIDERATIONS ====================
        
        # Eccentricity calculation
        # Static eccentricity: distance between center of mass and center of rigidity
        # Dynamic eccentricity: ±5% of building dimension (IS 1893 Cl 7.9.2)
        
        dynamic_eccentricity = 0.05 * min(self.building_length, self.building_width)
        
        torsion = {
            "code_provision": "IS 1893:2016 Cl 7.9 - Design for torsion",
            "dynamic_eccentricity": f"±{dynamic_eccentricity:.2f} m (5% of plan dimension)",
            "torsion_irregularity": "Check if max drift > 1.2 × avg drift",
            "mitigation": [
                "Place shear walls/columns at building periphery",
                "Symmetric arrangement of lateral load resisting elements",
                "Avoid re-entrant corners or provide separation joints",
                "Use high torsional rigidity elements (closed core walls)"
            ]
        }
        
        # ==================== DRIFT CALCULATIONS ====================
        
        # Inter-storey drift limit (IS 1893 Cl 7.11.1)
        drift_limit = 0.004 * self.floor_height * 1000  # mm
        
        # Approximate drift calculation (simplified)
        # Δ = (base_shear × height³) / (3 × E × I_effective)
        
        drift_control = {
            "code_limit": f"{drift_limit:.1f} mm (0.4% of storey height)",
            "design_drift": f"≈ 0.002-0.003 × storey height (typical)",
            "control_measures": [
                "Increase shear wall length/thickness",
                "Increase column sizes",
                "Reduce storey height",
                "Use stiffer lateral systems (core-outrigger)",
                "Consider viscous dampers or base isolation for extreme cases"
            ],
            "p_delta_effect": "Check if storey drift ratio × axial load ratio > 0.1"
        }
        
        # ==================== FOUNDATION INTERFACE ====================
        
        foundation_connection = {
            "base_fixity": "Fixed for frames, moment connection to foundation",
            "shear_wall_foundation": "Mat foundation or piled raft for shear walls",
            "overturning": "Check net tension at foundation level (T ≤ φ × Pullout_capacity)",
            "soil_bearing": "Increase foundation size if overturning induces tension",
            "anchorage": "Dowels from shear walls into foundation with development length"
        }
        
        # ==================== SYSTEM COMPARISON ====================
        
        system_comparison = {
            "moment_frame": {
                "efficiency": "Good for low-rise (≤12m)",
                "cost": "Moderate",
                "architectural_impact": "Maximum flexibility - no walls",
                "best_for": "Low seismic zones, architectural freedom needed"
            },
            "shear_wall": {
                "efficiency": "Excellent for mid-rise (12-40m)",
                "cost": "Higher initial, lower drift",
                "architectural_impact": "Core walls don't impact much",
                "best_for": "Moderate to high seismic zones"
            },
            "dual_system": {
                "efficiency": "Excellent for mid to high-rise",
                "cost": "Optimized (walls take most lateral, frames for gravity)",
                "architectural_impact": "Balanced - some walls needed",
                "best_for": "High seismic zones, tall buildings"
            },
            "core_outrigger": {
                "efficiency": "Excellent for super-tall (>50m)",
                "cost": "High but necessary",
                "architectural_impact": "Outrigger levels are utility floors",
                "best_for": "Super-tall buildings in high seismic/wind zones"
            }
        }
        
        # ==================== COMPILATION ====================
        
        result = {
            "selected_system": {
                "primary": primary_system,
                "description": system_description,
                "applicable_code": system_code,
                "building_height": f"{self.total_height:.1f} m ({self.num_floors} floors)"
            },
            "seismic_parameters": {
                "zone": self.seismic_zone,
                "zone_factor_Z": Z,
                "importance_factor_I": I,
                "response_reduction_factor_R": R,
                "ductility_class": ductility_class
            },
            "moment_frame_design": frame_design,
            "shear_wall_design": shear_wall_design,
            "bracing_system": bracing_design,
            "diaphragm_design": diaphragm,
            "torsion_considerations": torsion,
            "drift_control": drift_control,
            "foundation_connection": foundation_connection,
            "system_comparison": system_comparison,
            "design_process": [
                "1. Determine seismic base shear (V = Z×I×Sa/g / R×W)",
                "2. Distribute base shear vertically (Wi×hi method)",
                "3. Analyze 3D model for member forces",
                "4. Design members for combined gravity + lateral loads",
                "5. Detail connections per IS 13920:2016",
                "6. Check drift limits and P-Δ effects",
                "7. Verify torsional irregularities"
            ]
        }
        
        print(f"\n   Selected System: {primary_system}")
        print(f"   Ductility Class: {ductility_class} (R = {R})")
        print(f"   Seismic Zone: {self.seismic_zone} (Z = {Z})")
        print(f"   Drift Limit: {drift_limit:.1f} mm")
        
        return result


@dataclass
class SeismicDesignAnalysis:
    """Comprehensive seismic design considerations"""
    
    def __init__(self, building_weight: float, num_floors: int, floor_height: float,
                 seismic_zone: str, soil_type: str, building_type: str,
                 importance_factor: float = 1.0):
        self.building_weight = building_weight  # kN
        self.num_floors = num_floors
        self.floor_height = floor_height
        self.total_height = num_floors * floor_height
        self.seismic_zone = seismic_zone
        self.soil_type = soil_type
        self.building_type = building_type
        self.importance_factor = importance_factor
    
    def perform_seismic_analysis(self) -> Dict:
        """
        6. SEISMIC DESIGN CONSIDERATIONS (DETAILED)
        
        Complete seismic analysis per IS 1893:2016
        Includes base shear, modal analysis parameters, and design provisions
        """
        
        print("\n" + "="*100)
        print("6. SEISMIC DESIGN ANALYSIS")
        print("="*100)
        
        # ==================== SEISMIC ZONE PARAMETERS ====================
        
        # Zone factor (IS 1893 Table 3)
        zone_factors = {"I": 0.10, "II": 0.16, "III": 0.24, "IV": 0.36, "V": 0.40}
        Z = zone_factors[self.seismic_zone]
        
        # Importance factor I (already provided)
        I = self.importance_factor
        
        # Response reduction factor R (depends on structural system)
        if self.seismic_zone in ["IV", "V"]:
            R = 5.0  # SMRF required
        elif self.seismic_zone == "III":
            R = 4.0  # IMRF
        else:
            R = 3.0  # OMRF
        
        print(f"\n   Seismic Zone: {self.seismic_zone}")
        print(f"   Zone Factor (Z): {Z}")
        print(f"   Response Reduction (R): {R}")
        
        # ==================== SOIL TYPE AND SITE FACTOR ====================
        
        # Soil classification per IS 1893 Table 1
        soil_classification = {
            "Rock": {"type": "Type I - Rock or Hard Soil", "description": "SPT N > 30"},
            "Sand": {"type": "Type II - Medium Soil", "description": "SPT N = 10-30"},
            "Clay": {"type": "Type III - Soft Soil", "description": "SPT N < 10"},
            "Mixed": {"type": "Type II - Medium Soil (assumed)", "description": "Mixed profile"}
        }
        
        soil_info = soil_classification.get(self.soil_type, soil_classification["Sand"])
        
        # Time period calculation (IS 1893 Cl 7.6)
        # Method 1: Empirical formula (for preliminary design)
        # Ta = 0.075 × h^0.75 (for RC moment frame without brick infill)
        # Ta = 0.09 × h / √d (for other buildings)
        
        h = self.total_height  # meters
        d = math.sqrt(self.building_weight / (15 * self.num_floors))  # Approximate plan dimension
        
        # Empirical time period
        Ta_empirical = 0.075 * (h ** 0.75)  # For moment frames
        
        # More accurate formula for different building types
        if "Frame" in self.building_type:
            Ta = 0.075 * (h ** 0.75)
        else:
            Ta = 0.09 * h / math.sqrt(max(d, 1))  # Avoid division issues
        
        # ==================== DESIGN SPECTRAL ACCELERATION ====================
        
        # For medium soil (Type II), spectral acceleration coefficient Sa/g:
        # For T < 0.1s: Sa/g = 1 + 15T
        # For 0.1s ≤ T ≤ 0.4s: Sa/g = 2.5
        # For T > 0.4s: Sa/g = 1.0/T
        
        if Ta < 0.10:
            Sa_g = 1 + 15 * Ta
        elif Ta <= 0.40:
            Sa_g = 2.5
        else:
            Sa_g = 1.0 / Ta
        
        # For damping other than 5%, multiply by factor β (Table 3 of IS 1893)
        # Assuming 5% damping, β = 1.0
        
        # ==================== SEISMIC BASE SHEAR CALCULATION ====================
        
        # Design horizontal seismic coefficient (IS 1893 Cl 6.4.2)
        Ah = (Z / 2) * (Sa_g) * (I / R)
        
        # Design base shear
        Vb = Ah * self.building_weight  # kN
        
        print(f"   Time Period (Ta): {Ta:.2f} seconds")
        print(f"   Spectral Acceleration (Sa/g): {Sa_g:.2f}")
        print(f"   Design Base Shear: {Vb:.1f} kN ({Vb/self.building_weight*100:.1f}% of weight)")
        
        # ==================== VERTICAL DISTRIBUTION OF BASE SHEAR ====================
        
        # Distribution per IS 1893 Cl 7.7.1
        # Fi = Vb × (Wi × hi²) / Σ(Wj × hj²)
        
        floor_forces = []
        sum_Wh2 = 0
        
        # Assume equal floor weights for simplicity
        floor_weight = self.building_weight / self.num_floors
        
        for i in range(1, self.num_floors + 1):
            hi = i * self.floor_height
            Wh2 = floor_weight * (hi ** 2)
            sum_Wh2 += Wh2
        
        for i in range(1, self.num_floors + 1):
            hi = i * self.floor_height
            Wh2 = floor_weight * (hi ** 2)
            Fi = Vb * (Wh2 / sum_Wh2)
            
            floor_forces.append({
                "floor": i,
                "height_from_base": f"{hi:.1f} m",
                "floor_weight": f"{floor_weight:.1f} kN",
                "lateral_force": f"{Fi:.1f} kN",
                "force_percentage": f"{Fi/Vb*100:.1f}%"
            })
        
        # ==================== MODAL ANALYSIS REQUIREMENTS ====================
        
        # Number of modes to consider (IS 1893 Cl 7.8.4.3)
        # Should capture ≥ 90% of total mass
        
        num_modes_required = math.ceil(self.num_floors / 3)  # Typical: n/3 modes
        num_modes_required = max(num_modes_required, 3)  # Minimum 3 modes
        
        modal_analysis = {
            "method": "Response Spectrum Method (RSM)" if self.num_floors >= 5 else "Equivalent Static Method",
            "modes_required": f"{num_modes_required} modes minimum",
            "mass_participation": "≥90% in each principal direction",
            "modal_combination": "SRSS (Square Root of Sum of Squares) or CQC (Complete Quadratic Combination)",
            "directional_combination": "100% X + 30% Y + 30% Z (and permutations)"
        }
        
        # ==================== IRREGULARITIES CHECK ====================
        
        # IS 1893 Table 4 (Plan irregularities) and Table 5 (Vertical irregularities)
        
        irregularities = {
            "plan_irregularities": [
                {
                    "type": "Torsional irregularity",
                    "check": "Max drift > 1.2 × Avg drift at any level",
                    "consequence": "Increase design forces by 1.5× if irregular"
                },
                {
                    "type": "Re-entrant corners",
                    "check": "Projection > 15% of plan dimension",
                    "consequence": "Provide separation joint or design for stress concentration"
                },
                {
                    "type": "Diaphragm discontinuity",
                    "check": "Openings > 50% of diaphragm area",
                    "consequence": "Special analysis required"
                }
            ],
            "vertical_irregularities": [
                {
                    "type": "Stiffness irregularity (soft storey)",
                    "check": "Storey stiffness < 70% of storey above",
                    "consequence": "Multiply storey shears by 2.5"
                },
                {
                    "type": "Mass irregularity",
                    "check": "Storey mass > 200% of adjacent storey",
                    "consequence": "Dynamic analysis mandatory"
                },
                {
                    "type": "Vertical geometric irregularity",
                    "check": "Horizontal dimension > 150% of adjacent storey",
                    "consequence": "Special detailing at transition"
                }
            ]
        }
        
        # ==================== DUCTILE DETAILING REQUIREMENTS ====================
        
        # Per IS 13920:2016
        ductile_detailing = {
            "beams": {
                "flexural_reinforcement": [
                    "Top bars continuous over supports",
                    "Bottom bars ≥ 50% of top bars throughout span",
                    "Positive moment capacity ≥ 50% of negative moment capacity",
                    "Bar splices only in central 1/2 of span"
                ],
                "shear_reinforcement": [
                    "First stirrup at 50mm from face of support",
                    "Spacing ≤ d/4 in 2d length from support face",
                    "Spacing ≤ d/2 in remaining length",
                    "135° hooks for stirrups"
                ]
            },
            "columns": {
                "longitudinal_steel": [
                    "Min 0.8% of gross area (0.01 for rectangular, 0.008 for circular)",
                    "Max 6% (to ensure proper compaction)",
                    "Min 4 bars in rectangular, 6 bars in circular",
                    "Lap splices only in middle 1/2 of column height"
                ],
                "transverse_reinforcement": [
                    "Special confining steel in h_0 length from joint face",
                    "h_0 = max(D, L/6, 450mm)",
                    "Pitch ≤ min(0.25D, 8φ, 300mm) in confined length",
                    "Pitch ≤ min(0.5D, 16φ, 300mm) in unconfined length",
                    "135° hooks for ties/hoops"
                ]
            },
            "beam_column_joints": {
                "joint_reinforcement": [
                    "Hoops in joint region continuous with column ties",
                    "Spacing ≤ 150mm in joint",
                    "Special confining steel required",
                    "No bar cut-off in joint region"
                ],
                "joint_shear_check": [
                    "τv = V / (b × h) ≤ 1.25√fck for concrete",
                    "Provide additional stirrups if τv exceeds limit"
                ]
            }
        }
        
        # ==================== P-DELTA EFFECTS ====================
        
        # Check for second-order effects (IS 1893 Cl 7.10.4)
        # Stability coefficient θ = (P × Δ) / (V × h)
        # If θ > 0.10, P-Delta analysis required
        
        # Approximate check
        typical_storey_shear = Vb / self.num_floors
        typical_axial_load = self.building_weight / 10  # Assume 10 columns per floor
        assumed_drift = 0.003 * self.floor_height * 1000  # mm (0.3% drift)
        
        theta = (typical_axial_load * assumed_drift) / (typical_storey_shear * self.floor_height * 1000)
        
        if theta > 0.10:
            p_delta_note = f"θ = {theta:.2f} > 0.10 ⇒ P-Δ analysis REQUIRED"
        else:
            p_delta_note = f"θ = {theta:.2f} < 0.10 ⇒ P-Δ effects negligible"
        
        p_delta_analysis = {
            "stability_coefficient_theta": f"{theta:.3f}",
            "check_result": p_delta_note,
            "mitigation": "Increase lateral stiffness (shear walls) if θ > 0.10"
        }
        
        # ==================== FOUNDATION DESIGN FOR SEISMIC ====================
        
        foundation_seismic = {
            "overturning_moment": f"{Vb * self.total_height / 2:.1f} kNm (approximate)",
            "design_requirements": [
                "Check against overturning: Factor of safety ≥ 1.5",
                "Design for uplift tension in piles/footings",
                "Provide tie beams in both directions at plinth level",
                "Tie beam minimum size: 200×200 mm with 4 bars",
                "Anchorage dowels from walls/columns with full development"
            ],
            "soil_bearing_upgrade": "Increase allowable bearing by 25% for seismic load combinations"
        }
        
        # ==================== COMPILATION ====================
        
        result = {
            "seismic_zone_data": {
                "zone": self.seismic_zone,
                "zone_factor_Z": Z,
                "peak_ground_acceleration": f"{Z/2:.2f}g",
                "seismic_intensity": "Moderate" if Z < 0.24 else "High" if Z < 0.36 else "Very High"
            },
            "site_characteristics": {
                "soil_type": self.soil_type,
                "soil_classification": soil_info,
                "site_amplification": "Considered in spectral acceleration curve"
            },
            "structural_response": {
                "fundamental_period_Ta": f"{Ta:.3f} seconds",
                "spectral_acceleration_Sa/g": f"{Sa_g:.2f}",
                "response_reduction_R": R,
                "damping": "5% (standard for concrete structures)"
            },
            "base_shear_calculation": {
                "design_coefficient_Ah": f"{Ah:.4f}",
                "base_shear_Vb": f"{Vb:.1f} kN",
                "percentage_of_weight": f"{Vb/self.building_weight*100:.2f}%",
                "formula": "Vb = Ah × W, where Ah = (Z/2)×(Sa/g)×(I/R)"
            },
            "vertical_distribution": {
                "method": "Wi × hi² method (IS 1893 Cl 7.7.1)",
                "floor_forces": floor_forces[:5] + ["..."] + floor_forces[-2:] if len(floor_forces) > 7 else floor_forces,
                "note": "Higher floors receive greater lateral forces"
            },
            "modal_analysis": modal_analysis,
            "irregularities_check": irregularities,
            "ductile_detailing": ductile_detailing,
            "p_delta_effects": p_delta_analysis,
            "foundation_design": foundation_seismic,
            "design_checks": [
                "✓ Calculate base shear using seismic coefficient method",
                "✓ Distribute forces vertically using Wi×hi² method",
                "✓ Analyze 3D model with seismic loads in both directions",
                "✓ Check drift limits (0.4% of storey height)",
                "✓ Verify torsional irregularities",
                "✓ Check P-Δ effects if θ > 0.10",
                "✓ Design members for combined gravity + seismic loads",
                "✓ Detail per IS 13920:2016 for ductility",
                "✓ Check foundation for overturning and uplift"
            ]
        }
        
        return result


# Continue with remaining modules in next section due to length...
# Wind loads, detailed loads, materials, optimization follow similar structure

if __name__ == "__main__":
    print("\n" + "="*100)
    print("STRUCTURAL SYSTEM ANALYSIS - PART 2 (LATERAL SYSTEMS, SEISMIC)")
    print("="*100)
    
    # Example: Lateral system for 10-story commercial building
    lateral = LateralLoadResistingSystem(10, 3.5, 50, 30, "III", "Commercial")
    lateral_result = lateral.design_lateral_system()
    
    # Example: Seismic analysis
    seismic = SeismicDesignAnalysis(15000, 10, 3.5, "III", "Sand", "Commercial", 1.0)
    seismic_result = seismic.perform_seismic_analysis()
    
    print("\n" + "="*100)
    print("✅ PART 2 ANALYSIS COMPLETE")
    print("="*100)
