"""
COMPREHENSIVE STRUCTURAL SYSTEM ANALYSIS - FINAL MODULE

Final components:
9. Material grade selection with detailed engineering justification
10. Structural optimization strategies with quantifiable savings

This completes the comprehensive structural analysis suite.
"""

import numpy as np
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class MaterialGradeSelection:
    """Detailed material grade selection with engineering justification"""
    
    def __init__(self, num_floors: int, column_load: float, span: float,
                 exposure_condition: str, seismic_zone: str, durability_requirement: str):
        self.num_floors = num_floors
        self.column_load = column_load  # kN
        self.span = span  # meters
        self.exposure_condition = exposure_condition
        self.seismic_zone = seismic_zone
        self.durability_requirement = durability_requirement
    
    def select_materials(self) -> Dict:
        """
        9. MATERIAL GRADE SELECTION (CONCRETE AND STEEL) WITH JUSTIFICATION
        
        Selection based on:
        - Structural requirements (strength, ductility)
        - Durability requirements (exposure, cover)
        - Economic considerations
        - Construction feasibility
        - Code requirements (IS 456, IS 13920, IS 1786)
        """
        
        print("\n" + "="*100)
        print("9. MATERIAL GRADE SELECTION")
        print("="*100)
        
        # ==================== CONCRETE GRADE SELECTION ====================
        
        print("\n   A. CONCRETE GRADE SELECTION:")
        
        # Selection criteria based on structural requirements
        
        # 1. Based on building height/floors
        if self.num_floors <= 3:
            height_based_grade = "M20-M25"
            height_reasoning = "Low-rise building with moderate loads"
        elif self.num_floors <= 7:
            height_based_grade = "M25-M30"
            height_reasoning = "Mid-rise building requiring good strength"
        elif self.num_floors <= 15:
            height_based_grade = "M30-M40"
            height_reasoning = "High-rise building with high column loads"
        else:
            height_based_grade = "M40-M50 (M60 for columns)"
            height_reasoning = "Super-tall building requiring high-strength concrete"
        
        # 2. Based on durability/exposure (IS 456:2000 Table 5)
        exposure_requirements = {
            "Mild": {
                "min_grade": "M20",
                "min_cement": "300 kg/m³",
                "max_w_c_ratio": 0.55,
                "min_cover": "20 mm",
                "reasoning": "Interior of buildings, no exposure"
            },
            "Moderate": {
                "min_grade": "M25",
                "min_cement": "300 kg/m³",
                "max_w_c_ratio": 0.50,
                "min_cover": "30 mm (beams/slabs), 40 mm (columns)",
                "reasoning": "Sheltered from rain, moderate humidity"
            },
            "Severe": {
                "min_grade": "M30",
                "min_cement": "320 kg/m³",
                "max_w_c_ratio": 0.45,
                "min_cover": "45 mm",
                "reasoning": "Exposed to rain, coastal (non-saline), industrial"
            },
            "Very_Severe": {
                "min_grade": "M35",
                "min_cement": "340 kg/m³",
                "max_w_c_ratio": 0.40,
                "min_cover": "50 mm (75mm for beams in seawater)",
                "reasoning": "Coastal with saline spray, severe chemicals"
            },
            "Extreme": {
                "min_grade": "M40",
                "min_cement": "360 kg/m³",
                "max_w_c_ratio": 0.35,
                "min_cover": "75 mm",
                "reasoning": "Marine structures, direct seawater contact"
            }
        }
        
        exposure_data = exposure_requirements.get(self.exposure_condition, exposure_requirements["Moderate"])
        
        # 3. Based on column load (stress-based selection)
        # Assume column size 400x400mm, calculate required fck
        assumed_column_area = 0.4 * 0.4  # m²
        axial_stress = self.column_load / (assumed_column_area * 1000)  # N/mm²
        
        # Working stress ≈ 0.25 * fck (conservative)
        required_fck = axial_stress / 0.25
        
        if required_fck <= 20:
            load_based_grade = "M20"
        elif required_fck <= 25:
            load_based_grade = "M25"
        elif required_fck <= 30:
            load_based_grade = "M30"
        elif required_fck <= 40:
            load_based_grade = "M40"
        else:
            load_based_grade = "M50 or higher"
        
        # 4. Based on seismic requirements (IS 13920:2016)
        seismic_grade_requirements = {
            "I": {"min_grade": "M20", "reasoning": "Low seismicity"},
            "II": {"min_grade": "M20", "reasoning": "Low to moderate seismicity"},
            "III": {"min_grade": "M25", "reasoning": "Moderate seismicity - ductile detailing required"},
            "IV": {"min_grade": "M25", "reasoning": "High seismicity - special detailing required"},
            "V": {"min_grade": "M30", "reasoning": "Very high seismicity - highest ductility required"}
        }
        
        seismic_data = seismic_grade_requirements.get(self.seismic_zone, seismic_grade_requirements["III"])
        
        # 5. Based on durability requirements (service life)
        durability_grades = {
            "Standard": {"grade": "M25-M30", "life": "50 years", "reasoning": "Normal structures"},
            "Important": {"grade": "M30-M40", "life": "75-100 years", "reasoning": "Important public buildings"},
            "Monument": {"grade": "M40-M50", "life": "100+ years", "reasoning": "Landmark structures, monuments"}
        }
        
        durability = durability_grades.get(self.durability_requirement, durability_grades["Standard"])
        
        # Determine final recommended grade (take maximum of all requirements)
        all_grades = [height_based_grade, exposure_data["min_grade"], load_based_grade, seismic_data["min_grade"], durability["grade"]]
        
        # Extract numerical values for comparison
        def grade_value(grade_str):
            import re
            numbers = re.findall(r'\d+', grade_str)
            return int(numbers[0]) if numbers else 20
        
        max_grade_value = max([grade_value(g) for g in all_grades])
        
        if max_grade_value <= 20:
            recommended_concrete = "M20"
        elif max_grade_value <= 25:
            recommended_concrete = "M25"
        elif max_grade_value <= 30:
            recommended_concrete = "M30"
        elif max_grade_value <= 40:
            recommended_concrete = "M40"
        else:
            recommended_concrete = "M50"
        
        # Concrete grade breakdown for different elements
        concrete_grades_by_element = {
            "foundation": {
                "grade": "M25-M30",
                "reasoning": "Foundation requires good durability + higher cover, M25 minimum per IS 456"
            },
            "columns_lower_floors": {
                "grade": f"M{max(30, max_grade_value)}",
                "reasoning": "High axial loads require higher strength, typically M30-M50"
            },
            "columns_upper_floors": {
                "grade": f"M{max(25, max_grade_value-10)}",
                "reasoning": "Reduced loads allow lower grade, typically M25-M40"
            },
            "beams": {
                "grade": recommended_concrete,
                "reasoning": "Flexural members, grade matches column grade for monolithic construction"
            },
            "slabs": {
                "grade": recommended_concrete,
                "reasoning": "Same grade as beams for construction convenience"
            },
            "shear_walls": {
                "grade": f"M{max(30, max_grade_value)}",
                "reasoning": "Critical for lateral stability, M30 minimum recommended"
            }
        }
        
        # Concrete properties comparison table
        concrete_properties = {
            "M20": {"fck": 20, "fck_cube": 20, "Ec": 22360, "density": 25, "cost_relative": 1.00},
            "M25": {"fck": 25, "fck_cube": 25, "Ec": 25000, "density": 25, "cost_relative": 1.08},
            "M30": {"fck": 30, "fck_cube": 30, "Ec": 27386, "density": 25, "cost_relative": 1.15},
            "M40": {"fck": 40, "fck_cube": 40, "Ec": 31622, "density": 25, "cost_relative": 1.30},
            "M50": {"fck": 50, "fck_cube": 50, "Ec": 35355, "density": 25, "cost_relative": 1.50}
        }
        
        concrete_selection = {
            "selection_criteria": {
                "height_based": {"grade": height_based_grade, "reasoning": height_reasoning},
                "exposure_based": exposure_data,
                "load_based": {"grade": load_based_grade, "required_fck": f"{required_fck:.1f} N/mm²"},
                "seismic_based": seismic_data,
                "durability_based": durability
            },
            "recommended_grade": recommended_concrete,
            "grade_by_element": concrete_grades_by_element,
            "properties_comparison": concrete_properties,
            "mix_design_requirements": {
                "characteristic_strength": f"{max_grade_value} N/mm² at 28 days",
                "target_strength": f"{max_grade_value + 1.65 * 5:.1f} N/mm² (fck + 1.65σ)",
                "cement_type": "OPC 43 or 53 grade",
                "aggregates": "20mm and 10mm down graded aggregates",
                "admixtures": "Superplasticizer for M40+, retarder in hot weather",
                "curing": "Water curing for 14 days minimum (21 days for M40+)"
            },
            "special_concretes": {
                "high_performance_concrete": {
                    "grade": "M60-M80",
                    "use": "Columns in super-tall buildings",
                    "advantages": "Reduced column sizes, higher stiffness",
                    "cost_premium": "50-80% more than M30"
                },
                "self_compacting_concrete": {
                    "use": "Densely reinforced sections, complex geometries",
                    "advantages": "No vibration needed, better finish",
                    "cost_premium": "20-30% more than conventional"
                },
                "lightweight_concrete": {
                    "grade": "M20-M40 with expanded clay/shale",
                    "use": "Reduce dead load in long spans",
                    "advantages": "20-30% weight reduction",
                    "limitations": "Lower modulus of elasticity"
                }
            }
        }
        
        print(f"   Recommended Concrete Grade: {recommended_concrete}")
        print(f"   Governing Criteria: {max([h for h in all_grades if grade_value(h) == max_grade_value][0])}")
        
        # ==================== STEEL GRADE SELECTION ====================
        
        print("\n   B. REINFORCEMENT STEEL GRADE SELECTION:")
        
        # Steel grade options per IS 1786:2008
        steel_grades_available = {
            "Fe 415": {
                "fy": 415,
                "fu": 485,
                "elongation": "14.5% minimum",
                "use": "General construction, low to mid-rise",
                "availability": "Widely available",
                "cost_relative": 1.00
            },
            "Fe 500": {
                "fy": 500,
                "fu": 545,
                "elongation": "12% minimum",
                "use": "High-rise buildings, where steel savings needed",
                "availability": "Commonly available",
                "cost_relative": 1.05
            },
            "Fe 550": {
                "fy": 550,
                "fu": 585,
                "elongation": "10% minimum",
                "use": "Heavy industrial, very high-rise",
                "availability": "Available in major cities",
                "cost_relative": 1.10
            },
            "Fe 600": {
                "fy": 600,
                "fu": 660,
                "elongation": "10% minimum",
                "use": "Specialized applications, precast",
                "availability": "Limited availability",
                "cost_relative": 1.15
            }
        }
        
        # Selection based on seismic requirements
        if self.seismic_zone in ["IV", "V"]:
            seismic_steel_req = "Fe 415 or Fe 500 with ductility requirements per IS 13920"
            ductility_note = "Higher ductility crucial - Fe 415 preferred for better elongation"
        elif self.seismic_zone == "III":
            seismic_steel_req = "Fe 415/Fe 500 both acceptable"
            ductility_note = "Moderate ductility detailing required"
        else:
            seismic_steel_req = "Any grade acceptable"
            ductility_note = "Ductility not critical"
        
        # Selection based on economy
        # Higher grade steel reduces steel tonnage but costs slightly more
        if self.num_floors <= 5:
            economic_steel = "Fe 415"
            economic_reason = "Lower cost per ton, adequate for low-rise"
        elif self.num_floors <= 15:
            economic_steel = "Fe 500"
            economic_reason = "15-20% steel savings compared to Fe 415, justifies cost premium"
        else:
            economic_steel = "Fe 500/Fe 550"
            economic_reason = "Significant steel savings in heavily loaded members"
        
        # Selection based on member type
        steel_by_member = {
            "columns_main_bars": {
                "recommended": "Fe 500",
                "reasoning": "High axial loads benefit from higher strength",
                "typical_bars": "16mm, 20mm, 25mm, 32mm diameter"
            },
            "columns_ties": {
                "recommended": "Fe 415",
                "reasoning": "Confinement steel - ductility more important than strength",
                "typical_bars": "8mm, 10mm diameter"
            },
            "beams_main_bars": {
                "recommended": "Fe 500",
                "reasoning": "Steel savings in flexural reinforcement",
                "typical_bars": "12mm, 16mm, 20mm, 25mm diameter"
            },
            "beams_stirrups": {
                "recommended": "Fe 415",
                "reasoning": "Better ductility for shear reinforcement",
                "typical_bars": "8mm, 10mm diameter"
            },
            "slabs": {
                "recommended": "Fe 500",
                "reasoning": "Reduce bar sizes or increase spacing",
                "typical_bars": "8mm, 10mm, 12mm diameter"
            },
            "shear_walls": {
                "recommended": "Fe 500",
                "reasoning": "Both flexural and shear reinforcement",
                "typical_bars": "12mm, 16mm, 20mm (vertical), 10mm, 12mm (horizontal)"
            }
        }
        
        # Corrosion protection
        corrosion_protection = {
            "standard_bars": {
                "type": "Black TMT bars (Thermo-Mechanically Treated)",
                "protection": "Concrete cover + alkaline environment",
                "suitable_for": "Mild to moderate exposure"
            },
            "epoxy_coated": {
                "type": "Fusion-bonded epoxy coated rebars",
                "protection": "Epoxy coating 175-300 microns",
                "suitable_for": "Severe to very severe exposure (coastal)",
                "cost_premium": "40-60% more than black bars"
            },
            "galvanized": {
                "type": "Hot-dip galvanized rebars",
                "protection": "Zinc coating 600-1000 microns",
                "suitable_for": "Very severe to extreme exposure",
                "cost_premium": "80-100% more than black bars"
            },
            "stainless_steel": {
                "type": "Austenitic stainless steel (Grade 304/316)",
                "protection": "Inherent corrosion resistance",
                "suitable_for": "Extreme exposure, critical structures",
                "cost_premium": "400-600% more than black bars"
            }
        }
        
        # Final steel recommendation
        if self.seismic_zone in ["IV", "V"]:
            recommended_steel = "Fe 415 (for ductility in seismic zones)"
        elif self.num_floors > 10:
            recommended_steel = "Fe 500 (for economy in high-rise)"
        else:
            recommended_steel = "Fe 415/Fe 500 (both suitable)"
        
        steel_selection = {
            "available_grades": steel_grades_available,
            "seismic_requirements": {
                "recommended": seismic_steel_req,
                "ductility_note": ductility_note,
                "code_reference": "IS 13920:2016 Cl 5.2"
            },
            "economic_considerations": {
                "recommended": economic_steel,
                "reasoning": economic_reason,
                "steel_savings_Fe500_vs_Fe415": "15-20% (due to higher fy)"
            },
            "by_structural_element": steel_by_member,
            "recommended_grade": recommended_steel,
            "corrosion_protection_options": corrosion_protection,
            "special_steels": {
                "prestressing_steel": {
                    "type": "High-tensile steel wire/strand",
                    "strength": "1500-1860 N/mm²",
                    "use": "Post-tensioned slabs, prestressed beams",
                    "standard": "IS 6006"
                },
                "structural_steel": {
                    "type": "Mild steel plates/sections",
                    "grade": "IS 2062 Grade A/B/C",
                    "use": "Steel beams, columns, connections",
                    "typical_fy": "250 N/mm² (Grade A), 350 N/mm² (Grade C)"
                }
            },
            "quality_control": {
                "testing": "Tensile test every 25 tonnes or per IS 1786",
                "certification": "Test certificates from manufacturer mandatory",
                "storage": "Protect from rust - store above ground, cover in rain",
                "bending": "Cold bending - no heat bending allowed",
                "splicing": "Lap splices or mechanical couplers per IS 13920"
            }
        }
        
        print(f"   Recommended Steel Grade: {recommended_steel}")
        print(f"   Seismic Requirement: {seismic_steel_req}")
        
        # ==================== COST COMPARISON ====================
        
        # Approximate material costs (these vary by location and time)
        material_costs = {
            "concrete": {
                "M20": "₹5,000-5,500/m³",
                "M25": "₹5,400-6,000/m³",
                "M30": "₹5,800-6,500/m³",
                "M40": "₹6,500-7,500/m³",
                "M50": "₹7,500-8,500/m³"
            },
            "steel": {
                "Fe 415": "₹55,000-60,000/tonne",
                "Fe 500": "₹58,000-63,000/tonne",
                "Fe 550": "₹60,000-65,000/tonne"
            },
            "note": "Costs are approximate and vary with time, location, and market conditions"
        }
        
        # ==================== COMPILATION ====================
        
        result = {
            "concrete_selection": concrete_selection,
            "steel_selection": steel_selection,
            "cost_comparison": material_costs,
            "summary_recommendations": {
                "primary_concrete_grade": recommended_concrete,
                "column_concrete_lower_floors": concrete_grades_by_element["columns_lower_floors"]["grade"],
                "beam_slab_concrete": concrete_grades_by_element["beams"]["grade"],
                "foundation_concrete": "M25-M30",
                "primary_steel_grade": recommended_steel,
                "main_reinforcement": steel_by_member["beams_main_bars"]["recommended"],
                "ties_stirrups": steel_by_member["beams_stirrups"]["recommended"]
            },
            "value_engineering_tips": [
                "Use higher strength concrete in lower columns only (tapered strength)",
                "Use Fe 500 for main bars (15-20% steel savings)",
                "Use Fe 415 for ties/stirrups (better ductility, lower cost)",
                "Consider fly ash concrete (30-40% cement replacement)",
                "Use ready-mix concrete for quality and speed",
                "Optimize bar curtailment in beams (avoid full-length bars)",
                "Use mechanical couplers instead of laps in congested areas",
                "Standardize bar diameters (reduce cutting waste)"
            ],
            "sustainability_considerations": [
                "Fly ash 30-40% reduces carbon footprint by 25-30%",
                "GGBS (Ground Granulated Blast Furnace Slag) up to 50%",
                "Recycled aggregates for non-structural concrete",
                "Use regional materials to reduce transportation emissions",
                "Consider life-cycle cost, not just initial cost",
                "High-strength concrete reduces material volume"
            ]
        }
        
        return result


