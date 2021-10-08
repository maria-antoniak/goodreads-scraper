# Discussion Points

- Refactor of book service
  - Move toward common layers, i.e. multi-tier architecture
  - Async networking
  - Improved error handling
  - Config options

- Refactor/Creation of list/shelf service

The initial baseline full pulling a list was 33 secs, as of introducing async we're down to 5 seconds.

- Author Module
- Common Module

# Points to note

- Having not refactored reviews

# Additional Ideas

- Project name change (see README)
  - There a few other projects with this name
- Write an API
- Write tool to calculate diversity percentage
- Refactor reviews service, so it's not dependent on Selenium (Selenium is slow and brittle)
- Continue to extend tests (make it a mandatory requirement to commit)
- Include PR template to ensure standard is kept high