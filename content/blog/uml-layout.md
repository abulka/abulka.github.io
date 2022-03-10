---
title: "UML Layout"
linkTitle: "UML Diagram Layout"
date: 2011-04-06
description: >
  Developing a Layout Algorithm for UML diagrams
tags: ["UML", "Diagramming"]
---

# Developing a Layout Algorithm for UML diagrams

## Intro

Presented to the [Melbourne Patterns Group](https://melbournepatterns.wordpress.com/), Wednesday 6th April 2011 6:30 PM


## The Problem: Untangling UML Diagrams

![png your image](/blog/images/uml-layout-the-problem.png)

## Terms

- Nodes – these are the shapes/rectangles
- Edges – these are the lines connecting the shapes

## Background

- My UML tool is written in Python
- Existing layout libraries for e.g. python PyGraphviz has no windows port so I wrote my own
- Layout is reasonably hard to implement – academic papers are very complex and deal in a lot of math
- DIRTY SECRET OF ACADEMIA - Most Layout algorithms only deal with ‘points’ and don’t take into account real width and height

Thus for any real world use 
(unless dealing with network and particle visualisation where each node is the same size/shape),
it seemed to me that one needs to run an *overlap removal algorithm* after the layout to remove shape overlaps.

Overlap removal algorithm needs to minimise shape movement in order to respect the layout results

## What I developed

- I used a ‘spring layout’ adapted from java and javascript
- I developed my own overlap removal algorithm
- Developed a GUI sandbox test app for development

## Overlap Removal - Before and After

{{% figure src="/blog/images/uml-layout-before.png#floatleft" caption="before" %}}
{{% figure src="/blog/images/uml-layout-after.png#floatright" caption="after applying layout" %}}

## Unit Testing

Extensive unit tests were created to keep on top of the layout algorithm results.  A word document containing annotated screenshots for each test helped me enormously.

{{% figure src="/blog/images/uml-layout-unit-testing.png" caption="an overlap removal use case which became a unit test" %}}

Layout / persistence format was created for creating layout scenarios

```python
{'type':'node', 'id':'D25', 'x':6, 'y':7, 'width':159, 'height':106}
{'type':'node', 'id':'D13', 'x':6, 'y':119, 'width':119, 'height':73}
{'type':'node', 'id':'m1', 'x':170, 'y':9, 'width':139, 'height':92}
```

### Unit Testing Brittleness Avoided

Loose tests using (e.g. I created a function called `ensureYorder()` etc) were created so that the tests were not too brittle.  Slight variations in position are ignored. 

View this unit test file at the Pynsource GitHub repository [tests/test_overlaps1.py](https://github.com/abulka/pynsource/blob/master/src/tests/test_overlaps1.py). Here is an example unit test:

```python
def _LoadScenario3(self):
    self.g.LoadGraphFromStrings(TEST_GRAPH3)

def test3_5InsertedVerticallyTwoPushedDown(self):
    self._LoadScenario3()

    # move m1 to the left
    node = self.g.FindNodeById("m1")
    node.left, node.top = (6, 4)

    d97 = self.g.FindNodeById("D97")
    oldD97pos = (d97.left, d97.top)

    # assert m1 has been inserted vertically - two pushed down
    were_all_overlaps_removed = self.overlap_remover.RemoveOverlaps()
    self.assertTrue(were_all_overlaps_removed)
    self.assertEqual(2, self.overlap_remover.GetStats()["total_overlaps_found"])

    self.assertTrue(self._ensureYorder("m1", "D25", "D13"))
    self.assertTrue(self._ensureXorder("m1", "D97", "D98"))
    self.assertTrue(self._ensureXorder("D25", "D97", "D98"))
    self.assertTrue(self._ensureXorder("D13", "D97", "D98"))
    self.assertEqual(oldD97pos, (d97.left, d97.top))  # ensure D97 hasn't been pushed
```

Running the tests:

{{% figure src="/blog/images/uml-layout-test-run.png" caption="An example test run" %}}

Having a huge bank of unit tests helped in refactoring, too.  Imagine testing all the necessary scenarios by hand!

The final Results were pretty good!

{{% figure src="/blog/images/uml-layout-final-result-good.png" caption="A UML diagram after overlap removal" %}}

## Design Patterns Used

### Memento

- Memento was used to remember graph layout positions and then compare mementos to see if anything had ‘changed’ and thus drop out of the Spring layout algorithm early
- Memento was used to save/restore layouts in my test GUI – assigned to keys 0..9

### Blackboard

Blackboard pattern used to run layout several times and figure out which was the best, cleanest result using multiple criteria.  Each run is a ‘snapshot’

```
Snapshot 1 [6] LL  0   NN pre rm overlaps  5   LN  0   scale 1.6   bounds 23  (500, 473) <---
Snapshot 2 [4] LL  0   NN pre rm overlaps  5   LN  1   scale 1.4   bounds 30  (570, 537)
Snapshot 3 [5] LL  0   NN pre rm overlaps  6   LN  2   scale 2.0   bounds 17  (444, 393)
Snapshot 4 [2] LL  0   NN pre rm overlaps  4   LN  2   scale 1.4   bounds 34  (648, 537)
Snapshot 5 [3] LL  0   NN pre rm overlaps  5   LN  4   scale 2.0   bounds 21  (427, 508)
Snapshot 6 [1] LL  0   NN pre rm overlaps 10   LN  5   scale 2.0   bounds 18  (485, 379)
```

Python goodness helped in this ‘AI’ smartness

```python
def sortfunc(d):
  # this does the thinking!
  return (d['LL'], d['LN'], d['bounds_area_simple'], -d['scale'], d['NN_pre_OR']) 
```

## Future

- “Line  over node” overlap was abandoned as it started to get really complex with a lot of trigonometry and perhaps this area needs a more academic approach
- Non straight lines and line routing is probably the better direction
- Adding an understanding of UML semantics is another direction to research, so that e.g. base classes are above derived classes etc.

## Overlap Removal Server

In 2020 I needed to expose the overlap removal code as an API for javascript to use.

Here is that small research sub-project https://github.com/abulka/pynsource/tree/master/Research/overlap_removal_server


## Resources

### Code and Links

- Overlap removal code is Python, open source
- Part of my python UML tool [PyNSource](https://www.pynsource.com): Reverse engineer python source code into UML - display UML as Ascii art or PlantUML diagrams in a proper diagramming visual workspace.

### Slides on Scribd

[UML Graph Layout - Andy Talk - March 2011](http://www.scribd.com/doc/55976194/UML-Graph-Layout-Andy-Talk-March-2011 "View UML Graph Layout - Andy Talk - March 2011 on Scribd")

### Slides as HTML

*   The problem of laying out UML
*   Spring Layout
*   Mapping layout to Real World
*   OGL
*   MVC
*   Overlap Removal
*   Unit tests and unit test diagrams
*   Memento Design Pattern
*   Blackboard Design Pattern & Injecting sorting function
*   Future..

<iframe src="/files/UML-Graph-Layout-Andy-Talk-March-2011.html" name="frame1" scrolling="yes" frameborder="yes" align="center" height = "842px" width = "800">
</iframe>

### Slides as Pdf download

[View as pdf](/index.php/download_file/429/109/)

---

## Images

### Sample Images

![png your image](/images/uml/content/blog/newcat/uml/test-uml.png)

![png your image](/images/uml/fred-uml.png)

![](/blog/images/uml-layout-before.png) 
![](/blog/images/uml-layout-after.png)

{{% figure src="/blog/images/uml-layout-before.png#floatleft" caption="before" %}}
{{% figure src="/blog/images/uml-layout-after.png#floatright" caption="after applying layout" %}}

