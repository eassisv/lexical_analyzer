import sys, json


delimiters = set(" ", "<", "=", "(", ")", "{", "}", "\n", "\t", "+", "-", "*", "/", ";")


def load_json(file_name):
    f = open(file_name, "r")
    json_dict = json.load(f)
    f.close()
    return json_dict


automata = load_json("automata.json")
token_to_state = load_json("token_to_state.json")
f = open(sys.argv[1], "r")
source = f.read()
f.close()
print(source)


word = ""
line = column = 1
delimiter = False
symbol_table = []
for char in source:

    column += 1
    if char == "\n":
        line += 1
        column = 1

    if char in delimiters:
        delimiter = char != ""
        if word:
            if not delimiter:
                state, token = token_verify(word)
                symbol_table.append(
                    {"state": state, "token": token, "word": word, "line": line}
                )

    else:
        word += char
