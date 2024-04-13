import subprocess
import json
import os
from cleantext import clean
import pandas as pd

class Utils:

    def __init__(self, path="./sympgraph.csv"):
            self.df = pd.read_csv(path, encoding="latin-1")
            self.query_table = self.df["Source"].values

    def ranker(self, query):
        if len(query) > 1:
            query = [i for i in query if i in self.query_table]
            filter_df = self.df[self.df["Source"].isin(query)]
        elif len(query) == 1:
            if query[0] not in self.query_table:
                return "Invalid Query -- Try again"
            filter_df = self.df[self.df["Source"] == query[0]]
        else:
            return "Empty Query -- Try again"

        filter_df = filter_df[~filter_df["Target"].isin(query)]
        filter_df = filter_df.sort_values("Weight", ascending=False)
        filter_df.drop_duplicates(subset=["Target"], inplace=True)

        return filter_df["Target"].to_list()

    def process_input(self, input_text):
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
                output = self.read_output(filtered_output)
                return output
            else:
                return {'error': 'No output from subprocess'}
        else:
            return {'error': 'An error occurred while processing the input'}
        
    def read_output(self, data):
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
            extracted_data['symptoms'] = symptoms
        if diseases:
            extracted_data['diseases'] = diseases
        if diagnostics:
            extracted_data['diagnostics'] = diagnostics
        return json.dumps(extracted_data, indent=4)
