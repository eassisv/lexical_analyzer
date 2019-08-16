import re

automata = {0: {}}


def addTokenToAutomata(token):
    newState = len(automata)
    try:
        # add state to transition
        automata[0][token[0]].add(newState)
    except KeyError:
        # create index in dictionary
        automata[0][token[0]] = set([newState])
    for symbol in token[1::]:
        state = newState
        # TODO Colocar isso numa função vai ajudar
        newState = state + 1
        automata[state] = {symbol: newState}
    automata[state]["isTerminal"] = token


def filterGrammarRule(grammarLine):
    print("Filtrar linha: ", grammarLine)
    grammarLine = re.sub(r"\ +", "", grammarLine)
    ruleName, transitions = re.split(r"::=", grammarLine)
    transitions = list(
        map(
            lambda tr: tuple(re.sub(r">$", "", tr).split("<", maxsplit=1)),
            re.split(r"\|", transitions),
        )
    )
    return ruleName, transitions

# TODO Tornar essa função mais genérica, passando para ela argumentos para inicializar o estado
def addNewAutomataState(isTerminal=False, label=""):
    newState = len(automata)
    automata[newState] = {"isTerminal": label} if isTerminal else {}
    return newState

def addGrammarToAutomata(label, grammar):
    mapRuleToState = {"S": 0}
    for rule in grammar:
        name, transitions = filterGrammarRule(rule)
        try:
            automataState = mapRuleToState[name]
        except KeyError:
            automataState = mapRuleToState[name] = len(automata)
        automata[automataState] = {}
        for label, transition in transitions:
            try:
                state = mapRuleToState[label]
            except KeyError:

            try:
                automata[automata][label].add()

while True:
    try:
        token = input()
        if token == "":
            break
        addTokenToAutomata(token)
    except EOFError:
        break

label = ""
grammar = []
while True:
    try:
        line = input()
        if line == "":
            addGrammarToAutomata(label, grammar)
            grammar = []
            label = ""
            continue
        if label == "":
            label = line
        else:
            grammar.append(line)
    except EOFError:
        if grammar:
            addGrammarToAutomata(label, grammar)

        break


for state, value in automata.items():
    print(state, " | ", value)
