"""
An example reconciliation service API for Google Refine 2.0.

See http://code.google.com/p/google-refine/wiki/ReconciliationServiceApi.
"""
import os
import json

from worldcat.request.search import SRURequest
from worldcat.util.extract import extract_elements, pymarc_extract

from flask import Flask, request, jsonify, json
app = Flask(__name__)
app.debug = True

import logging
from logging import StreamHandler
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)


# Basic service metadata. There are a number of other documented options
# but this is all we need for a simple service.
metadata = {
    "name": "DEMO Worldcat Title Reconciliation Service",
    "defaultTypes": [{"id": "/entry/title", "name": "Entry Title"}],
    }

def search(query):
    """
    Search against Worldcat Search API
    """

    matches = []

    wskey = os.environ['WSKEY']
    s = SRURequest(wskey=wskey, query='srw.ti = "' + query + '"', maximumRecords='3')
    o = s.get_response()

    for r in pymarc_extract(o.data):
        title = ''
        control_num = 0
        for f in r.get_fields():
            if ( f.tag == '245' ):
                title = f.format_field()
                app.logger.info( title )
            if ( f.tag == '001' ):
                control_num = f.format_field()
                app.logger.info(control_num)

        matches.append({ "id": json.dumps(control_num), "name": json.dumps(title), "score": 100, "match": False, "type": [ {"id": "/entry/title", "name": "Entry Title"} ] })

    return matches


def jsonpify(obj):
    """
    Like jsonify but wraps result in a JSONP callback if a 'callback'
    query param is supplied.
    """
    try:
        callback = request.args['callback']
        response = app.make_response("%s(%s)" % (callback, json.dumps(obj)))
        response.mimetype = "text/javascript"
        return response
    except KeyError:
        return jsonify(obj)


@app.route("/reconcile", methods=['POST', 'GET'])
def reconcile():
    # If a single 'query' is provided do a straightforward search.
    query = request.form.get('query')
    if query:
        # If the 'query' param starts with a "{" then it is a JSON object
        # with the search string as the 'query' member. Otherwise,
        # the 'query' param is the search string itself.
        if query.startswith("{"):
            query = json.loads(query)['query']
        results = search(query)
        return jsonpify({"result": results})

    # If a 'queries' parameter is supplied then it is a dictionary
    # of (key, query) pairs representing a batch of queries. We
    # should return a dictionary of (key, results) pairs.
    queries = request.form.get('queries')
    if queries:
        queries = json.loads(queries)
        results = {}
        for (key, query) in queries.items():
            results[key] = {"result": search(query['query'])}
        return jsonpify(results)

    # If neither a 'query' nor 'queries' parameter is supplied then
    # we should return the service metadata.
    return jsonpify(metadata)

if __name__ == '__main__':
    app.run()
