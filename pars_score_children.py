import json

def average_score():
    with open("score_children.json", 'r') as f:
        data = f.read()
        data = json.loads(data)

    s = 0
    for i in range(1, 10):
        name = data["name"]
        s += float(data["Predmet{}_score".format(i)])

    score = round(s/i, 1)
    return(name, score)

print(average_score())
