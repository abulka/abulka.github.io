---
title: "Libraries & Tools"
linkTitle: "Libraries & Tools"
type: docs
weight: 20
tags: ["Software Product", "Vscode", "Electron", "Flask", "SQL"]
---

## Snippet Creator

This extension helps to automate snippet creation. Select the code you want to create snippet from and use command `Create Snippet` from the command palette or your custom keybind.

[https://github.com/abulka/vscode-snippet-creator](https://github.com/abulka/vscode-snippet-creator)

## Snippets Explorer

Visual Studio Code extension which displays all available language snippets in a TreeView

[https://github.com/abulka/vscode-snippets-explorer](https://github.com/abulka/vscode-snippets-explorer/issues)

![demo](https://raw.githubusercontent.com/abulka/vscode-snippets-explorer/master/images/videos/demo1.gif)

## Electron-Flask App Generator

Yoeman project generator to create an Electron app running a Flask server inside itself. Deployable via PyInstaller and Electron Forge packager.

Create an Electron App project that auto-starts a Flask server the electron app can call for services. Deployable as a single App that users can double click on and run.

https://github.com/abulka/generator-electron-flask


         _-----_     ╭──────────────────────────╮
        |       |    │  Welcome to the amazing  │
        |--(o)--|    │ generator-electron-flask │
       `---------´   │        generator!        │
        ( _´U`_ )    ╰──────────────────────────╯
        /___A___\   /
         |  ~  |     
       __'.___.'__   
     ´   `  |° ´ Y ` 

    ? App Name myapp
    ? Description My Electron application description
    ? Author's Name Fred Smith
    ? Author's Email fred@example.com
    ? license: Apache 2.0
    ? Package keywords (comma to split) python, js, great-app
    ? Run flask on port number? 5000
    ? Initial flask url (e.g. /hello or /hello-vue) to display? / hello
    ? Choose from misc options (Press <space> to select, <a> to toggle all, <i> to invert selection)
    ❯◉ Electron logging
    ◯ Print current working directory on startup
    ◯ Print node and electron versions on starrtup
    ◉ Fully quit on Mac on exit (without needing CMD-Q)
    ◉ Open Electron/Chrome DevTools in final app

Example of generated app:

![app running](https://github.com/abulka/generator-electron-flask/raw/main/doco/electron-flask-demo1.gif)

## Dedent for Dart

Dedent - Remove any common leading whitespace from every line in text. Ported from Python.

https://pub.dev/packages/dedent

## Relationship Manager

 A lightweight Object Database (no SQL used) class for Python 3

https://pypi.org/project/relationship-manager/

## Image Presenter

An image presentation tool, where you can click and zoom into various parts of a single image.

![](/projects/libraries/images/image-presenter.png)

Relevant text notes associated with each sub-area would appear when zoomed in.  Arrow keys/buttons allow you to step through a narrated sequence of zooms, so that you get can be carefully guided through an art image, or diagram.

Two demo prototype versions, using different underlying technologies:
- https://atug.com/image_presenter/layerjs/
- https://atug.com/image_presenter/zoomooz/

Source code currently unreleased.


## Jupyter Notebook Tools

A way of implementing complex calculators incl. scrolling text area UI widgets within Jupyter & Colaboratory Notebooks. 

### Scrolling Textareas for Jupyter Notebooks

Scrolling Textareas in a Python Jupyter Notebook, allows building a kind of "Calculator Playground".

![](/projects/websites/images/jupyter-calc-pi.gif)

Various Jupyter Notebooks at https://bitbucket.org/abulka/jupyter_play/src/master/ (private)

Gist of the scrolling textarea technique: https://gist.github.com/abulka/3043e8a4d78d2e26f872542524a0aa3e (public)


### Google Colaboratory

A way of implementing UI scrolling regions within Google Colaboratory Notebooks. 
Google Colaboratory, or "Colab" for short, is a version of Jupyter Notebooks, and allows you to write and execute Python in your browser.

This [Colab project](https://colab.research.google.com/drive/1_R4DAqhVgfPc4113N5VxHVeUJ9oxDMKM#scrollTo=bz9ue7M7cRPq) is a simpler version of the scrolling text area idea above, and needs to be fleshed out a little more fully to match the native Jupyter notebook functionality above.

![jupyter-google-colab-1](/projects/websites/images/jupyter-google-colab-1.gif)
