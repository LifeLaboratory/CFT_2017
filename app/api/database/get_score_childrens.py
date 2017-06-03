import json


def average_score():
    with open("score_children.json", 'r') as f:
        data = f.read()
        data = json.loads(data)
    s = 0
    score = []
    for score in data:
        if score != 'name':
            s
            s += float(data[score])

    score = round(s/(len(data)-1), 1)
    return data["name"], score

print(average_score())