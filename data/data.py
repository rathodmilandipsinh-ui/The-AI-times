import json

def get_interests():
    with open("data/interests.json","r") as f:
        interests = json.load(f)["interests"]
        return interests