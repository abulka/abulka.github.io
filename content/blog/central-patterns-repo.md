---
title: "Central Patterns Repository"
date: 2009-02-12
draft: false
---

Towards a central repository of Design Patterns

An authoritative central repository of Design Patterns does not exist.  There is a book called [The Pattern Almanac 2000](http://www.amazon.com/Pattern-Almanac-2000-Linda-Rising/dp/0201615673/ref=sr_1_4?ie=UTF8&s=books&qid=1236691007&sr=8-4) by Linda Rising however this is no more than an index of patterns - nothing of substance except a one line descrtipion.  And furthermore, it leaves out hundreds if not thousands of patterns - scattered across books, websites and people's code. 

> 2020 Update: Central repositories on the internet are now commonplace. For IDE plugins, programming language library packages (`npm` for Javascript, `pypi` for Python etc.), apps, software components for linux etc. Its more difficult to create such systems for design patterns because patterns are more nebulous - requiring textual descriptions rather concrete code. As such the best source of patterns is [Awesome Design Patterns](https://github.com/DovAmir/awesome-design-patterns) which links to all sorts of other web pages and resources incl. lists of patterns used in particular domains e.g. [es6 design patterns](https://github.com/ziyasal/design-patterns-and-idioms-in-es6), language specific patterns, [cloud architecture patterns](https://github.com/DovAmir/awesome-design-patterns#cloud-architecture), [Big Data patterns](https://github.com/DovAmir/awesome-design-patterns#big-data) etc.

## Prerequisites for a repository

Any new effort needs to have broad support and a way of contributing without having to go through vetting.  This way people can contribute their own patterns and the project can utilise the community.  Better to have too many patterns than not enough.  Perhaps a "moderated" category could be added for higher quality entries.

*   A specific "template" for inserting patterns would be a must.
*   A UML diagram (png) - also a must.
*   Code sample (any language / psuedo code) - highly desirable.  
*   You could have a page of thumbnails of uml diagrams - very enticing way to browse the repository.
*   Drop down tags for type of pattern - architectural, design, coding idiom.
*   Tags for related patterns - not sure how the references would work, perhaps like a wiki, so each pattern should have a unique id (no spaces).  e.g. Observer or MVC or NullObject etc.

## On the copyrighted design pattern material in books

Getting all the patterns from published design patterns books would be a boon - even if we could at least get the basic UML and idea of each pattern - and leave the copyrighted content alone.  Existing patterns books are a huge source of material if we could mine them.  It could perhaps be pitched to authors as a way of stimulating book sales since people who want to learn more could buy the book via the usual link to Amazon etc.

## Other ideas

It might be good to see the existing class libraries of the programming languages (e.g. Java, .NET, Python, Delphi and PHP) mined for patterns - and there is a real opportunity there to form pattern languages of how these patterns fit together within the one language platform. 

The repository should include architectural patterns, design patterns and language and coding patterns (sometimes known as idioms) - forming a wonderful continuum of detail.  Of course the essential ideas in the deep implementation detail would probably be found at the high level and vice vera, such is the nature of reality. :-)

## Links

In the absence of a central repository, here are some links to lists of design patterns and books.

- [Awesome Design Patterns](https://github.com/DovAmir/awesome-design-patterns)

- [Amazon.com: The _Pattern_ Almanac 2000: Linda _Rising_: Books](http://www.amazon.com/Pattern-Almanac-2000-Linda-Rising/dp/0201615673)

- [A list](https://web.archive.org/web/20080516215348/http://www.vico.org/pages/PatronsDisseny.html) of GOF patterns including part-whole and view-handler

- [A Theoretically-based Process for Organizing Design Pattern](http://www.google.com.au/url?sa=t&source=web&ct=res&cd=2&url=http%3A%2F%2Fhillside.net%2Fplop%2F2005%2Fproceedings%2FPLoP2005_shasso0_3.pdf&ei=ftOLSfeRGonOsAPhz8H-CA&usg=AFQjCNHHTPiWHzhVz-2nolHMEYMz_JnnWA&sig2=bzx7wyq2Mj--05ehoO61ow)s

- [Hillside.net - Online _Pattern Catalog_](https://web.archive.org/web/20070510145935/http://hillside.net/patterns/onlinepatterncatalog.htm)

- There was a new project starting up in 2009 -  not sure what came of it. Perhaps more information can be found by contacting [Paris Avgeriou and Uwe Van Heesch](https://scholar.google.com.au/scholar?q=Paris+Avgeriou+and+Uwe+Van+Heesch&hl=en&as_sdt=0&as_vis=1&oi=scholart)
