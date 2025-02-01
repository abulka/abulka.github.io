### Class Relationships: DEPRECATED
**Class Relationships**: Describes relationships between classes and interfaces, including optional relationship annotation (uses, contains, owns, etc.) and optional cardinality (e.g., 1, 1..*, 0..1). Single or multiple relationships. If one relationship, use `Class1 --> Class2 (relationship)`. For multiple relationships, indent the relationships under the class.  Nested relationships are indented further.
Whilst you can show relationships between classes in the `Classes:` section, this section is for summarizing all the relationships in one place, and is needed if you want to show nested class relationships e.g. for expressing the the chain: `Class6` uses `Class8` which in turn creates `Class9`.
```plaintext
Class Relationships:
  Class1
    --> Class2 (inherits)
    --> Class3 (implements)
  Class4 --> Class5 (depends on)
  Class6
    --> Class7 (contains, 1..*)
    --> Class8 (creates, 1)
      --> Class9 (owns, 0..1)
```



Sure, PT Diagrams, also have a `Class Relationships:` section where all the relationships are listed, one per line. But this section is a redundant, summary of the relationship shown in the Classes section and is entirely optional. Use it if you feel it adds value (see section below on Relationships).


#### Relationships

Philosophically, there are other paradigms besides data and behaviour. Relationships are a `thing`, so we have a `Class Relationships:` section and an `Imports:` section. 

The `Imports:` section is a list of files with relationships to other files. 

The `Class Relationships:` section is a list of classes with relationships to other classes. 

<img src="/blog/images/pt-diagram-class-relationships.png" alt="Plain Text 'UML Class Diagram' Class Relationships" width="60%">

<br>
<br>



### Treeview Example

Example for Treeview Construction, [example-treeview.ptd](/blog/uml/example-treeview.ptd)

This Use Case (sequence diagram as text) example represents the logic of some Treeview construction code, representing the functionality of my vscode extension [Snippets Explorer](/projects/libraries/snippets-explorer/) which shows vscode source code snippets in a treeview. This sequence 'diagram' example includes features like `[if]`, `[else]` and plenty of psuedo code descriptive text.




```
{{< andy/include-file path="content/blog/uml/example-treeview.ptd" >}}
```


![The beginning of a PT Diagram file](/blog/images/pt-diagram-screenshot1.png)
*beginning of a PT Diagram file*

<img src="/blog/images/pt-diagram-class.png" alt="Plain Text 'UML Class Diagram'" width="70%">
<br/>
<i>a class 'diagram' in PT Diagram notation</i>
<br/>
<br/>

![A pseudo code, sequence diagram example of a use case sequence](/blog/images/pt-diagram-screenshot2a.png)
*sequence 'diagrams'*

