"""
COMPREHENSIVE STRUCTURAL DESIGN SYSTEM - COMPLETE DEMONSTRATION

This script demonstrates all 10 aspects of deep structural system analysis:
1. Structural grid spacing with justification
2. Column sizes per floor
3. Beam sizing logic
4. Slab thickness calculation
5. Lateral load resisting system
6. Seismic design
7. Wind load analysis
8. Detailed load calculations
9. Material grade selection
10. Structural optimization

Run this to see complete engineering analysis with calculations and justifications.
"""

import json
from datetime import datetime

# Import all modules
from structural_system_detailed import (
    StructuralGridAnalysis,
    ColumnSizingAnalysis,
    BeamSizingLogic,
    SlabThicknessCalculation
)
from structural_system_detailed_part2 import (
    LateralLoadResistingSystem,
    SeismicDesignAnalysis
)
from structural_system_detailed_part3 import (
    WindLoadAnalysis,
    DetailedLoadCalculation
)
from structural_system_final_materials_optimization import (
    MaterialGradeSelection,
    StructuralOptimization
)


def print_section_header(title: str):
    """Print formatted section header"""
    print("\n" + "="*100)
    print(f" {title}")
    print("="*100)


def save_complete_report(results: dict, filename: str = None):
    """Save complete analysis to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"complete_structural_analysis_{timestamp}.json"
    
    # Convert any non-serializable values
    def clean_for_json(obj):
        if isinstance(obj, dict):
            return {k: clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [clean_for_json(item) for item in obj]
        else:
            return str(obj) if not isinstance(obj, (str, int, float, bool, type(None))) else obj
    
    cleaned_results = clean_for_json(results)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_results, f, indent=2, ensure_ascii=False)
    
    return filename


def run_complete_structural_analysis(
    # Building parameters
    plot_length: float = 50.0,
    plot_width: float = 30.0,
    num_floors: int = 10,
    floor_height: float = 3.5,
    building_type: str = "Commercial",
    
    # Location and environment
    location: str = "Mumbai",
    climate_zone: str = "Tropical",
    seismic_zone: str = "III",
    soil_type: str = "Sand",
    terrain_category: str = "3",
    exposure_condition: str = "Severe",
    
    # Building class and requirements
    building_class: str = "General",
    durability_requirement: str = "Standard",
    importance_factor: float = 1.0,
    
    # Project cost
    project_cost: float = 5000000
):
    """
    Run complete structural analysis with all 10 aspects
    
    Returns dictionary with all analysis results
    """
    
    print_section_header("🏗️  COMPREHENSIVE STRUCTURAL DESIGN SYSTEM - COMPLETE ANALYSIS")
    
    print(f"""
PROJECT PARAMETERS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Building Type:          {building_type}
Plot Dimensions:        {plot_length} m × {plot_width} m ({plot_length * plot_width:.0f} m²)
Number of Floors:       {num_floors}
Floor Height:           {floor_height} m
Total Height:           {num_floors * floor_height:.1f} m

Location:               {location}
Climate Zone:           {climate_zone}
Seismic Zone:           {seismic_zone}
Soil Type:              {soil_type}
Exposure:               {exposure_condition}

