# URSSI Fall Fellowship: Building Sustainable Plugin Ecosystems in Scientific Software

Tim Monko

*November 2025*

## When Plugins and Core Projects Lose Touch

[PLACEHOLDER: Brief introduction to napari - what it is, who uses it, how the plugin system works. Explain the scientific imaging context and Python ecosystem for readers who may not be familiar. 2-3 paragraphs explaining napari as a foundational tool with 500+ plugins, used across domains from neuroscience to materials science.]

Despite this growth, something concerning has been happening: collaboration between plugin developers and the core napari team has been declining. Maintenance practices became unsustainable, communication weakened, and development priorities drifted out of sync. This created challenges not just for napari, but for the researchers who depend on it.

This isn't unique to napari. Across scientific software, the relationship between foundational tools and their domain-specific extensions often becomes transactional rather than collaborative. Without active coordination, downstream developers risk duplicating efforts and struggling with maintenance, while foundational tools miss valuable input from their communities.

With support from the URSSI Early Career Fellowship and the Sloan Foundation, I've spent the past months working with the napari community to tackle this problem. Our goal: build infrastructure and practices that other scientific software communities can learn from and adapt.

## How I got here

[PLACEHOLDER: Your personal story - starting as independent plugin author of napari-ndev, experiencing the communication gap firsthand, challenges faced, transition to core contributor and community manager, what this journey revealed about the foundational-downstream divide]

## The Problem: How Ecosystems Drift Apart

The napari plugin ecosystem had a promising start. [CZI plugin grants](https://chanzuckerberg.com/rfa/napari-plugin-grants/) bootstrapped dozens of plugins, energy was high, and the community was growing. But this growth coincided with real challenges: an immature plugin system, many contributors new to Python packaging, and limited infrastructure for long-term maintenance.

When grants ended, the difficulties became apparent:

- Plugin maintenance slowed or stalled
- Communication between plugin developers and core napari weakened  
- A gap formed between what plugin developers needed and what core contributors knew about

Our 2023 napari survey captured the disconnect: 86% of respondents said creating a plugin was easy, but many cited unsustainable maintenance burden. Year over year, perceptions of how easy it was to contribute to napari core declined.

In community meetings, we heard consistent pain points: dependency conflicts with file format readers and writers, difficulty with deep learning tools, poor plugin discoverability, and uncertainty about what belongs in core versus what should be a plugin. Perhaps most telling—domain scientists building research software often lacked time, resources, or expertise for sustainable development, yet saw no clear path to get help.

The disconnect was mutual. Plugin developers felt dependent on napari but disconnected from its direction. Core contributors, focused on stabilizing napari itself, had lost awareness of what the broader ecosystem needed.

## What We Learned From Community Conversations

The most surprising thing about the working group wasn't the list of challenges—most were familiar. It was how much people wanted to help solve them.

Plugin developers volunteered to review each other's work. Facility staff offered to write documentation about Git basics. Experienced developers proposed programs where unmaintained plugins could find new maintainers. The conversation shifted from "what should napari provide" to "what can we build together."

One participant captured it well: plugin developers often see the core team as shepherds of the ecosystem without understanding the work involved in contributing to core. Meanwhile, plugin developers rely on the core team in ways the core team doesn't always realize and can't always support. What emerged clearly: people *want* to contribute beyond the core team—they just need the right infrastructure and invitation.

This desire to collaborate rather than consume is the foundation we're building on.

## What We're Building

The plugin sustainability initiative centers on three main objectives:

### 1. Modernize plugin development infrastructure

We're updating the [napari-plugin-template](http://github.com/napari/napari-plugin-template) and [documentation](https://napari.org/stable/plugins/index.html) to align with current best practices from [PyOpenSci](https://www.pyopensci.org/) and [Scientific Python](https://scientific-python.org/). This includes:

- Clear guidance for developers new to Python packaging
- Sustainable design patterns (like separating computational logic from visualization)
- Upgrade paths for legacy plugins to adopt modern practices

### 2. Build community review systems

Drawing inspiration from PyOpenSci's peer review process, we're creating both automated and human review infrastructure:

- **Automated quality checks** that catch common issues early (think friendly CI that suggests improvements)
- **Human review processes** where community volunteers provide feedback on maintainability and discoverability
- Community members have already volunteered as reviewers, suggesting approaches from automated repository checks to live video review sessions

### 3. Create recognition and affiliation programs

Modeled on [Astropy's affiliate program](https://www.astropy.org/affiliated/index.html), we're developing ways to:

- Recognize plugin contributions across domains
- Enable plugin donation programs where maintainers can hand off to willing stewards
- Support maintainer partnerships, potentially through a napari-plugins GitHub organization
- Lower barriers to collaborative maintenance

All of this work is happening through a plugin sustainability working group that meets at different times to include global participation. The group brings together core developers, plugin authors, facility staff, and users for open collaboration.

## Why It Matters Beyond napari

These challenges—sustaining domain-specific extensions, coordinating between foundational and downstream development, supporting novice contributors while maintaining quality—show up across scientific software. They're present in Python's scientific stack, astronomy tools, geosciences platforms, and beyond.

What might transfer from this work isn't specific technology, but an approach:

1. **Shift from viewing extensions as external to seeing them as collaborative partners**
2. **Create shared ownership** through working groups that span core and plugin developers
3. **Build infrastructure for collaboration**, not just distribution—review systems, donation programs, maintainer partnerships
4. **Enable cross-domain learning** where advances in one field benefit others through upstream contributions
5. **Recognize the full range of contributions** across the ecosystem

Our findings will help:

- Document sustainable practices for coordinating foundational tools and their extensions
- Provide reusable infrastructure (templates, review tools, affiliation models)
- Share lessons learned about community engagement across diverse stakeholder groups
- Support other projects facing similar sustainability challenges

All resources we create—updated templates, review tools, documentation—will be open source and documented for adaptation by other communities.

## How We're Engaging the Community

A central part of this project is open collaboration:

1. **Open resources**: The updated plugin template, review tools, and documentation will be published under permissive licenses with thorough documentation
2. **Collaborative working group**: Ongoing meetings at multiple times for global participation, with open Zulip and GitHub channels for asynchronous discussion
3. **Transparent process**: Regular updates shared with the community about progress and decisions
4. **Cross-community learning**: Plans to share findings at conferences like SciPy and through blog posts and documentation

## Thank You

This project is supported by the URSSI Early Career Fellowship, with funding from the Sloan Foundation. The fellowship provides both research support and the opportunity to engage deeply with the scientific software community.

Without this support, building these collaborative relationships and infrastructure wouldn't be possible. Thank you to URSSI and the Sloan Foundation for supporting this work, and to the napari community for showing up to build this together.

The most important outcome isn't any particular tool—it's the renewed collaborative relationship between napari and its plugin ecosystem. When foundational tools and their extensions work together, everyone benefits: developers don't duplicate effort, users get more reliable tools, and research moves forward on steadier ground.

## Contact and Follow Along

If you're working on scientific software with an extension ecosystem, or you're curious about sustainability practices for open source communities, I'd love to hear from you.

Follow our progress on [GitHub](https://github.com/napari), join conversations on [Zulip](https://napari.zulipchat.com/), or reach out directly at [PLACEHOLDER: your email].

We'll be sharing updates on infrastructure releases, working group insights, and early results from the affiliation program in the coming months.
