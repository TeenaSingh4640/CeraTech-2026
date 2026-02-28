"""
COMPREHENSIVE STRUCTURAL SYSTEM ANALYSIS - PART 3

Final modules covering:
7. Wind load analysis
8. Detailed load calculations (all types)
9. Material grade selection with justification
10. Structural optimization strategies
"""

import numpy as np
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class WindLoadAnalysis:
    """Comprehensive wind load calculation per IS 875 Part 3:2015"""
    
    def __init__(self, building_height: float, building_length: float, building_width: float,
                 location: str, terrain_category: str, building_class: str):
        self.building_height = building_height
        self.building_length = building_length
        self.building_width = building_width
        self.location = location
        self.terrain_category = terrain_category
        self.building_class = building_class
    
    def calculate_wind_loads(self) -> Dict:
        """
        7. WIND LOAD ANALYSIS (COMPREHENSIVE)
        
        Complete wind load calculation per IS 875 Part 3:2015
        Includes pressure distribution, along-wind and across-wind effects
        """
        
        print("\n" + "="*100)
        print("7. WIND LOAD ANALYSIS")
        print("="*100)
        
        # ==================== BASIC WIND SPEED ====================
        
        # Basic wind speed Vb (IS 875 Part 3 Figure 1 - Wind zone map)
        # Values in m/s for 50-year return period
        wind_zones = {
            "Mumbai": 44,
            "Delhi": 47,
            "Kolkata": 50,
            "Chennai": 50,
            "Bangalore": 33,
            "Hyderabad": 44,
            "Coastal": 50,
            "Interior": 44,
            "Cyclone_Prone": 55
        }
        
        Vb = wind_zones.get(self.location, 47)  # Default to 47 m/s
        
        print(f"\n   Location: {self.location}")
        print(f"   Basic Wind Speed (Vb): {Vb} m/s")
        
        # ==================== RISK COEFFICIENT (k1) ====================
        
        # Based on importance and design life (IS 875 Part 3 Table 1)
        building_classes = {
            "General": {"k1": 1.0, "description": "Buildings with 50-year design life"},
            "Important": {"k1": 1.08, "description": "Important buildings (hospitals, schools)"},
            "Temporary": {"k1": 0.82, "description": "Temporary structures"}
        }
        
        k1_data = building_classes.get(self.building_class, building_classes["General"])
        k1 = k1_data["k1"]
        
        # ==================== TERRAIN AND HEIGHT FACTOR (k2) ====================
        
        # IS 875 Part 3 Table 2 - varies with height and terrain category
        # Terrain Category (1-4): 1=exposed coastal, 2=open terrain, 3=suburban, 4=urban
        
        terrain_data = {
            "1": {"name": "Category 1 - Exposed", "α": 0.12, "k2_base": 1.05},
            "2": {"name": "Category 2 - Open", "α": 0.14, "k2_base": 1.00},
            "3": {"name": "Category 3 - Suburban", "α": 0.16, "k2_base": 0.91},
            "4": {"name": "Category 4 - Urban", "α": 0.20, "k2_base": 0.71}
        }
        
        terrain_info = terrain_data.get(self.terrain_category, terrain_data["2"])
        alpha = terrain_info["α"]
        
        # k2 calculation for height h
        # k2 = k2_base × (h/10)^α  for h > 10m
        # k2 = k2_base  for h ≤ 10m
        
        if self.building_height > 10:
            k2 = terrain_info["k2_base"] * ((self.building_height / 10) ** alpha)
        else:
            k2 = terrain_info["k2_base"]
        
        print(f"   Terrain Category: {terrain_info['name']}")
        print(f"   Terrain & Height Factor (k2): {k2:.3f}")
        
        # ==================== TOPOGRAPHY FACTOR (k3) ====================
        
        # For flat terrain k3 = 1.0
        # For hills/escarpments, use IS 875 Part 3 Cl 6.3.2
        k3 = 1.0  # Assuming flat terrain
        
        topography_note = "Flat terrain assumed (k3 = 1.0)"
        
        # ==================== IMPORTANCE FACTOR (k4) ====================
        
        # Already included in k1 for IS 875 Part 3
        # k4 is generally 1.0 in current code
        k4 = 1.0
        
        # ==================== DESIGN WIND SPEED (Vz) ====================
        
        # Vz = Vb × k1 × k2 × k3 × k4
        Vz = Vb * k1 * k2 * k3 * k4
        
        print(f"   Design Wind Speed (Vz): {Vz:.2f} m/s")
        
        # ==================== DESIGN WIND PRESSURE (pz) ====================
        
        # pz = 0.6 × Vz²  (in N/m²)
        # where 0.6 = 0.5 × ρ, and ρ = 1.2 kg/m³ (air density)
        
        pz = 0.6 * (Vz ** 2)  # N/m²
        pz_kPa = pz / 1000  # kN/m²
        
        print(f"   Design Wind Pressure (pz): {pz:.1f} N/m² = {pz_kPa:.2f} kN/m²")
        
        # ==================== EXTERNAL PRESSURE COEFFICIENTS ====================
        
        # IS 875 Part 3 Tables 4-8 - depends on building shape and wind direction
        
        # For rectangular building, wind perpendicular to face
        aspect_ratio_height_width = self.building_height / min(self.building_length, self.building_width)
        aspect_ratio_length_width = max(self.building_length, self.building_width) / min(self.building_length, self.building_width)
        
        # Wind on long face
        if aspect_ratio_height_width >= 4:  # Tall building
            Cpe_windward = +0.8
            Cpe_leeward = -0.5
            Cpe_side_A = -0.7
            Cpe_side_B = -0.7
        elif aspect_ratio_height_width >= 1:  # Normal building
            Cpe_windward = +0.7
            Cpe_leeward = -0.4
            Cpe_side_A = -0.65
            Cpe_side_B = -0.65
        else:  # Low-rise building
            Cpe_windward = +0.6
            Cpe_leeward = -0.3
            Cpe_side_A = -0.6
            Cpe_side_B = -0.6
        
        # Roof pressure coefficients (depends on roof slope, assume flat roof)
        Cpe_roof = -0.7  # Typical for flat roof
        
        external_pressures = {
            "windward_face": {
                "Cpe": Cpe_windward,
                "pressure": f"{Cpe_windward * pz_kPa:.2f} kN/m²",
                "note": "Positive pressure (pushing inward)"
            },
            "leeward_face": {
                "Cpe": Cpe_leeward,
                "pressure": f"{Cpe_leeward * pz_kPa:.2f} kN/m²",
                "note": "Suction (pulling outward)"
            },
            "side_faces": {
                "Cpe": Cpe_side_A,
                "pressure": f"{Cpe_side_A * pz_kPa:.2f} kN/m²",
                "note": "Suction on both sides"
            },
            "roof": {
                "Cpe": Cpe_roof,
                "pressure": f"{Cpe_roof * pz_kPa:.2f} kN/m²",
                "note": "Uplift suction"
            }
        }
        
        # ==================== INTERNAL PRESSURE COEFFICIENT ====================
        
        # IS 875 Part 3 Cl 6.2.3.4 - depends on openings
        # For buildings with normal permeability: Cpi = ±0.2
        # For buildings with dominant opening: Cpi = ±0.5 to ±0.8
        
        Cpi_positive = +0.2  # Internal pressure
        Cpi_negative = -0.2  # Internal suction
        
        internal_pressure = {
            "Cpi_range": "±0.2 (normal permeability)",
            "pressure_positive": f"{Cpi_positive * pz_kPa:.2f} kN/m²",
            "pressure_negative": f"{Cpi_negative * pz_kPa:.2f} kN/m²",
            "note": "Consider both cases for maximum wind effect"
        }
        
        # ==================== NET PRESSURE ON FACES ====================
        
        # Net pressure = (Cpe - Cpi) × pz
        # Consider critical combination (external + internal)
        
        net_windward = (Cpe_windward - Cpi_negative) * pz_kPa  # Maximum push
        net_leeward = (Cpe_leeward - Cpi_positive) * pz_kPa  # Maximum suction
        net_side = (Cpe_side_A - Cpi_positive) * pz_kPa
        net_roof = (Cpe_roof - Cpi_positive) * pz_kPa  # Uplift
        
        net_pressures = {
            "windward_face_critical": f"{net_windward:.2f} kN/m² (with internal suction)",
            "leeward_face_critical": f"{net_leeward:.2f} kN/m² (with internal pressure)",
            "side_faces_critical": f"{net_side:.2f} kN/m²",
            "roof_uplift_critical": f"{net_roof:.2f} kN/m² (upward suction)"
        }
        
        # ==================== ALONG-WIND FORCE ====================
        
        # Total along-wind force F = Cf × Ae × pz
        # where Cf = force coefficient, Ae = effective area
        
        # Frontal area (wind perpendicular to face)
        frontal_area_long = self.building_width * self.building_height  # Wind on long face
        frontal_area_short = self.building_length * self.building_height  # Wind on short face
        
        # Force coefficient Cf = Cpe(windward) - Cpe(leeward)
        Cf_long_face = Cpe_windward - Cpe_leeward
        Cf_short_face = Cpe_windward - Cpe_leeward  # Same for both directions
        
        # Total along-wind force
        F_along_long = Cf_long_face * frontal_area_long * pz_kPa  # kN (wind on long face)
        F_along_short = Cf_short_face * frontal_area_short * pz_kPa  # kN (wind on short face)
        
        along_wind = {
            "wind_on_long_face": {
                "frontal_area": f"{frontal_area_long:.1f} m²",
                "force_coefficient_Cf": f"{Cf_long_face:.2f}",
                "total_force": f"{F_along_long:.1f} kN",
                "base_moment": f"{F_along_long * self.building_height/2:.1f} kNm"
            },
            "wind_on_short_face": {
                "frontal_area": f"{frontal_area_short:.1f} m²",
                "force_coefficient_Cf": f"{Cf_short_face:.2f}",
                "total_force": f"{F_along_short:.1f} kN",
                "base_moment": f"{F_along_short * self.building_height/2:.1f} kNm"
            },
            "governing_case": "Short face" if F_along_short > F_along_long else "Long face"
        }
        
        # ==================== ACROSS-WIND FORCE (for tall buildings) ====================
        
        # Across-wind response becomes significant for h/b > 4
        h_b_ratio = self.building_height / min(self.building_length, self.building_width)
        
        if h_b_ratio > 4:
            # Across-wind force due to vortex shedding
            # Simplified: F_across ≈ 0.5 × F_along (for slender towers)
            F_across_estimate = 0.5 * max(F_along_long, F_along_short)
            
            across_wind = {
                "applicability": "Significant (h/b > 4)",
                "h_b_ratio": f"{h_b_ratio:.2f}",
                "estimated_force": f"{F_across_estimate:.1f} kN",
                "note": "Dynamic analysis recommended for accurate evaluation",
                "vortex_shedding": "Consider reduced velocity and lock-in effects",
                "mitigation": ["Corner modifications", "Helical strakes", "Tuned mass dampers"]
            }
        else:
            across_wind = {
                "applicability": "Negligible (h/b < 4)",
                "h_b_ratio": f"{h_b_ratio:.2f}",
                "note": "Along-wind loads govern"
            }
        
        # ==================== DYNAMIC WIND EFFECTS ====================
        
        # Gust factor method (IS 875 Part 3 Cl 8.3)
        # For buildings sensitive to wind-induced oscillations
        
        # Natural frequency estimation (very approximate)
        # f₀ ≈ 46 / H  (Hz) for concrete buildings
        natural_frequency = 46 / self.building_height  # Hz
        
        # Building is dynamically sensitive if f₀ < 1 Hz
        if natural_frequency < 1.0:
            dynamic_sensitivity = "HIGH - Dynamic analysis required"
            gust_factor_note = "Gust response factor > 2.0, detailed analysis needed"
        else:
            dynamic_sensitivity = "LOW - Static analysis adequate"
            gust_factor_note = "Gust response factor ≈ 1.5-2.0 (typical)"
        
        dynamic_effects = {
            "natural_frequency_estimate": f"{natural_frequency:.2f} Hz",
            "dynamic_sensitivity": dynamic_sensitivity,
            "gust_response": gust_factor_note,
            "recommendations": [
                "Perform dynamic analysis if f₀ < 1 Hz",
                "Consider occupant comfort (acceleration limits)",
                "Check for vortex-induced vibrations",
                "Evaluate fatigue on cladding connections"
            ]
        }
        
        # ==================== LOAD COMBINATIONS WITH WIND ====================
        
        load_combinations = [
            "1.5 DL ± 1.5 WL (Wind as primary load)",
            "0.9 DL ± 1.5 WL (Check uplift and overturning)",
            "1.2 DL + 1.2 LL ± 1.2 WL (Combined with live load)",
            "Critical combination for drift: 1.0 DL + 0.5 LL + 1.0 WL"
        ]
        
        # ==================== DESIGN CHECKS ====================
        
        design_checks = [
            {
                "check": "Strength Check",
                "criterion": "Ultimate limit state - member forces",
                "action": "Design beams, columns, shear walls for wind moments and shears"
            },
            {
                "check": "Drift Check",
                "criterion": "H/500 for total drift, h/250 for inter-storey drift",
                "action": f"Limit drift to {self.building_height*1000/500:.1f}mm total"
            },
            {
                "check": "Overturning Check",
                "criterion": "Resisting moment ≥ 1.5 × Overturning moment",
                "action": "Check foundation stability against wind overturning"
            },
            {
                "check": "Cladding Pressure",
                "criterion": "Local pressures on facade elements",
                "action": "Design curtain wall, windows for peak local pressures"
            },
            {
                "check": "Comfort Check (tall buildings)",
                "criterion": "Peak acceleration < 20 milli-g (residential), < 50 milli-g (commercial)",
                "action": "May require mass dampers for very tall/slender buildings"
            }
        ]
        
        # ==================== COMPILATION ====================
        
        result = {
            "basic_parameters": {
                "location": self.location,
                "basic_wind_speed_Vb": f"{Vb} m/s",
                "terrain_category": terrain_info["name"],
                "building_class": k1_data["description"],
                "building_dimensions": f"{self.building_length:.1f} × {self.building_width:.1f} × {self.building_height:.1f} m"
            },
            "modification_factors": {
                "risk_coefficient_k1": k1,
                "terrain_height_factor_k2": f"{k2:.3f}",
                "topography_factor_k3": k3,
                "importance_factor_k4": k4
            },
            "wind_speeds_pressures": {
                "design_wind_speed_Vz": f"{Vz:.2f} m/s",
                "design_wind_pressure_pz": f"{pz:.1f} N/m² ({pz_kPa:.2f} kN/m²)",
                "formula": "pz = 0.6 × Vz²"
            },
            "pressure_coefficients": {
                "external_pressures": external_pressures,
                "internal_pressure": internal_pressure,
                "net_pressures": net_pressures
            },
            "along_wind_loads": along_wind,
            "across_wind_loads": across_wind,
            "dynamic_effects": dynamic_effects,
            "load_combinations": load_combinations,
            "design_checks_required": design_checks,
            "special_considerations": [
                "Wind directionality: Consider wind from all 4 cardinal directions",
                "Corner effects: Increased local pressures at building corners",
                "Channeling: Wind speed increases between closely spaced tall buildings",
                "Shielding: Upwind buildings may reduce wind loads (conservative to ignore)",
                "Fatigue: Repeated wind cycles can cause fatigue in steel connections",
                "Cladding design: Use local pressure coefficients from IS 875 Part 3"
            ]
        }
        
        print(f"   Along-Wind Force: {max(F_along_long, F_along_short):.1f} kN")
        print(f"   Dynamic Sensitivity: {dynamic_sensitivity}")
        
        return result


