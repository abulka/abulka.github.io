---
title: "Transformation Interface Design Pattern"
linkTitle: "Transformation Interface"
date: 2019-01-04
type: docs
description: >
  An interface or layer, which offers services to transform an object into another format and back again.
tags: ["Design Patterns"]
---

![](http://www.andypatterns.com/files/71241233039311bgDSC1068.jpg)

## Introduction

The Transformation Interface is both a design pattern and an architectural pattern. It describes an interface or layer, which offers services to transform an object into another format and back again. A pair of methods on some class e.g. load/save are often the signature of a Transformation Interface.

### Simple Summary

Let me summarize the core idea in a simple way:

The fundamental insight of this pattern is elegantly simple: whenever you need to move data between two different representations, create a matched pair of transformation methods that:

1. Transform FROM your object TO something else (e.g., `displayInDialog()`)
2. Transform FROM something else BACK TO your object (e.g., `extractFromDialog()`)

The beauty is that this same simple concept works for many common programming scenarios:
- Object ↔ Dialog box
- Object ↔ Database
- Object ↔ File
- Object ↔ Network message
- Object ↔ Different data format

It's like having a reliable two-way street between different representations of your data. The pattern provides a clean, systematic way to handle these transformations without getting tangled up in complex frameworks.

It takes something that programmers often do ad-hoc (especially with GUI programming) and formalized it into a clear pattern that can be applied consistently across many similar situations.



## The Pattern

<iframe src="/files/andybulkatransformationinterfacepattern.html" name="frame1" scrolling="yes" frameborder="yes" align="center" height = "842px" width = "800">
</iframe>


Download as [pdf](/files/pdfs/AndyBulkaTransformationInterfacePattern.pdf).


## Reactive data and the Transformation Interface Pattern

The Transformation Interface pattern is less useful where data is reactive and the mapping is in a sense automatic e.g. in the Vue and other frameworks.

Modern reactive frameworks like Vue, React, Angular, and Svelte have essentially automated away the need for explicit transformation interfaces in the UI layer. Let me break down why:

Traditional (Transformation Interface Pattern):

```javascript
class User {
    // Manual transformations needed
    displayInForm(form) {
        form.name.value = this.name
        form.age.value = this.age
    }
    
    extractFromForm(form) {
        this.name = form.name.value
        this.age = form.age.value
    }
}
```

Modern Reactive Approach:

```javascript
// Vue
const user = ref({
    name: 'John',
    age: 30
})

// Template automatically syncs both ways
<template>
    <input v-model="user.name">
    <input v-model="user.age">
</template>
```

The transformation interface pattern becomes less necessary here because:

- Two-way Data Binding

  - Changes automatically propagate both ways
  - No need for explicit display/extract methods
  - Framework handles the synchronization


- Reactive State Management

  - State changes trigger automatic UI updates
  - No need to manually push changes to the view
  - Component re-renders handle the transformation


- Declarative Mappings

  - Relationships between data and UI are declared, not implemented
  - Framework handles the mechanics of keeping things in sync
  - Less boilerplate code needed


However, the pattern remains valuable for:

- Backend/API transformations
- File format conversions
- Database mappings
- Cross-system integrations
- Complex state transformations
- Cases where automatic reactivity isn't suitable or possible

The Transformation Interface pattern has evolved to be more useful for system boundaries and data transformations rather than UI interactions in modern web development.




## Examples

Here are some AI generated quick examples of the Transformation Interface pattern:

## Example 1: Person object ↔ Dialog box 
(using tkinter)

```python
from tkinter import *

class Person:
    def __init__(self, name="", age=0, email=""):
        self.name = name
        self.age = age
        self.email = email
        
    def display_in_dialog(self, dialog):
        """Transform FROM Person TO dialog fields"""
        dialog.name_var.set(self.name)
        dialog.age_var.set(str(self.age))
        dialog.email_var.set(self.email)
        
    def extract_from_dialog(self, dialog):
        """Transform FROM dialog fields BACK TO Person"""
        self.name = dialog.name_var.get()
        self.age = int(dialog.age_var.get() or 0)
        self.email = dialog.email_var.get()

class PersonDialog:
    def __init__(self, parent):
        self.name_var = StringVar()
        self.age_var = StringVar()
        self.email_var = StringVar()
        # ... dialog setup code ...
```

## Example 2: Product object ↔ JSON data

```python
class Product:
    def __init__(self, name="", price=0.0, stock=0):
        self.name = name
        self.price = price
        self.stock = stock
    
    def to_json(self):
        """Transform FROM Product TO JSON-compatible dict"""
        return {
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }
    
    def from_json(self, data):
        """Transform FROM JSON-compatible dict BACK TO Product"""
        self.name = data.get("name", "")
        self.price = float(data.get("price", 0.0))
        self.stock = int(data.get("stock", 0))
```

## Example 3: Invoice object ↔ Database record

```python
class Invoice:
    def __init__(self, invoice_no="", amount=0.0, customer=""):
        self.invoice_no = invoice_no
        self.amount = amount
        self.customer = customer
    
    def to_db_record(self):
        """Transform FROM Invoice TO database record dict"""
        return {
            "invoice_number": self.invoice_no,
            "total_amount": self.amount,
            "customer_name": self.customer
        }
    
    def from_db_record(self, record):
        """Transform FROM database record dict BACK TO Invoice"""
        self.invoice_no = record["invoice_number"]
        self.amount = float(record["total_amount"])
        self.customer = record["customer_name"]
```

## Javascript Examples

```javascript
// JavaScript Examples

// Example 1: User object ↔ Form
class User {
    constructor(username = "", email = "", role = "") {
        this.username = username;
        this.email = email;
        this.role = role;
    }
    
    displayInForm(form) {
        // Transform FROM User TO form fields
        form.querySelector('#username').value = this.username;
        form.querySelector('#email').value = this.email;
        form.querySelector('#role').value = this.role;
    }
    
    extractFromForm(form) {
        // Transform FROM form fields BACK TO User
        this.username = form.querySelector('#username').value;
        this.email = form.querySelector('#email').value;
        this.role = form.querySelector('#role').value;
    }
}

// Example 2: Task object ↔ Local Storage
class Task {
    constructor(title = "", dueDate = null, priority = "medium") {
        this.title = title;
        this.dueDate = dueDate;
        this.priority = priority;
    }
    
    toStorage() {
        // Transform FROM Task TO storage format
        return JSON.stringify({
            title: this.title,
            dueDate: this.dueDate?.toISOString(),
            priority: this.priority
        });
    }
    
    fromStorage(storageStr) {
        // Transform FROM storage format BACK TO Task
        const data = JSON.parse(storageStr);
        this.title = data.title;
        this.dueDate = data.dueDate ? new Date(data.dueDate) : null;
        this.priority = data.priority;
    }
}

// Example 3: Order object ↔ API payload
class Order {
    constructor(orderNo = "", items = [], total = 0) {
        this.orderNo = orderNo;
        this.items = items;
        this.total = total;
    }
    
    toApiPayload() {
        // Transform FROM Order TO API format
        return {
            order_number: this.orderNo,
            line_items: this.items.map(item => ({
                product_id: item.id,
                quantity: item.qty,
                unit_price: item.price
            })),
            total_amount: this.total
        };
    }
    
    fromApiPayload(payload) {
        // Transform FROM API format BACK TO Order
        this.orderNo = payload.order_number;
        this.items = payload.line_items.map(item => ({
            id: item.product_id,
            qty: item.quantity,
            price: item.unit_price
        }));
        this.total = payload.total_amount;
    }
}
```

# Transformation Interface in library functions

Twenty years after writing this pattern, it occurs to me that JSON.stringify() and JSON.parse(storageStr) is an example of a transformation interface, at the level of a library function. It's a simple, elegant way to transform data between objects and strings, and it's a pattern that's been widely adopted in many programming languages.

This pattern is so fundamental that it appears frequently in standard libraries, often dealing with:

- Data serialization/deserialization
- Text encoding/decoding
- Format conversion
- Stream processing
- Type conversion

and

- Serialization/Deserialization
- Marshalling/Unmarshalling
- Encoding/Decoding
- Packing/Unpacking
- Parser/Generator pairs
- Transform/Inverse Transform
- Reader/Writer pairs
- Import/Export functions
- Load/Save operations
- Store/Retrieve pairs
- Push/Pull operations
- Pack/Unpack methods
- Stringify/Parse operations
- Format/Parse pairs

### Examples

Here are more built-in transformation interface functions across various programming languages:

Python Built-in Transformations:
1. str.encode() / bytes.decode()
   - Transforms between strings and bytes
   - `text.encode('utf-8')` ↔ `bytes.decode('utf-8')`

2. pickle.dumps() / pickle.loads()
   - Transforms between Python objects and bytes
   - `pickle.dumps(obj)` ↔ `pickle.loads(bytes_data)`

3. int.to_bytes() / int.from_bytes()
   - Transforms between integers and byte representations
   - `num.to_bytes(4, 'big')` ↔ `int.from_bytes(byte_data, 'big')`

4. dict() / list() / tuple() / set() conversions
   - Transform between collection types
   - `dict(items)` ↔ `list(dictionary.items())`

5. datetime.strftime() / datetime.strptime()
   - Transforms between datetime objects and strings
   - `date.strftime('%Y-%m-%d')` ↔ `datetime.strptime(date_str, '%Y-%m-%d')`

JavaScript Built-in Transformations:
1. JSON.stringify() / JSON.parse()
   - Transforms between objects and JSON strings
   - `JSON.stringify(obj)` ↔ `JSON.parse(jsonStr)`

2. btoa() / atob()
   - Transforms between strings and base64
   - `btoa("hello")` ↔ `atob(base64Str)`

3. encodeURI() / decodeURI()
   - Transforms between strings and URI-encoded strings
   - `encodeURI(url)` ↔ `decodeURI(encodedUrl)`

4. Date.toISOString() / new Date(isoString)
   - Transforms between Date objects and ISO strings
   - `date.toISOString()` ↔ `new Date(isoString)`

5. Array.from() / .toArray() methods
   - Transforms between array-like objects and arrays
   - `Array.from(setObj)` ↔ `set.toArray()`

Java Built-in Transformations:
1. ObjectOutputStream.writeObject() / ObjectInputStream.readObject()
   - Transforms between objects and byte streams
   - `oos.writeObject(obj)` ↔ `ois.readObject()`

2. Base64.getEncoder().encode() / Base64.getDecoder().decode()
   - Transforms between bytes and base64
   - `Base64.getEncoder().encode(bytes)` ↔ `Base64.getDecoder().decode(base64Bytes)`

3. URLEncoder.encode() / URLDecoder.decode()
   - Transforms between strings and URL-encoded strings
   - `URLEncoder.encode(str, "UTF-8")` ↔ `URLDecoder.decode(encodedStr, "UTF-8")`

4. String.getBytes() / new String(bytes)
   - Transforms between strings and byte arrays
   - `str.getBytes()` ↔ `new String(bytes)`

5. Properties.store() / Properties.load()
   - Transforms between property objects and streams
   - `props.store(outputStream, comments)` ↔ `props.load(inputStream)`

Additional Cross-Language Examples:
1. XML Marshalling/Unmarshalling
   - Python: `xml.etree.ElementTree`
   - Java: JAXB `marshal()` / `unmarshal()`
   - JavaScript: `XMLSerializer` / `DOMParser`

2. CSV Reading/Writing
   - Python: `csv.reader()` / `csv.writer()`
   - Java: Various CSV libraries
   - JavaScript: CSV parsing libraries

3. Binary Data Formatting
   - Python: `struct.pack()` / `struct.unpack()`
   - Java: `ByteBuffer` put/get methods
   - JavaScript: `TypedArray` views


# Summary and Conclusion:

More generally, the `Transformation Interface` pattern is arguably the single abstract idea behind:

- Data Exchange:

  - ETL (Extract-Transform-Load) pairs
  - Import/Export handlers
  - Data mappers


- Persistence:

  - ORM (Object-Relational Mapping) conversions
  - Hydration/Dehydration
  - Materialization/Dematerialization


- Network:

  - Protocol encoders/decoders
  - Message formatters/parsers
  - Serializers/Deserializers


- GUI:

  - Model-to-View/View-to-Model transformations
  - Display/Update pairs
  - Render/Extract pairs
