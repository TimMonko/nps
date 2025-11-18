# Blog Post Implementation Plan

## Overview

Creating two blog posts about the napari plugin sustainability initiative:

1. **URSSI blog** - for broader scientific software community
2. **napari blog** - for napari community

## Key Requirements

### Tone and Style

- Natural, conversational voice (not LLM-corporate)
- Professional but accessible
- Direct and clear language
- Active voice
- Based on successful examples:
  - napari sustainability survey blog: https://napari.org/island-dispatch/blog/sustainability_survey.html
  - URSSI LLM fellowship blog: https://urssi.us/blog/2025/11/03/urssi-fall-fellowship-characterizing-the-impact-of-llm-generated-code-in-scientific-software/

### URSSI Blog Specifications

**Audience:** Broader scientific software / computing community (may not know napari)

**Structure:**

- Title: "URSSI Fall Fellowship: [Topic]"
- Author name and date at top
- Clear section headers:
  - "When [Problem Framing]"
  - "The Problem: [Description]"
  - "What We're Building" (with numbered objectives and subsections)
  - "What We Learned From Community Conversations"
  - "Why It Matters Beyond napari"
  - "How We're Engaging the Community"
  - "Thank You"
  - "Contact and Follow Along"

**Content Requirements:**

- Must introduce napari, scientific imaging context, and plugin ecosystem for external audience
- Acknowledge URSSI and Sloan Foundation support prominently
- Emphasize transferability to other scientific software communities
- Include Tim's personal story (plugin author → community manager)
- Highlight community-driven approach (not top-down)
- Use concrete examples from community meetings
- Focus on collaboration over transaction

**Length:** ~5 minute read

**Placeholders needed:**

- Introduction to napari and plugin ecosystem (2-3 paragraphs)
- Tim's personal story section
- Tim's contact email

### napari Blog Specifications

**Audience:** Existing napari community (users, developers, plugin authors)

**Structure:**

- Title: Simple and direct
- Section headers:
  - Introduction (brief, sets up sustainability topic)
  - "How I got here"
  - "Where we've been"
  - "What we've been learning"
  - "What we're working on"
  - "Where we're headed"
  - "Get involved"
  - Conclusion

**Content Requirements:**
- Assume familiarity with napari
- More specific community feedback details from meetings
- Direct call to action with concrete participation options
- Emphasize "we're in this together" 
- Include specific meeting notes/themes from Atlantic and Pacific sessions
- Conversational but professional tone

**Length:** ~5 minute read

**Placeholders needed:**

- Tim's personal story (napari-community focused)
- Specific call to action details (meeting links, how to volunteer, etc.)

## Community Meeting Themes to Include

### From Atlantic Session (2025/11/12)

- Need for standardized way to write plugins / "how to write code correctly"
- repo-review bot suggestions
- Live review possibilities (with privacy options)
- Motivation barriers for learning tooling
- Bundle improvements and advertising
- "Maintainer partner" / plugin donation ideas
- napari-plugin organization concept
- PyOpenSci-style review
- Readers/writers dependency hell issues
- Multi-package repos vs mono-repos

### From Pacific Session (2025/10/09)

- Plugin review desire (both giving and receiving)
- Documentation for getting started from ground up
- Automated quality check tooling
- Best practices documentation needed
- Plugin donation program (NAP proposal idea)
- Automated and human review
- Analytics discussion (showing metrics)
- PyOpenSci peer review model

## Key Messages

### Both Blogs Should Convey:

1. **The initial challenge:** Early boom with CZI grants, followed by maintenance stagnation and communication breakdown
2. **The mutual disconnect:** Plugin developers felt dependent but disconnected; core team lost awareness of ecosystem needs
3. **The surprise:** Community wants to *help build* solutions, not just receive them
4. **The approach:** Collaborative rather than transactional relationships
5. **The momentum:** napari itself is reinvigorated and on positive trajectory
6. **The goal:** Sustainable ecosystem where advances in one domain benefit others

### What to Avoid:

- LLM corporate speak ("leverage," "empower," "ecosystem synergy")
- Overly formal academic language
- Buzzwords and jargon
- Making it sound polished/perfect
- Top-down framing (should be collaborative)

### What to Include:

- Concrete examples from meetings
- Specific pain points (dependency hell, DL tools, readers/writers)
- Real quotes or paraphrased perspectives
- Honest acknowledgment of challenges
- Emphasis on community volunteers and contributions

## Reference Materials

- `blog_post_fellowship.md` - fellowship proposal (context, motivation, plans)
- `blog_post_hack.md` - community meeting notes (Atlantic & Pacific sessions)
- `blog_post_plan.md` - original planning document

## Implementation Notes

- Write in first person (Tim's voice)
- Use contractions where natural
- Short paragraphs for readability
- Bullet points for lists of features/approaches
- Be specific rather than general
- Show don't tell (use examples)
