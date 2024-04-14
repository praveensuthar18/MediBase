import json
import numpy as np
import pandas as pd

def get_posts_and_symptoms():
    posts = []
    symptoms_set = set()

    with open('./merged.json') as f:
        data = json.load(f)
        for obj in data:
            if 'symptoms' in obj.keys():
                symptoms =[s.lower().capitalize() for s in obj["symptoms"]]
                if symptoms:
                    posts.append(symptoms)
                    symptoms_set.update(symptoms)
                
    return posts, list(symptoms_set)


def build_symptom_edges():
    post_Mat = []
    posts, symptoms = get_posts_and_symptoms()
    for post in posts:
        symptom_Mat = [0]*len(symptoms)
        for symptom in post:
            index = symptoms.index(symptom)
            symptom_Mat[index] += 1
        post_Mat.append(symptom_Mat)  
    return post_Mat, symptoms


def create_sympgraph():
    post_Mat, symptoms = build_symptom_edges()
    symptomGraphShape = (len(symptoms),len(symptoms))
    symptomGraph = np.zeros(symptomGraphShape)

    for arr in post_Mat:
        mat = np.matrix(arr)
        postSymptomGraph = np.matmul(mat.transpose(), mat)
        symptomGraph += postSymptomGraph
    return symptomGraph.tolist(), symptoms

def build_sympgraph():
    edgeList = []
    graph, symptoms = create_sympgraph()
    for i, _ in enumerate(graph):
        for j in range(i + 1 ,len(graph)):
            source = symptoms[i]
            dest = symptoms[j]
            weight = graph[i][j]
            if weight > 1:
                edgeList.append([source, dest, weight])
    return edgeList

def save_sympgraph(edgeList):
    # Convert the edge list to a DataFrame
    df = pd.DataFrame(edgeList, columns=["Source", "Target", "Weight"])
    
    # Save the DataFrame to an Excel file
    df.to_excel('sympgraph.xlsx', index=False)

if __name__ == '__main__':
    save_sympgraph(build_sympgraph())
    print("Successully generated Sympgraph and saved in CSV")
