"""
Napari Plugin Sustainability Analysis Framework

This module provides tools for analyzing the health and sustainability 
of the napari plugin ecosystem using data from npe2api.
"""

import json
import requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid Tcl/Tk issues
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import seaborn as sns
import seaborn.objects as so
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up nice plotting defaults
plt.style.use('seaborn-v0_8')
sns.set_palette("colorblind")

class PluginAnalyzer:
    """
    Main class for analyzing napari plugin ecosystem data.
    
    This class provides methods to fetch, process, and analyze plugin data
    from the npe2api repository to assess plugin sustainability.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the analyzer.
        
        Args:
            data_dir: Directory to store cached data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.classifiers_data = None
        self.extended_data = None
        self.combined_data = None
        
        # API endpoints
        self.classifiers_url = "https://raw.githubusercontent.com/napari/npe2api/main/public/classifiers.json"
        self.extended_url = "https://raw.githubusercontent.com/napari/npe2api/main/public/extended_summary.json"
    
    def fetch_data(self, force_refresh: bool = False) -> None:
        """
        Fetch plugin data from npe2api repository.
        
        Args:
            force_refresh: If True, fetch fresh data even if cached files exist
        """
        classifiers_file = self.data_dir / "classifiers.json"
        extended_file = self.data_dir / "extended_summary.json"
        
        # Fetch classifiers data
        if force_refresh or not classifiers_file.exists():
            print("Fetching classifiers data...")
            response = requests.get(self.classifiers_url)
            response.raise_for_status()
            
            with open(classifiers_file, 'w') as f:
                json.dump(response.json(), f, indent=2)
            
            self.classifiers_data = response.json()
        else:
            print("Loading cached classifiers data...")
            with open(classifiers_file, 'r') as f:
                self.classifiers_data = json.load(f)
        
        # Fetch extended data
        if force_refresh or not extended_file.exists():
            print("Fetching extended summary data...")
            response = requests.get(self.extended_url)
            response.raise_for_status()
            
            with open(extended_file, 'w') as f:
                json.dump(response.json(), f, indent=2)
            
            self.extended_data = response.json()
        else:
            print("Loading cached extended summary data...")
            with open(extended_file, 'r') as f:
                self.extended_data = json.load(f)
        
        print(f"Loaded {len(self.classifiers_data.get('active', []))} active plugins")
        print(f"Loaded {len(self.extended_data)} detailed plugin records")
    
    def create_combined_dataset(self) -> pd.DataFrame:
        """
        Create a combined dataset from classifiers and extended data.
        
        Returns:
            DataFrame with combined plugin information
        """
        if self.classifiers_data is None or self.extended_data is None:
            raise ValueError("Data not loaded. Call fetch_data() first.")
        
        # Create extended data lookup
        extended_lookup = {plugin['normalized_name']: plugin for plugin in self.extended_data}
        
        combined_plugins = []
        
        # Process each category
        for category in ['active', 'withdrawn', 'deleted']:
            plugins = self.classifiers_data.get(category, [])
            
            for plugin_name, versions in plugins.items():
                # Get extended info
                extended_info = extended_lookup.get(plugin_name, {})
                
                # Create combined record
                record = {
                    'name': plugin_name,
                    'display_name': extended_info.get('display_name', plugin_name),
                    'category': category,
                    'summary': extended_info.get('summary', ''),
                    'author': extended_info.get('author', ''),
                    'license': extended_info.get('license', ''),
                    'home_page': extended_info.get('home_page', ''),
                    'current_version': extended_info.get('version', ''),
                    'classifier_versions': versions,
                    'pypi_versions': extended_info.get('pypi_versions', []),
                    'conda_versions': extended_info.get('conda_versions', []),
                    'project_urls': extended_info.get('project_url', [])
                }
                
                # Calculate derived metrics
                record['num_classifier_versions'] = len(versions) if versions else 0
                record['num_pypi_versions'] = len(record['pypi_versions'])
                record['num_conda_versions'] = len(record['conda_versions'])
                record['has_conda'] = record['num_conda_versions'] > 0
                record['has_pypi'] = record['num_pypi_versions'] > 0
                record['has_license'] = bool(record['license'] and record['license'].strip())
                record['has_homepage'] = bool(record['home_page'])
                record['has_project_urls'] = bool(record['project_urls'])
                
                combined_plugins.append(record)
        
        self.combined_data = pd.DataFrame(combined_plugins)
        return self.combined_data
    
    def analyze_distribution_patterns(self) -> Dict:
        """
        Analyze how plugins are distributed across PyPI and conda-forge.
        
        Returns:
            Dictionary with distribution analysis results
        """
        if self.combined_data is None:
            self.create_combined_dataset()
        
        df = self.combined_data
        
        # Distribution patterns
        distribution_stats = {
            'total_plugins': len(df),
            'active_plugins': len(df[df['category'] == 'active']),
            'withdrawn_plugins': len(df[df['category'] == 'withdrawn']),
            'deleted_plugins': len(df[df['category'] == 'deleted']),
            'pypi_only': len(df[df['has_pypi'] & ~df['has_conda']]),
            'conda_only': len(df[~df['has_pypi'] & df['has_conda']]),
            'both_pypi_conda': len(df[df['has_pypi'] & df['has_conda']]),
            'neither_pypi_conda': len(df[~df['has_pypi'] & ~df['has_conda']])
        }
        
        # Active plugin analysis
        active_df = df[df['category'] == 'active']
        distribution_stats.update({
            'active_pypi_only': len(active_df[active_df['has_pypi'] & ~active_df['has_conda']]),
            'active_conda_only': len(active_df[~active_df['has_pypi'] & active_df['has_conda']]),
            'active_both': len(active_df[active_df['has_pypi'] & active_df['has_conda']]),
            'active_neither': len(active_df[~active_df['has_pypi'] & ~active_df['has_conda']])
        })
        
        return distribution_stats
    
    def analyze_version_patterns(self) -> Dict:
        """
        Analyze version release patterns across plugins.
        
        Returns:
            Dictionary with version analysis results
        """
        if self.combined_data is None:
            self.create_combined_dataset()
        
        df = self.combined_data
        active_df = df[df['category'] == 'active']
        
        version_stats = {
            'avg_pypi_versions': active_df['num_pypi_versions'].mean(),
            'median_pypi_versions': active_df['num_pypi_versions'].median(),
            'max_pypi_versions': active_df['num_pypi_versions'].max(),
            'avg_conda_versions': active_df['num_conda_versions'].mean(),
            'median_conda_versions': active_df['num_conda_versions'].median(),
            'max_conda_versions': active_df['num_conda_versions'].max(),
        }
        
        # Find most prolific plugins
        version_stats['most_pypi_versions'] = active_df.nlargest(5, 'num_pypi_versions')[['name', 'num_pypi_versions']].to_dict('records')
        version_stats['most_conda_versions'] = active_df.nlargest(5, 'num_conda_versions')[['name', 'num_conda_versions']].to_dict('records')
        
        return version_stats
    
    def analyze_license_patterns(self) -> Dict:
        """
        Analyze license usage patterns across plugins.
        
        Returns:
            Dictionary with license analysis results
        """
        if self.combined_data is None:
            self.create_combined_dataset()
        
        df = self.combined_data
        active_df = df[df['category'] == 'active']
        
        # Clean and categorize licenses
        def categorize_license(license_str):
            if not license_str or license_str.strip() == '':
                return 'None/Unspecified'
            
            license_lower = license_str.lower()
            
            if 'mit' in license_lower:
                return 'MIT'
            elif 'bsd' in license_lower:
                if '3' in license_lower:
                    return 'BSD-3-Clause'
                elif '2' in license_lower:
                    return 'BSD-2-Clause'
                else:
                    return 'BSD (Unspecified)'
            elif 'apache' in license_lower:
                return 'Apache'
            elif 'gpl' in license_lower:
                if 'lgpl' in license_lower:
                    return 'LGPL'
                else:
                    return 'GPL'
            elif 'cc' in license_lower or 'creative commons' in license_lower:
                return 'Creative Commons'
            else:
                return 'Other'
        
        active_df['license_category'] = active_df['license'].apply(categorize_license)
        
        license_counts = active_df['license_category'].value_counts()
        
        license_stats = {
            'total_with_license': len(active_df[active_df['has_license']]),
            'total_without_license': len(active_df[~active_df['has_license']]),
            'license_distribution': license_counts.to_dict(),
            'most_common_license': license_counts.index[0] if len(license_counts) > 0 else None
        }
        
        return license_stats
    
    def find_napari_version_constraints(self) -> List[Dict]:
        """
        Identify plugins that may be constraining napari versions.
        
        This is a placeholder - would need to analyze actual dependency information
        from package metadata or requirements files.
        
        Returns:
            List of plugins with potential version constraints
        """
        # This would require fetching package metadata from PyPI
        # For now, return placeholder
        return [
            {"name": "analysis_placeholder", "constraint": "napari>=0.4.0,<0.5.0", "risk": "medium"}
        ]
    
    def generate_summary_report(self) -> str:
        """
        Generate a comprehensive summary report of the plugin ecosystem.
        
        Returns:
            Formatted string report
        """
        if self.combined_data is None:
            self.create_combined_dataset()
        
        dist_stats = self.analyze_distribution_patterns()
        version_stats = self.analyze_version_patterns()
        license_stats = self.analyze_license_patterns()
        
        report = f"""
