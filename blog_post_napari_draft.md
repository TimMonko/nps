# The napari plugin sustainability initiative

One of napari's biggest strengths has always been how extensible it is. With over 500 plugins on the [napari hub](https://napari-hub.org/), our community has built tools for everything from neuroscience to materials science, single-cell analysis to lattice light-sheet microscopy. These plugins represent real expertise and solve problems that napari core could never tackle on its own.

But we need to talk about what it takes to keep this ecosystem healthy.

## How I got here

[PLACEHOLDER: Your personal story - starting as plugin author of napari-ndev, the challenges you faced, what motivated your transition to core contributor and community manager, and how this gives you perspective on both sides of the plugin ecosystem]

## Where we've been

The early days of napari plugins were exciting. The [CZI plugin grants](https://chanzuckerberg.com/rfa/napari-plugin-grants/) got a lot of plugins started, the [plugin template](http://github.com/napari/napari-plugin-template) made it easier to begin, and there was real energy in the community.

But that early momentum came with challenges we're still working through. A lot of us were new to Python packaging. The plugin system was still figuring itself out. We didn't have solid infrastructure for long-term maintenance. When grants ended and the initial excitement wore off, the reality of sustainable software development hit. Maintenance got hard. Communication between plugin developers and the core team got quieter. A gap formed—not because anyone stopped caring, but because research software is genuinely difficult to sustain.

Our 2023 survey showed this clearly: 86% of you said making a plugin was easy, but many mentioned the burden of keeping it maintained. Year over year, people felt contributing to napari core was getting harder.

The good news? Napari is in a strong place right now. With new funding and momentum, the project is doing well, and we're hearing positive feedback from users, core developers, and plugin developers. This feels like the right time to close that gap.

## What we've been learning

Over the past months, we've been running a plugin sustainability working group—meeting at different times to include people across time zones. The conversations have been really helpful, not just for understanding what people need, but for seeing how much you all want to help build solutions.

Here's what we've heard:

**The basics are still barriers for many people.** We need better documentation for fundamentals—using Git and GitHub, understanding packaging, navigating the tooling landscape. These aren't exciting topics, but they're real obstacles for domain scientists trying to write sustainable software. Someone even linked [PyMODAQ's Git tutorial](https://pymodaq.cnrs.fr/en/latest/tutorials/git_tutorial.html) as an example of the kind of resource that's helpful.

**People want plugin review—both giving and getting it.** Multiple folks said they'd be interested in reviewing other people's plugins and getting feedback on their own. Some suggested automated checks (like a repo-review bot), others mentioned human reviews, even live video sessions with privacy options. The key thing: people want guidance and feedback, not gatekeeping. There's genuine interest in something like PyOpenSci's peer review process.

**The same pain points keep coming up.** Readers and writers are a consistent problem—dependency hell with things like `napari-aicsimageio`, which tries to support everything but creates complex environments. Deep learning and GPU tools are hard to get working reliably (especially things like StarDist on Windows). These affect both developers and users.

**People want to help.** This has been the most encouraging part. Plugin developers want to review each other's plugins, improve documentation, help maintain community tools, even volunteer to take over plugins that need new maintainers. There's talk of plugin donation programs, maintainer partnerships, maybe even a napari-plugins GitHub organization to make collaborative maintenance easier.

**Communication about napari changes could be better.** People want to know when napari's API changes or when new features come out that might be useful for plugins. We also need better plugin discovery—better tagging, clearer communication about what plugins do and how they fit together. Some mentioned wanting to know which plugins work well together (like knowing when packages pin Qt5).

One theme came through really clearly: many plugin developers see the core napari team as shepherds of the ecosystem, but feel somewhat separate from it—dependent on it, but without much say in where things go. What the working group has shown is that you *want* to be part of shaping where we're headed together.

## What we're working on

Based on what you've told us, here's what we're focusing on:

**Updated infrastructure.** We're modernizing the [plugin template](http://github.com/napari/napari-plugin-template) and [documentation](https://napari.org/stable/plugins/index.html) to follow current best practices from [PyOpenSci](https://www.pyopensci.org/) and [Scientific Python](https://scientific-python.org/). This includes:
- Better guidance on separating your computational code from your visualization code (MVC/MVP patterns that make maintenance way easier)
- Clearer explanations of when to use `@magicgui` versus building Qt widgets directly
- Documentation for the real basics—how to use Git, how GitHub works, how to set up testing
- Resources for different experience levels, from beginners to experienced developers

**Plugin review systems.** We're setting up both automated and human review:
- Automated tools that catch common issues early—think of it as a friendly CI check that suggests improvements
- Human review inspired by PyOpenSci, where you get personalized feedback on making your plugin more maintainable and discoverable
- Repo-review bots that check for best practices
- Possibly live review sessions (with privacy options) for people who want more direct feedback

**Affiliation and recognition.** We're creating a plugin affiliation program that recognizes contributions and encourages collaboration:
- Plugin donation programs where you can hand off a plugin to a willing new maintainer
- Maintainer partnerships to share the load
- Potentially a napari-plugins GitHub organization where community members can get "plugin contributor" or "plugin maintainer" roles that work across multiple repos
- Making it easier for plugins to become part of the broader napari ecosystem without requiring individual maintainers to do everything

**Better communication and discovery.** We're working on:
- Clearer ways to let plugin developers know about napari API changes and new features
- Better tagging and classification for plugins (possibly using existing Trove classifiers or adding to `napari.yaml`)
- Improved plugin discoverability on the hub
- Helping users understand which plugins work well together, like smaller bundles that complement the full napari bundle

## Get involved

This isn't about the core team "fixing" the plugin ecosystem—it's about all of us building it together. The sustainability initiative is creating infrastructure and processes that let the community support itself, share knowledge across domains, and make napari's extensibility sustainable for everyone.

Napari is in a good place. We have momentum, resources, and—most importantly—a community that wants to collaborate. The plugin ecosystem is maturing alongside core development. We're working to make sure that growth is sustainable for everyone.

[PLACEHOLDER: Your specific call to action - how people can join working group meetings, volunteer for reviews, share their experiences, etc.]

Here are some ways you can get involved:

- **Join the working group meetings** [add details/links]
- **Volunteer to review plugins** [add how to sign up]
- **Share your experiences**—what's worked, what hasn't, what you need [add discussion link]
- **Test the updated template and docs** and give us feedback
- **Consider plugin partnerships**—if you have an unmaintained plugin or want to co-maintain something, let us know
- **Help with documentation**, especially the getting-started guides for people new to packaging

## Let's build this together

The napari plugin ecosystem represents a lot of collective expertise and effort. When we invest in making it sustainable—through better infrastructure, collaborative review, shared maintenance—everyone benefits. Plugin developers get support and recognition. Users get more reliable tools. Core napari gets valuable input from the community. Research moves forward on stronger foundations.

This is about more than just maintaining code. It's about building a community where we support each other's work, learn across domains, and make sure napari keeps serving diverse scientific needs for years to come.

---

*Questions or ideas about plugin sustainability? Join us on [Zulip](https://napari.zulipchat.com/) or [GitHub discussions](https://github.com/napari/napari/discussions).*
