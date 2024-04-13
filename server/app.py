from flask import Flask, request, jsonify
import pysolr
from Utils import Utils

app = Flask(__name__)
util = Utils()
SOLR_URL = 'http://localhost:8983/solr/'  # Update with your Solr URL
CORE_NAME = 'healthify'  # Update with your Solr core name

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
    output = util.process_input(input_text)
    return output

@app.route('/ranker', methods=['POST'])
def ranker():
    # Get the parameters from the request
    query = request.json.get('query')
    # print(query)
    # Call the ranker method
    result = util.ranker([q.lower().capitalize() for q in query])

    # Return the result as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
