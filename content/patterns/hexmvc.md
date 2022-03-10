---
title: "HexMVC"
date: 2022-02-12
draft: false
type: docs
description: "Hexagonal Architecture pattern + Model View Controller (MVC)"
tags: ["Design Patterns", "MVC", "Controllers", "Javascript"]

---

Andy Bulka,  
March 2012

A new, architectural pattern for building multi-platform, scalable applications based on ideas from the Hexagonal Architecture pattern + Model View Controller (MVC).

**TLDR:** Write the application layer but don't import or use any libraries directly.  Wrap all "library" calls with Adapter objects, so that you can switch to other libraries easily. 

**TLDR:** "Libraries" can amazingly, include the application data Model itself, Database and persistence layers, the entire GUI and all calls to server APIs. Plug and play everything with this architecture!

# ![](/patterns/images/hexmvc/image16.png)

> This is a draft article, written in 2012. It could do with some further editing, but I've never gotten around to it, so finally decided to publish it anyway, in 2022.


## Abstract

HexMVC - This is my name for an architectural pattern that has arisen out of some long term research into PureMVC and ways to simplify it. Its also an attempt to fix some of the unsatisfactory aspects of traditional layered architectures by incorporating some core ideas out of the mysterious Hexagonal Architecture pattern.  The hexagonal structure allows us to put the model on a more equal footing with other layers - rather than always having the model ‘at the bottom’.  Its a rejection of a complex 'event'-ing framework in favour of multicast delegation based on interfaces. It uses dependency injection to configure apps to use different libraries and frameworks, whilst keeping the core app the same.

I will present a fully functional example code which can be configured to run under pure python or under .NET using a choice of different GUI libraries (wxpython or windows forms or wpf), different server libraries (bottle or .NET). Everything is switchable using config files. The persistence layer is also switchable and the servers implement REST APIs consistent with the services offered by the core App.

Note that the example code needs no framework code whatsoever, thus could be considered an architectural pattern - an abstract idea that can be implemented in any language and used in any project.  The pattern lets you develop a core application and swap in & out alternate gui's, persistence and services.  It prescribes how to add app functionality whilst keeping your design clean.

## Example - Python

Here is a real configuration Python file which assembles, injects and launches my sample application. The application consists of a GUI, a Server, a model with application logic.

```python
from ModelOo import Model
from ModelOoAdapter import ModelOoAdapter

#from PersistenceOoPickle import Persistence
from PersistenceOoHomegrown import Persistence

from ServerBottleAdapter import Server
#from ServerMockAdapter import Server

from ViewWxAdapter import MyWxApp
import wx
from UtilRandomStdpythonAdapter import RandomIntFunction
from UtilJsonStdpythonAdapter import JsonFromDictFunction
from App import App

# Create Model - Object Oriented instances in memory
model_oo = Model()
persistence = Persistence()
model = ModelOoAdapter(model_oo, persistence)

# Create Server
server = Server(host='localhost', port=8081)

# Create Gui
wxapp = MyWxApp(redirect=False)
gui = wxapp.myframe  # gui mediator inherits from gui rather than wrapping it

# Hook up Utility adapters
gui.random = RandomIntFunction
server.json_from_dict = JsonFromDictFunction

# Create Core Hexagon App and inject adapters
app = App(model, server, gui)
wx.CallAfter(app.Boot)

# Start Gui
wxapp.MainLoop() 
```

## Example - Javascript

