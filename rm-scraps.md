
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

