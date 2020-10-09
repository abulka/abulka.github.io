---
title: "Misc"
linkTitle: "Misc"
weight: 20
---


Apps and Websites released this year - 2019
===========================================

GitUML
------

UML visualisation for Git repositories _(website app)_.

Understand code quickly: Automatically generate UML class diagrams from source code residing in git repositories. Diagrams automatically update when you push code using git.

![point and click](https://www.gituml.com/static/home2/images_home/2017-10-19_09-43-34.bf679c329661.gif)

Visit [GitUML](http://www.gituml.com) now, create a free account and begin creating UML diagrams and documentation.

Pynsource
---------

UML tool for Python _(Desktop App for Mac, Window, Linux)_ - brand new version. 

Zoom in and out. PlantUML view. Auto Layout. Import Python 3 code.

[Version 1.71](http://www.pynsource.com) - new for 2019

![Pynsource hero](https://i.imgur.com/C8WrRDf.png "Pynsource Hero")

Visit the brand new dedicated website [pynsource.com.](http://www.pynsource.com)

Buy the [Pro Edition](http://www.pynsource.com/pricing.html) for $20 to unlock the zoom feature.  Community Edition is fully functional and open source - check out the [github repository](https://github.com/abulka/pynsource).  Donate to support this project _(donate link coming soon)_.

My Apps and Websites - 2018
===========================

Print42
-------

[Print42](http://www.print42.atug.com) is a log tailing GUI program which optionally echoes log lines to thermal printer tape. Its like a modern thermal printer version of a ticker tape for tailing log files. It features display font size options, search and filtering. You can also annotate the output with text fragments that you type in - or screenshots that you paste in. 

  
  
  
  
The video is 13 minutes long and covers the basic use cases, history of the project etc.  
  
As well as physically printing from Free42, the Print42 software can also be used to print HP Prime screenshots (from either the emulator or real HP Prime hardware via the HP connectivity kit).  
  
Outside the world of calculators, Print42 can be used to 'tail' log files (programmers take note) and to print graphic snippets from the web. Useful if you want to rapidly print information to stuff into your pocket or to study and annotate printouts of complex information, at your desk.  
  
If you are looking for a useful, fun new gadget, you might want to consider buying an Epson thermal printer and trying Print42. However you can also use Print42 with your regular desktop printer, for free.   
  
The website for downloads and further information is [www.print42.atug.com](http://www.print42.atug.com/)

Python to RPN
-------------

I am pleased to announce the Python to HP42S RPN converter website is online.  
[www.pyrpn.atug.com](http://www.pyrpn.atug.com)   
  
![[Image: python_rpn_ui_01.png?raw=1]](https://www.dropbox.com/s/nqfq01xaxvi4xnv/python_rpn_ui_01.png?raw=1)  
  
You write code in a high level structured language (which happens to be Python 3 syntax), hit a button and RPN is generated.   
  
![[Image: python_rpn_ui_02small.png?raw=1]](https://www.dropbox.com/s/3xcmxfxraxc6wej/python_rpn_ui_02small.png?raw=1)  
  
You then paste the RPN into Free42 or transfer it to your DM42 (by [creating a raw](https://www.swissmicros.com/dm42/decoder/)) - and it runs.

1.  Examples: [http://www.pyrpn.atug.com/examples](http://www.pyrpn.atug.com/examples)
2.  User Guide: [http://www.pyrpn.atug.com/help](http://www.pyrpn.atug.com/help)
3.  Canvas for 42S Simulator: [http://www.pyrpn.atug.com/canvas](http://www.pyrpn.atug.com/canvas)
4.  List of HP42S Commands Supported Reference: [http://www.pyrpn.atug.com/cmds](http://www.pyrpn.atug.com/cmds)

The converter supports core Python syntax (which is very powerful), but does not implement the built in Python libraries that you would get in desktop Python. You have to rely on the ability to call HP42S commands from Python to do your work - which of course you can do. Specifically, it has the following capabilities:

1.  Variables
2.  Functions, Multiple functions, nested functions
3.  Parameter passing, receiving return values, multiple return values
4.  if elif else
5.  Comparison operators == != > < >= <=
6.  Booleans True, False and operators not or and
7.  for loops, range(), for..in iteration through lists and dictionary keys
8.  while loops, while...else
9.  continue and break operations in for loops and while loops
10.  Lists and Dictionaries (basic operations only).
11.  Matrices, Pythonic matrix element access syntax \[row,col\]
12.  NumPy compatible slicing syntax for sub-matrices
13.  Complex numbers using either 42S or Python native syntax
14.  Expressions involving nested brackets
15.  assert
16.  Testing and clearing of flags
17.  Access most HP42S commands as function calls e.g. FIX(2)
18.  Some enhanced functions to make life easier e.g. varmenu() automates and simplifies the generation of MVAR based code.

My Other Apps and Consulting Services
=====================================

If you would like me to run a design patterns course or consult on your next software design, please check out my [product](/index.php/products/ "Products") page.  There is also an open source [Python UML tool](http://www.pynsource.com "Pynsource - UML tool for Python") you might be interested in, plus references to products I have developed over the years esp. the worldclass argumentation visualisation software Rationale and bCisive.

My Medium Articles - 2018 - 2020
================================

I've been publishing a lot on Medium recently. Why? Because the articles seems to get more widely read, and the Medium editor is so simple and produces beautifully formatted articles.

[Building a deployable Python-Electron App](https://medium.com/@abulka/electron-python-4e8c807bfa5e)

Building a normal, deployable application for Mac or Windows, using Python 3 is hard. There is nothing like Visual Studio or Delphi (remember that?) for Python where you can drag and drop to design a GUI, press a button and get an .exe or .app to give people. Sad. The closest you can get is to follow a long recipe of steps - which I outline here.

[Async/await for wxPython](https://medium.com/@abulka/async-await-for-wxpython-c78c667e0872)

Python 3 GUI apps with asynchronous functionality

[Getting Python and wxPython apps into the Ubuntu app store](https://medium.com/@abulka/getting-python-and-wxpython-apps-into-the-ubuntu-app-store-ccca7ae537a3)

Have you ever dreamt of getting your own apps in the Ubuntu app store? Here’s how.

[Django View logging is back-the-front](https://medium.com/@abulka/django-view-logging-is-back-the-front-7f9701d501de)

How the order of view request log messages in Django apps might be confusing, and how to fix it.

[TodoMVC implemented using traditional OO, Controllers and Events.](https://medium.com/@abulka/todomvc-implemented-using-traditional-oo-controllers-and-events-5e4c09f80cd4)

TodoMVC implemented in a classic Object Oriented way - which includes running code you can run in your browser.

[TodoMVC implemented using a game architecture — ECS.](https://medium.com/@abulka/todomvc-implemented-using-a-game-architecture-ecs-88bb86ea5e98)

Building traditional GUIs with the Entity Component System

_Coming soon_

[Literate Code Maps](https://github.com/abulka/lcodemaps)

Coming soon: A Medium article - for now this is a GitHub page. I've invented a diagramming methodology called Literate Code Maps which improve upon some aspects of UML - actually they are quite different and arguably more useful than UML for understanding complex source code projects. I've been using this notation for many years, and it might help you in your projects.

GitHub Projects
===============

A pair of extensions for Visual Studio Code
===========================================

Snippets Explorer
-----------------

Visual Studio Code extension which displays all available language snippets in a TreeView

[https://github.com/abulka/vscode-snippets-explorer](https://github.com/abulka/vscode-snippets-explorer/issues)

![demo](https://raw.githubusercontent.com/abulka/vscode-snippets-explorer/master/images/videos/demo1.gif)

Snippet Creator
---------------

This extension helps to automate snippet creation. Select the code you want to create snippet from and use command `Create Snippet` from the command palette or your custom keybind.

[https://github.com/abulka/vscode-snippet-creator](https://github.com/abulka/vscode-snippet-creator)

Brew Moments
------------

I've recently learned mobile app development using Flutter.  Here is my first app.

[https://abulka.github.io/brew-moments/](https://abulka.github.io/brew-moments/)

[![visit google playstore page](/files/cache/43f1dcf5a9ca2ae45b81aecb82779474_f432.png)](https://play.google.com/store/apps/details?id=com.wware.brew_moments)

# Sidebar

### My Developer Story

This stackoverflow timeline is like a resume - except its more fun and useful to look at.

*   [Story view](https://stackoverflow.com/story/andybulka)
*   [Traditional view](https://stackoverflow.com/cv/andybulka) 

### Building a deployable Python-Electron App

Here is my [latest article](http://bit.ly/python-electron-print42 ), published on Medium, about how to use Electron as a GUI front end to Python 3. It gets over 1,000 reads a week for some reason, more than any of my other articles.

### TodoMVC implementation articles

Here are my two recent articles implementing the classic Javascript TodoMVC app in various ways. These two articles shows you how to design apps. Its an alternative to using a modern javascript framework like Vue, Angular or React.

*   [Classic](https://medium.com/@abulka/todomvc-implemented-using-traditional-oo-controllers-and-events-5e4c09f80cd4) - OO, Controllers and Events
*   [ECS](https://medium.com/@abulka/todomvc-implemented-using-a-game-architecture-ecs-88bb86ea5e98) - using a game architecture
    
## xx

this is a test

### Pynsource

UML tool for Python source code - visit [www.pynsource.com](https://pynsource.com)

Version 1.76 - released Apr 22, 2020

\- **Zoom**, zoom to fit

\- Python 3 compatibility

\- New accurate **AST based** python parser

**\- Layout algorithm**

\- **Ascii UML** view built into the GUI, including an innovative Ascii UML layout

\- **PlantUML** view for beautiful renderings of UML

\- **Colour** sibling nodes

\- Open Source

### Print42

[Print42](http://www.print42.atug.com) is a log tailing GUI program which optionally echoes log lines to thermal printer tape. Its like a modern thermal printer version of a ticker tape for tailing log files. It features display font size options, search and filtering. You can also annotate the output with text fragments that you type in - or screenshots that you paste in.

### Python to RPN converter

Check out [Python to RPN](http://www.pyrpn.atug.com) if you have an old vintage HP Calculator that you want to program in Python!  Impossible?  See also my blog post [How I used the Python AST capabilities to build a Python to Rpn converter](http://www.andypatterns.com/index.php/blog/ast-parsing-python-generate-hp-calculator-rpn/ "AST Parsing with Python to generate HP Calculator RPN").

### ****HexMVC -** Design Pattern**

**HexMVC** - A new, lightweight, architectural pattern for building applications based on the Hexagonal layered architecture pattern + MVC – presented by Andy Bulka.  To be published 2019.

Design Patterns Training
------------------------

Elevate the **effectiveness of your entire programming team** - Andy can deliver his existing or a customised Design Patterns Course to your entire programming team - at your company's premises.  Check out the [details](/index.php/products/design_patterns_courses/ "Design Patterns Courses").

---

# Summary

after this point there will be a summary list of pages within the Projects
