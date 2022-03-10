---
title: "Refactoring to PureMVC"
date: 2009-04-01
draft: false
tags: ["Design Patterns", "GUI", "MVC", "Controllers", "Python", "wxPython", "Observer", "Refactoring"]
---

Let's look at how to refactor an existing architecture to the PureMVC architecture. Your application requires that you display 'model' data in some sort of UI 'view'.

![](/blog/images/puremvc20921233037638bgDSC9636.jpg)

## Introduction

### MVC Architectural Pattern

I have long been fascinated by the MVC (Model View Controller) architectural pattern, first conceived in the 1960's. What it promises, to those who can fathom its mysteries, is an orderly way of organising your application architecture. You define a de-coupled domain/business model that is oblivious to any GUI that might be displaying it. A mediating controller class usually looks after the dirty details of moving data between the model and GUI. You can even have multiple GUI representations of your single model e.g. a pie chart view and a bar chart view simultaneously displaying the same information out of the model.

There are many variants of MVC, and people use different terminology to mean the same thing, and conversely people use the same terminology to mean different things e.g. the view could be the GUI or it could be the mediating class looking after the GUI, which means it could actually end up meaning the controller...

### Model Gui Mediator

Some History.

I once wrote up a pattern called 
[MGM (Model Gui Mediator)]({{< ref "/patterns/mvca-pattern" >}}) 
which describes a version of MVC that I thought made sense in today's modern programming age. Today, GUI views were usually comprised of sophisticated controls/widgets rather than laboriously handcrafted graphic code that needed custom controller code to handle the intricate details of interacting with the view/GUI. Most of that low level controller interaction is now built in to the off the shelf widgets/controls.

The controller is now just a mediator between model and view – hence the “M” in MGM (Model-Gui-Mediator). You might prefer to think of the mediator as the controller, so the pattern could well have been called MGC (Model-Gui-Controller). Many modern variants of MVC e.g. MVP (Model View Presenter) and PAC (Presentation Abstraction Controller) and others probably fit into the basic idea of MGM.

![](/blog/images/puremvcfussMGM.png)

The behaviour of the MGM architecture is as follows:

![](/blog/images/puremvcfussMGM_UMLsequence.png)

_MGM pattern sequence diagram.  
M=Model (Data class) G=Gui (Form with an edit control on it) M=Mediator (Controller class)_

What we have illustrated above are two use cases:

*   In the first the user types some text into an edit field on a form, which causes the model to change – the model broadcasts the change and the GUI is updated (watch out for infinite loops here of course, which can be avoided by the gui update not triggering another change event).
    
*   The second use case is the model changing for some reason (e.g. being loaded from a file or some other part of the system altering the data) and the model broadcasting the change – again the Controller is observing and intercepts the broadcast and updates the GUI.
    

What is interesting about MGM is that it shows how simple the MVC pattern really can be, when understood in terms of today's modern GUI components. It also serves as a way of contrasting what PureMVC is offering. Read on.

### PureMVC

Along comes PureMVC.

I've since (2008-2009) become quite interested in the [PureMVC](http://www.puremvc.org) framework because it adds a few things that were missing from MGM.

![](/blog/images/puremvcfussCONCEPT1.png)

_PureMVC Conceptual Architecture_

Firstly PureMVC explicitly adds command classes – rather than just burying behaviour in controllers/mediators, we have an official way of organising behaviour. Sure, in MVC and MGM, any controller is free to delegate and invoke command classes to perform behaviour in a more organised way - but in PureMVC the details of this are a little more spelled out.

Secondly PureMVC adds service location, so that you end up with a nice de-coupled design – events are raised and anyone can register interest in an event/message. Thus the whole architecture becomes a lot more pluggable, flexible and neat.

Thirdly I believe PureMVC addresses scalability – for example it tells you exactly how to add multiple mediators to the system. Multiple commands and data proxies are also supported. You simply register all these classes and specify what noification messages are of interest to each of them.

## Rules of PureMVC

The model notifies, but doesn't listen and ultimately knows nothing about anything else in the system. Mediators notify and listen to messages. Commands are invoked (cmd.execute()) automatically by certain messages and they send out messages if they want to.

The facade is the communication hub.

Mediators look after gui elements, and this forms the view. Commands forms the controller. Proxies wrap model elements and this forms the model.  _Note that in the above diagram, there is a one to many relationship between the View and the Mediators, and between the Controller and the Commands, and between the Model and the Proxies._

## Refactoring to PureMVC

To show you just how useful and simple incorporating PureMVC can be, I have designed a step by step tutorial on how you introduce a PureMVC command driven, message notification driven architecture to your existing wxpython application.

We will start with a simple application that doesn't even have a model. We will first add a mediator, then a command class and then a proper model.

The application is a simple form which displays a textfield. When you hit ENTER, it converts anything you type into uppercase and displays it in the textfield. There is no “model” and no PureMVC architecture.

![](/blog/images/puremvcfuss_pythonGui.gif)

_Three screenshots of our simple wxPython application.  
We will use this as our starting point and refactor to PureMVC._

### 1. Starting Point

Here is the code for our simple wxpython application illustrated above. It has no proper model and does not use PureMVC. This is our starting point.

![](/blog/images/puremvcfussUMLstep0gui.png)

_Starting point – a simple wxpython app - a single form with a textfield control._

```python  
import wx

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)

class AppFrame(wx.Frame):
    myForm = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="Refactoring to PureMVC",size=(200,100))
        self.myForm = MyForm(self)

        self.myForm.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.myForm.inputFieldTxt)

    def onSubmit(self, evt):
        mydata = self.myForm.inputFieldTxt.GetValue()
        print "got", mydata
        self.myForm.inputFieldTxt.SetValue(mydata.upper())


class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
```

* * *

### 2. Add a mediator

Import PureMVC and add a mediator.

Let's add a mediator and create a PureMVC “view”. Mediators in PureMVC are classes which look after a gui – e.g. a wxpython form. Mediators can be built that look after larger or smaller chunks of your gui – depending on your situation. In our case we will build a mediator to look after the one form and its single textfield.

![](/blog/images/puremvcfussUMLstep2.png)

_Step 2 – the Mediator now intercepts the ENTER key event  
and performs the uppercasing behaviour in its onSubmit() handler._

**Steps**:

1.  Add the puremvc import statements
    
2.  Add a Mediator class
    
3.  Move the binding and onSubmit method out of the AppFrame and into the Mediator class
    
4.  Have the AppFrame create a PureMVC facade and register a mediator instance with the facade
    

