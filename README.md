The buildOrg project is a converter that takes a Excel format report (.xls) from Workday
and converts that into a flexible javascript view of an orgchart.  This gives a easy to
manage and much faster view of the org chart than the build in Workday capabilities.
The converter (in the converter directory) reads the report and outputs JSON of the form:
```
{
  "name": "Bob the boss",
   "children": [
     { "name": "Good Employee1" },
     { "name": "Good Employee2" },
     { "name": "Good Employee3",
       "children": [
       { "name": "Good Employee4" },
       { "name": "Good Employee5" }
       ]
     }]
}
```

The converter currently is set up to expect a org chart dump from Workday, but given each Workday instance
is customized and reports available also varies widely, you may need to customize to support your environment.

The viewer (in the html directory) is built using d3.js.  It shows the hierarchy of people, color coding for each level,
the ability to grow expand individual subtrees, counts of org size at each node, and even basic drag-drop to experiment with
org changes.

    