---
title: "Pynsource"
date: 2022-02-14
type: docs
draft: false
tags: ["UML", "Software Product", "Diagramming", "Python"]
---

Visit [pynsource.com.](http://www.pynsource.com)

Pynsource is a UML tool for Python a desktop App for Mac, Window and Linux.

![Pynsource hero](https://i.imgur.com/C8WrRDf.png "Pynsource Hero")

*Pynsource imports Python code and features zoom, Ascii and PlantUML views and Auto Layout*

Community Edition is free, fully functional and open source - check out the [Pynsource GitHub repository](https://github.com/abulka/pynsource). 

Buy the [Pro Edition](http://www.pynsource.com/pricing.html) for $20 to unlock the zoom feature and other pro features.

Visit the [Pynsource Home Page](http://www.pynsource.com)

## Built on wxdiagram

Pynsource's diagram canvas is powered by [wxdiagram]({{< ref "/projects/libraries/wxdiagram" >}}), a standalone MIT-licensed shape-and-connector canvas for wxPython. It began life as Pynsource's internal `ogl2` canvas — a fork of `wx.lib.ogl` created to fix drag rendering on modern macOS — before being extracted, renamed and published to PyPI in November 2026.

Pynsource is wxdiagram's main downstream consumer, and continues to drive its API and shake out its interaction bugs. The layout and overlap-removal algorithms Pynsource uses are described in [Developing a Layout Algorithm for UML diagrams]({{< ref "/blog/uml-layout" >}}).

Read the engineering story in [wxdiagram: a modern diagram canvas for wxPython]({{< ref "/blog/wxdiagram-canvas-for-wxpython" >}}) or the [wxdiagram documentation](https://abulka.github.io/wxdiagram/).
