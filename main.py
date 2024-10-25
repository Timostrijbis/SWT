import requests
import json

def main():
    query = '''
prefix golem: <https://golemlab.eu/graph/>
prefix gc: <https://ontology.golemlab.eu/>
prefix gd: <https://data.golemlab.eu/entity/>
prefix lrm: <http://iflastandards.info/ns/lrm/lrmoo/>

SELECT ?s ?title ?kudos ?comments ?keywords ?words ?characters ?rating WHERE { 
?s golem:fandom "Harry Potter - J. K. Rowling".
?s golem:title ?title .
?s golem:language "English" .
?s golem:numberOfKudos ?kudos .
?s golem:numberOfComments ?comments .
?s golem:numberOfChapters ?chapters.
?s golem:numberOfWords ?words.
?s golem:rating ?rating.

} LIMIT 300000
    '''

    query_2 = '''
prefix golem: <https://golemlab.eu/graph/> 
WITH GRAPH <https://golemlab.eu/graph/> 

SELECT ?s ?title ?kudos ?comments ?keywords ?words ?rating WHERE {
?s golem:fandom "Harry Potter - J. K. Rowling".
?s dcterms:title ?title .
?s dcterms:language "en" .
?s golem:numberOfKudos ?kudos .
?s golem:numberOfComments ?comments .
?s golem:numberOfWords ?words.
?s golem:keyword ?keywords.
?s golem:rating ?rating.
FILTER (?kudos>0)
} ORDER BY ?kudos
LIMIT 10000
'''


    url = 'http://graph.golemlab.eu:8890/sparql'
    results = requests.get(url, params={'query': query_2, 'format': 'json'}).json()
    keys = []
    fic_lib = {}
    id = ''
    for triple in results['results']['bindings']:
        for key, value in triple.items():
            if key == 's':
                id = value["value"]
                if id not in keys:
                    fic_lib[id] = {
                    "id" : value["value"],
                    "keywords" : [],
                    }
                    keys.append(id)
                    print('Number of stories in database:', len(keys))
                else:
                    pass
            elif key in ['title', 'kudos', 'comments', 'words', 'rating']:
                fic_lib[id][key] = value['value']
            elif key == "keywords":
                fic_lib[id][key].append(value[ 'value'])
            else:
                print('oeps', key, value['value'])
    for key in keys:
        duplicate_list = fic_lib[key]['keywords']
        fic_lib[key]['keywords'] = list(dict.fromkeys(duplicate_list))
        # duplicate_list = fic_lib[key]['characters']
        # fic_lib[key]['characters'] = list(dict.fromkeys(duplicate_list))



    # For the first set
    # with open("sample.json", "w") as outfile:
    #     json.dump(fic_lib, outfile, indent=4)

    with open("sample.json", "r+") as file:
        file_data = json.load(file)
        file_data.update(fic_lib)
        file.seek(0)
        json.dump(file_data, file, indent=4)

if __name__ == '__main__':
    main()


