# Ingestion

This feature ingests XML files from a repository and puts into the defined database.


## Highlights

- `cli.py`: Defines the user's CLI to interact with it  
- `usecase.py`: Handles the logic of scanning, parsing and writing on database.
- `repository.py`: Handles the logic of getting a stream of XML Schemas, convert it to Database Schemas and ask the database to write it via transactions.
- `parsing`: Defines parsers for each fragment of the XML. Each parser focuses on get information per context.
- `adapters`: Defines the XML Schemas that have the ability to be converted to table using the method `as_table`.

There is no domain model, and no need to it, but almost anemic XML Schemas that are convertable to Database Schemas.

## Data Repository

Your XML repository should looks like:

```
<repository>/
  <id-preffix>/
    <lattes-id>.xml
    ...
  .../
```

i.e.:

```
data/
    00/
        0000000000001.xml
        0000000000021.xml
        ...
    01/
        0100000000001.xml
        0100000000021.xml
        ...
    ...
```
