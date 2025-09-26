"""
Example usage of the Plugin Analyzer for napari sustainability analysis.

This script demonstrates how to use the analysis framework to:
1. Fetch plugin data from npe2api
2. Analyze distribution patterns
3. Generate sustainability reports
4. Create visualizations

Run this script to get started with plugin ecosystem analysis.
"""

from analysis.plugin_analyzer import PluginAnalyzer, quick_analysis
from pathlib import Path
import json

def main():
    """Main example demonstrating plugin analysis capabilities."""
    
    print("🔍 Napari Plugin Ecosystem Analysis")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = PluginAnalyzer(data_dir="data")
    
    # Fetch data (uses cache if available)
    print("\n📥 Fetching plugin data...")
    analyzer.fetch_data(force_refresh=False)  # Set to True for fresh data
    
    # Create combined dataset
    print("\n🔄 Processing plugin data...")
    df = analyzer.create_combined_dataset()
    print(f"✅ Processed {len(df)} plugins total")
    
    # Quick overview
    active_plugins = len(df[df['category'] == 'active'])
    withdrawn_plugins = len(df[df['category'] == 'withdrawn'])
    deleted_plugins = len(df[df['category'] == 'deleted'])
    
    print(f"📊 Quick Stats:")
    print(f"   • Active: {active_plugins}")
    print(f"   • Withdrawn: {withdrawn_plugins}")
    print(f"   • Deleted: {deleted_plugins}")
    
    # Distribution analysis
    print("\n📈 Analyzing distribution patterns...")
    dist_stats = analyzer.analyze_distribution_patterns()
    
    print(f"🏪 Package Distribution (Active Plugins):")
    print(f"   • PyPI only: {dist_stats['active_pypi_only']}")
    print(f"   • Conda-forge only: {dist_stats['active_conda_only']}")
    print(f"   • Both platforms: {dist_stats['active_both']}")
    print(f"   • Neither platform: {dist_stats['active_neither']}")
    
    # Version analysis
    print("\n🏷️  Analyzing version patterns...")
    version_stats = analyzer.analyze_version_patterns()
    
    print(f"📦 Version Statistics (Active Plugins):")
    print(f"   • Average PyPI versions: {version_stats['avg_pypi_versions']:.1f}")
    print(f"   • Average conda versions: {version_stats['avg_conda_versions']:.1f}")
    
    # License analysis
    print("\n⚖️  Analyzing license patterns...")
    license_stats = analyzer.analyze_license_patterns()
    
    print(f"📄 License Compliance:")
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
    
    # Create visualizations
    print("\n📊 Creating visualizations...")
    try:
        analyzer.create_visualizations()
        print("✅ Visualizations saved to reports/ directory")
    except Exception as e:
        print(f"⚠️  Visualization creation failed: {e}")
        print("📝 Analysis completed successfully, but without plots.")
    
    # Examples of specific analyses you might want to do
    print("\n🔍 Example Specific Analyses:")
    
    # Find plugins without conda packages
    active_df = df[df['category'] == 'active']
    pypi_only = active_df[active_df['has_pypi'] & ~active_df['has_conda']]
    
    print(f"\n📦 PyPI-only plugins (first 10):")
    for i, (_, plugin) in enumerate(pypi_only.head(10).iterrows()):
        print(f"   {i+1:2d}. {plugin['name']} ({plugin['num_pypi_versions']} versions)")
    
    # Find plugins with many versions (active development)
    most_versions = active_df.nlargest(5, 'num_pypi_versions')
    print(f"\n🚀 Most actively developed plugins (by version count):")
    for i, (_, plugin) in enumerate(most_versions.iterrows()):
        print(f"   {i+1}. {plugin['name']}: {plugin['num_pypi_versions']} PyPI versions")
    
    # Find plugins without licenses
    no_license = active_df[~active_df['has_license']]
    print(f"\n⚠️  Active plugins without licenses: {len(no_license)}")
    if len(no_license) > 0:
        print("   First few examples:")
        for i, (_, plugin) in enumerate(no_license.head(5).iterrows()):
            print(f"   • {plugin['name']}")
    
    print(f"\n🎉 Analysis complete! Check the reports/ directory for detailed results.")
    print(f"💡 Tip: Rerun with force_refresh=True to get the latest data from npe2api")


def demonstrate_custom_analysis():
    """Show how to do custom analysis beyond the built-in methods."""
    
    print("\n" + "=" * 50)
    print("🛠️  Custom Analysis Example")
    print("=" * 50)
    
    analyzer = PluginAnalyzer()
    analyzer.fetch_data()
    df = analyzer.create_combined_dataset()
    
    # Example: Find plugins that might be stale (few versions, basic info)
    active_df = df[df['category'] == 'active']
    
    potentially_stale = active_df[
        (active_df['num_pypi_versions'] <= 2) &  # Few versions
        (~active_df['has_homepage']) &           # No homepage
        (~active_df['has_project_urls'])         # No project URLs
    ]
    
    print(f"🔍 Potentially stale plugins: {len(potentially_stale)}")
    if len(potentially_stale) > 0:
        print("Examples:")
        for _, plugin in potentially_stale.head(5).iterrows():
            print(f"   • {plugin['name']}: {plugin['num_pypi_versions']} versions, author: {plugin['author'] or 'Unknown'}")
    
    # Example: Plugins with good metadata (could be models for others)
    well_maintained = active_df[
        (active_df['num_pypi_versions'] >= 5) &  # Multiple versions
        (active_df['has_license']) &             # Has license
        (active_df['has_homepage']) &            # Has homepage
        (active_df['has_conda'])                 # Available on conda
    ].sort_values('num_pypi_versions', ascending=False)
    
    print(f"\n✨ Well-maintained plugins (examples for others): {len(well_maintained)}")
    for _, plugin in well_maintained.head(5).iterrows():
        print(f"   • {plugin['name']}: {plugin['num_pypi_versions']} versions, on conda-forge")


if __name__ == "__main__":
    main()
    demonstrate_custom_analysis()
