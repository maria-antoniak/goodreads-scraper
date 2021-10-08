# Changes

The changes made relate to 3 main areas; maintainability, speed and additional features.

## Maintainability

- Code has been refactored into services.
- Data has been modeled in dataclasses.
- Type annotation introduced throughout codebase.
- A move toward common layers, i.e. multi-tier architecture.
- Improved error handling with decorators.
- Full test suite writen for legacy code and all new code. (Currently at 75%)
- Common code refactored to avoid duplication.

## Speed

### Introduced async in networking layer

The initial baseline for pulling a list was 33 secs, as of introducing async we're down to 5 seconds.
There is still some work to be done here, but I feel it's moving in the right direction.

## Features

### Config Options

Gives the user the option to easily choose the data they're interested in. In addition, it lessens processing time. 

### Generating Ids

This is helpful where a user has a data set of books/authors but no corresponding goodreads ids. 
Carver will help generate this data for you so you can use the other services unencumbered.

### Author Service

This is still in development, but the idea is — by the power of SPARQL — to 
give the user the option to pull author information as part of the metadata for a given book.
This can then to be used to classify on gender, country, language etc. I envisage it may help better understand 
the diversity (or sadly lack thereof) of a data set.

# Points to Note

- The review service is yet to be refactored.

# Additional Ideas

- Write an API.
- Write a service to calculate diversity percentage of dataset.
- Refactor review service, so it's not dependent on Selenium (Selenium is slow and brittle).
- Continue to extend tests (this should be a requirement for new code committed).