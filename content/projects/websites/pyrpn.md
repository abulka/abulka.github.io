---
title: "Python to RPN"
date: 2022-02-14
type: docs
draft: false
tags: ["Code Translation", "Software Product", "Calculators", "Python"]
---

A Python to HP42S RPN converter website [www.pyrpn.atug.com](http://www.pyrpn.atug.com)   
Allows you to program your old vintage HP Calculator in Python!

![[Image: python_rpn_ui_01.png?raw=1]](https://www.dropbox.com/s/nqfq01xaxvi4xnv/python_rpn_ui_01.png?raw=1)  
  
> See also my blog post [How I used the Python AST capabilities to build a Python to Rpn converter](http://www.andypatterns.com/index.php/blog/ast-parsing-python-generate-hp-calculator-rpn/ "AST Parsing with Python to generate HP Calculator RPN").

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
