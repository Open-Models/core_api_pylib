from datetime import datetime
import json
import requests
import sys

class CoreClient:
    """
    Client to perform API calls to CORE open access search engine (core.ac.uk).

    Navigate between millions of scientific articles and ressources
    provided by thousand of data provider through open science infrastructures.

    You must register to get an API key : https://core.ac.uk/services/api

    API documentation : https://api.core.ac.uk/docs/v3
    """
    ENDPOINT = "https://api.core.ac.uk/v3/"

    def __init__(self, api_key=None):
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def find(self, query="", entity="works", recent=False, limit=10, offset=0,
            title=None, doi=None, oai=None, issn=None, fields=[], types=[],
            year_min=None, year_max=None):
        """
        Find open science ressources through CORE API similarly to the
        web interface.

        Search any CORE entities like Works, Journals or Data Providers
        by DOI, ISSN, fields, types... or through a custom query to include
        anything.

        Custom method to facilitate research based on the API method search.
        """
        #Prepare all parameters to build a single query
        query_parameters = []

        if query:
            query_parameters.append(query)

        #Generate parameters for suggested search field of the web interface
        for search_field in ["title", "doi", "oai", "issn"]:
            field_value = locals()[search_field]
            if field_value:
                query_parameters.append(f'{search_field}:"{field_value}"')

        #Format all requested fields of study (like medicine or physics)
        #and document types (like research or thesis)
        if fields:
            query_parameters.append(self._format_field("fieldsOfStudy", fields))
        if types:
            query_parameters.append(self._format_field("documentType", types))

        #Specify date range for the selection
        if year_min or year_max:
            year_min = year_min if year_min is not None else 1789
            year_max = year_max if year_max is not None else datetime.now().year
            query_parameters.append(f"(yearPublished>={year_min} AND " + \
                    f"yearPublished<={year_max})")

        #Define sort by publication date to retrieve recent ressources
        sort_field = "publishedDate:desc" if recent else None

        #Format the final query string and perform the API search request
        formatted_query = " AND ".join(query_parameters)
        search_output = self.search(query=formatted_query, entity=entity, \
                limit=limit, offset=offset, sort=sort_field)

        return search_output.get("results")

    def search(self, query, entity="works", limit=10, offset=0, sort=None):
        """
        Search method of the API (using POST) to find research, journals,
        data providers and all CORE API entities.

        API search documentation : https://api.core.ac.uk/docs/v3#tag/Search

        note: not all parameters are implemented.
        """
        search_url = self.ENDPOINT + f"search/{entity}"

        parameters = {
                "q" : query,
                "limit" : limit,
                "offset" : offset,
                }
        if sort:
            parameters["sort"] = sort

        api_call = requests.post(search_url, headers=self.headers, 
                data=json.dumps(parameters))

        if api_call.status_code != 200:
            print(f"error: CORE API request fail, status {api_call.status_code}",
                    file=sys.stderr)
            return {}

        return api_call.json()

    @staticmethod
    def _format_field(field_name, field_values):
        """Format a single query field that has multiple values"""
        formatted_fields = [f'{field_name}:"{value}"' for value in field_values]
        #return example : '(documentType:"research" OR documentType:"thesis")'
        return "(" + " OR ".join(formatted_fields) + ")"
