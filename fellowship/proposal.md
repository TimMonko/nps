# Broadening napari’s role in scientific research through sustainable communication and collaboration with its domain-specific plugin ecosystem

## Project Goals and Objectives

Foundational scientific software tools deliver innovative, yet reliable methods for research across multiple domains. These tools often rely on community expansion by “downstream” libraries to meet domain-specific needs. [Napari](http://github.com/napari/napari), an open-source, multidimensional image viewer in Python, provides core infrastructure for visualizing and annotating scientific imaging data. Its extendable GUI has empowered a diverse ecosystem of over 500 [community-developed plugins](https://napari-hub.org/) (i.e., downstream libraries). Since the public announcement of napari in 2019 and the addition of plugin support soon after, collaboration among core contributors, plugin authors, and users has enabled research workflows that no single library could accomplish alone.

The napari project maintains key infrastructure for plugin developers and users, including an easily searchable [napari-hub](https://napari-hub.org/) website, a GUI to easily download plugins with the [napari-plugin-manager](https://github.com/napari/napari-plugin-manager), and tools to easily create plugins (including [documentation](https://napari.org/stable/plugins/index.html) and the [napari-plugin-template](http://github.com/napari/napari-plugin-template)). However, in recent years collaboration between plugin developers and the napari project has declined, leading to misaligned development priorities and unsustainable plugin development and maintenance. The 2023 napari survey (private) found that while 86% of respondents said contributing a plugin is easy, many noted the burden of maintenance; in addition, perceptions of ease in contributing to the napari project have declined annually.

As napari community manager, I have found that plugin developers often have deep expertise but limited interaction with napari core, while core contributors are unaware of the full breadth of available plugins. I experienced this gap firsthand—starting as an independent plugin author of [napari-ndev](http://github.com/ndev-kit/napari-ndev) long before becoming a core contributor—and saw how difficult it can be for foundational and downstream projects to communicate effectively. However, there is a consistent desire for there to be infrastructure to encourage and improve communication across the napari ecosystem. The present disconnect hampers sustainable development, not only in napari but across research software ecosystems. Without improved coordination, downstream authors risk duplication of efforts and suffer unsustainable maintenance burden, while foundational tools miss beneficial direction from the community.

This fellowship will therefore focus on improved infrastructure and effective communication for napari and its plugin ecosystem to leverage advances in one domain to other scientific domains. Thus, the fellowship will create a model transferable to other scientific software communities. Throughout the URSSI Fellowship, I will:

1. **Modernize the napari plugin development infrastructure** by updating the napari-plugin-template and documentation to follow current best practices from [Scientific Python](https://scientific-python.org/) and [PyOpenSci](https://www.pyopensci.org/), with a focus on sustainable design for novice package developers.

2. **Build shared, accessible communication channels and a plugin sustainability working group** that engenders proactive feedback and collaborative development between plugin authors, users, and the core napari project. 

3. **Create an initiative that encourages best practices and highlights community efforts** as a sustainable means for plugin authors to receive recognition and feedback in a way that collaborates with and advances the whole napari ecosystem.

4. **Document and share transferable guidance** for sustaining community advancement and mutual coordination between domain-specific extensions and foundational tools.

## Expected Impact on Scientific Software Community

Sustaining domain-specific extensions in cooperation with shared infrastructure is a widespread challenge in research software. In the napari ecosystem, many plugins were bootstrapped by [targeted grants](https://chanzuckerberg.com/rfa/napari-plugin-grants/), but maintenance often stagnated as funding ended and communication weakened, creating a divide between some widely used plugins and ongoing core development.

By improving tools and norms for foundational-downstream developer communication, this project aims to enable collaborative, rather than transactional, relationships among developers and support the shared adoption of current software development standards amongst both legacy and new plugins. Resources from [PyOpenSci](https://www.pyopensci.org/) and [Scientific Python](https://learn.scientific-python.org/development/) will be used to align standards of sustainable development while models like [Astropy’s](https://www.astropy.org/affiliated/index.html) affiliate program will inform a cross-domain, inclusive plugin recognition process. 

This project will produce a transferable model for shared development, where advances in one domain can be adapted across others. A shared upstream napari resource will serve to reduce duplication of effort, reduce maintenance burden, and generalize domain-specific functionality.  Improving the collaborative experience between foundational and downstream libraries will advance URSSI’s goal of improving long-term usability and interoperability of scientific software.

## Community Engagement Strategy

Engagement between plugin authors and the core napari team is central to building a  sustainable, community-maintained framework. Following napari’s successful working-group model that has introduced key progress in napari including the initial plugin implementations, I will lead the establishment of a plugin-sustainability working group through an open call made on our Github, [Zulip chat](https://napari.zulipchat.com/), [social media](https://bsky.app/profile/napari.org), and domain-specific forums. Both new and long-term plugin developers will be directly contacted for contributions in order to encourage a diverse set of perspectives. Domains that are not strongly integrated into the napari community will be sought out for participation. We will meet fortnightly at different times to accommodate global participation on Zoom, with asynchronous conversation on Zulip and Github. Weekly updates will be shared with the community. Community engagement will focus on generating a sustainable conversation where the napari core team, plugin developers, and napari users continue collaboration to improve all parts of the napari project. 

### **Month 1**

* Launch open call, establish the plugin sustainability working group and hold the first meeting.  
* Audit the napari-plugin-template and related documentation. Begin updates on improving packaging resources to meet modern best practices.

### **Month 2**

* Plan long-term plugin and project affiliation strategy with the napari community ensuring inclusivity beyond the most established plugins.  
* Continue working group activities, focused on identifying how core napari, plugin developers, and users envision a successful sustainable partnership.  
* Continue updates to the napari-plugin-template and plugin sustainability documentation.

### **Month 3**

* Implement initial communication and maintenance strategies identified by the working group, with continued group effort used to build a stronger community.  
* Begin implementation of the sustainable plugin affiliation program, creating a community organized unbiased review tool (modeled on [napari-hub-cli](https://github.com/chanzuckerberg/napari-hub-cli)) and team of reviewers sourced from both the napari core team and plugin authors.

### **Month 4**

* Modification of plugin affiliation program to address feedback, with this likely becoming the focus of the working group.  
* Completion of updates to the napari-plugin-template and related documentation. Improvements will focus on weaknesses or challenges identified by the working group.   
* Distribute the napari annual survey with additional questions tailored towards the goals of this project. Subsets of questions will be present whether a person is a napari contributor, plugin author, or user and be used to find weaknesses and strengths of the plugin system.

### **Month 5**

* Summarization and dissemination of the napari annual survey results to the community, using insights to further improve napari plugin sustainability.  
* Full effort put towards implementation of the plugin affiliation program and finding successful approaches to getting recognition and collaboration with the broader community.  
* Use of the napari annual survey results in collaboration with the plugin sustainability working group to guide modification of resources, project affiliation, and strategization.

### **Month 6**

* Share outcomes and learned practices with the broader scientific software research community, with a focus on sharing the cross-domain efforts that created a successful, collaborative, sustainable ecosystem.  
* Prepare materials for submission to a scientific research conference, such as SciPy.

## Evaluation Metrics

1. **Increased collaboration between the core napari project and the broader community** will be qualitatively evaluated by observations of both synchronous and asynchronous communication, especially through the plugin sustainability working group, and quantitatively by observing increased contributors to the napari project from non core contributors.  
2. **Modernization and sustainability efforts of plugins** will be evaluated quantitatively by the number of plugins implementing modern best practices and number of new plugins made with the improved napari-plugin-template.  
3. **The affiliation program** will be evaluated by number of program reviewers, number of affiliated plugins, and general community feedback about recognition, equity, and growth.  
4. **Upstreaming fellowship project efforts** will be evaluated by scientific python community sentiment and feedback during efforts to incorporate projects in broader scientific software communities like Scientific Python, PyOpenSci and The Turing Way.

## Project Deliverables

1. Continuation of **plugin sustainability working groups** and efforts therein to encourage **collaboration and mutually beneficial development** of napari and the plugin ecosystem.  
2. The napari plugin **affiliation program**, serving as a model for foundational tools to have sustainable interactions with downstream cross-domain tools.  
3. **Shared resources** highlighting collaborative communication strategies and cross-domain sustainability practices developed during the fellowship. 