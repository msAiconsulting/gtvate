#!/usr/bin/env python3
"""
Test script for the Acoustic Sensor Dashboard
Verifies data loading and basic functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from acoustic_dashboard import AcousticSensorDashboard
    print("✅ Successfully imported AcousticSensorDashboard")
    
    # Test data loading
    print("\n📊 Testing data loading...")
    dashboard = AcousticSensorDashboard()
    
    if dashboard.pressure_data is not None:
        print(f"✅ Pressure data loaded: {len(dashboard.pressure_data)} records")
        print(f"   Columns: {list(dashboard.pressure_data.columns)}")
    else:
        print("❌ Failed to load pressure data")
    
    if dashboard.acoustic_data is not None:
        print(f"✅ Acoustic data loaded: {len(dashboard.acoustic_data)} records")
        print(f"   Frequency bands: {len(dashboard.freq_columns)}")
        print(f"   Sample frequencies: {dashboard.freq_columns[:5]}")
    else:
        print("❌ Failed to load acoustic data")
    
    # Test basic functionality
    print("\n🎯 Testing basic functionality...")
    
    try:
        pressure_plot = dashboard.create_pressure_dashboard()
        print("✅ Pressure dashboard creation successful")
    except Exception as e:
        print(f"❌ Pressure dashboard creation failed: {e}")
    
    try:
        spectrum_plot = dashboard.create_acoustic_spectrum(0)
        print("✅ Acoustic spectrum creation successful")
    except Exception as e:
        print(f"❌ Acoustic spectrum creation failed: {e}")
    
    try:
        heatmap_plot = dashboard.create_acoustic_heatmap(50)
        print("✅ Acoustic heatmap creation successful")
    except Exception as e:
        print(f"❌ Acoustic heatmap creation failed: {e}")
    
    try:
        level_plot = dashboard.create_level_analysis()
        print("✅ Level analysis creation successful")
    except Exception as e:
        print(f"❌ Level analysis creation failed: {e}")
    
    try:
        stats = dashboard.create_statistics_panel()
        print("✅ Statistics panel creation successful")
    except Exception as e:
        print(f"❌ Statistics panel creation failed: {e}")
    
    print("\n🎉 All tests completed!")
    print("\n🌐 Dashboard is running at: http://localhost:7860")
    print("📖 Open your browser and navigate to the URL above")
    print("🔄 Use Ctrl+C in the terminal to stop the dashboard")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("  uv pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
