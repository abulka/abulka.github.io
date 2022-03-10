---
title: "Async/await for wxPython"
date: 2019-03-02
draft: false
tags: ["Async", "GUI", "Controllers", "Python", "wxPython"]
---

How to build Python 3 GUI apps with asynchronous functionality.

Python 3’s support of async/await is the new hotness, allowing cooperative computation with reduced complexity and without needing threads — as long as you use async compatible libraries like aiohttp etc. You can’t use the famous requests library because it is not async aware and will block, but not to worry, those other libraries have you covered.

See full article on Medium [here](https://medium.com/@abulka/async-await-for-wxpython-c78c667e0872).