Project Cost:           ${project_cost:,.0f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    # Dictionary to store all results
    complete_results = {
        "project_info": {
            "timestamp": datetime.now().isoformat(),
            "building_type": building_type,
            "plot_dimensions": f"{plot_length}m × {plot_width}m",
            "num_floors": num_floors,
            "total_height": num_floors * floor_height,
            "location": location,
            "seismic_zone": seismic_zone
        }
    }
    
    # ==================== 1. STRUCTURAL GRID ====================
    
    print_section_header("MODULE 1: STRUCTURAL GRID SPACING ANALYSIS")
    
    grid_analysis = StructuralGridAnalysis(
        plot_length=plot_length,
        plot_width=plot_width,
        building_type=building_type,
        num_floors=num_floors,
        seismic_zone=seismic_zone
    )
    
    grid_result = grid_analysis.design_optimal_grid()
    complete_results["1_structural_grid"] = grid_result
    
    # Extract key metrics for subsequent calculations
    num_bays_length = grid_result["grid_geometry"]["bays_in_length"]
    num_bays_width = grid_result["grid_geometry"]["bays_in_width"]
    total_columns = grid_result["grid_geometry"]["total_columns_per_floor"]
    span_length = float(grid_result["grid_geometry"]["span_length_direction"].split()[0])
    span_width = float(grid_result["grid_geometry"]["span_width_direction"].split()[0])
    avg_span = (span_length + span_width) / 2
    
    # ==================== 2. COLUMN SIZING ====================
    
    print_section_header("MODULE 2: COLUMN SIZING PER FLOOR")
    
    floor_area = plot_length * plot_width
    
    column_analysis = ColumnSizingAnalysis(
        num_floors=num_floors,
        floor_area=floor_area,
        num_columns=total_columns,
        seismic_zone=seismic_zone,
        building_type=building_type,
        span_avg=avg_span
    )
    
    column_result = column_analysis.calculate_column_sizes()
    complete_results["2_column_sizing"] = column_result
    
    # ==================== 3. BEAM SIZING ====================
    
    print_section_header("MODULE 3: BEAM SIZING LOGIC")
    
    beam_analysis = BeamSizingLogic(
        span_length=span_length,
        span_width=span_width,
        building_type=building_type,
        num_floors=num_floors
    )
    
    beam_result = beam_analysis.design_beams()
    complete_results["3_beam_sizing"] = beam_result
    
    # Extract beam dimensions
    beam_width = float(beam_result["primary_beams"]["dimensions"]["width"].split()[0]) / 1000  # Convert to meters
    beam_depth = float(beam_result["primary_beams"]["dimensions"]["overall_depth"].split()[0]) / 1000
    
    # ==================== 4. SLAB THICKNESS ====================
    
    print_section_header("MODULE 4: SLAB THICKNESS CALCULATION")
    
    slab_analysis = SlabThicknessCalculation(
        span_length=span_length,
        span_width=span_width,
        building_type=building_type,
        support_conditions="continuous"
    )
    
    slab_result = slab_analysis.calculate_slab_thickness()
    complete_results["4_slab_thickness"] = slab_result
    
    # Extract slab thickness
    slab_thickness = float(slab_result["recommended_thickness"]["final_thickness"].split()[0]) / 1000  # Convert to meters
    
    # ==================== 5. LATERAL LOAD SYSTEM ====================
    
    print_section_header("MODULE 5: LATERAL LOAD RESISTING SYSTEM")
    
    lateral_system = LateralLoadResistingSystem(
        num_floors=num_floors,
        floor_height=floor_height,
        building_length=plot_length,
        building_width=plot_width,
        seismic_zone=seismic_zone,
        building_type=building_type
    )
    
    lateral_result = lateral_system.design_lateral_system()
    complete_results["5_lateral_load_system"] = lateral_result
    
    # ==================== 6. SEISMIC DESIGN ====================
    
    print_section_header("MODULE 6: SEISMIC DESIGN ANALYSIS")
    
    # Estimate building weight
    floor_load_intensity = 12.0  # kN/m² approximate (DL + 0.25*LL)
    building_weight = floor_area * num_floors * floor_load_intensity
    
    seismic_analysis = SeismicDesignAnalysis(
        building_weight=building_weight,
        num_floors=num_floors,
        floor_height=floor_height,
        seismic_zone=seismic_zone,
        soil_type=soil_type,
        building_type=building_type,
        importance_factor=importance_factor
    )
    
    seismic_result = seismic_analysis.perform_seismic_analysis()
    complete_results["6_seismic_design"] = seismic_result
    
    # ==================== 7. WIND LOAD ====================
    
    print_section_header("MODULE 7: WIND LOAD ANALYSIS")
    
    building_height = num_floors * floor_height
    
    wind_analysis = WindLoadAnalysis(
        building_height=building_height,
        building_length=plot_length,
        building_width=plot_width,
        location=location,
        terrain_category=terrain_category,
        building_class=building_class
    )
    
    wind_result = wind_analysis.calculate_wind_loads()
    complete_results["7_wind_load"] = wind_result
    
    # ==================== 8. DETAILED LOADS ====================
    
    print_section_header("MODULE 8: DETAILED LOAD CALCULATIONS")
    
    # Extract column size for load calculation
    column_size_str = column_result["floor_wise_columns"]["Floor_1"]["column_size"].split("×")
    column_width = float(column_size_str[0].strip()) / 1000  # Convert to meters
    column_depth = float(column_size_str[1].split()[0].strip()) / 1000
    
    load_analysis = DetailedLoadCalculation(
        building_type=building_type,
        num_floors=num_floors,
        floor_area=floor_area,
        slab_thickness=slab_thickness,
        beam_size=(beam_width, beam_depth),
        column_size=(column_width, column_depth)
    )
    
    load_result = load_analysis.calculate_all_loads()
    complete_results["8_detailed_loads"] = load_result
    
    # ==================== 9. MATERIAL SELECTION ====================
    
    print_section_header("MODULE 9: MATERIAL GRADE SELECTION")
    
    # Get typical column load from floor 1
    column_load_str = column_result["floor_wise_columns"]["Floor_1"]["factored_load"]
    column_load = float(column_load_str.split()[0])
    
    material_selection = MaterialGradeSelection(
        num_floors=num_floors,
        column_load=column_load,
        span=avg_span,
        exposure_condition=exposure_condition,
        seismic_zone=seismic_zone,
        durability_requirement=durability_requirement
    )
    
    material_result = material_selection.select_materials()
    complete_results["9_material_selection"] = material_result
    
    # ==================== 10. OPTIMIZATION ====================
    
    print_section_header("MODULE 10: STRUCTURAL OPTIMIZATION STRATEGIES")
    
    structural_system = lateral_result["selected_system"]["primary"]
    
    optimization = StructuralOptimization(
        project_cost=project_cost,
        building_type=building_type,
        num_floors=num_floors,
        structural_system=structural_system
    )
    
    optimization_result = optimization.identify_optimizations()
    complete_results["10_optimization"] = optimization_result
    
    # ==================== SUMMARY ====================
    
    print_section_header("📊 EXECUTIVE SUMMARY")
    
    print(f"""
STRUCTURAL DESIGN SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. GRID SYSTEM:
   Configuration:           {num_bays_length} × {num_bays_width} bays
   Span Dimensions:         {span_length:.2f}m × {span_width:.2f}m
   Total Columns/Floor:     {total_columns}
   Grid Regularity:         {grid_result["seismic_considerations"]["grid_regularity"]}

2. MEMBER SIZING:
   Column (Floor 1):        {column_result["floor_wise_columns"]["Floor_1"]["column_size"]}
   Column (Top Floor):      {column_result["floor_wise_columns"][f"Floor_{num_floors}"]["column_size"]}
   Primary Beams:           {beam_result["primary_beams"]["dimensions"]["designation"]}
   Slab Thickness:          {slab_result["recommended_thickness"]["final_thickness"]}

3. LATERAL SYSTEM:
   Primary System:          {lateral_result["selected_system"]["primary"]}
   Ductility Class:         {lateral_result["seismic_parameters"]["ductility_class"]}
   Response Reduction (R):  {lateral_result["seismic_parameters"]["response_reduction_factor_R"]}

4. SEISMIC LOADS:
   Zone Factor (Z):         {seismic_result["seismic_zone_data"]["zone_factor_Z"]}
   Time Period:             {seismic_result["structural_response"]["fundamental_period_Ta"]}
   Base Shear:              {seismic_result["base_shear_calculation"]["base_shear_Vb"]}
   
5. WIND LOADS:
   Design Wind Speed:       {wind_result["wind_speeds_pressures"]["design_wind_speed_Vz"]}
   Wind Pressure:           {wind_result["wind_speeds_pressures"]["design_wind_pressure_pz"]}
   Along-Wind Force:        {wind_result["along_wind_loads"]["governing_case"]} governs

6. LOADS:
   Dead Load:               {load_result["load_summary"]["per_floor"]["dead_load"]}
   Live Load:               {load_result["load_summary"]["per_floor"]["live_load"]}
   Total Service Load:      {load_result["load_summary"]["per_floor"]["total_service"]}
   Building Weight:         {load_result["load_summary"]["entire_building"]["total_building_weight"]}

7. MATERIALS:
   Concrete Grade:          {material_result["summary_recommendations"]["primary_concrete_grade"]}
   Column Concrete:         {material_result["summary_recommendations"]["column_concrete_lower_floors"]}
   Steel Grade (Main):      {material_result["summary_recommendations"]["main_reinforcement"]}
   Steel Grade (Ties):      {material_result["summary_recommendations"]["ties_stirrups"]}

8. OPTIMIZATION:
   First Cost Savings:      {optimization_result["optimization_summary"]["first_cost_savings"]["subtotal"]}
   Lifecycle Savings:       {optimization_result["optimization_summary"]["lifecycle_savings"]["subtotal"]}
   Total Potential:         {optimization_result["optimization_summary"]["total_optimization_potential"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY RECOMMENDATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Use {num_bays_length}×{num_bays_width} regular grid for structural efficiency and cost savings
✓ Adopt {lateral_result["selected_system"]["primary"]} for lateral load resistance
✓ Use {material_result["summary_recommendations"]["column_concrete_lower_floors"]} concrete in lower columns
✓ Use {material_result["summary_recommendations"]["main_reinforcement"]} steel for main reinforcement
✓ Consider value engineering during schematic design for maximum impact
✓ Use modern formwork systems for repetitive floors
✓ Implement ductile detailing per IS 13920:2016 (Seismic Zone {seismic_zone})
✓ Maintain drift limits: {lateral_result["drift_control"]["code_limit"]} per IS 1893

DESIGN CODES REFERENCED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• IS 456:2000       - Plain and Reinforced Concrete - Code of Practice
• IS 1893:2016      - Criteria for Earthquake Resistant Design of Structures
• IS 875:2015       - Code of Practice for Design Loads (Parts 1, 2, 3)
• IS 13920:2016     - Ductile Detailing of Reinforced Concrete Structures
• IS 1786:2008      - High Strength Deformed Steel Bars and Wires for Concrete Reinforcement
• IS 2062:2011      - Steel for General Structural Purposes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    return complete_results


def main():
    """Main execution function"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                  ║
║           COMPREHENSIVE STRUCTURAL DESIGN SYSTEM - COMPLETE DEMONSTRATION                        ║
║                                                                                                  ║
║  This system provides deep engineering analysis with detailed calculations for all aspects       ║
║  of structural design per Indian Standard Codes (IS 456, IS 1893, IS 875, IS 13920)            ║
║                                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Run complete analysis with default parameters
    results = run_complete_structural_analysis()
    
    # Save results to file
    print_section_header("💾 SAVING ANALYSIS RESULTS")
    
    filename = save_complete_report(results)
    print(f"\n   ✓ Complete analysis saved to: {filename}")
    print(f"   ✓ File size: {len(json.dumps(results)) / 1024:.1f} KB")
    
    print_section_header("✅ ANALYSIS COMPLETE")
    
    print("""
All 10 modules have been executed successfully with detailed engineering calculations.

The comprehensive report includes:
  ✓ Structural grid spacing with engineering justification
  ✓ Column sizes for each floor with load calculations
  ✓ Beam sizing with span-depth ratios and reinforcement
  ✓ Slab thickness based on multiple design methods
  ✓ Lateral load resisting system selection and design
  ✓ Seismic analysis with base shear and force distribution
  ✓ Wind load calculation with pressure coefficients
  ✓ Complete load breakdown (dead, live, combinations)
  ✓ Material grade selection for concrete and steel
  ✓ Optimization strategies with quantified savings

Next steps:
  1. Review the generated JSON report for detailed calculations
  2. Run detailed 3D structural analysis in software (ETABS/SAP2000)
  3. Perform detailed design of critical members
  4. Prepare structural drawings
  5. Implement value engineering recommendations
  
For custom analysis, modify parameters in run_complete_structural_analysis() function.
""")
    
    print("="*100)
    print()


if __name__ == "__main__":
    main()
