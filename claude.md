# Claude AI Assistant Instructions for Napari Plugin Sustainability Project

## Project Overview
This is the **Napari Plugin Sustainability Initiative**, funded by the URSSI Fellowship program. The goal is to analyze the health and sustainability of the napari plugin ecosystem (~500+ plugins) and create working groups to improve long-term plugin maintenance.

## Key Project Components

### 1. Data Sources
- **classifiers.json**: Plugin categorization data (active/withdrawn/deleted) with version histories
- **extended_summary.json**: Detailed plugin metadata including:
  - PyPI and conda versions
  - License information
  - Author details
  - Project URLs
  - Dependencies

### 2. Analysis Goals
- **Version Analysis**: Track release patterns and update frequency
- **Download Metrics**: Assess plugin popularity and usage
- **Napari Pinning**: Identify plugins constraining napari versions
- **Package Availability**: PyPI vs conda-forge distribution patterns
- **License Compliance**: Categorize and track license types
- **Maintenance Status**: Identify stale or abandoned plugins

### 3. Community Engagement
- Create working groups for plugin sustainability
- Develop plugin affiliation programs
- Establish maintenance best practices
- Connect plugin developers with resources

## Preferred Communication Style

### When I ask for help:
1. **Be specific and actionable** - provide concrete next steps
2. **Reference data structures** - use actual field names from the JSON files
3. **Consider the ecosystem scale** - we're dealing with 500+ plugins
4. **Think sustainably** - solutions should be maintainable long-term

### Code Development Preferences:
- **Python-focused** - Use pandas, requests, matplotlib for analysis
- **Modular design** - Create reusable functions for different analyses
- **Data-driven** - Always validate assumptions with actual plugin data
- **Documentation** - Include docstrings and comments for maintainability

### Analysis Approach:
- **Start with exploratory analysis** - understand distributions and patterns
- **Identify outliers and edge cases** - these often reveal important insights
- **Create visualizations** - trends are easier to understand with plots
- **Generate actionable insights** - every analysis should lead to recommendations

## Current Workspace Structure
```
plugin-sustainability/
├── claude.md (this file)
├── community-one-pager.md (to be created)
├── analysis/ (Python analysis tools)
├── data/ (cached data and results)
└── reports/ (generated insights and visualizations)
```

## Key External Resources
- **npe2api repository**: Source of classifiers.json and extended_summary.json
- **weather-report**: Target for upstreaming analysis results
- **napari hub**: Community platform for plugin discovery
- **URSSI Fellowship**: Funding and methodology framework

## Common Tasks You Can Help With:

### Data Analysis
- Parse and explore plugin metadata
- Calculate sustainability metrics
- Generate summary statistics
- Create data visualizations

### Code Development
- Write analysis scripts
- Create data processing pipelines
- Implement metric calculations
- Build reporting tools

### Documentation
- Explain analysis methodologies
- Document findings and recommendations
- Create user guides for tools
- Draft community communications

## Project Success Metrics
1. **Comprehensive plugin ecosystem map** - understand current state
2. **Sustainability metrics defined** - quantify plugin health
3. **Working groups established** - active community engagement
4. **Best practices documented** - guidance for plugin developers
5. **Analysis tools created** - reusable for ongoing monitoring

## When Working Together:
- **Ask clarifying questions** if project context is unclear
- **Suggest improvements** to analysis approaches
- **Point out potential issues** with data quality or methodology
- **Recommend best practices** from open source sustainability research

Remember: This project aims to strengthen the entire napari plugin ecosystem for long-term sustainability and community health.