```python
import wx

import puremvc.interfaces #ADD
import puremvc.patterns.mediator #ADD

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)

class MyFormMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator): # ADD THIS CLASS
    NAME = 'MyFormMediator'

    def __init__(self, viewComponent):
        super(MyFormMediator, self).__init__(MyFormMediator.NAME, viewComponent)

        self.viewComponent.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.viewComponent.inputFieldTxt)

    def listNotificationInterests(self):
        return []

    def handleNotification(self, notification):
        pass

    def onSubmit(self, evt):
        mydata = self.viewComponent.inputFieldTxt.GetValue()
        print "got (mediator)", mydata
        self.viewComponent.inputFieldTxt.SetValue(mydata.upper())

class AppFrame(wx.Frame):
    myForm = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="Refactoring to PureMVC",size=(200,100))
        self.myForm = MyForm(self)

        self.mvcfacade = puremvc.patterns.facade.Facade.getInstance()  #ADD
        self.mvcfacade.registerMediator(MyFormMediator(self.myForm ))  #ADD
        # self.myForm.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.myForm.inputFieldTxt) #DELETE

    # def onSubmit(self, evt):  #DELETE THIS METHOD
    #     mydata = self.myForm.inputFieldTxt.GetValue()
    #     print "got", mydata
    #     self.myForm.inputFieldTxt.SetValue(mydata.upper())

class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
```

So now, instead of our AppFrame class binding to the `ENTER` key event and handling it via an `onSubmit` method, the mediator now does this – binding to the `ENTER` event in the constructor of the mediator.

All the `AppFrame` does now is create a PureMVC facade and register a mediator instance with the facade. Notice that we pass the GUI object, in this case the form, to the mediator as a parameter to the mediator's constructor – the GUI object is referred to by the mediator as the viewComponent.

The application now behaves exactly as before, except we now get the following diagnostic message:

![](/blog/images/puremvcfuss_step2mediator.png)

which proves the mediator is active. Of course this step doesn't really buy us any functionality yet, but at least we are on the road...

* * *

### 3. Command class

Move the business logic into a Command class.

Let's now move the behaviour (changing text to uppercase) out of the mediator and into a proper command class. This makes the mediator dumber – which is good, as all we want the mediator to do is look after the GUI, not house application logic.

![](/blog/images/puremvcfussUMLstep3cmd.png)

_Step 3 – the uppercasing behaviour is moved to the command class._

**Steps:**

1.  Import the puremvc command import
    
2.  Create a command class **DataSubmittedCommand** and implement execute
    
3.  Move the logic for updating the GUI display with uppercase text - out of the mediator and into the command object's execute method. The mediator now simply raises a `DATA_SUBMITTED` notification
    
4.  Define our own facade class called **AppFacade**and
    
    1.  Define the `DATA_SUBMITTED` message
        
    2.  Override `getInstance()` to implement the singleton design pattern ( just return a new `AppFacade`)
        
    3.  Override `initializeController()` registering the `DataSubmittedCommand` class, associating it with the `DATA_SUBMITTED` message. In other words, whenever the `DATA_SUBMITTED` message is raised, DataSubmittedCommand.`execute()` is called.
        
5.  Use our new concrete Facade rather than the default Facade in the `AppFrame` class startup code.
    
```python
import wx

import puremvc.interfaces
import puremvc.patterns.mediator
import puremvc.patterns.command #ADD

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)

class MyFormMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
    NAME = 'MyFormMediator'

    def __init__(self, viewComponent):
        super(MyFormMediator, self).__init__(MyFormMediator.NAME, viewComponent)

        self.viewComponent.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.viewComponent.inputFieldTxt)

    def listNotificationInterests(self):
        return []

    def handleNotification(self, notification):
        pass

    def onSubmit(self, evt):
        mydata = self.viewComponent.inputFieldTxt.GetValue()
        print"got (mediator)", mydata
        # self.viewComponent.inputFieldTxt.SetValue(mydata.upper()) # DELETE THIS LINE
        self.sendNotification(AppFacade.DATA_SUBMITTED, mydata, self.viewComponent)  #ADD THIS LINE

class DataSubmittedCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand): #ADD CLASS
    def execute(self, notification):
        print "execute (command)", notification.getBody()
        mydata = notification.getBody()
        viewComponent = notification.getType()
        viewComponent.inputFieldTxt.SetValue(mydata.upper())

class AppFacade(puremvc.patterns.facade.Facade): #ADD CLASS
    DATA_SUBMITTED = "DATA_SUBMITTED"

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeController(self):
        super(AppFacade, self).initializeController()
        super(AppFacade, self).registerCommand(AppFacade.DATA_SUBMITTED, DataSubmittedCommand)

class AppFrame(wx.Frame):
    myForm = None
    mvcfacade = None  #ADD

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="Refactoring to PureMVC",size=(200,100))
        self.myForm = MyForm(self)

        # self.mvcfacade = puremvc.patterns.facade.Facade.getInstance() # DELETE THIS LINE
        self.mvcfacade = AppFacade.getInstance()  #ADD THIS LINE
        self.mvcfacade.registerMediator(MyFormMediator(self.myForm))

class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
```

Notice that we had to create our own concrete Facade class instead of merely creating an instance of the default Facade class that PureMVC provides. This is because we now want to start defining our own messages (e.g. `DATA_SUBMITTED`).

Also notice (and this is the crux of this refactoring step) that the mediator no longer performs the business logic of converting the text to uppercase. Now instead it simply raises a notification `DATA_SUBMITTED` which the command class then picks up and acts upon.

Again, as with any good refactoring step, the behaviour of the application is exactly the same as before except for our diagnostic message which now emits:

![](/blog/images/puremvcfuss_step3command.png)

* * *

### 4. GUI access logic

Move the ability to access the GUI out of the Command class.

**Hey - isn't the command class doing too much now?** Notice, in the previous refactoring step, that the command class is not only converting the text to upercase (our simple business logic), but is also getting a bit too big for its boots – it is also stuffing the result back into the gui itself – altogether bypassing the meditor. We are actually encouraging this because we pass both the gui textfield data and a reference to the textfield as part of the notification message. This gives the command class direct access to the gui. The command class should really simply raise a notification and let the mediator do what it was designed to do, and stuff the uppercase text into the appropriate part of the GUI. Let's now do this.

Let's now have the command raise a notification message after it has done its work, and let the _mediator_ look after putting the result back into the gui.

**Steps:**

1.  Create a new message type `DATA_CHANGED` in the facade - don't register it against a command since it is simply a message that will be listened for by the existing meditor. In PureMVC, message notifications can be associated with the triggering of commands or simply be listened for by mediators.
    
2.  Add the message `DATA_CHANGED` to the list of messages the mediator is interested in viz.  
    ```python
    def listNotificationInterests(self):
        return [ AppFacade.DATA_CHANGED ]
    ```
    
