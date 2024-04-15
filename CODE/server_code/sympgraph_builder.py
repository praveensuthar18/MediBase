import json
import numpy as np
import pandas as pd

# Generate Posts and Symptoms form Json file
def get_posts_and_symptoms():
    posts = []
    symptoms_set = set()

    with open('./processed_medical_data.json') as f:
        data = json.load(f)
        for obj in data:
            if 'symptoms' in obj.keys():
                symptoms =[s.lower().capitalize() for s in obj["symptoms"]]
                if symptoms:
                    posts.append(symptoms)
                    symptoms_set.update(symptoms)
                
    return posts, list(symptoms_set)

# Generate Symptom Adjacency Matrix
def build_adjacency_matrix():
    post_Mat = []
    posts, symptoms = get_posts_and_symptoms()
    for post in posts:
        symptom_Mat = [0]*len(symptoms)
        for symptom in post:
            index = symptoms.index(symptom)
            symptom_Mat[index] += 1
        post_Mat.append(symptom_Mat)  
    return post_Mat, symptoms

# Build Sympgraph using adjacency matrix
def build_sympgraph():
    edgeList = []
    sym_Mat, symptoms = build_adjacency_matrix()
    shape = (len(symptoms),len(symptoms))
    sympgraph = np.zeros(shape)

    for arr in sym_Mat:
        mat = np.matrix(arr)
        localgraph = np.matmul(mat.transpose(), mat)
        sympgraph += localgraph

    graph = sympgraph.tolist()
    for i, val in enumerate(graph):
        for j in range(i + 1 ,len(graph)):
            src = symptoms[i]
            dest = symptoms[j]
            wgt = graph[i][j]
            if wgt > 1:
                edgeList.append([src, dest, wgt])
    return edgeList

# Save the symgraph
def save_sympgraph(edgeList):
    df = pd.DataFrame(edgeList, columns=["Source", "Target", "Weight"])
    df.to_excel('sympgraph.xlsx', index=False)

if __name__ == '__main__':
    save_sympgraph(build_sympgraph())
    print("Successully generated Sympgraph")
