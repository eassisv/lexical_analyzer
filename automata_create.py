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
    # print(transitions)
    transitions = list(
        map(
            lambda tr: tuple(re.sub(r">$", "", tr).split("<", maxsplit=1)),
            transitions.split("|"),
        )
    )

    # print(ruleName, " ", transitions)
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

    # print("*" * 100)
    # for state, value in automata.items():
    #     print(state, ":", value)
    # print("*" * 100)


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

    def eliminate(state):
        # print("mapNew: ", mapNewStates)
        for label in state.keys():
            if label == "isTerminal":
                continue
            # print("Wow: ", state)
            if len(state[label]) > 1:
                newLabel = str(sorted(list(state[label])))
                # print("NewLabel: ", newLabel)
                newState = mapNewStates.get(newLabel)
                if not newState:
                    # print(newLabel, " nao")
                    newState = addNewAutomataState()
                    mapNewStates[newLabel] = newState
                    for transition in state[label]:
                        # print("joinning: ", newState, " and ", transition)
                        joinStates(newState, transition)
                    eliminate(automata[newState])
                state[label] = newState
            else:
                state[label] = state[label].pop()

    for state in automata.copy().keys():
        eliminate(automata[state])


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

