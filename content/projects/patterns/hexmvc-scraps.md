
# Scraps

### Renamings of pureMvc terms to "Adapter"

*   PureMvc uses the term one or more "mediators" in front of gui plumbing - all sitting behind the term "View"
*   PureMvc uses the term one or more "proxies" in front of model plumbing - all sitting behind the term "Model"
*   PureMvc talks about many "commands" objects which all sit behind the term "Controller"
*   The Application "facade" is the centre.

The problem with these terms are that is debatable that these things are really proxies and mediators etc.  I rename them Adapters.

The other problem in puremvc is that additional plug in parts of the architecture (which is not catered for anyway) need pattern names too, so by using the generic name Adapter we can have infinite numbers of Adapters composing a system.

Plus Adapters are more conducive to the idea of interfaces.  Adapters offer the same interface, whilst the behind the scenes implementation changes - this is the very essence of what an Adapter is.  And its the very essence of what an interface is, and thus the injecting of adapters that conform to some interface is a good thing to do.  

You can further break controller functionality into command objects if you wish.

        ModelSqlAdapter

         |

         |  SQLObject

         |   .

         |  /\_\\

         v   |  

        ModelSql

### single vs. multicast - a neat symmetry

Multicasting via object delegates, single, multiple.  Ocassionally use direct function injections too (which can be single or multicast too).

Three different types of multicast injection

