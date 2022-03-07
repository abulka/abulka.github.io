---
title: "MGM Pattern"
linkTitle: "MGM Pattern"
date: 2019-01-04
toc_hide: true
type: projects
description: >
  Model-Gui-Mediator Pattern - the original version of [MVCA Architectural Pattern](/patterns/mvca-pattern)
  The MGM pattern is a variation of MVC (model view controller) or MVP (Model View Presenter) but takes into account the use of modern off the shelf GUI controls.
---

![](http://www.andypatterns.com/files/33971232953329bg-pods1.jpg)

## Introduction

This article is twenty years old - its ideas are now simplified and clarified at [MVCA pattern]({{< ref "/patterns/mvca-pattern.md" >}})

A [live demo](https://abulka.github.io/todomvc-oo/) running in a browser.

Tip for understanding this article:
This is arguably the traditional MVC pattern with terminology tweaked and clarified, and updated for 'modern' times where Views are no longer manually drawn but are instead off the shelf GUI widgets or DOM elements.

- Mediator == Controller
- GUI == View

## The Pattern

<iframe src="/files/andybulkamodelguimediatorpattern.html" name="frame1" scrolling="yes" frameborder="yes" align="center" height = "842px" width = "800">
</iframe>

Download as [pdf](/files/pdfs/AndyBulkaModelGuiMediatorPattern.pdf).


## Comments

Comments now disabled due to spam.

### Posted on Jan 18th, 2009

Hi Andy,  
  
I've read your article about the MGM Patterns, it's a great pattern.  
However, I have a question, could you please show me.  
  
Let say I have a Textbox (GUI), a business object with only 1 property Text,  
a mediator-view as your pattern defined.  
  
When changing Business.Text, this procedure is called:  

```
procedure setText(Value: String);  
begin  
  FText := Value;  
  NotifyChanges; // \*\*\* notify mediator to change Editbox content  
end;  
```

therefore, mediator is notified:  

```  
procedure BusinessChanged;  
begin  
  FGUI.Text := FBusiness.Text; // this makes Editbox OnChange fires  
end;  
```

OnChange event of Editbox:  

```  
procedure Edit1Change();  
begin  
Mediator := FindMediator(Self)  
Mediator.Business.Text := TEdit(Self).Text;  
{ \*\*\* This line would call Business.setText and make an infinity loop }  
end;  
```

The only method I've thought of is let the Mediator modify FText field of  
Business object. But in this way, Busniess and Mediator have to be in a same  
unit. Is there another way to solve this problem?  
  
Thanks for your sharing!  
Karr. C.

### Posted by Andy on Jan 18th, 2009

Thanks for your interest in the MGM pattern. Your assumption in the above code is that the Editbox OnChange fires when you programatically set the FGUI.Text, which would cause the event sequence  
  
```  
gui changes -> mgm notified -> changes model ->  
model notifies mgm -> mgm modifies gui -> gui changes  
```

and so on, infinitely!! See your lines marked \*\*\* highlighted lines above.  
  
However the Editbox OnChange fires only seems to fire when the text is altered by the user in the gui. It does not fire when the edit1.text is changed programatically. So there is no loop.  
  
I tried it in Delphi 6. Here is a sample delphi app that proves it.  
http://www.atug.com/downloads/mgmquickproof01.zip  
It has a cheaper form of mgm which I just whipped up, in order to demonstrate the point.  
  
P.S. If the event HAD fired, you could  
  
1. temporarily disable the event by rewiring the event handler to Nil before writing to it programatically, then restoring the event handler again (yuk, but possible. You often have to do this when using mgm with treeviews.)  
  
2. provide a way of setting the model data which does not trigger a notification. Make the private data public. Again, yuk.  
  
... anyway thankfully you don't need to do either of these things since Editbox OnChange does not fire when the edit1.text is changed programatically  
  
Hope this helps.  
\-Andy Bulka

### Posted by Anon on Jan 21st, 2009

Here is a [nice article](http://www.c-sharpcorner.com/UploadFile/shivprasadk/1246712242008074334AM/12467.aspx) on MVP pattern and the differences to MVC.

## Resources

[Old link](http://www.andypatterns.com/index.php?cID=46) on andypatterns.com 
