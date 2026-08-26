"""
Simple analysis script that focuses on the core functionality without visualizations.
Use this if you're having issues with matplotlib/GUI backends.
"""

from analysis.plugin_analyzer import PluginAnalyzer
from pathlib import Path

def simple_analysis():
    """Run a simple analysis without visualizations."""
    
    print("🔍 Napari Plugin Ecosystem - Text Analysis Only")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = PluginAnalyzer(data_dir="data")
    
    # Fetch data
    print("\n📥 Fetching plugin data...")
    analyzer.fetch_data(force_refresh=False)
    
    # Create combined dataset
    print("\n🔄 Processing plugin data...")
    df = analyzer.create_combined_dataset()
    print(f"✅ Processed {len(df)} plugins total")
    
    # Quick overview
    active_plugins = len(df[df['category'] == 'active'])
    withdrawn_plugins = len(df[df['category'] == 'withdrawn'])
    deleted_plugins = len(df[df['category'] == 'deleted'])
    
    print(f"\n📊 Quick Stats:")
    print(f"   • Active: {active_plugins}")
    print(f"   • Withdrawn: {withdrawn_plugins}")
    print(f"   • Deleted: {deleted_plugins}")
    
    # Distribution analysis
    print("\n📈 Analyzing distribution patterns...")
    dist_stats = analyzer.analyze_distribution_patterns()
    
    print(f"\n🏪 Package Distribution (Active Plugins):")
    print(f"   • PyPI only: {dist_stats['active_pypi_only']}")
    print(f"   • Conda-forge only: {dist_stats['active_conda_only']}")
    print(f"   • Both platforms: {dist_stats['active_both']}")
    print(f"   • Neither platform: {dist_stats['active_neither']}")
    
    # Version analysis
    print("\n🏷️  Analyzing version patterns...")
    version_stats = analyzer.analyze_version_patterns()
    
    print(f"\n📦 Version Statistics (Active Plugins):")
    print(f"   • Average PyPI versions: {version_stats['avg_pypi_versions']:.1f}")
    print(f"   • Average conda versions: {version_stats['avg_conda_versions']:.1f}")
    
    # License analysis
    print("\n⚖️  Analyzing license patterns...")
    license_stats = analyzer.analyze_license_patterns()
    
    print(f"\n📄 License Compliance:")
    print(f"   • With licenses: {license_stats['total_with_license']}")
    print(f"   • Without licenses: {license_stats['total_without_license']}")
    print(f"   • Most common: {license_stats['most_common_license']}")
    
    # Generate full report
    print("\n📋 Generating comprehensive report...")
    report = analyzer.generate_summary_report()
    
    # Save report
    report_path = Path("reports") / "latest_ecosystem_report.md"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved to: {report_path}")
    
    # Show some interesting findings
    active_df = df[df['category'] == 'active']
    
    # Top plugins by version count
    top_plugins = active_df.nlargest(5, 'num_pypi_versions')
    print(f"\n🚀 Most actively developed plugins:")
    for i, (_, plugin) in enumerate(top_plugins.iterrows()):
        print(f"   {i+1}. {plugin['name']}: {plugin['num_pypi_versions']} versions")
    
    # Plugins without licenses
    no_license = active_df[~active_df['has_license']]
    print(f"\n⚠️  Active plugins needing licenses: {len(no_license)}")
    
    # PyPI-only plugins (candidates for conda-forge)
    pypi_only = active_df[active_df['has_pypi'] & ~active_df['has_conda']]
    print(f"\n📦 PyPI-only plugins (conda-forge candidates): {len(pypi_only)}")
    
    print(f"\n🎉 Analysis complete!")
    print(f"📄 Full report available at: {report_path}")
    
    return report

if __name__ == "__main__":
    simple_analysis()
