import json

f = open("symbol_table.json", "r")
symbol_table = json.load(f)

f = open("table.json", "r")
table = json.load(f)
table = table["table"]

f = open("glc_info.json", "r")
glc_rules = json.load(f)

#   {
#     "line": 1,
#     "state": "79",
#     "token": "if",
#     "word": "if"
#   },


def parse():
    stack = [0]
    tape = symbol_table.copy()
    tape.append(dict(line=-1, state=-1, token="$", value="$"))

    while True:
        top = stack[-1]
        token = tape[0]["token"]

        action = table[top][token]

        print("top: {}\ntoken: {}\naction: {}".format(top, token, action))

        if action == "acc":
            print("Correct syntax")
            return

        if action == None:
            print("Wrong syntax")
            print(
                "Error in line: {}: syntax: {}".format(
                    tape[0]["line"], tape[0]["value"]
                )
            )
            return

        if action[0] == "s":
            stack.append(token)
            stack.append(int(action[1:]))
            tape.pop(0)
        else:
            rule = glc_rules[int(action[1:])]
            print("rule:", rule)
            del stack[-rule["len"] * 2 :]
            goto = table[stack[-1]][rule["name"]]
            stack.append(rule["name"])
            stack.append(int(goto))

        print("stack:", stack)
        if len(tape):
            print("tape:", tape[0])


parse()
