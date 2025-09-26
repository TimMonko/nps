# Napari Plugin Sustainability Analysis Framework

A comprehensive toolkit for analyzing the health and sustainability of the napari plugin ecosystem.

## Overview

This project provides tools to:

- **Analyze plugin distribution** across PyPI and conda-forge
- **Track version release patterns** and development activity  
- **Assess license compliance** and metadata quality
- **Identify maintenance risks** and sustainability opportunities
- **Generate reports and visualizations** for community engagement

## Data Sources

The analysis uses data from the [npe2api repository](https://github.com/napari/npe2api):

- **`classifiers.json`**: Plugin categorization (active/withdrawn/deleted) with version histories
- **`extended_summary.json`**: Detailed metadata including dependencies, licenses, and project URLs

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Example Analysis

```bash
python example_analysis.py
```

This will:
- Fetch the latest plugin data (cached locally)
- Analyze distribution patterns and sustainability metrics
- Generate a comprehensive report in `reports/`
- Create visualizations showing ecosystem health

### 3. Use the Analysis Framework

```python
from analysis.plugin_analyzer import PluginAnalyzer

# Initialize analyzer
analyzer = PluginAnalyzer()

# Fetch data
analyzer.fetch_data()

# Create combined dataset
df = analyzer.create_combined_dataset()

# Run specific analyses
dist_stats = analyzer.analyze_distribution_patterns()
version_stats = analyzer.analyze_version_patterns()
license_stats = analyzer.analyze_license_patterns()

# Generate full report
report = analyzer.generate_summary_report()
print(report)

# Create visualizations
analyzer.create_visualizations()
```

## Key Analyses

### Distribution Patterns
- Plugins available only on PyPI vs conda-forge
- Cross-platform availability assessment
- Package manager adoption trends

### Version Release Patterns  
- Release frequency and development activity
- Version count distributions
- Most actively maintained plugins

### License Compliance
- License usage patterns across the ecosystem
- Identification of unlicensed plugins
- Common license types and compatibility

### Sustainability Metrics
- Plugins at risk of abandonment
- Well-maintained plugins as examples
- Metadata quality assessment

## Generated Outputs

### Reports (`reports/` directory)
- **Comprehensive ecosystem analysis** with statistics and insights
- **Sustainability recommendations** for the community
- **Plugin-specific findings** highlighting maintenance needs

### Visualizations
- Plugin category distributions (active/withdrawn/deleted)
- Package availability patterns (PyPI vs conda-forge)
- Version count histograms showing development activity
- License compliance charts

### Data Cache (`data/` directory)
- Cached JSON files for faster subsequent analysis
- Automatically refreshed when force_refresh=True

## Customizing the Analysis

The framework is designed to be extensible. Examples of custom analyses:

```python
# Find potentially stale plugins
active_df = df[df['category'] == 'active']
stale_plugins = active_df[
    (active_df['num_pypi_versions'] <= 2) &
    (~active_df['has_homepage']) &
    (~active_df['has_project_urls'])
]

# Identify well-maintained plugins
exemplars = active_df[
    (active_df['num_pypi_versions'] >= 5) &
    (active_df['has_license']) &
    (active_df['has_conda'])
]

# Analyze specific plugin subsets
microscopy_plugins = df[df['summary'].str.contains('microscop', case=False, na=False)]
```

## Project Structure

```
plugin-sustainability/
├── analysis/
│   └── plugin_analyzer.py      # Main analysis framework
├── data/                       # Cached plugin data
├── reports/                    # Generated reports and plots
├── claude.md                   # AI assistant instructions
├── community-one-pager.md      # Community engagement document
├── example_analysis.py         # Usage examples
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Contributing to Sustainability

This analysis framework supports the broader **Napari Plugin Sustainability Initiative**:

### For Plugin Developers
- **Identify best practices** from well-maintained plugins
- **Assess your plugins' metadata** and distribution coverage
- **Connect with other maintainers** facing similar challenges

### For Institutions
- **Understand which plugins your research depends on**
- **Identify critical plugins needing support**
- **Develop plugin affiliation programs**

### For the Community
- **Track ecosystem health** over time
- **Prioritize sustainability efforts** based on data
- **Celebrate plugin maintainer contributions**

## URSSI Fellowship

This work is supported by the [US Research Software Sustainability Institute (URSSI)](https://urssi.us/) Fellowship program, which aims to improve the sustainability of research software infrastructure.

### Goals
1. **Comprehensive ecosystem mapping** - Understand current plugin health
2. **Community working groups** - Connect maintainers and users  
3. **Best practices documentation** - Share successful maintenance strategies
4. **Funding pathway development** - Connect plugins with resources
5. **Long-term monitoring tools** - Track ecosystem evolution

## Get Involved

### Immediate Actions
- **Run the analysis** on your local environment
- **Contribute plugin metadata** improvements
- **Share findings** with the napari community
- **Suggest additional analyses** via GitHub issues

### Community Participation
- **Join napari Zulip** for discussions: [napari.zulipchat.com](https://napari.zulipchat.com)
- **Attend community calls** (schedule TBD)
- **Contribute to working groups** around plugin sustainability

### Contact
- **GitHub**: [napari/plugin-sustainability](https://github.com/napari/plugin-sustainability)
- **Email**: plugin-sustainability@napari.org
- **Community**: [napari.org/community](https://napari.org/community/)

---

*Building a more sustainable future for scientific image analysis tools.*
