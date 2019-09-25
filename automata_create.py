import re

automata = {0: {}}


def addTransitionToAutomata(state, label, toState):
    try:
        automata[state][label].add(toState)
    except KeyError:
        automata[state][label] = set([toState])


def addTerminalLabelToState(state, name=""):
    automata[state]["isTerminal"] = name


def addNewAutomataState():
    newState = len(automata)
    automata[newState] = {}
    return newState


def addTokenToAutomata(token):
    newState = addNewAutomataState()
    # the first token symbol goes to the first automata state
    addTransitionToAutomata(0, token[0], newState)
    for symbol in token[1::]:
        state = newState
        newState = addNewAutomataState()
        addTransitionToAutomata(state, symbol, newState)
    addTerminalLabelToState(newState, token)


def filterGrammarLine(grammarLine):
    grammarLine = re.sub(r"\ +", "", grammarLine)
    ruleName, transitions = re.split(r"::=", grammarLine)
    transitions = list(
        map(
            lambda tr: tuple(re.sub(r">$", "", tr).split("<", maxsplit=1)),
            re.split(r"\|", transitions),
        )
    )
    return ruleName, transitions


def addGrammarToAutomata(grammarLabel, grammar):
    # the initial state of grammar must be labeled with 'S'
    mapNameToState = {}

    def getStateForName(name):
        try:
            return mapNameToState[name]
        except KeyError:
            mapNameToState[name] = addNewAutomataState()
            return mapNameToState[name]

    for line in grammar:
        name, rules = filterGrammarLine(line)
        newState = getStateForName(name)
        for label, rule in rules:
            toState = getStateForName(rule)
            if name == "S":
                addTransitionToAutomata(0, "", newState)
            addTransitionToAutomata(newState, label, toState)
    addTerminalLabelToState(getStateForName(""), grammarLabel)


def joinStates(state1, state2):
    for key in automata[state2].keys():
        if key == "isTerminal":
            addTerminalLabelToState(state1, automata[state2][key])
            continue
        for transition in automata[state2][key]:
            addTransitionToAutomata(state1, key, transition)


def removeEpsilonTransitions():
    seen = set()

    def removeEpsilon(state):
        if state in seen:
            return
        seen.add(state)
        try:
            for transition in automata[state][""].copy():
                removeEpsilon(transition)
                joinStates(state, transition)
            del automata[state][""]
        except KeyError:
            return

    removeEpsilon(0)


def eliminateNonDeterminism():
    mapNewStates = {}
    seen = set()

    def eliminate(state):
        for transition in state:
            if len(state[transition]) > 1:
                pass
            else:
                state[transition] = state[transition].pop()

    states = automata.values()
    for state in states:
        eliminate(state)


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


removeEpsilonTransitions()
for state, value in automata.items():
    print(state, ":", value)
eliminateNonDeterminism()

for state, value in automata.items():
    print(state, ":", value)

