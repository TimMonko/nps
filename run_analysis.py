"""
Test script to run the napari plugin analysis with beautiful visualizations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analysis.plugin_analyzer import PluginAnalyzer

def main():
    """Run the plugin analysis with beautiful seaborn.objects plots."""
    
    print("🚀 Starting napari plugin ecosystem analysis...")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = PluginAnalyzer(data_dir="data")
    
    try:
        # Fetch data
        print("\n📥 Fetching plugin data...")
        analyzer.fetch_data(force_refresh=False)
        
        # Create combined dataset
        print("🔄 Processing plugin data...")
        df = analyzer.create_combined_dataset()
        print(f"✅ Processed {len(df)} plugins")
        
        # Quick stats
        active_count = len(df[df['category'] == 'active'])
        withdrawn_count = len(df[df['category'] == 'withdrawn'])
        deleted_count = len(df[df['category'] == 'deleted'])
        
        print("📊 Plugin Status:")
        print(f"   • Active: {active_count}")
        print(f"   • Withdrawn: {withdrawn_count}")
        print(f"   • Deleted: {deleted_count}")
        
        # Create visualizations
        print("\n🎨 Creating beautiful visualizations...")
        analyzer.create_visualizations()
        
        # Generate report
        print("\n📋 Generating analysis report...")
        report = analyzer.generate_summary_report()
        
        # Save report
        from pathlib import Path
        from datetime import datetime
        
        report_path = Path("reports") / f"ecosystem_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"✅ Report saved to: {report_path}")
        
        print("\n🎉 Analysis complete!")
        print("📁 Check the reports/ directory for:")
        print("   • Beautiful PNG visualizations")
        print("   • Comprehensive analysis report")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
