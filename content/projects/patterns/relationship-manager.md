
---
title: "Relationship Manager - Design Pattern"
linkTitle: "Relationship Manager"
date: 2001-08-04
description: >
  A central mediating class which records all the one-to-one, one-to-many and many-to-many relationships between a group of selected classes. Basically a cheap object relational database.
---

![](http://www.andypatterns.com/files/62371233035718bgDSC1367.jpg)

## Abstract

A central mediating class which records all the one-to-one, one-to-many and many-to-many relationships between a group of selected classes. Classes that use a Relationship Manager to implement their relationship properties and methods have a consistent metaphor and trivial implementation code (one line calls). In contrast - traditional "pointer" and "arraylist" techniques of implementing relationships are fully flexible but often require a reasonable amount of non-trivial code which can be tricky to get working correctly and are almost always a pain to maintain due to the detailed coding and coupling between classes involved.

## The Official Pattern

<iframe src="/files/andybulkarelationshipmanagerpattern.html" name="frame1" scrolling="yes" frameborder="yes" align="center" height = "842px" width = "800">
</iframe>

## Usage and Theory

Relationship Manager - Usage and Theory

This page documents how to use my implementations of the Relationship Manager pattern. RM Relationship Manager has been implemented in Python, Boo (.net), C# (.net) and Java.

Included are examples of how to code using relationship manager, covering all possible modelling scenarios (e.g. one to one, one to many etc.).  See also the Boo implementation page for a fully worked out example of a person and order class.  The Java download also has a real world example implemented.

I also spend some time describing, in more theoretical terms, the scope of the relationship manager approach, in other words - what are all the possible relationships between objects and how RM can model them.

### Its a Object Relational Database

In a sense, an [Object Database](https://en.wikipedia.org/wiki/Object_database) is an implementation of the RM pattern. 
The *intent* of the RM pattern is lighter weight, to replace the wirings between objects
rather than acting as a huge central database.

Here is a very simple implementation of RM in Python:

```python
class RelationshipManager:
  def __init__(self):
      self.Relationships = []
  def AddRelationship(self, From, To, RelId=1):
      if not self.FindObjects(From, To, RelId):
        self.Relationships.append( (From, To, RelId) ) # assoc obj
  def RemoveRelationships(self, From, To, RelId=1):
      if not From or not To:
          return
      lzt = self.FindObjects(From, To, RelId)
      if lzt:
          for association in lzt:
              self.Relationships.remove(association)
  def FindObjects(self, From=None, To=None, RelId=1):
      resultlist = []
      match = lambda obj,list,index : obj==list[index] or obj==None
      for association in self.Relationships:
          if match(From,association,0) and match(To,association,1) and RelId==association[2]:
              if From==None:
                  resultlist.append(association[0])
              elif To==None:
                  resultlist.append(association[1]) 
              else:
                  resultlist.append(association)
      return resultlist
  def FindObject(self, From=None, To=None, RelId=1):
      lzt = self.FindObjects(From, To, RelId)
      if lzt:
        return lzt[0]
      else:
        return None
  def Clear(self):
      del self.Relationships[0:]
```

and you could use it like this:

```python
import unittest, random

class TestCase00(unittest.TestCase):
    def setUp(self):
        self.rm = RelationshipManager()
    def checkBasic00(self):
        self.rm.AddRelationship('a','b')
        self.rm.AddRelationship('a','c')
        assert self.rm.FindObjects('a',None) == ['b','c']
        assert self.rm.FindObjects(None,'a') == []
        assert self.rm.FindObjects(None,'b') == ['a']
        assert self.rm.FindObjects(None,'c') == ['a']
    def checkBasic01Singular(self):
        self.rm.AddRelationship('a','b')
        self.rm.AddRelationship('a','c')
        assert self.rm.FindObject(None,'b') == 'a'
        assert self.rm.FindObject(None,'c') == 'a'
        assert self.rm.FindObject('a',None) == 'b' # could have been 'c' - arbitrary
```

For the full Python 3 implementation see 
https://github.com/abulka/relationship-manager

Hoping to get a `pip` package sometime soon.

### What's it good for?

What is Relationship Manager good for?

> I'd appreciate an 'how to use' example to get a quick / better idea on what it's useful for when programming  
  
The basic idea with relationship manager is that it is like a dictionary, which maps relationships between two things, be they object references or strings or whatever. In my examples I usually use strings, though object references are commonly used too, in order to  
map relationships between object instances.

The benefit over a dictionary is that you can have multiple mappings  
e.g.
```
a -> 1  
a -> 2  
a -> 3
```

Then you can ask what 'a' points to and get the result `[1, 2, 3]`.
You can also ask what is pointing to 3, and get the result `a`.
  
One common use of this technology is to do all your wiring between objects using a relationship manager, thereby saving yourself having to implement your own one to many lists and having to maintain fiddly backpointer logic etc. So you still have e.g. an `AddOrder(o)` method on your e.g. `Person` class...its just that you implement the method using a one line call to the relationship manager - simple!  e.g.

```python
class Person:  
    def AddOrder(o):  
        RM.addRelationship(self, o, 'personToOrderRelationship')  
    def GetOrders():  
        return RM.findObjectsPointedToByMe(self,'personToOrderRelationship') 
```

There is a bit more of a tutorial code sample in the post [http://tinyurl.com/9xz5m](http://tinyurl.com/9xz5m)

### Modelling relationships

What methods do I put where when modelling relationships?

I recommend that you use the [templates](#UsageTemplates) table to figuring out what methods to put where for each type of classic relationship you want to model.  For example, to implement a **one to many** relationship between two classes X and Y, you would use template 4 or 5 (use the latter if you want bidirectionality)

## Documentation

Note that the C# and Java implementations have a slightly cleaner set of methods and a few extra methods - and also use a nice interface to talk to.  The method names are substantially the same though.

### C# and Java API

```java
public enum Cardinality  
{  
    OneToOne,  
    OneToMany,  
    ManyToOne,  
    ManyToMany  
}

public enum Directionality  
{  
    UniDirectional,  
    DirectionalWithBackPointer,  
    DoubleDirectional  
}

interface IRelationshipManager {
  void AddRelationship(object fromObj, object toObj, string relId);  
  void AddRelationship(object fromObj, object toObj);  
  void EnforceRelationship(string relId, Cardinality cardinality);  
  void EnforceRelationship(string relId, Cardinality cardinality, Directionality directionality);  
  IList FindObjectsPointedToByMe(object fromObj, string relId);  
  object FindObjectPointedToByMe(object fromObj, string relId);  
   IList FindObjectsPointingToMe(object toObj, string relId);  
  object FindObjectPointingToMe(object toObj, string relId);  
  void RemoveRelationship(object fromObj, object toObj, string relId);  
  void RemoveAllRelationshipsInvolving(object obj, string relId);  
  int Count();  
  int CountRelationships(string relId);  
  void Clear();  
  bool DoesRelIdExistBetween(object fromObj, object toObj, string relId);  
  IList FindRelIdsBetween(object fromObj, object toObj);
}
```

### Abstract API

| Return Type            | Function Name           | Short-hand |
|-------------------|-----------------|------|
| void | addRelationship(from, to, id) | R(f,t) |
| void | removeRelationship(from, to, id) | NR(f,t) |
| List | findObjectsPointedToByMe(from, id) | PS(f) |
| List | findObjectsPointingToMe(to, id) | BS(t) |
| void  | EnforceRelationship(id, cardinality, bidirectionality) | ER(id, c, bi) |
| Object | findObjectPointedToByMe(fromMe, id, cast) | P(f) |
| Object | findObjectPointingToMe(toMe, id, cast) | B(t) |
| void | removeAllRelationshipsInvolving(object, id) | NRS(o) |

For example `Object` is just one of *your* objects which you added with `addRelationship()`.

Re `cast` that's just in case you need to cast to a type. This might have been possible in the [boo language](http://boo-language.github.io/) for .NET (which is now dead). Please adapt to your language as needed. Dynamic languages don't need casting.


### Enforcing Relationships

You can enforce relationships. For example EnforceRelationship() works like this:

```
ER("xtoy", "onetoone", "directional")
```

The relationship is registered as being one to one and directional, so that e.g. when you add a second relationship between the same two objects the first relationship is automatically removed - ensuring the relationship is always one to one. Alternatively, the implementation could raise an exception (go into the source and change it if this is what you need).

### Finding just one object

The pair of find methods `FindObjectPointedToByMe()` and `FindObjectPointedToByMe()` only find _one_ object (even though there may be more), and cast it to the appropriate type.  This is a commonly used convenience method - the more painful way would be to use `FindObjectsPointingToMe()` and just grab the first object from the returned list.
Exactly which object is found is undefined, but would typically be the first one added.

### Relationship Id

What to use as the Relationship Id?

This is either an integer or a string.  I have chosen to use a string in the C# and Java implementations, since you can describe relationships easily in this way rather than having to map from an integer back to some meaningful description.

```
RM.addRelationship(fromObject, toObject, relationshipId)
```

will raise an exception if relationshipId is an empty string.  

All other functions (except for addRelationship) can pass either an empty string or "\*" as the relationshipId, which means you are searching for any relationship at all.  You would usually only want to do this if there is only _one_ relationship between class X and class Y, then your P and NR calls can specify "\*" as the relationshipId in order to match any relationship between these two objects.  Alternatively, you can use relationship manager's overloaded versions of all its routines (except for addRelationship) which don't take a relationshipId where relationshipId defaults to "\*".

## Table of Templates

### Classic "relationship scenarios"

How to implement relationships using sets of Relationship Manager methods

Here is a list of classic "relationship scenarios" (e.g. one to one, one to many etc.) and how to implement them using the Relationship Manager API.

The right hand side of the below table shows python code using calls to RM (relationship manager) using the shorthand notation for the function names.  For long hand names just substitute in the appropriate name e.g. instead of RM.R() you would call rm.AddRelationship().

Note: The method names below are just suggestions. Normally you would use better method names that pertain to your application domain.

* Instead of `.addY(y)` you might have `addOrder(order)`.
* Instead of `.getX()` you might have `getCustomer()`.
* Instead of `getAllY()` you might have `.getOrders()` etc.

### Table

This table uses the [Shortened API](#abstract-api) calls for brevity. E.g. `RM.ER` means call `EnforceRelationship` on your Relationship Manager instance.

{{< content/rm_api_possibilites >}}


Code which supports the ideas in the theory above is provided in this [python program](http://www.atug.com/downloads/pythonRmProof.zip) or simply view the code and results as a [pdf](http://www.atug.com/downloads/pythonRmProof.pdf).

# More Detail on each template

Here are some further notes on using each template.  I don't cover each variation, so see the above table for the complete list of possibilites.  I also use slightly different method names here just in case you don't like the `setX` and `setY` syntax I have been using.

## One to one

![](http://www.atug.com/andypatterns/images/rm_the1.gif)

Class X points to class Y.

### Methods on class X

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void  | setPointer(y) | `R(x, y, "xtoy")` |
| Y     | getPointer()  | `P(x, "xtoy")` |
| void  | clearPointer() | `NR(x, y, "xtoy")` |

### Methods on class Y

None.

### Notes:

1.  The clearPointer() implementation needs to get a reference to **y** in order to call `NR(x,**y**,...)`.  The implementation can either call its own `getPointer()` method to get a reference to **y**, e.g. clearPointer() would be implemented as `NR(x, getPointer() ,"xtoy")`.  Alternatively the getPointer() implementation can make a second call to relationship manager itself e.g.  `clearPointer()` would be implemented as `NR(x, P(x,"xtoy"),"xtoy")`.
2.  If there is only _one_ relationship between class X and class Y, then your P and NR calls can specify "\*" as the relationshipId in order to match any relationship between these two objects.  Alternatively, you can use the overloaded P and NR calls which don't take a relationshipId at all. _\[not sure if this note on overloaded methods is relevant to the latest C# and Java implementations\]_

![](http://www.atug.com/andypatterns/_themes/canvas/acnvrule.gif)

## One to one, with back pointer

![](http://www.atug.com/andypatterns/images/rm_the2.jpg)

Class X points to class Y.   
Class Y can deduce a back pointer to class X.

### Methods on class X

Same as one to one, i.e.

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void | setPointer(y) | `R(x, y, "xtoy")` |
| Y     | getPointer()  | `P(x, "xtoy")` |
| void  |clearPointer() | `NR(x, y, "xtoy")` |

### Methods on class Y

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| X | getBackPointer() | B(y, "xtoy") |

_and optionally setter methods ..._

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void | setBackPointer(x) | `R(x, y, "xtoy")`<br> _or simply call `x.setPointer(this)`_ |
| void  | clearBackPointer() | `NR(x, y, "xtoy")`<br>_or simply call `x._clearPointer()`_ |

### Notes:

1.  An implicit back-pointer (i.e. a back reference) is always deducible, when using a relationship manager, thus instead of wiring up an explicit pointer relationship as a back-pointer , you can implement a back-pointer using an implicit back reference on an existing relationship (in this case the "xtoy" relationship) instead. i.e. see  `getBackPointer()` on class Y.
2.  Notice all the relationshipId's in this example (in both classes) are the same viz. "xtoy"
3.  In implementing X methods, whenever you need a reference to **y**, just call this.`getPointer()`.  Similarly, in implementing Y methods, whenever you need a reference to **x**, just call this.getBackPointer().  See discussion on this _above_.
4.  If you chose to have backpointer setter methods on class Y, you need not necessarily call the wrapping methods on X in order to implement them e.g. `setBackPointer(x)` is implemented by simply calling `x.setPointer(this)` (although it is recommended that you do, since X is the 'controlling' class for the relationship - see [Martin Fowler 'Refactorings'](https://martinfowler.com/books/refactoring.html) p. 197 "Change Unidirectional Association to Bidirectional").  You could alternatively call the relationship manager directly, thus setBackPointer(x) becomes a call to `R(x, y, "xtoy")` and `clearBackPointer()`  becomes a call to `NR(x, y, "xtoy")`.
5.  If you are trying to enforce a one to one relationship, then you should stricltly speaking, remove any exising relationship between a1 and b1 before creating a relationship between a2 and b1.  However relationship manager will remove the previous relationship for you automatically. See discussion on this behaviour. 

### Discussion on back pointers

One of the benefits of the relationship manager pattern is that *you don't have to explicitly wire up and maintain back-pointers*.  Once you add a pointer relationship, you get the back pointer relationship available, for free.  And once you delete the pointer relationship, the back-pointer relationship goes away automatically too.

However if you want to delete or change the back-pointer relationship (from Y's perspective) then you must talk to the relationship manager in terms of the relationship "xtoy".  If you imlplement  the back-pointer relationship as a different relationship, with a different relationshipId, then you will fall prey to the same out of synch problems that traditional spaghetti wiring techniques often fall prey to.  The trick is to treat the relationship as two sides of the *one relationshipId*.

![](http://www.atug.com/andypatterns/_themes/canvas/acnvrule.gif)

## One to many

 ![](http://www.atug.com/andypatterns/images/rm_the3.gif)

Class X points to many instances of class Y.

### Methods on class X

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void | add(y) | `R(x, y, "xtoy*")` |
| list | getAll() | `PS(x, "xtoy*")` |
| void  | remove(y)  | `NR(x, y, "xtoy*")` |

### Methods on class Y

None.

### Notes:

1.  Notice that the relationshipId has a `*` symbol in it.  This means that you can add multiple relationships of that type without the relationship manager removing the prior relationship. Not sure which of my Relationship Manager implementations auto-support this - its been so long ago...

## One to many, with back pointers

![](http://www.atug.com/andypatterns/images/rm_the4.gif)

### Methods on class X

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void | add(y) | `R(x, y, "xtoy*")` |
| list | getAll() | `PS(x, "xtoy*")` |
| void  | remove(y)  | `NR(x, y, "xtoy*")` |

### Methods on class Y

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| X | getBackPointer() | `B(y, "xtoy*")` |

_and optionally setter methods ..._

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void | setBackPointer(x) | `R(x, y, "xtoy*")`<br> _or simply call `x.setPointer(this)`_ |
| void  | clearBackPointer() | `NR(x, y, "xtoy*")`<br>_or simply call `x._clearPointer()`_ |

* * *

# Some More Deep Theory

Skip this section if you just want to get on with coding... 😉

### All possible relationship scenarios?

When looking at all the possibiliteis of relationships between two classes, you get **one to one, one to many, many to one** and **many to many**.  You have the variations generated by whether the relationships are **directional** or **bi-directional. ** Finally, you have variations of whether you put methods on one class or the other - for example, you could omit methods on e.g. the rhs. class, or you could go to the other extreme and provide a full range of methods on the rhs. class. 

Note that some combinatorial possibilities do not make sense and are left out of the table below. 

*   `S` means **singular** **API** - this makes sense for one to one relationships, or the many side (ironically) of one to many relationships.  It consists of methods like **get, set, clear**.
*   `P` means **plural** **API**\- this makes sense where you are dealing with collections, a _many_ concept.  It consists of methods like **add, remove, getall**.
*   `-`   means no methods relating to the relationship have been implemented on that class.

Blank cells mean "not applicable".

| [Scenario](#UsageTemplates) (see above) | directional  | bi-directional |
|-----------|---------------------------|---------------------------|
|           | _one to one_<br>`1 --> 1`  | _one to one_<br>`1 <--> 1`  |
| #1.       | S       \-                 |                           |
| #2.       | \-       S                |                           |
| #3.       |                           |   S        S              |
| #3A.<br> (composite, pointing to self)| S | |
|           | _one to many_<br>`1 --> *`  | _one to many_<br>`1 <--> *`  |
| #4.       | P      \-                  |                           |
| #5.       |                           | P       S                 |
|           | _many to one_<br>`* --> 1`  | _many to one_<br>`* <--> 1`   |
| #6.       | \-       P                |                           |
| #7.       |                           | S         P               |
|           | _many to many_<br>`* --> *` | _many to many_<br>`* <--> *` |
| #8.       | P      \-                  |                           |  
| #9.       | \-      P                 |                           |
| #10.      |                   |    P       P                      |

_An attempt at mapping the theoretical relationship possibilities_

The above table shows all the possible relationship scenarios between two classes.  It indicates various possibilities as to the methods you can add to either class.  For example a one to many relationship where the "many" side has no need of any methods to see who is pointing at it, would use template 4.

### Interesting Addendem

<iframe src="/files/rm-one to one and many maps 01.html" name="frame1" scrolling="yes" frameborder="yes" align="center" height = "842px" width = "800">
</iframe>

### Bi-directional implementations of directional relationships

We must distinguish between a relationship that in its meaning, goes both ways, and a relationship which goes one way only.  And furthermore, implementationally, you can have RM methods on one class only, on the other class only, or on both classes.  The meaning of the relationship and the implementation (methods to create and look up those relationships) are two different things!

Thus when you put an API (relationship manager methods) on both classes this might seem to imply that you are implementing bi-directionality.  However this does not mean that the "relationship" points in both directions.  The meaning of the relationship is often in one direction only, and the existence of methods on both classes merely gives you a convenient way of querying the relationships that exist.

Thus the same relationship id should be used in both classes e.g. `"xtoy"` (notice the sense of directionality is built into the name of the relationship!), even though it is a bidirectional relationship in the sense that there is an API on both classes allowing each class to find the other class.  In the following implementation of a one to many relationship between class X and class Y, notice the same relationship id `"xtoy"` must be used in both classes.

```python
class X:  
    def __init__(self):        RM.ER("xtoy", "onetomany",   
                                     "bidirectional")  
    def addY(self, y): RM.R(self, y, "xtoy")  
    def getAllY(self):  return RM.PS(self, "xtoy")  
    def removeY(self, y):      RM.NR(self, y, "xtoy")  
    

class Y:  
    def setX(self, x): RM.R(x, self, "xtoy")  
    def getX(self):     return RM.P(self, "xtoy")  
    def clearX(self):          RM.NR(self, self.getX(), "xtoy")  
```

### More on Directionality and Backpointers

Relationships are here considered directional.  So when you add a relationship with R(a,b) then **a** points to **b**.

Using a relationship manager you can get it deduce who is pointing at you, which means you get 'back-references' for free.  However being able to determine a back-reference doesn't mean that the model you are building _officially_ has this pointer connection.  Thus we must distinguish official pointers from deducible back references / back pointers. 

To find what **a** points to, use P(a).  To find out what is pointing at **b**, use B(b).  

| API Short-hand | Description |
|:----------:|----------|
| P(a)      | Find Pointer From |
| B(b)	    | Find Back Reference To      |

Thus, just because you point at something doesn't mean it is officially pointing back at you. But, using a relationship manager you can deduce who is pointing at you.

So if...

| API Short-hand | Comment |
|:----------:|----------|
| R(a,b)     | if you make **a** point to **b** |

then...

| API Short-hand | Comment |
|:----------:|----------|
| P(a) == b   | **a** points to **b** |
| B(b) == a   | the thing pointing at **b** is **a** |
| P(b) == null   | **b** doesn't point at anything<br> _(crucial distinction - see above line)._ |
| B(a) == null   | nothing is pointing back at **a** |

### More on Backpointers

Backpointers are pointers on the "receiving end" of a relationship, so that the receiving object knows who is pointing at it.  For example when a Customer places an Order, it might be convenient for any particular order instance to know which customer ordered it.  I think you can choose to conceive of the backpointer in a few different ways:

*   as an extra, separate relationship or
*   as part of the one bidirectional relationship or
*   merely a convenience method in the implementation in the r.h.s. class

The easiest way of implementing this backpointer without using relationship manager is to follow the Martin Fowler refactoring technique - see Martin Fowler 'Refactorings' p. 197 "Change Unidirectional Association to Bidirectional" - this will ensure you get the wiring correct.  In this refactoring, you decide which class is the master and which is the slave etc.  See the before and after python pdf below for an example of the correct wiring.

The way of implementing a backpointer using relationship manager is simply to call the **findObjectPointingToMe(toMe, id)** method.  Since a RM holds all relationships, it can answer lots of questions for free - just like SQL queries to a database.  See the before and after python pdf below for an example of using findObjectPointingToMe().

### Before and After - Modeling Composite Design Pattern  in Python

The following [code](http://www.atug.com/andypatterns/code/proxydecorator01.zip) is a good example of how the use of RM saves you from having to explicitly maintain backpointers. P.S. To run the code you also need the support files found [here](http://www.atug.com/downloads/pythonRmProof.zip).  View the code below (requires the flash plugin) - showing an implementation of a Composite Pattern, with back pointer - or simply read the [pdf](http://www.atug.com/downloads/rm_annotation_by_ANDY_01.PDF) directly.

<iframe src="/files/rm_annotation_by_ANDY_01.html" name="frame1" scrolling="yes" frameborder="yes" align="center" height = "842px" width = "800">
</iframe>

## A concrete example

This example uses the Boo .NET assembly, which is quite usable from other .NET langauges like C# and VB.NET etc.  Alternatively you can adapt this example to use the pure C# implementation assembly (something I should publish here at some stage).

Say you want to model a Person class which has one or more Orders.  The Orders class has a backpointer back to the Person owning it.

![](http://www.atug.com/andypatterns/images/PersonToOrderUsingRM001.gif)

Instead of hand coding and reinventing techniques for doing all the AddOrder() methods and GetOrders() methods etc. using ArrayLists and whatever, we can do it using the relationship manager object instead, which turns out to be simpler and faster and less error prone. 

The RM (relationship manager) is implemented in this particular example as a static member of the base BO (business object) class.  Thus in this situation all business objects will be using the same relationship manager.

Here is the c# code to implement the above UML:

```c#
using System;
using System.Collections;
using RelationshipManager55;

namespace WindowsApplicationUsing\_RelationshipManagerDllTest001 {
  ///   
  /// BO is the base Business Object class which holds a single static reference  
  /// to a relationship manager. This one relationship manager is  
  /// used for managing all the relationships between Business Objects.  
  ///   
  public class BO // Base business object  
  {
    static protected RM1 RM = new RM1();
  }

  ///   
  /// Person class points to one or more orders.  
  /// Implemented using a relationship manager rather   
  /// than via pointers and arraylists etc.  
  ///   
  public class Person: BO {
    public string name;

    static Person() {
      RM.ER("p->o", "onetomany", "bidirectional");
    }

    public Person(string name) {
      this.name = name;
    }
    public override string ToString() {
      return "Person: " + this.name;
    }

    public void AddOrder(Order o) {
      RM.R(this, o, "p->o");
    }
    public void RemoveOrder(Order o) {
      RM.NR(this, o, "p->o");
    }
    public IList GetOrders() {
      return RM.PS(this, "p->o");
    }
  }

  ///   
  /// Order class points back to the person holding the order.  
  /// Implemented using a relationship manager rather             /// than via pointers and arraylists etc.  
  ///   
  public class Order: BO {
    public string description;

    public Order(string description) {
      this.description = description;
    }
    public override string ToString() {
      return "Order Description: " + this.description;
    }

    public void SetPerson(Person p) {
      RM.R(p, this, "p->o"); // though mapping is bidirectional,  
      there is still a primary relationship direction !

    }
    public Person GetPerson() {
      return (Person) RM.P(this, "p->o");
    }
    public void ClearPerson() {
      RM.NR(this, this.GetPerson(), "p->o");
    }
  }

}
```

Here is the project source code [WindowsApplicationUsing RelationshipManagerDllTest001.rar](http://www.atug.com/downloads/RmBooNet/WindowsApplicationUsing%20RelationshipManagerDllTest001.rar) 

### Future Directions

A generics version of relationship manager would be cool - that way no casting would be required. Presently all calls to relationship manager return objects - which you have to cast to the specific type you actually have stored.

## Resources

See [original andypatterns page](http://www.andypatterns.com/index.php?cID=44)