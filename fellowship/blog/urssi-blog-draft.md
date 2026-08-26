# URSSI Fall Fellowship: Building Sustainable Plugin Ecosystems in Scientific Software

Tim Monko

*November 2025*

## When Plugins and Core Projects Lose Touch

[PLACEHOLDER: Brief introduction to napari - what it is, who uses it, how the plugin system works. Explain the scientific imaging context and Python ecosystem for readers who may not be familiar. 2-3 paragraphs explaining napari as a foundational tool with 500+ plugins, used across domains from neuroscience to materials science.]

But over the past few years, something concerning happened: collaboration between plugin developers and the core napari team started to decline. Maintenance became harder to sustain, communication got quieter, and priorities drifted out of sync. This wasn't just a napari problem—it's a pattern I've seen repeated across scientific software, where the relationship between foundational tools and their domain-specific extensions becomes transactional rather than collaborative.

With support from the URSSI Early Career Fellowship and the Sloan Foundation, I've been working with the napari community to address this. Our goal is to build infrastructure and practices that other scientific software communities can learn from and adapt.

## How I Got Here

[PLACEHOLDER: Your personal story - starting as independent plugin author of napari-ndev, experiencing the communication gap firsthand, challenges faced, transition to core contributor and community manager, what this journey revealed about the foundational-downstream divide]

## How I got here

[PLACEHOLDER: Your personal story - starting as independent plugin author of napari-ndev, experiencing the communication gap firsthand, challenges faced, transition to core contributor and community manager, what this journey revealed about the foundational-downstream divide]

## The Problem: How Ecosystems Drift Apart