# Napari Plugin Ecosystem Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Statistics
- Total plugins tracked: {dist_stats['total_plugins']:,}
- Active plugins: {dist_stats['active_plugins']:,}
- Withdrawn plugins: {dist_stats['withdrawn_plugins']:,}
- Deleted plugins: {dist_stats['deleted_plugins']:,}

## Distribution Patterns
### All Plugins
- PyPI only: {dist_stats['pypi_only']:,}
- Conda-forge only: {dist_stats['conda_only']:,}
- Both PyPI and conda-forge: {dist_stats['both_pypi_conda']:,}
- Neither: {dist_stats['neither_pypi_conda']:,}

### Active Plugins Only
- PyPI only: {dist_stats['active_pypi_only']:,}
- Conda-forge only: {dist_stats['active_conda_only']:,}
- Both PyPI and conda-forge: {dist_stats['active_both']:,}
- Neither: {dist_stats['active_neither']:,}

## Version Release Patterns
- Average PyPI versions per plugin: {version_stats['avg_pypi_versions']:.1f}
- Median PyPI versions per plugin: {version_stats['median_pypi_versions']:.0f}
- Maximum PyPI versions: {version_stats['max_pypi_versions']:,}

- Average conda versions per plugin: {version_stats['avg_conda_versions']:.1f}
- Median conda versions per plugin: {version_stats['median_conda_versions']:.0f}
- Maximum conda versions: {version_stats['max_conda_versions']:,}

