Loaded by both classes. Standalone `\usepackage{coursecommon}` supplies configuration without loading subject notation or selecting a page layout. The title and heading helpers use the surrounding class's title facilities.

### Setup keys

| Key | Default | Meaning |
| --- | --- | --- |
| `author` | Empty | Author name |
| `course-code` | Empty | Short code, such as PHYS 101 |
| `course-title` | Empty | Full course title |
| `term` | Empty | Term, also the default title/heading date |
| `textbook` | Empty | Stored textbook title; read with the metadata accessor |
| `textbook-author` | Empty | Stored textbook author |
| `mode` | `worked` | `worked`, `worksheet`, or `compact` |
| `problem-breaks` | `flow` | `page` or `flow`; consulted in worked mode |
| `assignment-breaks` | `flow` | `page` or `flow` before subsequent assignments |
| `section-breaks` | `page` | `page` or `flow` between assignment roles |
| `font-profile` | Pazo in homework; Pagella in notes or standalone common | `pazo`, `pagella`, or `euler`; select during class loading |

Unknown keys and invalid choice values produce LaTeX key errors. Setting `textbook` metadata does not automatically add it to the generated title.
