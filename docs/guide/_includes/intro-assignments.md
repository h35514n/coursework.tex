`coursepsets` loads `courseassignments` to manage assignment declarations and output, including equation, figure, and table numbering.
Use the homework class for the complete assignment layout.

### Fragment files

| Role | Filename | Requirement and output |
| --- | --- | --- |
| Statement | `problem<ID>.tex` | Required for each selected problem in every mode |
| Solution | `solution<ID>.tex` | Required in worked mode. It can be empty. Other modes never read it. |
| Guide | `guide<ID>.tex` | Optional in every mode |
| Discussion | `discussion<ID>.tex` | Optional in worked mode only |

IDs must start with a letter or digit, followed by letters, digits, hyphens, or underscores.
The renderer omits a role section when none of its selected files exist, but an existing empty file can create a section.

Assignment IDs must be unique within the document, and problem IDs must be unique within their assignment.
Once an assignment is printed, it cannot accept more declarations or be printed again.
Object counters continue across each problem's roles.
See the [homework instructions]({{ '/homework/' | relative_url }}) for complete projects and page-break settings.
