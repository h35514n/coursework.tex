`coursepsets` loads `courseassignments`.
This package controls assignment state and output.
Use the homework class for the complete assignment layout.
The package also changes equation, figure, and table numbers.

### Fragment files

| Role | Filename | Requirement and output |
| --- | --- | --- |
| Statement | `problem<ID>.tex` | Required for each selected problem in every mode |
| Solution | `solution<ID>.tex` | Required in worked mode. It can be empty. Other modes never read it. |
| Guide | `guide<ID>.tex` | Optional in every mode |
| Discussion | `discussion<ID>.tex` | Optional in worked mode only |

IDs start with a letter or digit.
Subsequent characters can be letters, digits, hyphens, or underscores.
The renderer omits a role section if none of its selected files exist.
An existing empty file can create a section.

Assignments have unique IDs in the document.
Problem IDs are unique within an assignment.
After output, an assignment cannot accept more declarations or print again.
Object counters continue across each problem's roles.
See the [homework instructions]({{ '/homework/' | relative_url }}) for complete projects and page-break settings.