## License Analysis
- Plugins with licenses: {license_stats['total_with_license']:,}
- Plugins without licenses: {license_stats['total_without_license']:,}
- Most common license: {license_stats['most_common_license']}

### License Distribution:
"""
        
        for license_type, count in license_stats['license_distribution'].items():
            percentage = (count / dist_stats['active_plugins']) * 100
            report += f"- {license_type}: {count:,} ({percentage:.1f}%)\n"
        
        report += f"""

## Sustainability Insights
- Distribution coverage: {((dist_stats['active_both'] + dist_stats['active_pypi_only']) / dist_stats['active_plugins'] * 100):.1f}% of active plugins available on PyPI
- Conda-forge adoption: {(dist_stats['active_both'] + dist_stats['active_conda_only']) / dist_stats['active_plugins'] * 100:.1f}% of active plugins available on conda-forge
- License compliance: {(license_stats['total_with_license'] / dist_stats['active_plugins'] * 100):.1f}% of active plugins have specified licenses

## Recommendations
1. Encourage conda-forge packaging for PyPI-only plugins to improve accessibility
2. Help unlicensed plugins adopt appropriate open source licenses
3. Monitor plugins with low version counts for potential maintenance issues
4. Focus sustainability efforts on plugins with high version counts (active development)
"""
        
        return report
    
    def create_visualizations(self, output_dir: str = "reports") -> None:
        """
        Create beautiful visualization plots using seaborn.objects for the analysis.
        
        Args:
            output_dir: Directory to save plot files
        """
        if self.combined_data is None:
            self.create_combined_dataset()
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        df = self.combined_data
        active_df = df[df['category'] == 'active'].copy()
        
        # Set the seaborn theme
        sns.set_theme(style="whitegrid", palette="husl")
        
        # 1. Plugin Categories Pie Chart
        print("🎨 Creating plugin categories visualization...")
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        category_counts = df['category'].value_counts()
        colors = sns.color_palette("Set2", len(category_counts))
        
        wedges, texts, autotexts = ax.pie(category_counts.values, 
                                         labels=category_counts.index, 
                                         autopct='%1.1f%%',
                                         colors=colors,
                                         startangle=90)
        ax.set_title('Napari Plugin Categories', fontsize=16, fontweight='bold', pad=20)
        
        # Make percentage text more readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.savefig(output_path / 'plugin_categories.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Distribution Patterns using seaborn.objects
        print("📊 Creating distribution patterns visualization...")
        
        # Prepare data for distribution plot
        dist_data = []
        for _, plugin in active_df.iterrows():
            if plugin['has_pypi'] and plugin['has_conda']:
                dist_data.append({'plugin': plugin['name'], 'distribution': 'Both PyPI & Conda', 'count': 1})
            elif plugin['has_pypi']:
                dist_data.append({'plugin': plugin['name'], 'distribution': 'PyPI Only', 'count': 1})
            elif plugin['has_conda']:
                dist_data.append({'plugin': plugin['name'], 'distribution': 'Conda Only', 'count': 1})
            else:
                dist_data.append({'plugin': plugin['name'], 'distribution': 'Neither', 'count': 1})
        
        dist_df = pd.DataFrame(dist_data)
        
        # Create the seaborn.objects plot
        (
            so.Plot(dist_df, x="distribution", y="count")
            .add(so.Bar(color=".6", edgecolor="white", edgewidth=2), so.Count())
            .layout(size=(12, 8))
            .label(
                title="Active Plugin Distribution Patterns",
                x="Distribution Platform",
                y="Number of Plugins"
            )
            .theme({
                "axes.spines.right": False,
                "axes.spines.top": False,
                "axes.titlesize": 16,
                "axes.titleweight": "bold"
            })
            .save(output_path / 'distribution_patterns.png', dpi=300, bbox_inches='tight')
        )
        
        # 3. Version Count Distribution using seaborn.objects
        print("📈 Creating version distribution visualization...")
        
        # Prepare version data
        version_data = []
        for _, plugin in active_df.iterrows():
            version_data.append({'plugin': plugin['name'], 'platform': 'PyPI', 'versions': plugin['num_pypi_versions']})
            version_data.append({'plugin': plugin['name'], 'platform': 'Conda', 'versions': plugin['num_conda_versions']})
        
        version_df = pd.DataFrame(version_data)
        
        (
            so.Plot(version_df, x="versions", color="platform")
            .add(so.Bars(alpha=0.7), so.Hist(bins=30))
            .layout(size=(12, 8))
            .label(
                title="Version Count Distribution by Platform",
                x="Number of Versions",
                y="Number of Plugins"
            )
            .theme({
                "axes.spines.right": False,
                "axes.spines.top": False,
                "axes.titlesize": 16,
                "axes.titleweight": "bold"
            })
            .save(output_path / 'version_distribution.png', dpi=300, bbox_inches='tight')
        )
        
        # 4. License Distribution using seaborn.objects
        print("⚖️ Creating license distribution visualization...")
        
        # Categorize licenses
        def categorize_license(license_str):
            if not license_str or license_str.strip() == '':
                return 'None/Unspecified'
            
            license_lower = license_str.lower()
            
            if 'mit' in license_lower:
                return 'MIT'
            elif 'bsd' in license_lower:
                if '3' in license_lower:
                    return 'BSD-3-Clause'
                elif '2' in license_lower:
                    return 'BSD-2-Clause'
                else:
                    return 'BSD (Other)'
            elif 'apache' in license_lower:
                return 'Apache'
            elif 'gpl' in license_lower:
                if 'lgpl' in license_lower:
                    return 'LGPL'
                else:
                    return 'GPL'
            elif 'cc' in license_lower or 'creative commons' in license_lower:
                return 'Creative Commons'
            else:
                return 'Other'
        
        active_df['license_category'] = active_df['license'].apply(categorize_license)
        license_counts = active_df['license_category'].value_counts().head(10)
        
        # Create license data for seaborn.objects
        license_data = [{'license': license, 'count': count} for license, count in license_counts.items()]
        license_df = pd.DataFrame(license_data)
        
        (
            so.Plot(license_df, y="license", x="count")
            .add(so.Bar(color=".6", edgecolor="white", edgewidth=1))
            .layout(size=(12, 8))
            .label(
                title="License Distribution (Active Plugins)",
                x="Number of Plugins",
                y="License Type"
            )
            .theme({
                "axes.spines.right": False,
                "axes.spines.top": False,
                "axes.titlesize": 16,
                "axes.titleweight": "bold"
            })
            .save(output_path / 'license_distribution.png', dpi=300, bbox_inches='tight')
        )
        
        # 5. Create a comprehensive summary plot with traditional matplotlib/seaborn
        print("✨ Creating ecosystem summary visualization...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Napari Plugin Ecosystem Summary', fontsize=20, fontweight='bold')
        
        # Category donut chart
        category_counts = df['category'].value_counts()
        colors = sns.color_palette("Set2", len(category_counts))
        wedges, texts, autotexts = ax1.pie(category_counts.values, 
                                          labels=category_counts.index,
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          pctdistance=0.85)
        
        # Create donut by adding white circle in center
        centre_circle = Circle((0,0), 0.70, fc='white')
        ax1.add_artist(centre_circle)
        ax1.set_title('Plugin Status Distribution', fontweight='bold')
        
        # Distribution bar chart
        sns.barplot(data=dist_df, x='distribution', y='count', 
                   estimator=sum, ax=ax2, palette="viridis")
        ax2.set_title('Active Plugin Distribution', fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        
        # Version scatter plot
        scatter_data = active_df[active_df['num_pypi_versions'] > 0]
        ax3.scatter(scatter_data['num_pypi_versions'], scatter_data['num_conda_versions'], 
                   alpha=0.6, s=50, c=sns.color_palette("husl", 1)[0])
        ax3.set_xlabel('PyPI Versions')
        ax3.set_ylabel('Conda Versions')
        ax3.set_title('PyPI vs Conda Version Counts', fontweight='bold')
        
        # License bar chart
        license_counts_top8 = active_df['license_category'].value_counts().head(8)
        sns.barplot(y=license_counts_top8.index, x=license_counts_top8.values, 
                   ax=ax4, palette="plasma")
        ax4.set_title('Top License Types', fontweight='bold')
        ax4.set_xlabel('Number of Plugins')
        
        plt.tight_layout()
        plt.savefig(output_path / 'ecosystem_summary.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✨ All visualizations saved to {output_path}/")
        print("📊 Generated plots:")
        print("   • plugin_categories.png - Plugin status distribution")
        print("   • distribution_patterns.png - Platform availability")
        print("   • version_distribution.png - Version count histograms")
        print("   • license_distribution.png - License type distribution")
        print("   • ecosystem_summary.png - Comprehensive overview")


# Convenience function for quick analysis
def quick_analysis(force_refresh: bool = False) -> str:
    """
    Perform a quick analysis of the napari plugin ecosystem.
    
    Args:
        force_refresh: Whether to fetch fresh data
        
    Returns:
        Summary report as string
    """
    analyzer = PluginAnalyzer()
    analyzer.fetch_data(force_refresh=force_refresh)
    analyzer.create_combined_dataset()
    
    report = analyzer.generate_summary_report()
    analyzer.create_visualizations()
    
    return report


if __name__ == "__main__":
    # Example usage
    print("Starting napari plugin ecosystem analysis...")
    report = quick_analysis(force_refresh=False)
    
    # Save report
    report_path = Path("reports") / f"ecosystem_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"Analysis complete! Report saved to: {report_path}")
    print("\nSummary:")
    print(report[:500] + "..." if len(report) > 500 else report)
