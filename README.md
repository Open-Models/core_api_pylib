<h1 align="center">
    <img src="https://core.ac.uk/resources/core-logo.png" alt="core-logo" width="300"/>
    <br/>
    Python Library for CORE API
</h1>

Search knowledge between millions of scientific documents in open access from thousands of data providers (universities,
OA journals, institutes...) around the world using [CORE](https://core.ac.uk/) search engine. Prototype of an implementation of the CORE API (v3) methods.

> *Official API documentation* : https://api.core.ac.uk/docs/v3

## Installation

1/ Register to CORE to get an API key : https://core.ac.uk/services/api

2/ Clone the repository locally : `git clone https://github.com/Open-Models/core_api_pylib.git`

3/ Install python dependency : `python3 -m pip install requests`

## Usage

Find open access resources using [CORE query language](https://api.core.ac.uk/docs/v3#section/How-to-search) :

```python
import core_api_lib as oacore

client = oacore.CoreClient("YOUR-SECRET-KEY")

papers = client.find('"open science" AND culture', recent=True, \
                        types=["research", "thesis"], limit=5)
```

> `find` is not an API method but a function to simulate the search engine, build on top of `search` method.

More information in the [library documentation](documentation.md).

## Community

Alpha stage, **no one should rely on this software**, incomplete, untested, unsecure.

This library is provided by people around the project [open-models.org](https://open-models.org) under the open license [GNU AGPL](LICENSE).

Development is open to contribution on [GitHub](https://github.com/Open-Models/core_api_pylib), welcoming any improvement. Asks for features if you're unable to produce them, someone may help.

*Enjoy your programming journey in open science !*
