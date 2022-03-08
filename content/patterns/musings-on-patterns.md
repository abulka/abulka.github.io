---
title: "Appendix: Musings on Design Patterns"
date: 1900
type: docs
description: "Are design patterns dead?"
draft: false
---

Capturing hard-won software design experience in the form of design patterns and
architectural patterns is a noble cause that everyone can contribute to.

You can contribute by writing patterns and maybe even coming to a [Plop patterns
conference](http://hillside.net/patterns/). 

Basically when you see a software
development technique a few times, and see that it isn't yet documented - write
it up in Pattern format and give it a name!

A pattern is more than just a "tip"
or technique though - a pattern represents an abstract idea - that can be
implemented in various ways depending on your circumstances.

# The Patterns Movement

The Patterns Movement is spearheaded by <a href="https://www.hillside.net/plop/2020/">Hillside and the Plop conferences</a>, held each year.

There are a couple of things I would like to see happen in the patterns world.

- First, it would be nice if there was a single, authoritative repository of patterns. Yes an attempt has been made - a catalog book and and various websites - but nothing authoratative. I started a list of links [here](/index.php/blog/central_repository/ "Towards a central repository of Design Patterns").

- Secondly, it would be nice to have deep design pattern support in UML within all our favourite IDE's. For example Netbeans has it all - coding, form design, UML and design pattern support - albiet not as integrated as it could be and not as polished as it could be. **Update:** Unfortunately Netbeans seems to have dropped UML support in recent builds.

### Comments indicating Pattern usage
If IDE's are not your cup of tea, then how about this: source code should have comment markers indicating where the patterns are, so that a reverse engineering tool can visualise not only the UML but also where the patterns are.

My own UML tool PyNSource will have such a feature - est. June 2011 <i>(turns out this never happened :-)</i>.

### Executable UML
Further advancements are arguably executable UML and even the possibility of building software without code.
I muse a bit about this in my blog entry on [software visualisation](/index.php/blog/visualising_software/ "Visualising Software") and my paper on [design pattern tools](/index.php/design_patterns/pattern_automation/ "Design Pattern Automation"). 

### A repository of patterns

First, it would be nice if there was a single, authoritative repository of patterns. Yes an attempt has been made - a catalog book and and various websites - but nothing authoratative.  I'm starting a list of links [here](/index.php/blog/central_repository/ "Towards a central repository of Design Patterns").

Patterns at all levels need to be core **visual** building blocks of IDE's, or at the very least, extractable from source code into some visual UML tool - rather than being design ghosts that float around, implicit, in our source code.
