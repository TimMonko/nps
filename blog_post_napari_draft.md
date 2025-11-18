# The napari plugin sustainability initiative

One of napari's biggest strengths has always been how extensible it is. With over 500 plugins on the [napari hub](https://napari-hub.org/), our community has built tools for everything from neuroscience to materials science, single-cell analysis to lattice light-sheet microscopy. These plugins represent deep expertise and solve problems that napari core could never address on its own.

But we need to talk about what it takes to keep this ecosystem healthy over the long term.

## How I got here

[PLACEHOLDER: Your personal story - starting as plugin author of napari-ndev, the challenges you faced, what motivated your transition to core contributor and community manager, and how this gives you perspective on both sides of the plugin ecosystem]

## Where we've been

The early days of napari plugins were exciting. The [CZI plugin grants](https://chanzuckerberg.com/rfa/napari-plugin-grants/) got a lot of plugins off the ground, the [plugin template](http://github.com/napari/napari-plugin-template) made it easier to get started, and there was a lot of energy in the community.

But that initial push came with challenges we're still dealing with. A lot of us were new to Python packaging. The plugin system itself was still figuring things out. We didn't have great infrastructure for long-term maintenance. When grants ended and the initial excitement wore off, the reality of sustainable software development set in. Maintenance became burdensome. Communication between plugin developers and the core team got quieter. A gap formed—not because anyone stopped caring, but because doing research software is hard.

Our 2023 survey showed this pretty clearly: 86% of you said making a plugin was easy, but many mentioned the burden of keeping it maintained. Year over year, people felt it was getting harder to contribute to napari itself.

The good news is that napari is in a strong place right now. With new funding and momentum, the project is doing well, and we're hearing positive feedback from users, core developers, and plugin maintainers. This feels like the right time to address the gap.

## What we've been learning

Over the past months, we've been running a plugin sustainability working group, meeting at different times to include people across time zones. The conversations have been really helpful—not just for understanding what people need, but for seeing how much the community wants to help build solutions.

Here's what we've heard:

**The basics are still hard for a lot of people.** We need better documentation for fundamentals—using Git and GitHub, understanding packaging, navigating the tooling. These aren't exciting topics, but they're real barriers for domain scientists trying to write sustainable software.

**People want plugin review.** Multiple folks said they'd be interested in both giving and getting feedback on plugins. Some suggested automated checks for best practices, others mentioned human reviews, even live video sessions. The key thing: people want guidance and feedback, not gatekeeping.

**The same pain points keep coming up.** Readers and writers are a consistent problem, along with dependency conflicts and getting deep learning/GPU tools to work. These affect developers and users both.

**People want to help.** This has been the most encouraging part. Plugin developers want to review other people's plugins, improve documentation, help maintain community tools, even volunteer to take over plugins that need new maintainers.

One theme that's come through clearly: a lot of plugin developers see the core napari team as shepherds of the ecosystem, but feel somewhat separate from it—dependent on it, but without much input into where it's going. What the working group has shown is that the community *wants* to be part of shaping our collective future.

## What we're working on

Based on your feedback, here's what we're focusing on:

**Updated infrastructure.** We're modernizing the [plugin template](http://github.com/napari/napari-plugin-template) and [documentation](https://napari.org/stable/plugins/index.html) to follow current best practices from [PyOpenSci](https://www.pyopensci.org/) and [Scientific Python](https://scientific-python.org/). This includes better guidance on things like separating your computational code from your visualization code (MVC/MVP patterns that make maintenance easier), clearer explanations of when to use different approaches, and resources for different experience levels.

**Plugin review systems.** We're setting up both automated quality checks and human review. The automated tools will help catch common issues early—think of it as a friendly CI check that suggests improvements. The human review component, inspired by PyOpenSci, will give you personalized feedback on making your plugin more maintainable and discoverable.

**Affiliation and recognition.** We're creating a plugin affiliation program that recognizes contributions and encourages collaboration across domains. This includes exploring plugin donation programs (where you can hand off a plugin to a willing new maintainer), maintainer partnerships, and potentially a napari-plugins GitHub organization to make collaborative maintenance easier.

**Better communication.** We're working on clearer ways to let plugin developers know about napari API changes and new features that might be useful. We're also looking at better tagging and discoverability for plugins, to help users find the right tools and developers find potential collaborators.

## Where we're headed

This isn't about the core team "fixing" the plugin ecosystem—it's about all of us building it together. The sustainability initiative is about creating infrastructure and processes that let the community support itself, share knowledge across domains, and make napari's extensibility not just powerful, but sustainable.

Napari is in a good place right now. We have momentum, resources, and—most importantly—a community that wants to collaborate. The plugin ecosystem is maturing alongside core development. We're working to make sure that growth is sustainable for everyone.

## Get involved

[PLACEHOLDER: Your specific call to action - how people can join working group meetings, volunteer for reviews, share their experiences, etc.]

Here are some ways you can participate:

- **Join the working group meetings** [add details/links]
- **Volunteer to review plugins** [add how to sign up]
- **Share your experiences**—what's worked, what hasn't [add discussion link]
- **Test the updated template and docs** and give us feedback
- **Consider plugin partnerships**—if you have an unmaintained plugin or want to co-maintain something, let us know
- **Help with documentation**, especially the getting-started guides

## Let's build this together

The napari plugin ecosystem represents a lot of collective expertise and effort. When we invest in making it sustainable—through better infrastructure, collaborative review, shared maintenance—everyone benefits. Plugin developers get support and recognition. Users get more reliable tools. Core napari gets valuable input from the community. Research moves forward on stronger foundations.

This is about more than just maintaining code. It's about building a community where we support each other's work, learn across domains, and make sure napari continues serving diverse scientific needs for years to come.

---

*Questions or ideas about plugin sustainability? Join us on [Zulip](https://napari.zulipchat.com/) or [GitHub discussions](https://github.com/napari/napari/discussions).*
