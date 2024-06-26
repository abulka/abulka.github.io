---
title: "MVC-App Architectural Pattern"
linkTitle: "MVC-App Pattern"
date: 2019-01-04
type: docs
description: >
  MVC-App simply means "Model View Controller Application" - all four roles are necessary to any implementation.
tags: ["Design Patterns", "GUI", "MVC", "Controllers", "Javascript", "Observer", "Refactoring"]
---

## Introduction

This article describes the "MVC-App Architectural Pattern" which you can use to design your software applications, when you need to support a GUI.  It is not a framework, it is a small set of principles which let you build sane, modular GUIs in any language, using any off the shelf UI components.

> For the original, deprecated, MGM pattern which initially inspired this "MVC-App Pattern" pattern, see [MGM pattern]({{< ref "/patterns/mgm-pattern.md" >}})

## TodoMVC-OO

This is the classic Javascript [TodoMVC app](https://github.com/tastejs/todomvc) implemented **without a framework** 😄, simply using plain Object Oriented programming + a traditional MVC design pattern. 

Distinct, mediating `Controller` classes are the key to this implementation.

<img src="https://github.com/tastejs/todomvc-app-css/raw/master/screenshot.png" width="500">

Running demo [here](https://abulka.github.io/todomvc-oo/index.html).

---

## MVCA Architectural Pattern

This project fully implements the TodoMVC specification. It is implemented without a framework, using plain Object Oriented programming + the **MVCA** architectural design pattern:

Whilst the MVC (Model View Controller) pattern is commonly and glowingly referred to, implementations can vary widely. Most documentation on MVC, including the official [wikipedia article](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) is vague on definitions and details.  This TodoMVC-OO project uses the MVCA pattern (formerly the [MGM](docs_other/mgm.md) pattern) which is a clear and unambiguous interpretation of MVC, with the following key ideas:

- The **View** means a modern GUI framework, and therefore is usually already available to be used by the programmer.
- One or more **Controllers** mediate between the View and the rest of the Application, listening for GUI events. Nobody else knows about the View.
- The **Model** is traditional data, may contain some business logic, and may broadcast events when its attributes change.
- The **Application** owns the model(s), holds view state and contains some business logic methods.
- An **Eventing** system is needed, traditionally Observer pattern but the stronger decoupling and the proper event objects of the Publisher-Subscriber pattern is preferred.

Thus MVCA simply means "**M**odel **V**iew **C**ontroller **A**pplication" - all four roles are necessary to any implementation.

<!-- ![MVCA Architecture](https://github.com/abulka/todomvc-oo/raw/master/out/docs_other/plantuml/mvca-architecture-v2.svg?sanitize=true) 
    this version doesn't render the internal images (which are base64 encoded) due to "because it violates the following Content Security Policy directive:..."
    but serving the same image via github.io works ok.
-->

![MVCA Architecture](https://abulka.github.io/todomvc-oo/images/mvca-architecture-v2.svg?sanitize=true)

- The above diagram was generated semi-automatically from Javascript source code residing in GitHub using [GitUML](www.gituml.com).
- Click [here](https://abulka.github.io/todomvc-oo/images/mvca-architecture-v2.svg?sanitize=true) for more diagram detail as a .svg and the ability to zoom. 
- View this actual [diagram 181](https://www.gituml.com/viewz/181) on GitUML.

## MVCA In Detail

Let's go through the four parts of the MVCA pattern, which is precisely adhered to by this TodoMVC-OO implementation. Actually there is a fifth important part - the eventing system - which glues it all together - let's look at the Model first.

### Model

The **Model** is traditional, may contain some business logic, and may broadcast events when its attributes change.

By traditional, I mean the Model does not know about anything else except perhaps other models. Its the core model of your data, the domain of the what the application is all about. In the case of the Todo application, it is a collection of Todo items, which can be marked completed. 

```javascript
class TodoItem {
    constructor(title, id, completed) {
        this._title = title == undefined ? "" : title;
        this._completed = completed == undefined ? false : completed;
        this.id = id == undefined ? util.uuid() : id;  // no getter/setter needed
    }

    get title() {
        return this._title;
    }

    set title(v) {
        this._title = v;
        this.dirty()
    }

    get completed() {
        return this._completed;
    }

    set completed(v) {
        this._completed = v;
        this.dirty()
    }

    get as_dict() {
        return {
            id: this.id,
            title: this.title,
            completed: this.completed
        }
    }

    delete() {
        notify_all("deleted todoitem", this)
    }

    dirty() {
        notify_all("modified todoitem", this, {during_load: false})
    }
}
```

The Model is usually broken into many smaller interconnected models in an attempt to reflect the real world domain being implemented as software. The Model can be implemented as mere objects in memory or a full-fledged database model, or a [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping) mapping between the two.  In our case, we have a pure memory model, which gets persisted into local browser storage as JSON.

You will find that some 'model' concepts are more about how the information is presented in the GUI, thus I recommend these are kept as attributes of the Application class, and referred to as the *view state* or *view model*. The attribute `filter` is an example of such view state.  The Application class can also hold collections of models which is what we do in this project:

```javascript
class Application {
    constructor(config) {
        this.todos = []  // model collection
        this.filter = 'all'  // view model, options are: 'all', 'active', 'completed'
        ...
    }
```

The model can be fat or thin - a fat model will have more business logic in the model. A thin model will most business or application logic in the Application class, treating the model as just data structures.

Finally, the Model needs to participate in the internal eventing system. Whenever an attribute changes it should send out a notification event - this is why most attributes of our `TodoItem` class are accessed via getter and setter methods. For example setting `title` or `completed` will trigger an internal event to whoever may be listening. This internal eventing mechanism is how Controllers know to update the GUI with updated model information.

### View

The **View** means a modern GUI framework, and as such is already available to be used by the programmer. 
In our case, our modern GUI framework is the browser DOM which you can build in HTML:

```html
<input id="toggle-all" class="toggle-all" type="checkbox">
```

then Controllers use the GUI native eventing system to listen for interesting events

```javascript
this.gui.$toggle_all.on('change', handler)
```

### Controller

The Controller is the most interesting aspect of MVC.

In many software designs, the Controller isn't necessarily a single thing. A bunch of stray GUI event handler functions are in reality, part of the 'controller role'. Code that copies data from the model into the GUI/DOM is also part of the Controller role.
I feel the challenge of GUI architectures is to tame the role of Controller into some semblance of coherance and symmetric organisation. Which is why MVCA prescribes creating Controller classes.

In TodoMVC-OO we have a Controller class `ControllerTodoItem` and instantiate one per TodoItem model instance. That's arguably a lot of controller instances, but this approach allows fine grained updating of the DOM. In contrast, the Jquery version of TodoMVC rebuilds the entire todo DOM on each refresh - something that might become inefficient for non-toy apps.

In TodoMVC-OO we have a Controller class `ControllerHeader` for looking after the header part of the GUI and `ControllerFooter` for looking after the footer area, which is where the `filter` buttons are and the count of uncompleted todo items is displayed. The number of Controllers you create is up to you: one Controller per GUI element for fine grained updates, a more relaxed approach of one Controller per related group of GUI elements (my preference) or arguably even one Controller for all GUI elements! I go into more academic detail on this topic in my [MGM](docs_other/mgm.md) pattern paper.

By clearly defining what a mediating Controller is, and organising our app into different sensible controllers, we tame our design and prevent it from turning into spaghetti. 

- View events *only* talk to Controllers:
    - View events ('gui events' e.g. via `.on('click', ...)`) go to one or more Controllers.
    - Controllers update the View, usually in reponse to an 'internal event' notification.

and
- The Controller talks to the rest of the system:
    - Accesses App view state.
    - Calls App business logic methods.
    - Modifies the Model directly.

and
- The Controller listens for 'internal events' broadcast from Model & App.

Whilst that may seem like a lot to understand, its basically saying Controllers talk to the GUI - nobody else does. Controllers then call into the rest of the system to get things done

Importantly, we must resist putting business logic into the Controller, simply let the controller call the Application to do what needs to be done. The Controller should do the minimal possible work, mediating and translating between the View and the rest of the system (the App + Model).

### Application

The role of the Application is also important and often overlooked/undocumented. The Application owns the Model, and looks after persisting it. The Application can listen for internal Model events.

Whilst it is fine to wire Controllers directly to model instances, you will also need the Application to hold "view state" e.g. like the state of the active "filter" in this Todo application.  The Application is a centralised class, a kind of hub - to hold higher level business logic and more complex model manipulations. The Application class's functionality can of course be composed of smaller pieces as software grows more complex but a class called `Application` should always still exist.

### Eventing System

Eventing is an important consideration in decoupling models from controllers, and to facilitate abstract communication between objects.

Two eventing systems should be distinguished:
- **GUI native**: The native eventing system of the GUI Framework e.g. DOM `.on('click', ...`
- **Internal**: Your choice of an application system wide eventing system e.g. Publish-Subscribe e.g. `document.addEventListener("hello", (event) => { ... })`

Both eventing systems are used in the TodoMVC-OO implementation. As you can see in the diagram above, DOM eventing reaches the Controllers, but no further. The remaining eventing is internal.

Here is a [Literate Code Map](https://github.com/abulka/lcodemaps) of the event flow of TodoMVC-OO. Events are reified as coloured objects, each different event gets a different colour. 
![todomvc event flow](https://raw.githubusercontent.com/abulka/todomvc-oo/master/out/docs_other/plantuml/todomvc-oo-event-flow-gituml-134.png)
*TodoMVC-OO event flow.*

- The above diagram was generated semi-automatically from Javascript source code residing in GitHub using [GitUML](www.gituml.com).
- Click [here](https://abulka.github.io/todomvc-oo/images/todomvc-oo-event-flow-gituml-134.svg) for more diagram detail as a .svg and the ability to zoom. 
- View this actual [diagram 134](https://www.gituml.com/viewz/134) on GitUML.

The eventing pattern depicted here is [Publisher-Subscriber](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) where real event objects are 'broadcast' into the ether/event bus/system/whatever - allowing any code in the system to subscribe and respond - the point is, the code emitting the event does not have references to receiver object/methods.

The Javascript built in Publisher-Subscriber eventing approach is more flexible and powerful than the [Observer](https://en.wikipedia.org/wiki/Observer_pattern) pattern since the Observer pattern *requires observers to know about* and subscribe to Subject objects, which is not always possible or convenient. More dicussion on the differences can be found [in this article](https://hackernoon.com/observer-vs-pub-sub-pattern-50d3b27f838c) and on [Stackoverflow](https://stackoverflow.com/questions/6439512/difference-between-observer-pattern-and-event-driven-approach). Thus we use Publisher-Subscriber eventing (event name → object method) rather than the traditional Observer pattern (object → object) approach. 

I used to be a fan of the traditional Observer pattern but in my later years find the Publisher-Subscriber pattern to be simpler and more powerful - plus Publisher-Subscriber is built into Javascript you simply `document.addEventListener("hello", (event) => { ... })` to listen and `document.dispatchEvent(new CustomEvent(event_name, { detail: {from: from, data: data } }))` to notify all.

The Javascript built in Publisher-Subscriber eventing system is used as the internal eventing system of this TodoMVC-OO implementation.


## Application Bootstrapping

To get things running, some bootstrapping code will create an instance of the Application which in turn creates all the Controllers and loads the Model. 
The bootstrapping in TodoMVC-OO is done in `app.js` which creates an instance of Application which is defined in `application.js`.

```javascript
(function (window) {
    let config = {...}
    new Application(config)
})(window);
```

Notice that a `config` object with a list of callback methods is passed into the Application. 

Giving the Application class knowledge of individual Controller classes and all the GUI view elements they need is arguably contaminating the Application class with too much GUI view and Controller knowledge. 

The solution I use is to pass the Application a `config` object which contains a bunch of callbacks. Each callback function will magically create a Controller instance, wired to look after its GUI elements. Each callback function hides, within itself, references to the DOM - which we don't want the Application to have. In this way, the bootstrapping code and the Controller code are the only parts of the architecture that know about the View specifics (which we want to restrict).

Thus whenever the Application needs to instantiate a Controller (e.g. each time a TodoItem is created) it calls a `config` callback function.
Another example is during bootup - some permanent Controllers need to be created, like the Controller looking after the header area, so the Application calls 
`this.callback_config.cb_header(this)` which creates an instance of the `ControllerHeader` wired to `$('.new-todo')` and `$('.toggle-all')`.  The Application only needs to know the callback function names and thus remains pure.

Notice in the `config` object below that each callback refers to the view through JQuery syntax e.g. `$('ul.todo-list')` and passes these references into the contructor of the Controller:

```javascript
let config = {
    // Callback to create the todo item controllers - are added as needed

    cb_todo: function (app, todo) {
        new ControllerTodoItem(
            app,
            todo,
            { $todolist: $('ul.todo-list') }
        )
    },

    // Callbacks to create the permanent controllers

    cb_header: function (app) {
        new ControllerHeader(
            app,
            {
                $input: $('.new-todo'),
                $toggle_all: $('.toggle-all')
            }
        )
    },
    cb_footer: function (app) {
        new ControllerFooter(
            app,
            {
                $footer: $('footer'),
                $footer_interactive_area: $('.footer')
            })
    }
}
```

Of course the Controller itself will have further references to View DOM elements, however these references should be based on searching *within* the outer DOM element passed to the Controller - thus achieving some degree of 'component-isation' and re-use. For example the same Controller could be used to look after different DOM elements with different element id's.

## TodoMVC-OO Conclusion

This project fully implements the TodoMVC specification and is implemented without a framework, using plain Object Oriented programming + MVCA architectural design pattern, as described above.

Running demo [here](https://abulka.github.io/todomvc-oo/index.html).

### Improvements

In this implementation, I notice that footer renders too early rather than right at the end of the initial render. Its just a subtle flash of the footer when the page is initially redrawn, but I'd like to correct this.

---

### Resources

- Official [TodoMVC project](http://todomvc.com/) with other TodoMVC implementations (e.g. Vue, Angular, React etc.)
- [TodoMVC-ECS](https://github.com/abulka/todomvc-ecs) - My "Entity Component System" implementation of TodoMVC
- [MVCA](https://abulka.github.io/gui-showdown/main_mvca.html) another example of an app implemented using the MVCA architecture (Javascript, open source)
- Andy's [GUI Showdown](https://abulka.github.io/gui-showdown) The same application, implemented in various ways - which is better, cleaner, more understandable etc. (Javascript, open source)
  - OO
  - MVCA
  - ECS
  - PLAIN
  - VUE
- [MGM](docs_other/mgm.md) pattern (older version of MVCA, presented at a Patterns Conference)
<!-- - [Used by](https://github.com/abulka/todomvc-oo) -->
<!-- - [Website](https://www.gituml.com/editz/134) -->
<!-- - [Blog](https://www.gituml.com/editz/136) -->
<!-- - [FAQ](https://www.gituml.com/editz/136) -->

- I'm recently loving [Flet](https://flet.dev/docs/) which lets you build Flutter GUIs using Python.  However I miss the reactivity of Vuejs and even Flutter. So I put together a quick solution - instead of imperitively allowing the Flet UI control event callbacks e.g. on_click, to update the UI directly, we update a reactive model, which in turn updates the Flet UI.  A full example is at https://github.com/abulka/freactive-python.  It shows how such a simplified architecture can (even without the Observer classes) can achieve similar functionality to the TodoMVC-OO architecture.

### Diagramming

- [GitUML](https://www.gituml.com) diagramming used for this project
- [Literate Code Mapping](https://github.com/abulka/lcodemaps) diagramming used for this project
<!-- - [Medium article]()  (coming in Apr 2020) -->

<!-- ### Support

- [Stack Overflow](http://stackoverflow.com/questions/tagged/MVCA)
- [Twitter](http://twitter.com/unjazz) -->

## Credit

Created by [Andy Bulka](http://andypatterns.com)

Note: This project is not not officially part of the [TodoMVC project](http://todomvc.com/) - as it is does not use a MVC framework library, nor does it meet the criterion of "having a community" around it.  On the other hand, perhaps a pattern is equivalent enough to a framework - after all there is a plain Javascript TodoMVC implementation officially available using ad-hoc techniques. Plus, there has been a "community" around the Object Oriented MVC pattern for decades now - hasn't there? 😉



