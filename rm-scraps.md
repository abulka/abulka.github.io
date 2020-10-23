
![](http://www.andypatterns.com/files/62371233035718bgDSC1367.jpg)



## Usage and Theory

Relationship Manager - Usage and Theory


Included are examples of how to code using relationship manager, covering all possible modelling scenarios (e.g. one to one, one to many etc.).  

See also the Boo implementation page for a fully worked out example of a person and order class.  The Java download also has a real world example implemented.

I also spend some time describing, in more theoretical terms, the scope of the relationship manager approach, in other words - what are all the possible relationships between objects and how RM can model them.

### Its a Object Relational Database



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



SCRAPS

Code which supports the ideas in the theory above is provided in this [python program](http://www.atug.com/downloads/pythonRmProof.zip) or simply view the code and results as a [pdf](http://www.atug.com/downloads/pythonRmProof.pdf).




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


![](http://www.atug.com/andypatterns/_themes/canvas/acnvrule.gif)
* * *


However if you want to delete or change the back-pointer relationship (from Y's perspective) then you must talk to the relationship manager in terms of the relationship "xtoy".  If you implement the back-pointer relationship as a different relationship, with a different relationshipId, then you will fall prey to the same out of synch problems that traditional spaghetti wiring techniques often fall prey to.  The trick is to treat the relationship as two sides of the *one relationshipId*.


### Even more (scraps)

If you chose to have backpointer setter methods on class Y, you need not necessarily call the wrapping methods on X in order to implement them e.g. `setBackPointer(x)` is implemented by simply calling `x.setPointer(this)` (although it is recommended that you do, since X is the 'controlling' class for the relationship - see [Martin Fowler 'Refactorings'](https://martinfowler.com/books/refactoring.html) p. 197 "Change Unidirectional Association to Bidirectional").

You could alternatively call the relationship manager directly, thus setBackPointer(x) becomes a call to `R(x, y, "xtoy")` and `clearBackPointer()`  becomes a call to `NR(x, y, "xtoy")`.






### One to many

 ![](http://www.atug.com/andypatterns/images/rm_the3.gif)

Class X points to many instances of class Y.

#### Methods on class X

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void | add(y) | `R(x, y, "xtoy*")` |
| list | getAll() | `PS(x, "xtoy*")` |
| void  | remove(y)  | `NR(x, y, "xtoy*")` |

#### Methods on class Y

None.

#### Notes:

1.  Notice that the relationshipId has a `*` symbol in it.  This means that you can add multiple relationships of that type without the relationship manager removing the prior relationship. Not sure which of my Relationship Manager implementations auto-support this - its been so long ago...

### One to many, with back pointers

![](http://www.atug.com/andypatterns/images/rm_the4.gif)

#### Methods on class X

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void | add(y) | `R(x, y, "xtoy*")` |
| list | getAll() | `PS(x, "xtoy*")` |
| void  | remove(y)  | `NR(x, y, "xtoy*")` |

#### Methods on class Y

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| X | getBackPointer() | `B(y, "xtoy*")` |

_and optionally setter methods ..._

| Returns | Example method name | Implementation in RM |
|-----------|-----------------|-----------------|
| void | setBackPointer(x) | `R(x, y, "xtoy*")`<br> _or simply call `x.setPointer(this)`_ |
| void  | clearBackPointer() | `NR(x, y, "xtoy*")`<br>_or simply call `x._clearPointer()`_ |

* * *




## Appendix - Constraints

Not sure exactly what this document is about, I'd have to study it (it was created 20 years ago) - but it looks kind of interesting.

<iframe src="/files/rm-one to one and many maps 01.html" name="frame1" scrolling="yes" frameborder="yes" align="center" height = "842px" width = "800">
</iframe>


