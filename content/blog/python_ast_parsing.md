---
title: "Python AST Parsing"
date: 2018-06-01
draft: false
---

How I used the Python AST capabilities to build the [Python to Rpn converter](https://pyrpn.atug.com/).

## Python compilation pipeline

My program works at the AST stage of the compilation pipeline:  
  
![Image: hacking-python-asts-pycon-de-2017-suhas](/blog/images/python_ast_parsing_design_of_compiler.jpg)  

Specifically my approach has been to use Python's built in ability to parse itself into an AST [Abstract Syntax Tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree), then to traverse this tree using the visitor design pattern to generate the RPN.  

> The Python AST parser is built into Python and thus requires that you be running Python to use it.

## Example

For example, parsing the following Python code with `ast.parse`:

```python
import ast
import astunparse
print(astunparse.dump(ast.parse('x = 1 + 2')))
```

will generate the following AST data structure representing `x = 1 + 2`

```
Module(body=[Assign(
  targets=[Name(
    id='x',
    ctx=Store())],
  value=BinOp(
    left=Num(n=1),
    op=Add(),
    right=Num(n=2)))])
```

## Reception to the talk

The reception to the talk entitled "Leveraging the Python AST, Python’s hidden DOM" was good, but became fun and buoyant once the audience realised I had targeted an old HP calculator !

![old HP calculator](https://upload.wikimedia.org/wikipedia/commons/b/bb/Hp42s_face.jpeg)

with this fancy Python technology - especially when I pulled out my HP calculator collection for all to see and touch. 😄
  
\-Andy Bulka

## Resources

- [Python AST talk slides](https://docs.google.com/presentation/d/1_qNKLofUwPhs_LsF-AQM-0WstS2jeYrusU5El4RLfnc/edit?usp=sharing) of the talk I gave to a local Python User Group in Melbourne, Australia, about how I used the Python AST capabilities to build the Python to Rpn converter. 
- [Python to Rpn converter](https://pyrpn.atug.com/) which uses these AST conversion capabilities to convert Python code into HP calculator RPN code.