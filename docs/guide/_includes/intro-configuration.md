Both classes load `coursecommon` for shared configuration.
Loading it separately with `\usepackage{coursecommon}` provides configuration without subject notation or page layout.
Its title and heading commands use the surrounding class's title functions.

### Setup keys

| Key | Default | Meaning |
| --- | --- | --- |
| `author` | Empty | Author name |
| `course-code` | Empty | Short code, such as PHYS 101 |
| `course-title` | Empty | Full course title |
| `term` | Empty | Term and default date for titles and headings |
| `textbook` | Empty | Stored textbook title. Read it with the metadata accessor. |
| `textbook-author` | Empty | Stored textbook author |
| `mode` | `worked` | `worked`, `worksheet`, or `compact` |
| `problem-breaks` | `flow` | `page` or `flow` in worked mode |
| `assignment-breaks` | `flow` | `page` or `flow` before subsequent assignments |
| `section-breaks` | `page` | `page` or `flow` between assignment roles |
| `font-profile` | Pazo in homework. Pagella in notes or standalone common. | `pazo`, `pagella`, or `euler`. Select it when the class loads. |

Unknown keys and invalid choices produce LaTeX key errors.
Textbook metadata is stored for use through the metadata accessor and is not automatically included in the title.
