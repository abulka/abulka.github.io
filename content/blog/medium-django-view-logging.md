---
title: "Django View logging is back-the-front"
date: 2019-09-04
draft: false
---

Have you ever looked through your Django log files and console messages, felt something was out of order and didn’t make sense, but couldn’t quite put your finger on it?

Here is an example of what I mean. Here is some view code:

```python
def diagramz_list(request, template_name="list.html"):
    log.info("diagramz_list has been called")
    ...
    return render(request, template_name, {"object_list": diagrams})
```

that gets routed via `url(r”^listz$”, views.diagramz_list, name=”listall”)`.

Let’s look at the log file and console messages that get generated when you do the usual python manage.py runserver and using the browser, visit endpoint /listz:

```
[2018–10–20 14:42:50] [INFO] diagramz_list has been called
[2018–10–20 14:42:51] [INFO] “GET /listz HTTP/1.1” 200 119585
```

Can you see the problem?

Right — the hit on the endpoint /listz gets logged *after* the output of the logging statement which says “diagramz_list has been called”.
That’s counterintuitive for me when I do logfile analysis.

> IMO — the Django endpoint call should be logged immediately.


See full article on Medium [here](https://medium.com/@abulka/django-view-logging-is-back-the-front-7f9701d501de).