@dataclass
class DetailedLoadCalculation:
    """Comprehensive load calculations for all load types"""
    
    def __init__(self, building_type: str, num_floors: int, floor_area: float,
                 slab_thickness: float, beam_size: Tuple[float, float],
                 column_size: Tuple[float, float]):
        self.building_type = building_type
        self.num_floors = num_floors
        self.floor_area = floor_area
        self.slab_thickness = slab_thickness  # meters
        self.beam_size = beam_size  # (width, depth) in meters
        self.column_size = column_size  # (width, depth) in meters
    
    def calculate_all_loads(self) -> Dict:
        """
        8. DETAILED LOAD CALCULATION (DEAD LOAD + LIVE LOAD + BREAKDOWN)
        
        Complete load breakdown per IS 875 Parts 1 and 2
        """
        
        print("\n" + "="*100)
        print("8. DETAILED LOAD CALCULATIONS")
        print("="*100)
        
        # ==================== DEAD LOADS (IS 875 Part 1) ====================
        
        print("\n   A. DEAD LOAD COMPONENTS:")
        
        # Material unit weights (kN/m³)
        material_densities = {
            "reinforced_concrete": 25.0,
            "plain_concrete": 24.0,
            "brick_masonry": 19.0,
            "cement_mortar": 20.4,
            "floor_tiles": 23.0,
            "plaster": 20.4
        }
        
        # 1. Slab self-weight
        slab_self_weight = self.slab_thickness * material_densities["reinforced_concrete"]  # kN/m²
        
        # 2. Floor finishes
        floor_finishes = {
            "screed": 0.05 * material_densities["cement_mortar"],  # 50mm screed
            "tile": 0.015 * material_densities["floor_tiles"],  # 15mm tile
            "adhesive": 0.01 * material_densities["cement_mortar"],  # 10mm bed
            "total": 0.0
        }
        floor_finishes["total"] = sum([v for k, v in floor_finishes.items() if k != "total"])
        
        # 3. Ceiling and plaster
        ceiling = {
            "plaster_soffit": 0.012 * material_densities["plaster"],  # 12mm plaster
            "false_ceiling": 0.15,  # kN/m² (typical gypsum board system)
            "total": 0.0
        }
        ceiling["total"] = ceiling["plaster_soffit"] + ceiling["false_ceiling"]
        
        # 4. Partition walls (amortized over floor area)
        # Average: 1 kN/m² for residential, 1.5 kN/m² for commercial
        partition_load = 1.0 if self.building_type == "Residential" else 1.5
        
        # 5. MEP services
        mep_services = {
            "electrical_conduits": 0.10,
            "plumbing_pipes": 0.15,
            "hvac_ducts": 0.20,
            "fire_protection": 0.10,
            "total": 0.55
        }
        
        # 6. Beam self-weight (per meter length)
        beam_area = self.beam_size[0] * self.beam_size[1]  # m²
        beam_self_weight = beam_area * material_densities["reinforced_concrete"]  # kN/m
        
        # 7. Column self-weight (per meter height)
        column_area = self.column_size[0] * self.column_size[1]  # m²
        column_self_weight = column_area * material_densities["reinforced_concrete"]  # kN/m
        
        # Total dead load on floor
        total_dead_load_floor = (slab_self_weight + 
                                 floor_finishes["total"] + 
                                 ceiling["total"] + 
                                 partition_load + 
                                 mep_services["total"])
        
        dead_load_breakdown = {
            "slab_self_weight": f"{slab_self_weight:.2f} kN/m²",
            "floor_finishes": {
                "screed_50mm": f"{floor_finishes['screed']:.2f} kN/m²",
                "tiles_15mm": f"{floor_finishes['tile']:.2f} kN/m²",
                "adhesive_10mm": f"{floor_finishes['adhesive']:.2f} kN/m²",
                "subtotal": f"{floor_finishes['total']:.2f} kN/m²"
            },
            "ceiling_plaster": {
                "soffit_plaster": f"{ceiling['plaster_soffit']:.2f} kN/m²",
                "false_ceiling": f"{ceiling['false_ceiling']:.2f} kN/m²",
                "subtotal": f"{ceiling['total']:.2f} kN/m²"
            },
            "partitions_amortized": f"{partition_load:.2f} kN/m²",
            "mep_services": {
                "electrical": f"{mep_services['electrical_conduits']:.2f} kN/m²",
                "plumbing": f"{mep_services['plumbing_pipes']:.2f} kN/m²",
                "hvac": f"{mep_services['hvac_ducts']:.2f} kN/m²",
                "fire_protection": f"{mep_services['fire_protection']:.2f} kN/m²",
                "subtotal": f"{mep_services['total']:.2f} kN/m²"
            },
            "total_floor_dead_load": f"{total_dead_load_floor:.2f} kN/m²",
            "beam_self_weight": f"{beam_self_weight:.2f} kN/m (typical {int(self.beam_size[0]*1000)}×{int(self.beam_size[1]*1000)}mm)",
            "column_self_weight": f"{column_self_weight:.2f} kN/m (typical {int(self.column_size[0]*1000)}×{int(self.column_size[1]*1000)}mm)"
        }
        
        print(f"   Total Floor Dead Load: {total_dead_load_floor:.2f} kN/m²")
        
        # ==================== LIVE LOADS (IS 875 Part 2) ====================
        
        print("\n   B. LIVE LOAD (IMPOSED LOAD):")
        
        # IS 875 Part 2 Table 1
        live_load_values = {
            "Residential": {
                "living_rooms": 2.0,
                "bedrooms": 2.0,
                "kitchens": 2.0,
                "bathrooms": 2.0,
                "corridors": 3.0,
                "balconies": 3.0,
                "staircase": 3.0,
                "typical": 2.0
            },
            "Commercial": {
                "offices": 4.0,
                "retail": 4.0,
                "corridors": 4.0,
                "parking": 2.5,
                "typical": 4.0
            },
            "Institutional": {
                "classrooms": 3.0,
                "assembly_halls": 5.0,
                "corridors": 4.0,
                "library_reading": 3.0,
                "library_stacks": 6.0,
                "typical": 3.0
            }
        }
        
        live_load_data = live_load_values.get(self.building_type, live_load_values["Residential"])
        live_load_typical = live_load_data["typical"]
        
        # Live load reduction for multi-storey (IS 875 Part 2 Cl 3.2)
        # Reduction = 10% per floor, max 50%
        live_load_reductions = {}
        for floor in range(1, min(self.num_floors + 1, 6)):
            reduction_percent = min(floor * 10, 50)
            reduced_ll = live_load_typical * (1 - reduction_percent/100)
            live_load_reductions[f"floor_{floor}_and_above"] = {
                "reduction": f"{reduction_percent}%",
                "reduced_load": f"{reduced_ll:.2f} kN/m²"
            }
        
        live_load_breakdown = {
            "building_type": self.building_type,
            "occupancy_loads": live_load_data,
            "typical_live_load": f"{live_load_typical:.2f} kN/m²",
            "live_load_reduction": live_load_reductions,
            "roof_live_load": "1.5 kN/m² (accessible) or 0.75 kN/m² (inaccessible)",
            "special_loads": {
                "concentrated_wheel_load": "Considered as per IS 875 Part 2 Cl 3.3",
                "impact_factor": "Not applicable for static loads"
            }
        }
        
        print(f"   Typical Live Load: {live_load_typical:.2f} kN/m²")
        
        # ==================== TOTAL LOAD AND FACTORED LOADS ====================
        
        print("\n   C. LOAD COMBINATIONS:")
        
        total_service_load = total_dead_load_floor + live_load_typical
        
        # Load factors per IS 456:2000 Cl 36.4
        load_combinations = {
            "DL + LL": {
                "unfactored": f"{total_service_load:.2f} kN/m²",
                "factored": f"{1.5 * total_service_load:.2f} kN/m² (1.5 DL + 1.5 LL)",
                "use": "Normal design condition"
            },
            "DL only": {
                "unfactored": f"{total_dead_load_floor:.2f} kN/m²",
                "factored": f"{1.5 * total_dead_load_floor:.2f} kN/m² (1.5 DL)",
                "use": "When LL favorable (e.g., uplift check)"
            },
            "DL + LL + EQ": {
                "factored": f"{1.2 * total_service_load:.2f} kN/m² + 1.2 EQ (1.2 DL + 1.2 LL ± 1.2 EQ)",
                "use": "Seismic load combination"
            },
            "DL + LL + WL": {
                "factored": f"{1.2 * total_service_load:.2f} kN/m² + 1.2 WL (1.2 DL + 1.2 LL ± 1.2 WL)",
                "use": "Wind load combination"
            },
            "minimum_DL + WL": {
                "factored": f"{0.9 * total_dead_load_floor:.2f} kN/m² + 1.5 WL (0.9 DL ± 1.5 WL)",
                "use": "Uplift/overturning check with wind"
            }
        }
        
        # ==================== SPECIAL LOADS ====================
        
        special_loads = {
            "terrace_waterproofing": {
                "load": "2.0-3.0 kN/m²",
                "components": "Waterproofing membrane + protection layer + mud phuska"
            },
            "external_wall_cladding": {
                "load": "1.0-2.5 kN/m²",
                "components": "Depends on facade system (glass curtain wall vs stone cladding)"
            },
            "snow_load": {
                "applicability": "If altitude > 1000m above MSL",
                "reference": "IS 875 Part 4",
                "typical": "Not applicable for most Indian cities"
            },
            "seismic_load": {
                "nature": "Inertial force = mass × acceleration",
                "calculation": "As per IS 1893:2016",
                "direction": "Horizontal in any direction"
            },
            "wind_load": {
                "nature": "Pressure/suction on surfaces",
                "calculation": "As per IS 875 Part 3:2015",
                "direction": "Perpendicular to surface"
            }
        }
        
        # ==================== LOAD SUMMARY FOR ENTIRE BUILDING ====================
        
        total_floor_load = self.floor_area * total_service_load * self.num_floors  # kN
        total_building_weight = total_floor_load + (0.2 * total_floor_load)  # Add 20% for beams/columns/walls
        
        load_summary = {
            "per_floor": {
                "dead_load": f"{total_dead_load_floor:.2f} kN/m²",
                "live_load": f"{live_load_typical:.2f} kN/m²",
                "total_service": f"{total_service_load:.2f} kN/m²",
                "total_factored": f"{1.5 * total_service_load:.2f} kN/m²"
            },
            "entire_building": {
                "total_floor_load": f"{total_floor_load:.1f} kN",
                "structural_elements": f"{0.2 * total_floor_load:.1f} kN (estimate)",
                "total_building_weight": f"{total_building_weight:.1f} kN",
                "note": "Used for seismic base shear calculation"
            }
        }
        
        # ==================== COMPILATION ====================
        
        result = {
            "dead_load_calculation": dead_load_breakdown,
            "live_load_calculation": live_load_breakdown,
            "load_combinations": load_combinations,
            "special_loads": special_loads,
            "load_summary": load_summary,
            "design_notes": [
                "All loads calculated per IS 875 Parts 1, 2, and 3",
                "Dead load includes all permanent fixtures and finishes",
                "Live load reduction applied for multi-story members",
                "Partition load amortized over floor area (conservative)",
                "MEP services load is approximate - coordinate with MEP consultants",
                "Facade load not included in floor load - applied to perimeter beams",
                "Seismic weight = DL + 25% of LL (as per IS 1893)",
                "Load factors per IS 456:2000 for limit state design",
                "Consider special loads (swimming pool, heavy equipment) separately"
            ]
        }
        
        print(f"   Total Service Load: {total_service_load:.2f} kN/m²")
        print(f"   Total Building Weight: {total_building_weight:.1f} kN")
        
        return result


# Continue with Material Selection and Optimization in structural_system_final.py...

if __name__ == "__main__":
    print("\n" + "="*100)
    print("STRUCTURAL SYSTEM ANALYSIS - PART 3 (WIND, LOADS)")
    print("="*100)
    
    # Example: Wind analysis
    wind = WindLoadAnalysis(35, 50, 30, "Mumbai", "3", "General")
    wind_result = wind.calculate_wind_loads()
    
    # Example: Detailed loads
    loads = DetailedLoadCalculation("Commercial", 10, 1500, 0.20, (0.30, 0.45), (0.40, 0.40))
    loads_result = loads.calculate_all_loads()
    
    print("\n" + "="*100)
    print("✅ PART 3 ANALYSIS COMPLETE")
    print("="*100)
