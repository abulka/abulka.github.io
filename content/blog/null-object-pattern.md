---
title: "Null Object Pattern"
date: 2002-10-04
draft: false
tags: ["Design Patterns", "UML", "Python"]
---

## Null Object Design Pattern

Sometimes I make the joke that design patterns are all about getting rid of if-else statements from your code. The null object pattern is an example of a pattern that does just that - check out the code at the bottom for details.

## What is it?

A Null Object provides a surrogate for another object that shares the same interface, but does nothing.  
  
> _This pattern was originally written up by Bobby Wolf, in Pattern Languages of Program Design 3._

## UML

![null objject uml](http://www.andypatterns.com/files/27251232690646nullobjectUML.png)

_Null Object Pattern_

## Have I used it?

Yes, I have used this pattern a few times in my work.  You have to be a little bit careful about managing the swapping of null obect for the real thing.  If bits of your code are pointing to the null object then you can't easily swap in the real thing.  Better to put the null object / real object behind a proxy so that nobody knows what you are doing!

## Documentation

<iframe style="border: 1px solid #CCC; border-width: 1px; margin-bottom: 5px; max-width: 100%;"
            src="//www.slideshare.net/slideshow/embed_code/key/rLP5FBttyUUc7B" frameborder="0" marginwidth="0"
            marginheight="0" scrolling="no" width="668" height="714"> </iframe>

*Scroll down through the course pages above - or use the page next/previous buttons.*

[Null Object Design Pattern](//www.slideshare.net/tcab22/null-object-design-pattern-presentation "Null Object Design Pattern") chapter from [Andy Bulka's](https://www.slideshare.net/tcab22) Design Patterns course book.

## Example Code

Here is a Python example.  The class named `API` is a real class with real functionality in it (note the name of this class could be anything, and not have anything to do with API's).  

We decide that we want to *optionally* log calls to our API class using a `Logger` class. So we modify our API class to call out to the `Logger` class.

### Without Null Object

```python
from time import asctime, localtime

class AbstractObject: pass   # pretend python has abstract classes

class RealLogging:
    def Log(self, msg):
        print 'Logged at', asctime(localtime()), msg

# Proxy / wrapper around either null or real logger. 

class Logger:
    def __init__(self):
        self.logger = RealLogging()
    def Log(self, msg):
        if self.logger:
            self.logger.Log(msg)
    def On(self):
        self.logger = RealLogging()
    def Off(self):
        self.logger = None
Logger = Logger()

# Usage: 

class API:
    def doA(self):
        if Logger.logger:
            Logger.Log('Am calling A')
        print 'A done.'
    def doB(self):
        if Logger.logger:
            Logger.Log('Am calling B')
        print 'B done.'

o = API()
o.doA()
o.doB()

Logger.Off()
o.doA()
o.doB()
```

### With Null Object

```python
# Null Object Pattern 

class AbstractLogging:
    def Log(self, msg): pass

from time import asctime, localtime

class RealLogging(AbstractObject):
    def Log(self, msg):
        print 'Logged at', asctime(localtime()), msg

class NullLogging(AbstractObject):
    def Log(self, msg):
        return

# Proxy / wrapper around either null or real logger. 

class Logger:
    def __init__(self):
        self.On()
    def Log(self, msg):
        self.logger.Log(msg)
    def On(self):
        self.logger = RealLogging()
    def Off(self):
        self.logger = NullLogging()
Logger = Logger()

# Usage: 

class API:
    def doA(self):
        Logger.Log('Am calling A')
        print 'A done.'
    def doB(self):
        Logger.Log('Am calling B')
        print 'B done.'

o = API()
o.doA()
o.doB()

Logger.Off()
o.doA()
o.doB()
```

### Output

Without logging:

```
A done.
B done.
```

With logging:

```
Logged at Fri Jan 23 17:28:01 2009 Am calling A
A done.
Logged at Fri Jan 23 17:28:01 2009 Am calling B
B done.
```

Notice that in the null object implementation, there are no "if statements" in the client code (API class), which means we turn on logging by injecting in a different instance of `Logger` rather than checking a flag. Arguably this is more flexible and cleaner. You even have more options to swap (or inject) different kind of `Logger` classes with this pattern. 

The Null Object pattern is about switching in a `Logger` class that does nothing.
