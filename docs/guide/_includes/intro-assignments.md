Loaded by `coursepsets`. This package owns assignment state and rendering; use the homework class for the supported complete layout. It also changes equation, figure, and table numbering, so it is not a notation-only package.

### Fragment contract

| Role | Filename | Required / rendered |
| --- | --- | --- |
| Statement | `problem<ID>.tex` | Required for each selected problem in all modes |
| Solution | `solution<ID>.tex` | Required in worked mode; may be empty; never read in other modes |
| Guide | `guide<ID>.tex` | Optional, available in every mode |
| Discussion | `discussion<ID>.tex` | Optional, worked mode only |

IDs begin with a letter or digit and then contain only letters, digits, hyphens, or underscores. A role section is omitted when none of its selected fragment files exist, not merely because a file is empty.

Assignments have unique IDs; problem IDs are unique within an assignment. A rendered assignment cannot accept further declarations or render again. Object counters continue for a problem across its roles. See [homework recipes]({{ '/homework/' | relative_url }}) for complete projects and page-break controls.
