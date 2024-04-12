import json
import requests
from cleantext import clean



request_content_type = 'text/plain'

url = 'https://ii.nlm.nih.gov/metamaplite/rest/annotate'

headers = {'Accept' : 'text/plain'}


def create_payload(inputtext):
    payload = []

    
    payload.append(('inputtext', clean(inputtext)))
    payload.append(('docformat', 'freetext'))
    payload.append(('resultformat', 'json'))

    srcs = 'all'
    semantic_types = 'all'
    for source in srcs.split(','):
        payload.append(('sourceString', source))
    for semtype in semantic_types.split(','):
        payload.append(('semanticTypeString', semtype))

    return payload


def annotate(text):
    mm_request = [text]
    # concepts, error = self.mm.extract_concepts(mm_request, [1, 2])
    
    payload = create_payload(text)
    extracted_data = {}
    try:
        resp = requests.post(url, payload, headers=headers, timeout=5)
        data = resp.json()        
        symptoms = []
        diseases = []
        diagnostics = []
        for item in data:
            for concept in item['evlist']:
                concept_info = concept['conceptinfo']
                if "sosy" in concept_info['semantictypes']:
                    if concept_info['preferredname'] != 'Symptoms' and concept_info['preferredname'] != 'symptoms':
                            symptoms.append(concept_info['preferredname'])
                elif "dsyn" in concept_info['semantictypes']:
                    diseases.append(concept_info['preferredname'])
                elif "diap" in concept_info['semantictypes']:
                    diagnostics.append(concept_info['preferredname'])

        if len(symptoms):
            extracted_data['symptoms'] = symptoms
        if len(diseases):
            extracted_data['diseases'] = diseases
        if len(diagnostics):
            extracted_data['diagnostics'] = diagnostics

        return extracted_data

    except requests.exceptions.Timeout:
        print('Request timed out')
    except requests.exceptions.RequestException as e:
        print('Request error:', e)
    
    return extracted_data

# request_content_type = 'application/x-www-form-urlencoded'