Here is a Todo app implementation in Javascript [http://jsfiddle.net/tcab/mC5qA/](https://www.google.com/url?q=http://jsfiddle.net/tcab/mC5qA/&sa=D&source=editors&ust=1644533497537306&usg=AOvVaw2IyZvhDC0eV65oxs-1pTn-)

![javascript-impl-add](/patterns/images/hexmvc/javascript-impl-add.png)

```html
<select id="list" size="10" style="width: 15em"></select><br/>
<button id="plusBtn">  +  </button>
<button id="minusBtn">  -  </button>
```

```javascript
/*
MODEL
*/

var ListModel = function (items) {
    this._items = items;
    this._selectedIndex = -1;
};
 
ListModel.prototype = {
 
    getItems : function () {
        return [].concat(this._items);
    },
 
    addItem : function (item) {
        this._items.push(item);
    },
 
    removeItemAt : function (index) {
        var item = this._items[index];
        this._items.splice(index, 1);
        maxindex = this._items.length - 1;
        if (this._selectedIndex > maxindex) {
            this.setSelectedIndex(maxindex);
        }
        return item;
    },
    
    getSelectedIndex : function () {
        return this._selectedIndex;
    },
 
    setSelectedIndex : function (index) {
        this._selectedIndex = index;
    }
 
};

var ListModelAdapter = function (model) {
    this._model = model;
};

ListModelAdapter.prototype = {
 
    getItems : function () {
        return this._model.getItems();
    },
 
    addItem : function (item) {
        this._model.addItem(item);
        $(document).trigger('MODEL_THING_ADDED', {item: item});
    },
 
    removeItemAt : function (index) {
        var item = this._model.removeItemAt(index);
        $(document).trigger('MODEL_CHANGED', {item: item});
    },
    
    getSelectedIndex : function () {
        return this._model.getSelectedIndex();
    },
 
    setSelectedIndex : function (index) {
        var previousIndex = this._selectedIndex;
        this._model.setSelectedIndex(index);
        $(document).trigger('MODEL_SELECTION_CHANGED', {previous: previousIndex});
    }
    
};


/* 
VIEW 
*/

var ListViewAdapter = function (model) {
    this._model = model;
};
 
ListViewAdapter.prototype = {
 
    show : function () {
        this.rebuildList();
    },
 
    rebuildList : function () {
        console.log("VIEW REBUILD with index at " + this._model.getSelectedIndex());            
        var list = $('#list');
        list.html('');
        var items = this._model.getItems();
        var i = 0;
        for (var key in items) {
            list.append($('<option value="' + i + '">' + items[key] + '</option>')); 
            i++;
        }
        this.updateSelected();
    },
    
    updateSelected : function () {
        console.log("VIEW updateSelected "  + this._model.getSelectedIndex());
        $('#list')[0].value = this._model.getSelectedIndex();
    },
    
    onAdd : function () {
        $(document).trigger('CMD_ADD_ITEM');
    },
    
    onDelete : function () {
        $(document).trigger('CMD_DELETE_ITEM');
    },
    
    onListSelectionChanged : function (e) {
        $(document).trigger('CMD_SELECTION_CHANGED', e);
    },
    
};

/* 
CONTROLLER
*/

var ListController = function (model) {
    this._model = model;
};
 
ListController.prototype = {
 
    cmdAddItem : function () {
        var item = prompt('Add item:', '');
        if (item)
            this._model.addItem(item);
    },
 
    cmdDelItem : function () {
        var index = this._model.getSelectedIndex();
        console.log("controller delItem " + index);
        if (index != -1)
            this._model.removeItemAt(this._model.getSelectedIndex());
    },
 
    cmdUpdateSelected : function (e) {
        console.log("CONTROLLER updateSelected " + e.target.selectedIndex);
        this._model.setSelectedIndex(e.target.selectedIndex);
    },
    
};

/*
Bootstrap
*/

$(function () {
    //var model = new ListModel(['aaa', 'bbb', 'ccc', 'ddddd']);
    var model = new ListModelAdapter(new ListModel(['aaa', 'bbb', 'ccc', 'ddddd']));
    var view = new ListViewAdapter(model);
    var controller = new ListController(model);  // can also pass in view if you need it.
                                               
    // Private eventing between gui and gui adapter
    $('#plusBtn').click(function () { view.onAdd() });
    $('#minusBtn').click(function () { view.onDelete() });
    $('#list').change(function (e) { view.onListSelectionChanged(e); });
    // More abstract application eventing
    $(document).bind('CMD_ADD_ITEM', function(e) { controller.cmdAddItem(); });
    $(document).bind('CMD_DELETE_ITEM', function(e) { controller.cmdDelItem(); });
    $(document).bind('CMD_SELECTION_CHANGED', function(e, info) { controller.cmdUpdateSelected(info); });                                           
    $(document).bind('MODEL_THING_ADDED', function(e, info) { view.rebuildList(); });
    $(document).bind('MODEL_CHANGED', function(e, info) { view.rebuildList(); });
    $(document).bind('MODEL_SELECTION_CHANGED', function(e, info) { view.updateSelected(); });
                                                 
    view.show();
});
```

> There are more source code implementations in [the appendix](/patterns/hexmvc/#hexmvc-source-code)

## HexMvc History

### MGM days

My initial simplification and re-telling of MVC came with my [MGM pattern](/patterns/mvca-pattern/) where I simply said (well perhaps not so simply, given that it was a paper for a design patterns conference) was that in these (more modern) days where we have proper, sophisticated GUI widgets with eventing and self rendering - there was a need to retell the MVC story - which was traditionally also looking after all eventing, user interaction and even rendering of the GUI.

So I came up with MGM (model-gui-mediator) where the mediator took on the roles of intercepting events from the GUI widget, sticking info into the model, and also of populating the GUI with fresh information.  The “mediator” class (the last “M” in MGM - although visually it sat more in the middle - between the model and the gui) was a controller and view adapter in one - whereas these days I would separate these two roles, as you will see in HexMVC.  

The benefit of this variation of the MVC design pattern was that was practical and minimalist.  It dealt with the reality of modern gui widgets, whether they be GUI widgets or html DOM elements and created only a single class that mediated with a model.  In a sense it was the simplest MVC possible, whilst retaining model and gui separation.

### Next steps

As I learned more about the roles involved in MVC, and encountered variants that teased apart those roles more fully (like pureMVC) I became interested in upscaling my MVC approach a little so that it was more all encompassing and took into account whole-application considerations, like providing a central controller layer for housing many ‘commands’.  

Then I became interested in bootstrapping the wiring of whole apps with MVC architectures, and eventually in the swappability of guis and models - which led to HexMVC.

### HexMVC in a nutshell

> **TLDR:** Write the application layer but don't import or use any libraries directly.  Wrap all library calls with Adapter objects, so that you can switch to other libraries easily.

HexMVC says that there must be a view class that looks after the off the shelf GUI widget (or in the case of the browser, the DOM element).  In the wild, the term “view” is ambiguous and sometimes means the gui adapter or the gui or both.  I use the term view adapter for the class that looks after the widget/DOM element.

So far this is not controversial.  HexMVC then goes on to say a few more interesting things:

- Firstly, that models and GUI widgets should be treated on an equal footing, and be “adapted”.

- Secondly, that generic, application eventing should occur between adapters and a central controller - any private eventing between the gui and its adapter should remain private. In the case of model adapters, they implement all the eventing and the models remain pure.  

- Lastly, the application and controller are bound together as the “application hub”, which may be split into many command objects. The application layer talks to the orbiting sattelite functionality via the adapter interfaces, and thus the application is insulated from changes in the “implementation”.  Adapters can, more efficiently, also talk to each other directly, but again, only through the adapter interfaces.

More broadly, the HexMVC approach is wired up through dependency injection and eventing and as you may have noticed, the use of adapters - more specifically families of adapters - so that different implementations can be plugged in without the application noticing.  An adapter is essentially a ‘driver’ you install for a particular implementation being used - like a new printer driver for a new printer.  That’s where the ‘hex’ comes into it, from the ‘hexagonal’ architecture pattern idea (later renamed “ports and adapters”).

### Rules and Roles:

Note: when I say ‘notifies’ I mean via notifications via eventing - which is managed/wired up by dependency injection - and not through layers actually knowing about each other.

*   view layer notifies controller, model layer usually does not notify controller, but it could.
*   model layer often efficiently notifies view layer directly, yes.
*   view layer can read from model later directly, yes - but not modify it.
*   controller can manipulate both model and view layers.


## Layered Architectures

I had always been fascinated by the idea of pluggable, modular application designs where you could plug in decoupled services/functionality into an app.  Its a truth that adding functionality adds complexity almost exponentially - it becomes harder and harder to add features without introducing problems and inteference.  I wanted a way out of that.

Simple layering:

![](/patterns/images/hexmvc/image8.png)

A recent talk I gave on layered architectures reinforced the benefits of layering. However I found numerous people talking about the limitations of having the model ‘at the bottom’ of the layering stack.  Plus lots of people were introducing an ‘infrastructure layer’ which stood vertically and had access to all layers.  

![](/patterns/images/hexmvc/image1.png)

Finally, there were all these techniques for breaking out of layers, like broadcast notifications, eventing and dependency injection.  So I got to thinking that maybe a different metaphor was needed, something a bit less vertical, and more like a circle.

![](/patterns/images/hexmvc/image10.png)

*Possible evolution of layering*

When teaching design patterns courses including sessions about the adapter pattern, I would always end that particular session with the idea of using adapters as a way of insulating an app from the ‘bad outside world’ and adapt all external libraries.  It was a radical, intriguiing idea - possibly a bit impractical and theoretical. So I ended up trying to build such a system anyway.

![](/patterns/images/hexmvc/image18.png)

Alistair Cockburn described a [hexagonal architecture](https://www.google.com/url?q=http://alistair.cockburn.us/Hexagonal%2Barchitecture&sa=D&source=editors&ust=1644533497539284&usg=AOvVaw2f2mT_1Zk2v3iJ84jJRrNP) (later renamed Ports and Adapters pattern) which had services, gui’s, db, etc. around a central app.  The application talked to adapters.  

![](/patterns/images/hexmvc/image24.gif)

*The hexagonal architecture*

> 
This was the architecture I was intrigued by, but there were no reference implementations, and a lot of the writing on the webpage seemed theoretical and sketchy - like a half baked idea that nobody had actually tried.  So I went ahead and built something similar - as simply as possible.

I had always liked the [PureMvc](https://www.google.com/url?q=http://puremvc.org/&sa=D&source=editors&ust=1644533497539894&usg=AOvVaw0krRSlmvdpyy7V-x2aGNRS) pattern, which was a bold retelling of the mvc architecture pattern.  It described all the roles in an mvc architecture, and provided strict rules as to who knows who and how the sequence of interactions went.  I wrote a number of [articles](https://www.google.com/url?q=http://www.andypatterns.com/index.php/blog/puremvc_refactor/&sa=D&source=editors&ust=1644533497540127&usg=AOvVaw1wOxO1elRARnO7oLGybGMF) about it.

![](/patterns/images/hexmvc/image2.png)

It is a framework and has been ported to most languages.  In practice I found it effective though tedious because of all the rules and registrations - and with its home grown eventing system it is tedious to declare event types, register handlers etc.  I wanted something simpler, whilst keeping the good stuff.  When I implemented an early/partial HexMvc version of a minimal PureMvc sample app, I was able to remove all references to the PureMvc framework and simplify the resulting application - the cost was a dozen extra lines of code to get it working the same.  But being able to remove an entire framework and get the the same result was certainly encouraging.

## HexMVC Fundamentals

### App in the centre

We start the basic hexagonal architecture with the idea of application in the core.

The application talks to interfaces, which are implemented by adapters.

![](/patterns/images/hexmvc/image11.png)

*The controller too, lives inside the central app hub.*

#### The App

*   Holds refs to the core adapters (server, gui, model)
*   Wires the core adapters so they know about the app
*   App has job of housing the domain logic and app logic and thus the controller/commands.
*   App sometimes mediates - calls come in and the app sends them out again. Defines one or two methods that an adapter may need (e.g. for that adapter to communicate some info to or get some info from another adapter)  Mediation role.
*   Defines Boot() and Shutdown()
*   Injects multicast dependencies

Note the app does not instantiate objects - this is done by the bootstrapper.

#### Layers as slices through the App circle.

Thus we have taken top down layering and making it round a “Application Hub” instead.  If you follow one particular event flow e.g. from gui to model and back again, you get a traditional view-controller-model top down layered cake.

![](/patterns/images/hexmvc/image17.png)

But by allowing for more event flows and more services plugged in to a hub, we get a more flexible and interesting architecture, which is still a layered one.  Thus you can get different layers depending on where you start and where you finish.  Nobody is ‘on top’ or ‘on the bottom’.

E.g. I add a server layer which provides REST services to the web, as an example of another significant layer.

#### Interfaces Everywhere

As GOF says in its introduction, one of the main two OO principles is “Program to an interface, not an implementation”.  This allows clients to be decoupled from the implementation.

#### Adpaters Everywhere

In HexMvc we write adapters to implement the interfaces. The adapters’ purpose is to provide a level of indirection between the application logic and the substantive thing the application is talking to.

### HexMvc Control flow

In HexMvc I pretty much follow the PureMvc rules and call sequences.

#### The rules

*   The Model notifies, but doesn't listen and ultimately knows nothing about anything else in the system.
*   View sends messages to controller and listens for incoming messages from model.
*   Controller commands are created and invoked by certain messages and they send out messages if they want to.

#### The typical call sequence

Here the gui adapter raises command events and listens for notification events.  A command event is an event that causes the controller to do something (which may then indirectly instantiate a command object to the work).  A notification event would be e.g. the model layer saying ‘something has changed’.  Controllers act directly on the model / model adapter layer and don’t typically raise events.  The model layer doesn’t listen for events, but can generate notification events.

![](/patterns/images/hexmvc/image15.png)

### Controller

The controller makes available an abstract chunk of information that the view renders, so in that sense a HexMvc controller is like a traditional web controller class.

*   Controller listens for GUI command messages
*   Responds by implementing the business logic  - optionally uses command objects to do the work
*   Talks to the model adapter and other adapters

*   Offers other functionality that can get invoked directly (not just from eventing) e.g. from the server service. Provides information as implementation independent, abstract chunks e.g. dictionaries, datastructures, vanilla app objects.

Note that controllers shouldn’t get too ‘view specific’ - these roles are performed by the View Adapter.  Choosing templates and constructing juicy, view specific data structures are not jobs for the controller.

### Eventing

I use a simplified eventing system (see in depth discussion on eventing later in this document).

#### Application specific eventing vs gui eventing

The adapters is where you implement application specific eventing.  The Gui itself may have some eventing but this is gui implementation specific and not to be confused with the eventing that the application uses.  Its the gui adapter for example, that intercepts gui specific eventing and rasies the appropriate application event.  The gui adapater similarly listens for the appropriate application event and does something with it, like poke values into controls on a windows form.

### The Bootstrapper

Instantiation of adapters and the things they adapt (the ‘ring’ objects) should be outside the App.  Theoretically you inject different ring adapters into the app and the app will still work.  That’s the whole point.

*   Instantiates all instances of objects
*   Injects normal dependencies, wires up the ring adapters to talk to each other if needed
*   Can be considered configuration

### Dependency Injection

The bootstrapper has aspects of a factory in that it instantiates the correct objects.

It then uses dependency injection config bootup everywhere to configure

When you wire up your objects to point to each other you are doing dependency injection - as long as the objects are not instantiating instances of the objects they are pointing to themselves, and the injection is done from ‘outside’. The objects being injected are thus depending on an abstraction or interface - which is injected later.

## HexMvc in Detail

![](/patterns/images/hexmvc/image6.png)

All in One HexMvc Diagram

### App to GUI boundary

Swappable guis, just rewrite the gui adapter

![](/patterns/images/hexmvc/image23.png)

### View

We should distinguish between the view adapter and the view ‘renderer’/controls.  The latter ‘ring object’ can be hand crafted by code or built by nice high level form building tools - and should have absolutely no knowledge of the app.

*   Views renderers are totally dumb.  
*   View Adapter on the other hand know both about the dirty details of view controls and how to populate them.
*   The View Adapter binds to or overrides GUI specific events and translates these into application events.  Conversely the GUI adapter listens for relevant application events (e.g. model ‘I have changed’) and responds by updating the real GUI.
*   The View Adapter talks directly to the app/controller to get information.  Just as with the server adapter, this information is made available as an abstract chunk of information that is independent of the view.  Its up to the view or ther server to ‘render’ it appropriately.

For example, its the gui adapters that recieve events from e.g. the model, regarding things that change and need to be re-rendered. Anytime you switch GUI implementations, you put in place a different adapter - ensuring it hooks into and participates in the same eventing infrastructure.

The interface to your alternate gui adapters is, of course, the same.  

Its the gui adapters that recieve events from e.g. the model, regarding things that change and need to be re-rendered. Anytime you switch GUI implementations, you put in place a different adapter - ensuring it hooks into and participates in the same eventing infrastructure.

Typically the gui adapter listens for application events and updates the particular gui in a particular way.

### App to Model boundary

#### Model

The Model contains the raw domain classes and their relationships.  The model adapter interface is what the app deals with.

HexMvc favours a thin model approach where the majority of domain and business logic is kept in the  controller because

*   A thin model means you can rebuild a model rapidly as needed, for different implementations (see more info on this below).  You preserve the hard domain and business logic in the controller, which never changes.  The App and Controller are the core which never changes.
*   A centralised coordinated domain logic with undo/redo in a central place is something I’m trying out at this stage of my programming!

![](/patterns/images/hexmvc/image5.png)

Here you can see that when the application talks to the model, it talks via an adapter, via an interface.

#### Eventing in the model adapter

Similarly the model adapter is the where model ‘onchange’ application events are raised.  The model remains pure and simple.  The model’s “Add Some Entity” operation is implemented by the model adapter, which pokes the information into the pure model and then its the model adapter which raises the relevant onchange application notification event.

#### Model no longer at the bottom

It may seem strange to have the model as a sattelite rather than in the heart of the application.  But to put the model inside the app centre would to make the same ‘mistake’ as putting the model at the bottom of the traditional layer cake.  Its not necessarily wrong, its just inflexible and not in the spirit of pluggability.

#### Why have multiple model implementations?

This lets you switch out the model for a differently implemented model.  Now this may sound strange - swapping out a different model, as the model is typically a core part of an application and independent of any particular implementation.  But you need to be able to do this because I found that when implementing a ORM model which auto persists to a db, I had to annotate my classes with a certain syntax.  In my regular OO model, none of this syntax was needed. So I couldn’t use the same source code for my model - my model was not ‘pure’ enough. Implementation details were, rightly or wrongly, creeping into my pure model.  Further evidence of this was that my model implementations operated differently - my OO version had to work harder to store collections, whereas the ORM model had that functionality for free, due to the underlying SQL db.

Thus switching model implementations is no different to switching out gui implementations.

That’s why models are out on the ring and not in the centre - they are not reified but are just another application service.  This also means that a thin model approach is best, so that business logic is not duplicated, and can be kept in the core app - which is where I like it best these days anyway.

#### Different ‘back ends’ to a model

Model swappability is not to be confused with the idea of different ‘back ends’ to a model.  When you keep the model code the same and switch in different persistence or database backends - that is merely a nice feature of a particular model implementation.  Its an implementation which has some persistence flexibility.  But if I don’t want to conform to that particular e.g. Ruby ActiveRecord paradigm, with its particular model annotations and syntax - I don’t have to.  HexMvc allows me to swap in a totaly different model paradigm, with entirely different model syntax and annotations - its completely flexible.

### Model to Persistence boundary

As we said earlier, the model adapter provides the overall interface to the 'model subsystem'. The model adapter methods include model manipulation and access methods, as well as persistence methods. e.g.

![](/patterns/images/hexmvc/image7.png)

Behind the model adapter is the pure model and possibly a persistence object.  The persistence class is itself adapted behind an interface, so that different persistence techniques can be used.  The model adapter coordinates both the pure model and the swappable persistence class.

![](/patterns/images/hexmvc/image20.png)

The persistence class knows about the model, it has to, in order to get persistence data in and out of it.

The underlying real model class provides the model methods, obviously.

The underlying real persistence class provides the persistence methods.

#### Different persistence techniques

Typically you do not need an explicitly coded persistence object ‘backend’ if your model already uses the ORM pattern, and persistes automatically to a db.  And usually you can choose the db vendor through config files.

But if you are hand-crafting your own persistence backend mechanism which can be swapped for other persistence mechanisms, then the following design seems a reasonable approach.![](/patterns/images/hexmvc/image13.png)

#### Is an abstract persistence interface possible?

An alternative ‘swappable persistence backend approach’ I tried was to have the model communicate with an abstract persistence interface which you can swap - this prooved too hard. But again, if you can pull it off, that's fine. Just hide all this stuff behind the Model Adapter.

#### Switchable db persistence backends to a ‘particular’ model.

Here we are talking about a model that has swappable persistence backends.  As mentioned earlier, the idea of different persistence/implementation ‘back ends’ to a model is to be distinguished from swapping entire model implementations.  

*   When you swap model implementations your model code changes and has different code syntax annotations and implementation logic.
*   When you swap persistence back-ends, the model code stays the same and a configuration file lets you switch in different a persistence / database backend.

#### On file names and connection strings

The Model Adapter LoadAll() optionally does take a filename as a parameter e.g. LoadAll(‘mydata.txt’). This is fine for when the app wants to specify a persistence file to load/save to and is the common case catered for.  

If you are e.g. persisting to a database using a connection string, there is now more information to be specified than a mere filename e.g. database name, username, password etc.  We arguably should not contaminate the interface of ModelAdapter with all sorts of Persistence specific methods and parameters - after all, the ModelAdapter must be a straightforward interface that can be implemented by various persistence implementations - so that persistence implementations can be swapped in/out seamlessly.

The solution is to move this problem into the configuration/wiring/bootup stage where the Persistance object is instantiated and configured. For example, In the case of Sql database persistence, a Persistence class is not needed since the Model is auto persisted.  In this case the ModelSqlAdapter implements the required LoadAll methods by doing nothing. And the connection string etc. is done in the configuration.

### App to Server boundary

Server thread is like another gui layer, just write a different server adapter

![](/patterns/images/hexmvc/image22.png)

#### Careful with your call sequence

A slightly different call sequence is needed when providing a server interface to your app.

*   You can’t simply have the server subscribe to model onchange notifications, because the server must prepare and return a response immediately - at the end of the incoming request.  
*   You can’t can’t have the server raise an application event which the controller then picks up and acts on, because you typically want an immediate response so that a response object can be built.

This means the server must call directly into the controller and get the information it needs, and the controller must call directly into the model (adapter) to make changes and get results.  This is not strange, this is simply the web mvc approach.

![](/patterns/images/hexmvc/image19.png)

#### Its not necesssarily a synchronous / asynchronous issue

Note that this is not a synchronous / asynchronous issue - since most eventing whilst appearing semantically asynchronous is actually all implemented synchronously.  Its more an issue of incoming function calls on the server needing to do all their work within the same function call, whereas with an eventing approach, work is broken up across several function calls and returned using several function calls.

#### Implications

This all means that controller commands must be able to be invoked directly or invocable as a result of an event being raised.

Note that the model can still send its onChange notifications, its just that the server is not hooked up to them - but other subsystems might be.  So this allows for webpages to indirectly affect a desktop GUI view - neat.

![](/patterns/images/hexmvc/image3.png)

Example of using the REST api via a web browser.  The GUI updates itself simultaneously!

Aside: Threading introduces a bit of complexity, watch out for communication between threads, added a mutex method on the app, which can do anything needed

## Appendix

### Adapters

More elaboration on [HexMVC adapters](/patterns/hexmvc-adapters) and Adapter Patterns in general.

### Events

More elaboration on [HexMVC eventing](/patterns/hexmvc-eventing) and Event Patterns in general.

### HexMVC Source Code

Here is the directory of code used to develop the ideas in this article. It contains various versions of implementations, mainly in Python and .NET.  I need to document it sometime.

[https://github.com/abulka/pynsource/tree/master/Research/hexmvc](https://github.com/abulka/pynsource/tree/master/Research/hexmvc)

P.S. There is no reason it is located in the `pynsource` GitHub project directory - it just happened that way. It should be moved to its own repository.

## Presentation in 2012

I presented the HexMVC pattern to the Melbourne Patterns Group in 2012.

Re the talk - yeah it was full on 1.75 hours, 10 people - quite a complex topic.  I got some useful feedback re points that could be clearer etc. A couple of heart felt applauses and one guy came up to me and shook my hand with enthusiasm.   A few others didn't say as much as I hoped - I guess I was looking for a bit more feedback. I probably didn't pause enough and allow audience participation like I normally do - I just barrelled through the material a bit.  Its not easy, esp. - when presenting something complex and new-ish for the first time.

### Post Presentation Clarifications

Thanks for those who came and listened to my HexMvc talk last night. If anyone is interested in accessing and commenting on the google doc which will soon be an article on my website, please [email me](mailto:abulka@gmail.com) for access.  I was also hoping for some ‘peer review’ on my talk so please send me your thoughts if you get time - I would really appreciate the feedback.

Meanwhile here are some more considered responses to a few of last night’s questions:

#### Q: ‘What’s the distinction between the model and the model adapter’

A: The application should treat the model adapter as if it were the model. And as Stewart reminded me of my own point (thanks!), the adapter adds the application eventing so that the model is not contaminated with that eventing infrastructure stuff. The adapter also hides model specific operations that are done in different ways e.g. FindThings() lives in the model adapter and is implemented totally differently in the OO model adapter implementation vs. the SQL model adapter implementation (which utilises a fast sql query).  Yes, there seems to be some flexibility re whether you put model subsystem functionality into the model or its model adapter. Certainly business rules and exceptions I would put in the controller, and keep the model subsystem thin.

#### Q: ‘The server becomes just another view’

A: Yes - and yey - it all turns out to be very symmetrical.  Though because the services offered by the server REST api are available via http then you might access these services without any sort of browser/view - just trawling for data and making command calls into the application.  Perhaps this subsystem should be called ‘services’ not server?  Done, I’ve renamed it.

#### Q: ‘Why in the diagram does the App point to the GUI but in fact the GUI gets updated directly from the model via notifications’

A: Good point, my ‘arrows’ and their directions could have been made clearer.  The connection between the core app and the gui is one of composition and rarely used.  Its the eventing from view to controller and from model to view that forms 90% of the communication with the view.  My sequence diagrams showed this, but my overal structural diagram was, let us say, a bit more abstract and loose re this point.  Here is an updated diagram that should make things clearer:

![](/patterns/images/hexmvc/image11.png)

POST TALK THOUGHTS:

Look at the ideas of [‘obvious’ framework](https://www.google.com/url?q=http://obvious.retromocha.com/&sa=D&source=editors&ust=1644533497596031&usg=AOvVaw3G_JvaDfacMb4Ki6Z4oU07) which is based on Uncle Bob’s thoughts. It has an independent APP and a plugs/jacks approach.

Asked for more info in a [github post.](https://www.google.com/url?q=https://github.com/RetroMocha/obvious/issues/2&sa=D&source=editors&ust=1644533497596383&usg=AOvVaw1J3id81clTw9cpbH3F_u04)

