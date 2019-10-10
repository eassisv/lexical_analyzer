import json

token_to_state = {}
f = open("automata.json", "r")
automata = json.load(f)
f.close()
for state in automata:
    try:
        token_to_state.setdefault(automata[state]["is_terminal"], state)
    except KeyError:
        continue

f = open("token_to_state.json", "w")
json.dump(token_to_state, f, sort_keys=True, indent=2)
