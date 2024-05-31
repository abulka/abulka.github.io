---
title: "Electron-Flask App Generator"
linkTitle: "Electron-Flask App Generator"
type: docs
weight: 20
tags: ["Software Product", "Yeoman Generator", "Python", "Electron", "Flask"]
---

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
