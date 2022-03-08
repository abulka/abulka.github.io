---
title: "Literate Code Mapping"
date: 2020-11-23T12:43:14+11:00
type: docs
draft: false
---

*Diagramming Methodology Specification*

Literate Code Maps are diagrams which help programmers understand the structure and behaviour of source code. 

## Example

![code map example 01](https://raw.githubusercontent.com/abulka/lcodemaps/master/images/example-01.svg?sanitize=true)

Code Map diagrams differ from UML diagrams in that they 
focus on real source code fragments and lots of 
rich-text formatted story-telling narrative. 
They combine class and sequence diagrams into the same
diagram, offering step by step numbering to follow the behaviour of a use case story. 

## The 5 laws of literate code mapping

1. Boxes represent any scope or namespace - be creative
1. Show structure and behaviour in the same diagram
1. Code compartments in boxes contain code fragments and richly formatted narrative
1. Lines representing function calls between boxes are numbered to tell a story
1. Cross reference numbers can appear anywhere to associate ideas

Think of literate code maps like UML class diagrams where the classes are now boxes which can represent more things, and lines represent function calls as well as structure.  Boxes contain one or more extra compartments containing real code fragments and rich narrative.

See full website dedicated to Literate Code Mapping [here](https://abulka.github.io/lcodemaps/).
