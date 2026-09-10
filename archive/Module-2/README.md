# Module 2: Database Documentation

## Status

The editable source is [`diagrams.dot`](diagrams.dot), the exported architecture
sheet is [`architecture.svg`](architecture.svg), and the design notes are in
[`technical-documentation.md`](technical-documentation.md).

## Required Deliverables

- Entity-relationship diagram for the finalized database schema
- Class diagram for the application models
- Login sequence diagram
- Student job-application sequence diagram
- Role-based use-case diagram for students, recruiters, and administrators
- Application-status state diagram
- Deployment diagram
- Two additional supporting diagrams to reach the project's nine-diagram target
- Short technical documentation linking the diagrams to the implementation

Diagram sources should be committed alongside exported SVG files so that the
documentation can be maintained when the schema or API changes.

Regenerate the SVG with Graphviz from this folder:

```powershell
dot -Tsvg diagrams.dot -o architecture.svg
```