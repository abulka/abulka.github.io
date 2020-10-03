
---
title: "Relationship Manager - Design Pattern"
linkTitle: "Relationship Manager"
date: 2019-01-04
description: >
  A central mediating class which records all the one-to-one, one-to-many and many-to-many relationships between a group of selected classes.
---

## Introduction 1233

Andy's Published Design Patterns
These four papers are substantial works which have been presented at KoalaPlop (Asian Pacific Conference on Pattern Languages of Programs) in both 2000 and 2001.  My shepherds (paper peer reviewers) were:

- Jim Coplien (MGM pattern)
- Ali Arsanjani (TI pattern)
- James Noble (RM pattern).  

These final versions also incorporate comments and reviews from the attendees of KoalaPlop 2000 and 2001.

## Abstract

A central mediating class which records all the one-to-one, one-to-many and many-to-many relationships between a group of selected classes. Classes that use a Relationship Manager to implement their relationship properties and methods have a consistent metaphor and trivial implementation code (one line calls). In contrast - traditional "pointer" and "arraylist" techniques of implementing relationships are fully flexible but often require a reasonable amount of non-trivial code which can be tricky to get working correctly and are almost always a pain to maintain due to the detailed coding and coupling between classes involved.


## Intro2

Presented at ....

