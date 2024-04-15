import subprocess
import json
import os
from cleantext import clean
import pandas as pd
import re

class Helper:

    def __init__(self, path="./sympgraph.xlsx"):
            self.df = pd.read_excel(path, engine='openpyxl')
            self.query_table = self.df["Source"].values

    # Fetch Aditional Symptoms based on the query
    def fetch_additional_symptoms(self, query):
        query = [i for i in query if i in self.query_table]
        result = []
        if query:
            result = self.df.loc[self.df["Source"].isin(query) & ~self.df["Target"].isin(query)]
            result = result.sort_values("Weight", ascending=False).drop_duplicates("Target")["Target"].tolist()
        return result[:10]

    # Annotate query using MetaMap
    def annotate_query(self, input_text):
        if not input_text:
            return {'error': 'No input provided'}

        current_dir = os.getcwd()
        os.chdir('metamaplite')
        req = clean(input_text)

        command = f'echo "{req}" | ./metamaplite.sh --pipe --freetext --outputformat=json --overwrite'

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        os.chdir(current_dir)
    
        if result.returncode == 0:
            filtered_lines = [line for line in result.stdout.split('\n') if 'warning' not in line.lower()]
            filtered_output = '\n'.join(filtered_lines)
            if filtered_output.strip(): 
                output = self.parse_output(filtered_output)
                return output
            else:
                return {'error': 'No output from subprocess'}
        else:
            return {'error': 'An error occurred while processing the input'}

    # Parse the dat to extract relevant medical data
    def parse_output(self, data):
        data1 = json.loads(data)
        symptoms = []
        diseases = []
        diagnostics = []
        for item in data1:
            for concept in item['evlist']:
                concept_info = concept['conceptinfo']
                if "sosy" in concept_info['semantictypes']:
                    if concept_info['preferredname'] not in ['Symptoms', 'symptoms']:
                        symptoms.append(concept_info['preferredname'])
                elif "dsyn" in concept_info['semantictypes']:
                    diseases.append(concept_info['preferredname'])
                elif "diap" in concept_info['semantictypes']:
                    diagnostics.append(concept_info['preferredname'])

        extracted_data = {}
        if symptoms:
            extracted_data['symptoms'] = symptoms + self.fetch_additional_symptoms([q.lower().capitalize() for q in symptoms])
            extracted_data['symptoms']  = [self.remove_parentheses_and_quotes(symptom) for symptom in extracted_data['symptoms']]
        if diseases:
            extracted_data['diseases'] = diseases
        if diagnostics:
            extracted_data['diagnostics'] = diagnostics
        return json.dumps(extracted_data, indent=4)
    
    def remove_parentheses_and_quotes(self, text):
        pattern = r"\([^)]*\)|\"[^\"]*\""
        return re.sub(pattern, "", text)