The napari plugin ecosystem got off to a strong start. [CZI plugin grants](https://chanzuckerberg.com/rfa/napari-plugin-grants/) bootstrapped dozens of plugins, the community was energized, and there was genuine excitement about what was possible. But that early growth came with challenges: the plugin system was still maturing, many contributors were new to Python packaging, and infrastructure for long-term maintenance was limited.

When grants ended, things got harder:

- Plugin maintenance slowed or stopped entirely
- Communication between plugin developers and core napari got quieter
- A gap opened up between what plugin developers needed and what core contributors knew about

Our 2023 napari survey captured this disconnect well: 86% of respondents said creating a plugin was easy, but many mentioned the burden of maintenance. Year over year, people felt it was getting harder to contribute to napari core.

In community meetings, certain pain points kept coming up: dependency hell with file format readers and writers (especially `napari-aicsimageio`), getting deep learning and GPU tools to work reliably, plugins being hard to discover, confusion about what belongs in core napari versus what should be a plugin. Maybe most telling—domain scientists writing research software often didn't have time, resources, or expertise for sustainable development, but they didn't see a clear path to get help either.

The disconnect went both ways. Plugin developers felt dependent on napari but disconnected from where it was headed. Core contributors, focused on stabilizing napari itself, had lost touch with what the broader ecosystem needed.

## What We Learned From Community Conversations

The most surprising part of the working group wasn't the list of challenges—most of those were already familiar. It was how much people wanted to help fix them.

Plugin developers volunteered to review each other's work. Facility staff offered to write documentation about Git basics. Experienced developers suggested programs where unmaintained plugins could find new maintainers. The conversation wasn't "what should napari do for us," it was "what can we build together."

Someone in one of the meetings put it well: plugin developers often see the core team as shepherds of the whole ecosystem, but don't necessarily understand how much work it takes to contribute to core. At the same time, plugin developers rely on the core team in ways the core team doesn't always know about and can't always support. What came through clearly: people *want* to contribute beyond the core team—they just need the right infrastructure and invitation to do it.

That desire to collaborate rather than just consume—that's what we're building on.

## What We're Building

The plugin sustainability initiative has three main objectives:

### 1. Modernize plugin development infrastructure

We're updating the [napari-plugin-template](http://github.com/napari/napari-plugin-template) and [documentation](https://napari.org/stable/plugins/index.html) to follow current best practices from [PyOpenSci](https://www.pyopensci.org/) and [Scientific Python](https://scientific-python.org/). This means:

- Clearer guidance for people new to Python packaging
- Better documentation of sustainable design patterns (like how to separate your computational code from your visualization code)
- Helping people learn the basics—Git, GitHub, testing, CI—without assuming prior knowledge
- Upgrade paths for existing plugins to adopt modern practices

### 2. Build community review systems

We're setting up both automated and human review, inspired by PyOpenSci's peer review process:

- **Automated quality checks** that catch common issues early—like a friendly CI bot that suggests improvements
- **Human review** where community volunteers give feedback on making plugins more maintainable and discoverable
- Community members have already volunteered to review, suggesting everything from automated repo-health checks to live video review sessions

### 3. Create recognition and affiliation programs

Looking at models like [Astropy's affiliate program](https://www.astropy.org/affiliated/index.html), we're figuring out how to:

- Recognize plugin contributions across different domains
- Enable plugin donation programs where maintainers can hand off plugins to willing new stewards
- Support maintainer partnerships, potentially through a napari-plugins GitHub organization
- Make collaborative maintenance easier and less intimidating

All this work happens through a plugin sustainability working group that meets at different times for global participation. The group includes core developers, plugin authors, facility staff, and users.

## Why It Matters Beyond napari

These challenges—sustaining domain-specific extensions, coordinating between foundational and downstream projects, supporting novice contributors while maintaining quality—aren't unique to napari. They show up across scientific software, from Python's scientific ecosystem to astronomy tools to geosciences platforms.

What might be transferable from this work isn't any particular piece of technology, but the approach:

1. **Thinking about extensions as collaborative partners**, not external add-ons
2. **Creating shared ownership** through working groups that include both core and extension developers
3. **Building infrastructure for collaboration**, not just distribution—review systems, donation programs, maintainer partnerships
4. **Enabling cross-domain learning** where advances in one field benefit others through upstream contributions
5. **Recognizing all kinds of contributions** across the ecosystem

Our work will produce:

- Documentation of sustainable practices for coordinating foundational tools and their extensions
- Reusable infrastructure (templates, review tools, affiliation models) that other projects can adapt
- Lessons learned about community engagement across diverse groups
- Support for other projects facing similar challenges

Everything we create—updated templates, review tools, documentation—will be open source and documented so other communities can use and adapt it.

## How We're Engaging the Community

Open collaboration is central to this project:

1. **Open resources**: The updated plugin template, review tools, and documentation will all be published under permissive licenses with documentation for how to adapt them
2. **Collaborative working group**: We meet at multiple times for global participation, with open Zulip and GitHub channels for async discussion
3. **Transparent process**: We share regular updates with the community about what we're doing and why
4. **Cross-community learning**: We're planning to share what we learn at conferences like SciPy and through blog posts and documentation

## Thank You

This project is supported by the URSSI Early Career Fellowship, with funding from the Sloan Foundation. The fellowship gives me both research support and the opportunity to engage deeply with the scientific software community.

Without this support, building these relationships and infrastructure wouldn't be possible. Thank you to URSSI and the Sloan Foundation for making this work possible, and to the napari community for showing up and being willing to build this together.

Honestly, the most important outcome isn't any particular tool or program—it's the collaborative relationship between napari and its plugin ecosystem feeling healthier than it has in a while. When foundational tools and their extensions work together, everyone benefits: developers don't duplicate effort, users get more reliable tools, and research moves forward on steadier ground.

## Contact and Follow Along

If you're working on scientific software with an extension ecosystem, or if you're curious about sustainability practices for open source communities, I'd love to hear from you.

You can follow our progress on [GitHub](https://github.com/napari), join conversations on [Zulip](https://napari.zulipchat.com/), or reach out to me directly at [PLACEHOLDER: your email].

We'll be sharing updates on infrastructure releases, insights from the working group, and early results from the affiliation program over the coming months.