@dataclass  
class StructuralOptimization:
    """Comprehensive structural optimization strategies"""
    
    def __init__(self, project_cost: float, building_type: str, num_floors: int,
                 structural_system: str):
        self.project_cost = project_cost
        self.building_type = building_type
        self.num_floors = num_floors
        self.structural_system = structural_system
    
    def identify_optimizations(self) -> Dict:
        """
        10. STRUCTURAL OPTIMIZATION STRATEGIES WITH QUANTIFIABLE SAVINGS
        
        Comprehensive optimization across design, material, construction, and lifecycle
        All savings are approximate and depend on project specifics
        """
        
        print("\n" + "="*100)
        print("10. STRUCTURAL OPTIMIZATION STRATEGIES")
        print("="*100)
        
        # ==================== DESIGN OPTIMIZATION ====================
        
        print("\n   A. DESIGN OPTIMIZATION:")
        
        design_optimizations = {
            "1_grid_rationalization": {
                "strategy": "Regularize column grid, eliminate grid offsets",
                "impact": "Formwork reuse, construction speed",
                "potential_savings": "8-12% on formwork costs",
                "implementation": [
                    "Use consistent bay sizes throughout building",
                    "Minimize column size variations (3-4 sizes max)",
                    "Avoid column offsets between floors",
                    "Align grid with architectural module (300mm)"
                ],
                "quantified_saving": f"${self.project_cost * 0.04:.0f} (4% of project cost)"
            },
            "2_beam_depth_optimization": {
                "strategy": "Optimize beam depth to minimum required",
                "impact": "Reduced concrete volume, lower building height",
                "potential_savings": "5-8% on concrete volume",
                "implementation": [
                    "Use span-depth ratio limits (L/12 to L/15)",
                    "Consider two-way slabs to reduce beam sizes",
                    "Use drop beams instead of wide shallow beams",
                    "Coordinate with MEP for depth constraints"
                ],
                "quantified_saving": f"${self.project_cost * 0.025:.0f} (2.5% average)"
            },
            "3_column_size_optimization": {
                "strategy": "Use high-strength concrete to reduce column sizes",
                "impact": "Smaller columns, more usable area",
                "potential_savings": "10-15% reduction in column size",
                "implementation": [
                    "Use M40-M50 in lower floors instead of M30",
                    "Reduce column size by ~20% with higher grade",
                    "Gain 0.5-1% more carpet area",
                    "Pay ~20% premium on concrete, save on col size"
                ],
                "quantified_saving": f"${self.project_cost * 0.015:.0f} (1.5% net benefit)",
                "additional_benefit": f"Gain {self.num_floors * 30 * 0.01:.1f} m² carpet area"
            },
            "4_slab_system_optimization": {
                "strategy": "Use efficient slab systems for longer spans",
                "impact": "Reduced slab thickness, fewer beams",
                "potential_savings": "10-20% on floor structure",
                "options": {
                    "conventional_slab": "baseline",
                    "flat_slab": "10-15% savings on formwork, faster construction",
                    "post_tensioned_slab": "15-20% thinner slab, longer spans",
                    "hollow_core_slab": "30% lighter, faster erection"
                },
                "quantified_saving": f"${self.project_cost * 0.06:.0f} (6% with PT slab)"
            },
            "5_foundation_optimization": {
                "strategy": "Optimize foundation type based on soil",
                "impact": "Right foundation for soil conditions",
                "potential_savings": "15-25% on foundation cost",
                "decision_matrix": {
                    "good_soil": "Isolated footings (least cost)",
                    "moderate_soil": "Combined footings or strip footings",
                    "poor_soil": "Raft foundation (economical for many columns)",
                    "very_poor": "Piled foundation (necessary but expensive)"
                },
                "quantified_saving": f"${self.project_cost * 0.03:.0f} (3% of project)"
            }
        }
        
        # ==================== MATERIAL OPTIMIZATION ====================
        
        print("\n   B. MATERIAL OPTIMIZATION:")
        
        material_optimizations = {
            "1_cement_replacement": {
                "strategy": "Replace cement with fly ash/GGBS",
                "impact": "Lower cost, lower carbon footprint",
                "potential_savings": "15-20% on cement cost",
                "implementation": [
                    "Use 30-40% fly ash in M25-M40 concrete",
                    "Use up to 50% GGBS in coastal areas (better durability)",
                    "Adjust mix design for workability",
                    "Extend curing period by 3-5 days"
                ],
                "quantified_saving": f"${self.project_cost * 0.02:.0f} (2% of project cost)",
                "co2_reduction": "25-30% reduction in embodied carbon"
            },
            "2_steel_grade_upgrade": {
                "strategy": "Use Fe 500 instead of Fe 415 for main bars",
                "impact": "15-20% reduction in steel tonnage",
                "potential_savings": "10-12% on steel cost (net)",
                "calculation": [
                    "Fe 500 costs 5% more per tonne",
                    "But 18% less tonnage needed",
                    "Net savings: 18% - 5% = 13%"
                ],
                "quantified_saving": f"${self.project_cost * 0.025:.0f} (2.5% of project)",
                "note": "Applicable to main bars, not ties/stirrups"
            },
            "3_recycled_aggregates": {
                "strategy": "Use recycled aggregates for non-structural elements",
                "impact": "Lower aggregate cost, sustainability",
                "potential_savings": "8-10% on aggregate cost",
                "implementation": [
                    "Use in plinth beams, boundary walls",
                    "Use in pavements, non-structural masonry",
                    "Not recommended for structural concrete",
                    "Ensure proper crushing and grading"
                ],
                "quantified_saving": f"${self.project_cost * 0.01:.0f} (1% of project)"
            },
            "4_admixture_optimization": {
                "strategy": "Use admixtures for performance enhancement",
                "impact": "Better workability, strength, durability",
                "types": {
                    "superplasticizer": "10-15% cement reduction for same strength",
                    "retarder": "Avoids cold joints, better in hot weather",
                    "accelerator": "Early strength gain, faster construction",
                    "waterproofing": "Integral waterproofing for basements"
                },
                "quantified_saving": f"${self.project_cost * 0.015:.0f} (1.5% net benefit)"
            }
        }
        
        # ==================== CONSTRUCTION OPTIMIZATION ====================
        
        print("\n   C. CONSTRUCTION OPTIMIZATION:")
        
        construction_optimizations = {
            "1_formwork_system": {
                "strategy": "Use modern formwork systems for repetitive floors",
                "impact": "Faster construction, better quality, fewer workers",
                "potential_savings": "20-25% on formwork cost",
                "options": {
                    "conventional_timber": "baseline (100%)",
                    "steel_props_plywood": "10% faster, 5% cost savings",
                    "table_forms": "20-25% cost savings, 30% faster",
                    "aluminum_formwork": "35-40% cost savings, 50% faster (for >50 reuses)"
                },
                "quantified_saving": f"${self.project_cost * 0.05:.0f} (5% with table forms)",
                "note": "Aluminum formwork needs 50+ reuses to justify"
            },
            "2_precast_elements": {
                "strategy": "Use precast for stairs, façade, bathroom pods",
                "impact": "Faster construction, better quality control",
                "potential_savings": "15-20% on construction time",
                "elements": {
                    "precast_stairs": "40% faster than cast-in-place",
                    "precast_facade_panels": "30% faster installation",
                    "bathroom_pods": "50% faster, better waterproofing",
                    "precast_beams": "Suitable for industrial buildings"
                },
                "quantified_saving": f"${self.project_cost * 0.03:.0f} (3% + time savings)"
            },
            "3_construction_sequencing": {
                "strategy": "Optimize construction sequence and logistics",
                "impact": "Reduced idle time, better resource utilization",
                "potential_savings": "10-15% on project duration",
                "implementation": [
                    "Parallel work on multiple floors",
                    "Just-in-time material delivery",
                    "Overlap structural and MEP works",
                    "Use critical path method (CPM) scheduling"
                ],
                "quantified_saving": f"${self.project_cost * 0.04:.0f} (4% from time savings)"
            },
            "4_quality_control": {
                "strategy": "Robust QC to avoid rework and repairs",
                "impact": "Fewer defects, lower lifecycle costs",
                "potential_savings": "5-8% (avoiding rework)",
                "implementation": [
                    "Cube testing every pour (1 sample per 100 m³)",
                    "Bar bending schedule adherence",
                    "Cover block placement (maintain cover)",
                    "Joint waterstops in basements",
                    "Third-party inspection for critical elements"
                ],
                "quantified_saving": f"${self.project_cost * 0.02:.0f} (2% average)"
            }
        }
        
        # ==================== VALUE ENGINEERING ====================
        
        print("\n   D. VALUE ENGINEERING:")
        
        value_engineering = {
            "1_design_stage_VE": {
                "phase": "Schematic Design (SD)",
                "potential_savings": "15-20% (highest impact phase)",
                "focus_areas": [
                    "Structural system selection (frame vs wall vs hybrid)",
                    "Grid optimization and span rationalization",
                    "Foundation type based on detailed soil investigation",
                    "Building height optimization (balance floors vs height)"
                ],
                "process": "Multi-disciplinary workshop with architect, structural, MEP, contractor"
            },
            "2_DD_stage_VE": {
                "phase": "Design Development (DD)",
                "potential_savings": "8-12%",
                "focus_areas": [
                    "Member sizing optimization",
                    "Material grade selection",
                    "Construction methodology review",
                    "Prefabrication opportunities"
                ],
                "process": "Iterative design optimization with cost tracking"
            },
            "3_CD_stage_VE": {
                "phase": "Construction Documents (CD)",
                "potential_savings": "3-5%",
                "focus_areas": [
                    "Bar detailing optimization (curtailment)",
                    "Specification review (avoid over-specification)",
                    "Constructability review",
                    "Value alternatives in bid documents"
                ],
                "process": "Final review before tender"
            },
            "total_VE_potential": f"${self.project_cost * 0.15:.0f} (15% cumulative across all phases)"
        }
        
        # ==================== LIFECYCLE OPTIMIZATION ====================
        
        print("\n   E. LIFECYCLE COST OPTIMIZATION:")
        
        lifecycle_optimization = {
            "durability_upgrade": {
                "investment": "Add 5-8% upfront for better materials",
                "benefit": "50% reduction in maintenance over 50 years",
                "lifecycle_saving": "20-30% total lifecycle cost",
                "measures": [
                    "Higher concrete grade (better durability)",
                    "Extra cover + epoxy coating in coastal areas",
                    "Integral waterproofing instead of membrane",
                    "Better quality sealants and expansion joints"
                ],
                "payback_period": "10-15 years"
            },
            "energy_efficiency": {
                "investment": "5-10% for envelope optimization",
                "benefit": "25-30% reduction in HVAC energy",
                "lifecycle_saving": "Payback in 5-8 years",
                "measures": [
                    "Thermal insulation (walls and roof)",
                    "High-performance glazing (low-E, double-glazed)",
                    "Shading devices (external, movable)",
                    "Thermal mass optimization"
                ],
                "annual_energy_saving": f"${self.project_cost * 0.002:.0f}/year"
            },
            "adaptability": {
                "investment": "2-4% for flexible design",
                "benefit": "Easier future modifications, higher resale value",
                "measures": [
                    "Larger spans for layout flexibility",
                    "Flat slab for reconfiguration ease",
                    "Extra capacity in MEP systems (20% headroom)",
                    "Modular partition systems"
                ],
                "value_addition": "10-15% higher property value"
            }
        }
        
        # ==================== TOTAL OPTIMIZATION POTENTIAL ====================
        
        total_savings_potential = {
            "design_optimization": 0.08,  # 8%
            "material_optimization": 0.05,  # 5%
            "construction_optimization": 0.10,  # 10%
            "value_engineering": 0.15,  # 15%
            "lifecycle_optimization": 0.25  # 25% (over lifecycle)
        }
        
        total_first_cost_saving = sum([v for k, v in total_savings_potential.items() if k != "lifecycle_optimization"])
        total_first_cost_saving_amount = self.project_cost * total_first_cost_saving
        
        lifecycle_saving = self.project_cost * 2.5 * total_savings_potential["lifecycle_optimization"]  # Assume lifecycle cost = 2.5x first cost
        
        optimization_summary = {
            "first_cost_savings": {
                "design": f"${self.project_cost * 0.08:.0f} (8%)",
                "materials": f"${self.project_cost * 0.05:.0f} (5%)",
                "construction": f"${self.project_cost * 0.10:.0f} (10%)",
                "value_engineering": f"${self.project_cost * 0.15:.0f} (15%)",
                "subtotal": f"${total_first_cost_saving_amount:.0f} ({total_first_cost_saving*100:.0f}% of first cost)"
            },
            "lifecycle_savings": {
                "durability_upgrade_savings": f"${lifecycle_saving * 0.4:.0f}",
                "energy_efficiency_savings": f"${lifecycle_saving * 0.4:.0f}",
                "adaptability_value_addition": f"${lifecycle_saving * 0.2:.0f}",
                "subtotal": f"${lifecycle_saving:.0f} (over 50-year life)"
            },
            "total_optimization_potential": f"${total_first_cost_saving_amount + lifecycle_saving:.0f}",
            "note": "Actual savings depend on project specifics, market conditions, and execution quality"
        }
        
        # ==================== IMPLEMENTATION ROADMAP ====================
        
        implementation_roadmap = {
            "schematic_design": [
                "✓ Optimize structural system selection",
                "✓ Rationalize grid layout",
                "✓ Select foundation type based on soil report",
                "✓ Conduct VE workshop #1"
            ],
            "design_development": [
                "✓ Optimize member sizes (beams, columns, slabs)",
                "✓ Select material grades",
                "✓ Evaluate precast opportunities",
                "✓ Conduct VE workshop #2"
            ],
            "construction_documents": [
                "✓ Optimize bar detailing and curtailment",
                "✓ Review specifications (avoid over-spec)",
                "✓ Prepare constructability review",
                "✓ Finalize bid alternates"
            ],
            "procurement": [
                "✓ Early contractor involvement (if design-build)",
                "✓ Bulk material procurement for better rates",
                "✓ Pre-qualification of suppliers",
                "✓ Negotiate price escalation clauses"
            ],
            "construction": [
                "✓ Use modern formwork systems",
                "✓ Implement robust QC procedures",
                "✓ Monitor and control material waste",
                "✓ Optimize construction sequencing"
            ]
        }
        
        # ==================== COMPILATION ====================
        
        result = {
            "design_optimizations": design_optimizations,
            "material_optimizations": material_optimizations,
            "construction_optimizations": construction_optimizations,
            "value_engineering_process": value_engineering,
            "lifecycle_cost_optimization": lifecycle_optimization,
            "optimization_summary": optimization_summary,
            "implementation_roadmap": implementation_roadmap,
            "key_recommendations": [
                "Start VE from schematic design - biggest impact",
                "Use higher-strength materials strategically (not everywhere)",
                "Invest in good formwork for repetitive work",
                "Don't compromise on durability - lifecycle cost matters",
                "Engage contractor early if possible (design-build/CM)",
                "Use BIM for clash detection and quantity optimization",
                "Regular design reviews with cost tracking",
                "Consider both first cost and lifecycle cost"
            ],
            "risk_mitigation": [
                "Don't over-optimize - maintain adequate safety factors",
                "Peer review critical optimizations",
                "Avoid unfamiliar technologies without proper expertise",
                "Budget 10-15% contingency for uncertainties",
                "Document all optimization decisions and assumptions"
            ]
        }
        
        print(f"\n   Total First Cost Savings Potential: ${total_first_cost_saving_amount:.0f} ({total_first_cost_saving*100:.0f}%)")
        print(f"   Total Lifecycle Savings Potential: ${lifecycle_saving:.0f}")
        
        return result