3.  Inside the mediator's handleNotification method, check for the message matching `DATA_CHANGED` and move the logic that updates the gui in here.
    
4.  We stop passing the meditor's view component as part of the message to the command – the command class doesn't need that reference to the gui anymore.
    

Ironically the code that updates the GUI started in wxapp, then moved to the meditor, then into the command class, then end up now back in the meditor again! What sort of refactoring is this!?  
  
Well the point is that we have separated two aspects of that code - the uppercase logic is now correctly in the command class and the updating of the GUI correctly in the mediator class. The roles are being performed by the correct classes. The meditor is the only one that knows about the intricacies of the GUI. And its all notification message driven and nicely de-coupled – the command class is triggered in response to an abstract notification `DATA_SUBMITTED` and sends the result back to the mediator using another abstract notification DATA\_CHANGED. PureMVC is working as intended (though we don't have a proper model yet).

```python
import wx

import puremvc.interfaces
import puremvc.patterns.mediator
import puremvc.patterns.command

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)

class MyFormMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
    NAME = 'MyFormMediator'

    def __init__(self, viewComponent):
        super(MyFormMediator, self).__init__(MyFormMediator.NAME, viewComponent)

        self.viewComponent.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.viewComponent.inputFieldTxt)

    def listNotificationInterests(self):
        return [ AppFacade.DATA_CHANGED ]   #ADD

    def handleNotification(self, notification):
        if notification.getName() == AppFacade.DATA_CHANGED:                  #ADD
            print "handleNotification (mediator)", notification.getBody()     #ADD
            mydata = notification.getBody()                                   #ADD
            self.viewComponent.inputFieldTxt.SetValue(mydata)                 #ADD

    def onSubmit(self, evt):
        mydata = self.viewComponent.inputFieldTxt.GetValue()
        print "got (mediator)", mydata
        self.sendNotification(AppFacade.DATA_SUBMITTED, mydata, self.viewComponent)

class DataSubmittedCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
        print "execute (command)", notification.getBody()
        mydata = notification.getBody()
        # viewComponent = notification.getType() # DELETE THIS LINE
        # viewComponent.inputFieldTxt.SetValue(mydata.upper()) # DELETE THIS LINE
        self.sendNotification(AppFacade.DATA_CHANGED, mydata.upper())   #ADD


class AppFacade(puremvc.patterns.facade.Facade):

    DATA_SUBMITTED = "DATA_SUBMITTED"
    DATA_CHANGED = "DATA_CHANGED"   #ADD

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeController(self):
        super(AppFacade, self).initializeController()

        super(AppFacade, self).registerCommand(AppFacade.DATA_SUBMITTED, DataSubmittedCommand)

class AppFrame(wx.Frame):
    myForm = None
    mvcfacade = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="Refactoring to PureMVC",size=(200,100))
        self.myForm = MyForm(self)

        self.mvcfacade = AppFacade.getInstance()
        self.mvcfacade.registerMediator(MyFormMediator(self.myForm ))

class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
```

Our diagnostic now shows how the flow of execution moves from the GUI to the mediator, to the command, and then back to the mediator again.

![](/blog/images/puremvcfuss_step4command.png)

* * *

### 5. Add a Model

You've been waiting for this step, I know. Let's add a proper model.

![](/blog/images/puremvcfussUMLstep5model.png)

_Adding a model to our architecture._

In the PureMVC framework's way of looking at things, the Model should be wrapped by a “Model Proxy” class. Just like the mediator wraps and looks after the GUI, the proxy wraps and looks after the model. In this refactoring step, we are going to add the Proxy class and use it as the model.

From the command class point of view, instead of putting the result of the business logic straight back into the GUI, the command class now writes the uppercase string to the model proxy. The model proxy then sends out a notification that the model data has changed - which the mediator picks up and acts on by updating the form inputfield control/widget. Basically we have a complete PureMVC architecture functioning now (see sequence diagram below).

Steps:

1.  Import the proxy namespace
    
2.  Define a class `DataModelProxy` which will hold the data (the string we are entering in and upper-casing). The proxy class sends a notification whenever the data changes, enabling e.g. the mediator to update the gui.
    
3.  Create and register the the Proxy class in the startup phase
    
4.  Change the command so that it looks up the model proxy and updates it with the uppercase string.
    
5.  Mediator is told about the data that changes by the model proxy raising a DATA\_CHANGED message. In response, the meditor takes the data and puts it in the GUI.
    
When the mediator has been notified by the model - how does the mediator get access to the model proxy data? 

Well it can be given a reference to the data proxy so that it can get the data itself, or the notification message can contain the actual data (remember that notification messages have two additional parameters after the message name – `getBody()` and `getType()` and it is up to you what you put there. Finally, the Mediator is within its rights to look up the data proxy itself if it wants using the `self.facade.retrieveProxy(...)` lookup technique.

```python
import wx

import puremvc.interfaces
import puremvc.patterns.mediator
import puremvc.patterns.command
import puremvc.patterns.proxy #ADD

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)

class MyFormMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
    NAME = 'MyFormMediator'

    def __init__(self, viewComponent):
        super(MyFormMediator, self).__init__(MyFormMediator.NAME, viewComponent)

        self.viewComponent.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.viewComponent.inputFieldTxt)

    def listNotificationInterests(self):
        return [ AppFacade.DATA_CHANGED ]

    def handleNotification(self, notification):
        if notification.getName() == AppFacade.DATA_CHANGED:
            print "handleNotification (mediator)", notification.getBody()
            mydata = notification.getBody()
            self.viewComponent.inputFieldTxt.SetValue(mydata)

    def onSubmit(self, evt):
        mydata = self.viewComponent.inputFieldTxt.GetValue()
        print "got (mediator)", mydata
        self.sendNotification(AppFacade.DATA_SUBMITTED, mydata, self.viewComponent)

class DataSubmittedCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
        print "execute (command)", notification.getBody()
        mydata = notification.getBody()
        # self.sendNotification(AppFacade.DATA_CHANGED, mydata.upper())  # DELETE LINE
        self.datamodelProxy = self.facade.retrieveProxy(DataModelProxy.NAME)  #ADD
        self.datamodelProxy.setData(mydata.upper())                           #ADD


class DataModelProxy(puremvc.patterns.proxy.Proxy): #ADD

    NAME = "DataModelProxy"

    def __init__(self):
        super(DataModelProxy, self).__init__(DataModelProxy.NAME, [])
        self.data = ""

    def setData(self, data):
        self.data = data
        print "setData (model)", data
        self.sendNotification(AppFacade.DATA_CHANGED, self.data)

class AppFacade(puremvc.patterns.facade.Facade):

    DATA_SUBMITTED = "DATA_SUBMITTED"
    DATA_CHANGED = "DATA_CHANGED"

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeController(self):
        super(AppFacade, self).initializeController()

        super(AppFacade, self).registerCommand(AppFacade.DATA_SUBMITTED, DataSubmittedCommand)


class AppFrame(wx.Frame):
    myForm = None
    mvcfacade = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="Refactoring to PureMVC",size=(200,100))
        self.myForm = MyForm(self)

        self.mvcfacade = AppFacade.getInstance()
        self.mvcfacade.registerMediator(MyFormMediator(self.myForm ))
        self.mvcfacade.registerProxy(DataModelProxy())   #ADD

class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
```

![](/blog/images/puremvcfuss_step5model.png)

* * *

## Taking Stock

Intermission – Taking Stock.

At this stage the PureMVC architecture is fully operational.

Here is the class diagram:

![](/blog/images/puremvcfussUMLstep5takestock.png)

_Class diagram of our application thus far._

Here is the sequence diagram:

![](/blog/images/puremvcfussUMLstep5sequence.png)

_Sequence diagram of what happens after the user types in some text  
and hits ENTER in the GUI._

Note that the proxy, mediator and command classes actually have a very convenient `sendNotification` method _on themselves_ (rather than having a reference to the facade's `sendNotification` method as illustrated in the above sequence diagram). In actuality, these self.`sendNotification` methods ultimately get routed to the facade anyway, so the sequence diagram above is essentially correct.

> “Aha” moment – several roles have been distilled out of two hacky lines of code

Its interesting that we have distilled three roles out of the original, two simple lines of code:

```python
mydata = self.myForm.inputFieldTxt.GetValue()
self.myForm.inputFieldTxt.SetValue(mydata.upper())
```

The above code gets some user input text, converts it to uppercase and stuffs it back into the GUI. After our PureMVC refactoring steps, those roles are now spread out across various classes and a major architectural revamp. The roles are:

*   Getting the data in and out of the GUI (mediator)
    
*   Converting the text to uppercase (command)
    

And we have added in an additional role which the original code didn't do

*   Holding and storing an independent representation of the text being displayed (model proxy)
    

Sure, we've added complexity – boy have we ever. But now we have something amazingly scalable. We won't be scaling this application up in this tutorial, however there are a couple more refactoring steps to do in order to tidy up a few things.

* * *

### 6. Model Proxy

Add a real Model behind the Model Proxy and Initialise the Model.

Let's now add a proper model that the model proxy wraps. In our simple example so far, this step seems redundant as it may seem easier to keep the string stored in the model proxy. Why not make the model proxy be the model?

In more complex projects, model proxies can become properly useful – possibly representing a number of model objects under the one model proxy, or even returning result sets due to the underlying data model being a database.

Another reason to separate the ModelProxy from the Model is that the ModelProxy class is free to “play ball” with the PureMVC framework e.g. sending out various notification messages whenever data gets changed etc. whereas a Model class is typically oblivious to such things (and probably should remain so). In our example, the DataModelProxy sends out a `DATA_CHANGED` notification – both in the constructor, and also whenever setData() is called.

![](/blog/images/puremvcfussUMLstep6.png)

_Adding a real model behind the model proxy._

**Steps:**

1.  Add a proper model class `Data` and have the `DataModelProxy` wrap it.
    
2.  Initialise the model with an initial string - and watch the default text appear in the GUI when the application starts up!
    

```python
import wx

import puremvc.interfaces
import puremvc.patterns.mediator
import puremvc.patterns.command
import puremvc.patterns.proxy

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)

class MyFormMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
    NAME = 'MyFormMediator'

    def __init__(self, viewComponent):
        super(MyFormMediator, self).__init__(MyFormMediator.NAME, viewComponent)

        self.viewComponent.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.viewComponent.inputFieldTxt)

    def listNotificationInterests(self):
        return [ AppFacade.DATA_CHANGED ]

    def handleNotification(self, notification):
        if notification.getName() == AppFacade.DATA_CHANGED:
            print "handleNotification (mediator)", notification.getBody()
            mydata = notification.getBody()
            self.viewComponent.inputFieldTxt.SetValue(mydata)

    def onSubmit(self, evt):
        mydata = self.viewComponent.inputFieldTxt.GetValue()
        print "got (mediator)", mydata
        self.sendNotification(AppFacade.DATA_SUBMITTED, mydata, self.viewComponent)

class DataSubmittedCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
        print "execute (command)", notification.getBody()
        mydata = notification.getBody()
        self.datamodelProxy = self.facade.retrieveProxy(DataModelProxy.NAME)
        self.datamodelProxy.setData(mydata.upper())

class DataModelProxy(puremvc.patterns.proxy.Proxy):

    NAME = "DataModelProxy"

    def __init__(self):
        super(DataModelProxy, self).__init__(DataModelProxy.NAME, [])
        #self.data = "" # DELETE THIS LINE
        self.realdata = Data()   #ADD
        self.sendNotification(AppFacade.DATA_CHANGED, self.realdata.data)   #ADD

    def setData(self, data):
        #self.data = data # DELETE THIS LINE
        self.realdata.data = data   #ADD
        print "setData (model)", data
        #self.sendNotification(AppFacade.DATA_CHANGED, self.data) # DELETE THIS LINE
        self.sendNotification(AppFacade.DATA_CHANGED, self.realdata.data)   #ADD

class Data: #ADD CLASS
    def __init__(self):
        self.data = "Hello - hit enter"

class AppFacade(puremvc.patterns.facade.Facade):

    DATA_SUBMITTED = "DATA_SUBMITTED"
    DATA_CHANGED = "DATA_CHANGED"

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeController(self):
        super(AppFacade, self).initializeController()

        super(AppFacade, self).registerCommand(AppFacade.DATA_SUBMITTED, DataSubmittedCommand)


class AppFrame(wx.Frame):
    myForm = None
    mvcfacade = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="Refactoring to PureMVC",size=(200,100))
        self.myForm = MyForm(self)

        self.mvcfacade = AppFacade.getInstance()
        self.mvcfacade.registerMediator(MyFormMediator(self.myForm ))
        self.mvcfacade.registerProxy(DataModelProxy())

class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
```

### The Application Initialisation Sequence

Getting intitial Model data into the GUI.

A nice effect here is that the string **"Hello - hit enter"** in the Data class magically appears in the GUI when the application starts up. How cool – some of this PureMVC architecture is starting to pay off. How does this happen? Well, notice that the DataModelProxy sends out a DATA\_CHANGED notification in its constructor (when it is also creating the instance of the real model Data class). The mediator intercepts this notification and displays the string in the GUI form.

![](/blog/images/puremvcfuss_step6refine.png)

_Two screenshots of our PureMVC wxPython application, showing how the model data magically appears in the GUI form on application startup._

* * *

### 7. Startup code

Move the startup code into a startup command class

Personally I'm not convinced this step is really necessary - however this step follows the convention on how PureMVC applications are put together.

![](/blog/images/puremvcfussUMLstep7startupcmd.png)

_The new startup command class._

Moving most of the startup code into its own command class may have the benefit of organising your code a little more, at the cost of complexity – I mean, we already have a nice place for constructing classes etc in the constructor of the AppFrame class. Even if we move some startup code into its own startup command class, we still need to create the form and the facade in AppFrame, so why not keep all the startup code in the one place? On the other hand, by moving what we can into the startup command, we may be helping decouple the AppFrame startup code from the knowledge of all the other clases involved in your framework e.g. mediators, commands etc. Certainly in a Flex application where namespaces are tightly controlled, or even a more serious python application where namespaces are more of an issue, having a startup comand class is a good thing.

1.  Move the startup code into a startup command class
    
2.  Change our initialisation to invoke the startup command via a notification message
    
```python
import wx

import puremvc.interfaces
import puremvc.patterns.mediator
import puremvc.patterns.command
import puremvc.patterns.proxy

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)

class MyFormMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
    NAME = 'MyFormMediator'

    def __init__(self, viewComponent):
        super(MyFormMediator, self).__init__(MyFormMediator.NAME, viewComponent)

        self.viewComponent.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.viewComponent.inputFieldTxt)

    def listNotificationInterests(self):
        return [ AppFacade.DATA_CHANGED ]

    def handleNotification(self, notification):
        if notification.getName() == AppFacade.DATA_CHANGED:
            print "handleNotification (mediator)", notification.getBody()
            mydata = notification.getBody()
            self.viewComponent.inputFieldTxt.SetValue(mydata)

    def onSubmit(self, evt):
        mydata = self.viewComponent.inputFieldTxt.GetValue()
        print "got (mediator)", mydata
        self.sendNotification(AppFacade.DATA_SUBMITTED, mydata, self.viewComponent)

class DataSubmittedCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
        print "execute (command)", notification.getBody()
        mydata = notification.getBody()
        self.datamodelProxy = self.facade.retrieveProxy(DataModelProxy.NAME)
        self.datamodelProxy.setData(mydata.upper())

class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand): #ADD CLASS
    def execute(self, notification):
        print "startup execute (command)", notification.getBody(), notification.getType()
        wxapp = notification.getBody()

        self.facade.registerMediator(MyFormMediator(wxapp.myForm))
        self.facade.registerProxy(DataModelProxy())

class DataModelProxy(puremvc.patterns.proxy.Proxy):

    NAME = "DataModelProxy"

    def __init__(self):
        super(DataModelProxy, self).__init__(DataModelProxy.NAME, [])
        self.realdata = Data()
        self.sendNotification(AppFacade.DATA_CHANGED, self.realdata.data)

    def setData(self, data):
        self.realdata.data = data
        print "setData (model)", data
        self.sendNotification(AppFacade.DATA_CHANGED, self.realdata.data)

class Data:
    def __init__(self):
self.data="Hello - hit enter"

class AppFacade(puremvc.patterns.facade.Facade):

    STARTUP = "STARTUP"   #ADD
    DATA_SUBMITTED = "DATA_SUBMITTED"
    DATA_CHANGED = "DATA_CHANGED"

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeController(self):
        super(AppFacade, self).initializeController()

        super(AppFacade, self).registerCommand(AppFacade.STARTUP, StartupCommand)   #ADD
        super(AppFacade, self).registerCommand(AppFacade.DATA_SUBMITTED, DataSubmittedCommand)

    def startup(self, app):   #ADD METHOD
        self.sendNotification( AppFacade.STARTUP, app )

class AppFrame(wx.Frame):
    myForm = None
    mvcfacade = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="Refactoring to PureMVC",size=(200,100))
        self.myForm = MyForm(self)

        self.mvcfacade = AppFacade.getInstance()
        # self.mvcfacade.registerMediator(MyFormMediator(self.myForm )) # DELETE
        # self.mvcfacade.registerProxy(DataModelProxy()) # DELETE
        self.mvcfacade.startup(self)   #ADD

class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
```

![](/blog/images/puremvcfuss_step7startupcmd.png)

## Conclusion

Here is the final UML.

![](/blog/images/puremvcfussUMLstep999.png)

_Final UML of our example_

You may notice that there are hardly any dependencies between classes. This is because classes communicate with each other via the PureMVC message notification system. This takes the form of a string message broadcast to the “world” e.g. e.g. **facade.sendNotification(“DATA\_CHANGED”, notificationMsg)** - the sender doesn't really care who handles it. Or it can take the form of looking up model instances, again by string references e.g. **facade.retreiveProxy(“datamodelproxy1”)**. We end up with a very decoupled design. Nice.

### Too much Complexity?

This series of refactorings has shown how you can really complicate your application by utilising the PureMVC framework. :-)

Seriously, on the positive side, you now have a scalable architecture where you can add more notification messages, more mediators, more commands – and everything will fit together. I think that a framework has value not just because of what it does, but rather because it guides you in how to structure your application – how to name your classes and where to put them, and how they play together.

If your application is simple it may not be worthwhile incorporating PureMVC, however hopefully this tutorial has shown you that it is not that hard to start with the PureMVC approach. I may have inspired you to use PureMVC with even your simple apps!

Finally, this tutorial has shown that you can hack something up in wxPython and then later, switch to PureMVC when you need to, in a step by step way.

Source code for all the steps is available [here](http://www.atug.com/downloads/puremvcrefactor_python.zip).

If you prefer a java example walkthrough, click [here](http://www.andypatterns.com/index.php?cID=86 "Refactoring to PureMVC - Java version").

\-Andy Bulka  
March 2009

P.S. This blog posting was presented as a talk to the Melbourne Patterns Group on the 1st April, 2009.

## Comments

### Posted by Arun George on Feb 15th, 2012  
Great article on pureMVC and its applicalbility through a simple example. This is cool. A very simple example which explains the complexity :) .  
  

### Posted by Byron Harris on May 25th, 2012  
Thanks for providing this example. It helps me in applying the concepts in the PureMVC documentation to Python and wxPython.  
  
A few minor points about the example code:  
  
- In the `DataSubmittedCommand.execute()`, it's not necessary to add attribute datamodelProxy since Command classes are meant to be stateless. Therefore you can just make datamodelProxy a method variable.  
  
- In `StartupCommand.execute()`, the variable named wxapp is inappropriate named. It's actually an AppFrame instance that is passed.

### Posted by T.Javed on Sep 25th, 2012
Thank You so much!  
  
I had read all the pureMVC documentation but was finding it hard to grasp it until I came across this nice little tutorial. It helped me a lot to clearly understand the pureMVC concept and implementation.  
  
cheers!

### Posted by Demolishun on Oct 20th, 2012

Putting logic in the controller does not make sense to me:

http://weblog.jamisbuck.org/2006/10/18/skinny-controller-fat-model  

http://stackoverflow.com/questions/235233/asp-net-mvc-should-business-logic-exist-in-controllers  
  
I am starting down the path to using pureMVC in my projects, but your example is confusing. It seems to me that the controller is supposed to be light weight and act as glue. What is the reasoning for putting the business logic in the controller and not the model?  
  
When I began to understand MVC it clicked in my head that the model would be independent and could be swapped out just like the view. I am also a little concerned about the AppFrame knowing about the Facade. This makes it harder to swap out the view. Or am I looking at this the wrong way?

***

## Java Example

Refactoring to PureMVC - Java

Here is a Java version of the tutorial I originally wrote in wxPython. It leaves out most of the commentary and concentrates on the code, so please read the [original tutorial](http://www.andypatterns.com/index.php?cID=84 "Refactoring to PureMVC") for more detail about the meaning of the refactoring steps.

I have used the same class names and the logic is identical (except for the parameters to the notification message DATA\_SUBMITTED, which I have swapped around due to the fact that in the Java PureMVC framework the getBody() parameter is of type object whereas in dynamic Python the type of this paramter is more flexible – more explanation is found below).

### 1. Starting Point

Step 1. Create a Basic Java GUI application form

Create a Java GUI application. Either hand code it or e.g. use Netbeans to kick start you. Then drop a

```javax.swing.JTextField jTextField1```

to the form. Don't bother adding any behaviour yet, lets get cracking with the refactoring.

### 2. Add a mediator

Step 2. Import PureMVC and add a mediator

Here is the mediator.

```java
/*
 * MyFormMediator.java
 */
package org.andy;

import org.puremvc.java.patterns.mediator.Mediator;

import org.puremvc.java.interfaces.INotification;
import javapuremvcminimal01.JavaPureMVCMinimal01Form;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class MyFormMediator extends Mediator implements ActionListener {

    public static final String NAME = "MyFormMediator";

    public MyFormMediator(JavaPureMVCMinimal01Form viewComponent)
    {
        super(NAME, null);

        setViewComponent(viewComponent);
        viewComponent.inputFieldTxt.addActionListener(this);
    }

    public void actionPerformed(ActionEvent evt) {
        JavaPureMVCMinimal01Form form = (JavaPureMVCMinimal01Form) viewComponent;

        form.inputFieldTxt.setText(form.inputFieldTxt.getText().toUpperCase());
    }
}
```

Here is the application startup code, which was generated automatically by Netbeans 6.5 and the startup method was modified to create the PureMVC facade and mediator.

```java
/*
 * JavaPureMVCMinimal01App.java
 */

package javapuremvcminimal01;

import org.jdesktop.application.Application;
import org.jdesktop.application.SingleFrameApplication;

import org.puremvc.java.patterns.facade.Facade;
import org.andy.MyFormMediator;

/**
 * The main class of the application.
 * Based on a Netbeans 6.5 template.
 */
public class JavaPureMVCMinimal01App extends SingleFrameApplication {
    public JavaPureMVCMinimal01Form myForm;

    /**
     * At startup create and show the main frame of the application.
     */
    @Override protected void startup() {
        myForm = new JavaPureMVCMinimal01Form(this);
        Facade mvcfacade = Facade.getInstance();
        mvcfacade.registerMediator(new MyFormMediator(myForm));
        show(myForm);
    }
    …
    …
}
```

Since we need access to the textField in the swing form generated by netbeans, we declare a public variable for ourselves. Netbeans seems to make all the gui elements private – so we are fighting that.

```java
/*
 * JavaPureMVCMinimal01Form.java
 *  (by default Netbeans names this JavaPureMVCMinimal01View but I renamed it).
 */

package javapuremvcminimal01;

import javax.swing.JFrame;

public class JavaPureMVCMinimal01Form extends FrameView {

    public javax.swing.JTextField inputFieldTxt;  // ADD

    public JavaPureMVCMinimal01Form(SingleFrameApplication app) {
        super(app);

        initComponents();
        inputFieldTxt = jTextField1;  // ADD

        …
        …

}
```
### 3. Command class

Step 3. Move the business logic into a Command class

Let's now move the behaviour (changing text to uppercase) out of the mediator and into a proper command class.

```java
/*
 * DataSubmittedCommand.java
 */

package org.andy;

import org.puremvc.java.interfaces.ICommand;
import org.puremvc.java.interfaces.INotification;
import org.puremvc.java.patterns.command.SimpleCommand;

import javapuremvcminimal01.JavaPureMVCMinimal01Form;

public class DataSubmittedCommand extends SimpleCommand implements ICommand {

    public void execute(INotification notification)
    {
        String mydata = (String) notification.getType();
        JavaPureMVCMinimal01Form viewComponent = (JavaPureMVCMinimal01Form) notification.getBody();
        viewComponent.inputFieldTxt.setText(mydata.toUpperCase());
    }
}
```

When the execute method gets called the first thing the execute code should do is decode the notification message for juicy information. Its fairly arbitrary how you use the notification class fields .getBody() and getType(). In the java implementation the only limitation is that getBody() holds an object and getType() a string. Use your own convention on how to use these two parameters, which can be different for each unique notifcation message - just make sure your sendNotification sends the right things to match how you are decoding things.

In the example so far, in the notification message DATA\_SUBMITTED I use the getBody() field to pass a reference to the viewcomponent, i.e. the form. This is only a temporary situation, we will later change this so that the command simply raises a message and let the mediator deal with the viewcomponent (which is the mediators job). I use the getType() parameter of the notification message to hold the text of the edit control at the time when the use hit ENTER.

Now the mediator has changed a little. It no longer does the work of uppercase, it delegates this entirely to the command class simply by raising a DATA\_SUBMITTED message:

```java
/*
 * MyFormMediator.java
 */
package org.andy;

import org.puremvc.java.patterns.mediator.Mediator;

import org.puremvc.java.interfaces.INotification;
import javapuremvcminimal01.JavaPureMVCMinimal01Form;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class MyFormMediator extends Mediator implements ActionListener {

    public static final String NAME = "MyFormMediator";

    public MyFormMediator(JavaPureMVCMinimal01Form viewComponent)
    {
        super(NAME, null);

        setViewComponent(viewComponent);
        viewComponent.inputFieldTxt.addActionListener(this);
    }

    public void actionPerformed(ActionEvent evt) {
        JavaPureMVCMinimal01Form form = (JavaPureMVCMinimal01Form) viewComponent;

        // form.inputFieldTxt.setText(form.inputFieldTxt.getText().toUpperCase());  // DELETE THIS LINE
        this.sendNotification(AppFacade.DATA_SUBMITTED, viewComponent, form.inputFieldTxt.getText());
    }

}
```

Note that another way to send a notification message (instead of sendNotification) is:

```java
import org.puremvc.java.patterns.observer.Notification;

this.facade.notifyObservers(new Notification(AppFacade.DATA_SUBMITTED, 
        viewComponent, form.inputFieldTxt.getText()));
```

however this is a bit PureMVC old school and not quite as clean as what we have used.

We also have needed to create our own concrete Facade class so that we can define our own message types.

```java
/*
 * AppFacade.java
 */

package org.andy;

import org.puremvc.java.patterns.facade.Facade;

public class AppFacade extends Facade {

    public static final String DATA_SUBMITTED = "DATA_SUBMITTED";

    private static AppFacade instance = null;

    public static AppFacade getInst()
    {
        if (instance == null) {
            instance = new AppFacade();
        }
        return (AppFacade) instance;
    }

    @Override
    protected void initializeController()
    {
        super.initializeController();

        registerCommand(DATA_SUBMITTED, DataSubmittedCommand.class);
    }
}
```

And of course we instantiate our own concrete facade instead of the base class facade:

```java
/*
 * JavaPureMVCMinimal01App.java
 */
    …
    …

    @Override protected void startup() {
        myForm = new JavaPureMVCMinimal01Form(this);

        Facade mvcfacade = Facade.getInstance();
        Facade mvcfacade = AppFacade.getInst();

        mvcfacade.registerMediator(new MyFormMediator(myForm));
        show(myForm);
    }
```

### 4. GUI Access Logic

Step 4. Move the ability to access the GUI out of the Command class

Let's now have the command raise a notification message after it has done its work, and let the _mediator_ look after putting the result back into the gui.

```java
/*
 * MyFormMediator.java
 */
package org.andy;

import org.puremvc.java.patterns.mediator.Mediator;

import org.puremvc.java.interfaces.INotification;
import javapuremvcminimal01.JavaPureMVCMinimal01Form;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class MyFormMediator extends Mediator implements ActionListener {

    public static final String NAME = "MyFormMediator";

    public MyFormMediator(JavaPureMVCMinimal01Form viewComponent)
    {
        super(NAME, null);

        setViewComponent(viewComponent);
        viewComponent.inputFieldTxt.addActionListener(this);
    }

    public void actionPerformed(ActionEvent evt) {
        JavaPureMVCMinimal01Form form = (JavaPureMVCMinimal01Form) viewComponent;

        // form.inputFieldTxt.setText(form.inputFieldTxt.getText().toUpperCase());  DELETE
        this.sendNotification(AppFacade.DATA_SUBMITTED, viewComponent, form.inputFieldTxt.getText());
    }

    @Override
    public String[] listNotificationInterests()
    {
        return new String[] {AppFacade.DATA_CHANGED};
    }

    @Override
    public void handleNotification(INotification notification)
    {    
        if(notification.getName().equals(AppFacade.DATA_CHANGED))
        {
            System.out.println("handleNotification (mediator) " + notification.getType());

            String mydata = (String) notification.getType();
            JavaPureMVCMinimal01Form form = (JavaPureMVCMinimal01Form) viewComponent;
            form.inputFieldTxt.setText(mydata);
        }
    }
}

/*
 * DataSubmittedCommand.java
 */

package org.andy;

import org.puremvc.java.interfaces.ICommand;
import org.puremvc.java.interfaces.INotification;
import org.puremvc.java.patterns.command.SimpleCommand;

// import javapuremvcminimal01.JavaPureMVCMinimal01Form;  DELETE

public class DataSubmittedCommand extends SimpleCommand implements ICommand {

    public void execute(INotification notification)
    {
        String mydata = (String) notification.getType();
        // JavaPureMVCMinimal01Form viewComponent = (JavaPureMVCMinimal01Form) notification.getBody();  DELETE
        // viewComponent.inputFieldTxt.setText(mydata.toUpperCase());  DELETE
        this.sendNotification(AppFacade.DATA_CHANGED, null, mydata.toUpperCase());
    }
}
```

Notice that the mediator is putting the result of the command behaviour (the uppercasing of user entered text) into the gui – the command is not touching the GUI anymore, which explains why the command no longer needs to import the GUI form class JavaPureMVCMinimal01Form.

The command class DataSubmittedCommand simply raises a notification, passing the changed text as part of the notifcation message (we are using the getType() parameter to hold the uppercased string – though we could have passed it around in the getBody() parameter).

Finally we need to add the new notification message type to the facade:

```java
/*
 * AppFacade.java
 */
package org.andy;

import org.puremvc.java.patterns.facade.Facade;

public class AppFacade extends Facade {

    public static final String DATA_SUBMITTED = "DATA_SUBMITTED";
    public static final String DATA_CHANGED = "DATA_CHANGED";
    …
    …
}
```

### 5. Add a Model

Step 5. Add a Model

Let's add a proper model. For now we leave out the real model behind the proxy and use the proxy class as both proxy and model.

```java
/*
 * DataModelProxy.java
 */
package org.andy;

import org.puremvc.java.patterns.proxy.Proxy;

public class DataModelProxy extends Proxy {

    public static final String NAME = "DataModelProxy";

    private String data;

    public DataModelProxy()
    {
        super(NAME, null);
        this.data = "";
    }

    public void setData(String data) {
        this.data = data;
        System.out.println("setData (model) " + data);
        this.sendNotification(AppFacade.DATA_CHANGED, null, this.data);
    }
}
```

We alter the command class to poke the uppercase string into the model. We then let the model notify the world that the model data has altered.

```java
/*
 * DataSubmittedCommand.java
 */

package org.andy;

import org.puremvc.java.interfaces.ICommand;
import org.puremvc.java.interfaces.INotification;
import org.puremvc.java.patterns.command.SimpleCommand;


public class DataSubmittedCommand extends SimpleCommand implements ICommand {

    public void execute(INotification notification)
    {
        String mydata = (String) notification.getType();
        // this.sendNotification(AppFacade.DATA_CHANGED, null, mydata.toUpperCase());  DELETE
        DataModelProxy datamodelProxy = (DataModelProxy) facade.retrieveProxy(DataModelProxy.NAME);
        datamodelProxy.setData(mydata.toUpperCase());
    }
}
```

Finally we need to instantiate and register the DataModelProxy instance in the application's startup code:

```java 
/*
 * JavaPureMVCMinimal01App.java
 */

package javapuremvcminimal01;

import org.jdesktop.application.Application;
import org.jdesktop.application.SingleFrameApplication;
import org.puremvc.java.patterns.facade.Facade;
import org.andy.MyFormMediator;

public class JavaPureMVCMinimal01App extends SingleFrameApplication {
    public JavaPureMVCMinimal01Form myForm;

    /**
     * At startup create and show the main frame of the application.
     */
    @Override protected void startup() {
        myForm = new JavaPureMVCMinimal01Form(this);
        Facade mvcfacade = AppFacade.getInst();
        mvcfacade.registerMediator(new MyFormMediator(myForm));
        mvcfacade.registerProxy(new DataModelProxy());
        show(myForm);
    }
    …
    …
}
```

### 6. Model Proxy

Step 6. Add a real Model behind the Model Proxy and Initialise the Model

Let's now add a proper model that the model proxy wraps.

```java
/*
 * Data.java
 */
package org.andy;

public class Data {

    public String data;
    
    public Data() {
        this.data = "Hello - hit enter";
    }
}

/*
 * DataModelProxy.java
 */
package org.andy;

import org.puremvc.java.patterns.proxy.Proxy;

public class DataModelProxy extends Proxy {

    public static final String NAME = "DataModelProxy";

    // private String data; DELETE
    private Data realdata;

    public DataModelProxy()
    {
        super(NAME, null);
        // this.data = ""; DELETE
        this.realdata = new Data();
        this.sendNotification(AppFacade.DATA_CHANGED, null, this.realdata.data);
    }

    public void setData(String data) {
        // this.data = data; DELETE
        this.realdata.data = data;
        System.out.println("setData (model) " + data);
        // this.sendNotification(AppFacade.DATA_CHANGED, null, this.data); DELETE
        // this.sendNotification(AppFacade.DATA_CHANGED, null, this.realdata.data); DELETE
    }
}
```

I have make the model string data public to keep the example simple. Feel free to add setters and getters.

### 7. Startup code

Step 7. Move the startup code into a startup command class

Let's now create a startup command and move as much of the startup logic into there.

```java
/*
 * StartupCommand.java
 */
package org.andy;

import org.puremvc.java.interfaces.ICommand;

import org.puremvc.java.interfaces.INotification;
import org.puremvc.java.patterns.command.SimpleCommand;

import javapuremvcminimal01.JavaPureMVCMinimal01App;

public class StartupCommand extends SimpleCommand implements ICommand {

    public void execute(INotification notification)
    {
        System.out.println("startup execute (command) " + notification.getBody());

        JavaPureMVCMinimal01App app = (JavaPureMVCMinimal01App) notification.getBody();
        facade.registerMediator(new MyFormMediator(app.myForm));
        facade.registerProxy(new DataModelProxy());
    }
}
```

We need register the startup command with the facade and define a STARTUP message which will be used to trigger it:

```java
/*
 * AppFacade.java
 */
package org.andy;

import org.puremvc.java.patterns.facade.Facade;
import javapuremvcminimal01.JavaPureMVCMinimal01App;

public class AppFacade extends Facade {

    public static final String STARTUP = "STARTUP";
    public static final String DATA_SUBMITTED = "DATA_SUBMITTED";
    public static final String DATA_CHANGED = "DATA_CHANGED";

    private static AppFacade instance = null;

    public static AppFacade getInst()
    {
        if (instance == null) {
            instance = new AppFacade();
        }
        return (AppFacade) instance;
    }

    @Override
    protected void initializeController()
    {
        super.initializeController();

        registerCommand(STARTUP, StartupCommand.class);
        registerCommand(DATA_SUBMITTED, DataSubmittedCommand.class);
    }

    public void startup(JavaPureMVCMinimal01App app)
    {
        this.sendNotification(STARTUP, app, null);
    }
}
```

And we need to alter the application startup code to do less. Notice that we lose the need for some imports, thus proving that a reason for having the startup command is to decouple and loosen dependencies.

```java
/*
 * JavaPureMVCMinimal01App.java
 */

package javapuremvcminimal01;

import org.jdesktop.application.Application;
import org.jdesktop.application.SingleFrameApplication;
// import org.puremvc.java.patterns.facade.Facade;
import org.andy.AppFacade;
// import org.andy.MyFormMediator;
// import org.andy.DataModelProxy;

public class JavaPureMVCMinimal01App extends SingleFrameApplication {
    public JavaPureMVCMinimal01Form myForm;

    /**
     * At startup create and show the main frame of the application.
     */
    @Override protected void startup() {
        myForm = new JavaPureMVCMinimal01Form(this);
        Facade AppFacade mvcfacade = AppFacade.getInst();
        // mvcfacade.registerMediator(new MyFormMediator(myForm));
        // mvcfacade.registerProxy(new DataModelProxy());
        mvcfacade.startup(this);
        show(myForm);
    }
    …
    …
}
```

Since we are calling a brand new `startup()` method on our concrete facade, and this method is not declared in the Facade base class, we need to change the declaration we have been using from Facade to AppFacade. The author of PureMVC recommends this technique of bootstrapping however whether the `startup()` method officially makes it into the base class in future versions of PureMVC remains to be seen. We don't have to hold our breath for this, as you can see, we simply define our own `startup()` method on our own concrete facade class.

### 8. Packaging

Step 8. Java specific – Organise the classes into packages

You could potentially move the classes into packages that reflect the roles they are playing. How about:

*   Data and DataModelProxy → **Model** package
    
*   DataSubmittedCommand and StartupCommand → **Controller** package
    
*   MyFormMediator and JavaPureMVCMinimal01Form → **View** package
    

and we might as well...

*   JavaPureMVCMinimal01App and AppFacade → **App** package
    

Here are a couple of screenshots of the GUI in operation:

![](http://www.atug.com/images/PureMvcRefactorImages/puremvcfussJAVA1.png)

```
compile:

run:

startup execute (command) javapuremvcminimal01.JavaPureMVCMinimal01App@1e67ac

handleNotification (mediator) Hello - hit enter
```

User hits ENTER

![](http://www.atug.com/images/PureMvcRefactorImages/puremvcfussJAVA2.png)

```
setData (model) HELLO - HIT ENTER

handleNotification (mediator) HELLO - HIT ENTER
```

### Conclusion (Java)

We have seen how we can introduce PureMVC into an existing Netbeans application, step by step. I haven't hooked up the about box or the menus into the PureMVC system because these things were created by default by Netbeans and I was focussed simply on duplicating the Python minimalist example. 

The [Python refactoring steps above]({{< relref "#1-starting-point" >}}) contain more explanation than this Java example, so that may be useful to study too.  

## Resources

- The [Java source code](http://www.atug.com/downloads/puremvcrefactor_java.zip) for this example.
- The [Python source code](http://www.atug.com/downloads/puremvcrefactor_python.zip) for this example.