*   Inject a single object to a var (destination expects an interface to be adhered to, doesn't care about the object)
*   Inject append to a multicast var (destination expects an interface to be adhered to, doesn't care about the object). Calls on the object's method are the same as if it was a single object.  The multicasting is hidden.  But same philosophy.  Thus we dispense with eventing and anything complex.  Its all just function calls on objects, where the object is anything that satisfies an interface/convention.
*   Inject just a function - not an object (e.g. see my random function).  

Sometimes, instead of a ring object calling a method on a delegate attribute (which is either a single object, multicast object or a function itself) you might just have the ring object call a method on a another object - where you know the nature of the other object. E.g. server calling an app method.  But even this is just calling a single object method that has been injected.  Its just that it looks like app.CmdBlah rather than observers.CMD\_BLAH in other words it amounts to the same thing.

\---

An event is a message sent by an object to signal the occurrence of an action. The action could be caused by user interaction, such as a mouse click, or it could be triggered by some other program logic. The object that raises the event is called the event sender. The object that captures the event and responds to it is called the event receiver.

In event communication, the event sender class does not know which object or method will receive (handle) the events it raises. What is needed is an intermediary (or pointer-like mechanism) between the source and the receiver. The .NET Framework defines a special type (Delegate) that provides the functionality of a function pointer.

A delegate is a class that can hold a reference to a method. Unlike other classes, a delegate class has a signature, and it can hold references only to methods that match its signature. A delegate is thus equivalent to a type-safe function pointer or a callback. While delegates have other uses, the discussion here focuses on the event handling functionality of delegates. A delegate declaration is sufficient to define a delegate class. The declaration supplies the signature of the delegate, and the common language runtime provides the implementation. The following example shows an event delegate declaration.


\# http://www.scribd.com/doc/53516831/22/Observer

Define a one-to-many dependency between objects so that when oneobject changes state, all its dependents are notified and updated automatically.

The .NET optimized code demonstrates the same code as above but uses moremodern, built-in .NET features. This example uses .NET multicast delegates which arean implementation of the Observer pattern. Delegates are type safe function pointers that have the ability to call a method. Multicast delegates are comprised of multiple methods that are called serially in the order in which they were added using the C# +=operator.

The Observer design pattern is one of two Gang-of-Four design patterns (the other is theIterator pattern) that have found their way, not only into the .NET Framework libraries,but also in the .NET languages themselves. When programming an ASP.NET or aWindows application you are most likely working with events and event handlers.Events and Delegates, which are first class language features, act as the subject andobservers respectively as defined in the Observer pattern.

The Observer pattern emphasizes good object-oriented programming in that it promotes loose coupling. Observers register and unregister themselves with subjects that maintain a list of interested observers. The subject does not depend on any particular observer, as long as the delegates are of the correct type for the event. The event and delegate paradigm in .NET represents an elegant and powerful implementation of the Observer design pattern.

\# http://en.wikipedia.org/wiki/Delegation\_(programming)

In object-oriented programming, a multicast delegate is a delegate that points to several methods.\[2\]\[3\] Multicast delegation is a mechanism that provides functionality to execute more than one method. There is a list of delegates maintained internally, and when the multicast delegate is invoked, the list of delegates is executed.

\# http://stackoverflow.com/questions/5583623/delegates-vs-observer-patterns

One advantage of the observer pattern is that if you have a large number even events that are generally always subscribed to by an interested party, then passing a single object into a method to subscribe to the events is much easier than subscribing to each event individually. With C#'s lack of specifying interfaces and methods for anonymous classes as can be done with Java, implementing the observer pattern becomes a bit more laborious so most opt for using events anyway.

Another benefit of the traditional observer pattern is that it handles better in cases where you need to interrogate the subscriber for some reason. I've come across this need with objects that pass a web-service boundary where there are problems with delegates whereas the observer pattern is just simply a reference to another object so it works fine as long as your serialization keeps integrity of references within the object graph like the NetDataContractSerializer does. In these cases it's possible to discriminate between subscribers that should be removed before making the service boundary based on whether the referenced subscriber is also within the same object graph.

\-----------------------

GUI event going to model and back again.

[https://docs.google.com/file/d/0B4pSq5nm19n4VEVaZm1YRTlRMW0yVDBEbWJyM2R1UQ/edit](https://www.google.com/url?q=https://docs.google.com/file/d/0B4pSq5nm19n4VEVaZm1YRTlRMW0yVDBEbWJyM2R1UQ/edit&sa=D&source=editors&ust=1644533497589481&usg=AOvVaw39H_137A7_IdD39EBTIr95)

\-----

# The roles

Its often useful to look at the roles/responsibilities that various classes and layers take on in a design.  HexMvc takes an ‘opinion’ on who does what - its not necessarily truth, its just a particular opinion.  

Furthermore, by looking at roles, it helps us get concrete about what each class/word means.  Being a ‘controller’ means different things to different people.  And depending on what decade’s technology you are using, ‘view’ can mean different things too - e.g. low level drawing code in the 60’s or perhaps windows forms filled with smart widget controls of the 90’s all the way to the modern browsers of the 2000’s.

\---

Actually ‘implementations of an interface’ are everywhere - not necessarily always an adapter.  There is something that is wrapped or delegated to, so there is a strong sense of adapter though.

\---

One insight at this point might be that wiring up one-to-one pointers and wiring up one-to-many pointers/observers in this way are just variations of the same thing.

Similarly, when you wire up the observers of an object, by adding them repeatedly using += to a list in a multicast variable, you are also doing dependency injection, except with a multicast flavour.

Its all just wiring.  Its just that some wires are one-to-one and others are one-to-many.

\---

and reeven Cannot use Model Adapter notifications for rendering server views because the same server method that received the request must prepare response.

With a server situation, you can use events as long as they are implemented synchronously.

After you dispatch the event you are blocked till the return stack of function calls exhausts itself, then you continue and reply with the response object.

you don't want model layer really knowing about the layer above.  model typically broadcasts very abstract notifications.  and you don't want lower later talking upwards.

its ok for gui adapter to know about the app/controller and use a very specific notification/function call because its a higher layer talking downwards.  Plus you have no choice, the controller must call functionality deeper down - whether that its raising an event or making a function call.

\------

Ironic that even though HexMvc 'flattens' out our layering and makes its a ring, we still don't want models knowing about the app.  Ok for gui's to know about the app though.  So there's an asymmetry in our symmetry!

\---------

My wx pure minimalist gui adapter is an example of a wrapping (compositional) adapter.

My wx architecture 3 gui adapter is an example of an inheritance based adapter.

\----

The Application is only really talking to and presuming that something implements an interface - e.g. a gui layer interface, which is supplied by one adapter or another, and implemented in whatever way each particular adapter sees fit (e.g. one gui framework or another).

\--
