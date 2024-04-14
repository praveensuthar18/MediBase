import subprocess
import json
import os
from cleantext import clean
import pandas as pd
import re

class Utils:

    def __init__(self, path="./sympgraph.xlsx"):
            self.df = pd.read_excel(path, engine='openpyxl')
            self.query_table = self.df["Source"].values

    def fetch_additional_symptoms(self, query):
        query = [i for i in query if i in self.query_table]
        result = []
        if query:
            result = self.df.loc[self.df["Source"].isin(query) & ~self.df["Target"].isin(query)]
            result = result.sort_values("Weight", ascending=False).drop_duplicates("Target")["Target"].tolist()
        return result[:10]

    def annotate_query(self, input_text):
        if not input_text:
            return {'error': 'No input provided'}

        # Get the current working directory
        current_dir = os.getcwd()

        # Change directory to where metamaplite.sh is located
        os.chdir('metamaplite')
        req = clean(input_text)
        # Replace the quoted text with user input
        command = f'echo "{req}" | ./metamaplite.sh --pipe --freetext --outputformat=json --overwrite'

        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Change back to the original directory
        os.chdir(current_dir)
    
        if result.returncode == 0:
            # Filter out lines containing "warning"
            filtered_lines = [line for line in result.stdout.split('\n') if 'warning' not in line.lower()]

            # Join the filtered lines back into a single string
            filtered_output = '\n'.join(filtered_lines)
            # print(result.stdout)
            if filtered_output.strip():  # Check if stdout is not empty
                output = self.parse_output(filtered_output)
                return output
            else:
                return {'error': 'No output from subprocess'}
        else:
            return {'error': 'An error occurred while processing the input'}
        
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
    # Regular expression pattern to match text within parentheses or quotes
        pattern = r"\([^)]*\)|\"[^\"]*\""
    # Replace the matched pattern with an empty string
        return re.sub(pattern, "", text)

# Apply the function to each symptom in the list