if __name__ == "__main__":
    print("\n" + "="*100)
    print("STRUCTURAL SYSTEM ANALYSIS - FINAL MODULE (MATERIALS & OPTIMIZATION)")
    print("="*100)
    
    # Example: Material selection
    materials = MaterialGradeSelection(
        num_floors=10,
        column_load=5000,  # kN
        span=7.5,  # m
        exposure_condition="Severe",
        seismic_zone="III",
        durability_requirement="Standard"
    )
    material_result = materials.select_materials()
    
    # Example: Optimization strategies
    optimization = StructuralOptimization(
        project_cost=5000000,  # $5M
        building_type="Commercial",
        num_floors=10,
        structural_system="Dual System"
    )
    optimization_result = optimization.identify_optimizations()
    
    print("\n" + "="*100)
    print("✅ COMPLETE STRUCTURAL ANALYSIS SUITE FINISHED")
    print("="*100)
    print("\nAll 10 modules implemented:")
    print("  1. ✓ Structural grid spacing")
    print("  2. ✓ Column sizes per floor")
    print("  3. ✓ Beam sizing logic")
    print("  4. ✓ Slab thickness calculation")
    print("  5. ✓ Lateral load resisting system")
    print("  6. ✓ Seismic design")
    print("  7. ✓ Wind load analysis")
    print("  8. ✓ Detailed load calculations")
    print("  9. ✓ Material grade selection")
    print(" 10. ✓ Structural optimization")
    print("\n" + "="*100 + "\n")
