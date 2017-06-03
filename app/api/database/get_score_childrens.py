import json


def average_score(name_child):
    with open("score_children.json", 'r') as f:
        DATA = f.read()
        DATA = json.loads(DATA)
    s = 0
    print(DATA)
    for data in DATA:
        print(DATA[data]['name'], ' -> ', name_child)
        if DATA[data]['name'] == name_child:
            s = 0
            _score = {score: data[score] for score in data}
            for score in data:
                if score != 'name':
                    s += float(data[score])
            score = round(s/(len(data)-1), 1)
            return _score, score
    return None
#print(average_score())