import json

def fi(i):
    i += 1
    return i

def average_score(name_child):
    with open("score_children.json", 'r') as f:
        DATA = f.read()
        DATA = json.loads(DATA)
    s = 0
    #print(DATA)
    for data in DATA:
        #print(DATA[data]['name'], ' -> ', name_child)
        if DATA[data]['name'] == name_child:
            s = 0
            for score in DATA[data]:
                #print(score)
                if score != 'name':
                    s += float(DATA[data][score])
            score = round(s/(len(DATA[data])-1), 1)
            return DATA[data]
    return None
#print(average_score())