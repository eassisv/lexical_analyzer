import sys, json, re


def load_json(file_name):
    f = open(file_name, "r")
    json_dict = json.load(f)
    f.close()
    return json_dict


def verify_token(token):
    state = 0
    for char in token:
        try:
            state = automata[str(state)][char]
        except KeyError:
            return -1, ""

    try:
        return (
            token_to_state[automata[str(state)]["is_terminal"]],
            automata[str(state)]["is_terminal"],
        )
    except KeyError:
        return -1, ""


def record_on_table(word, line):
    state, token = verify_token(word)
    symbol_table.append({"state": state, "token": token, "word": word, "line": line})


to_ignore = set([" ", "\t", "\n", '"'])
delimiters = set(
    [
        " ",
        "<",
        ">",
        "=",
        "==",
        ">=",
        "<=",
        "(",
        ")",
        "{",
        "}",
        "\n",
        "\t",
        "+",
        "-",
        "*",
        "/",
        ";",
    ]
)
symbol_table = []
automata = load_json("automata.json")
token_to_state = load_json("token_to_state.json")


f = open(sys.argv[1], "r")
source = f.read()
f.close()
print(source)


word = delimiter = ""
line = column = 1
for char in source:
    column += 1

    if char in delimiters:
        if re.match(r'^\".*$', word):
            word += char
            char = " "
        elif word:
            record_on_table(word, line)
            word = ""
        if (delimiter + char) not in delimiters:
            record_on_table(delimiter, line)
            delimiter = ""
        delimiter += "" if char in to_ignore else char
    else:
        word += char
        if re.match(r'^\".*\"$', word):
            record_on_table(word, line)
            word = ""
            delimiter = ""
        if delimiter:
            record_on_table(delimiter, line)
            delimiter = ""

    if char == "\n":
        line += 1
        column = 1

if delimiter:
    record_on_table(delimiter, line)


for i in symbol_table:
    print(i)

f = open("symbol_table.json", "w")
json.dump(symbol_table, f, indent=2, sort_keys=True)
f.close()
