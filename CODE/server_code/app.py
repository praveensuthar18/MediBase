from flask import Flask, request, jsonify
import pysolr
from Utils import Utils
from flask_cors import CORS
app = Flask(__name__)
util = Utils()
SOLR_URL = 'http://localhost:8983/solr/'  # Update with your Solr URL
CORE_NAME = 'healthify'  # Update with your Solr core name

CORS(app)
# Enable CORS on all routes
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})

# Initialize Solr client
solr = pysolr.Solr(f'{SOLR_URL}{CORE_NAME}', always_commit=True)

@app.route('/search', methods=['POST'])
def search():
    request_data = request.json
    if not request_data or 'query' not in request_data:
        return jsonify({'error': 'JSON object with "query" key is required in the request body'}), 400
    
    query_words = request_data['query']
    if not query_words:
        return jsonify({'error': 'Query parameter "query" must be a list of words'}), 400
    
    # Construct the Solr query to search for each word in symptoms field
    solr_query = ' OR '.join([f'symptoms:{word}' for word in query_words])
    
    # Sort the Solr results based on relevance (number of occurrences of query words in symptoms)
    solr_params = {
        'q': solr_query,
        'wt': 'json',  # Response format,
        'sort':  'score desc',
        'fl': '*,score'
    }
    
    solr_response = solr.search(**solr_params)
    
    if solr_response:
        return jsonify(solr_response.docs)
    else:
        return jsonify({'error': 'No results found'}), 404
    

@app.route('/process-query', methods=['POST'])
def process():
    input_text = request.json.get('query')
    output = util.annotate_query(input_text)
    return output

if __name__ == '__main__':
    app.run(debug=True, port=8080)
