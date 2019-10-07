import re

automata = {0: {}}


def add_transition_to_automata(state, label, to_state):
    try:
        automata[state][label].add(to_state)
    except KeyError:
        automata[state][label] = set([to_state])


def add_terminal_label_to_state(state, name=""):
    automata[state]["is_terminal"] = name


def add_new_state_to_automata():
    new_state = len(automata)
    automata[new_state] = {}
    return new_state


def add_token_to_automata(token):
    new_state = add_new_state_to_automata()
    # the first token symbol goes to the first automata state
    add_transition_to_automata(0, token[0], new_state)
    for symbol in token[1::]:
        state = new_state
        new_state = add_new_state_to_automata()
        add_transition_to_automata(state, symbol, new_state)
    add_terminal_label_to_state(new_state, token)


def filter_grammar_line(grammar_line):
    grammar_line = re.sub(r"\ +", "", grammar_line)
    rule_name, transitions = re.split(r"::=", grammar_line)
    transitions = list(
        map(
            lambda tr: tuple(re.sub(r">$", "", tr).split("<", maxsplit=1)),
            transitions.split("|"),
        )
    )

    return rule_name, transitions


def add_grammar_to_automata(grammar_name, grammar):
    # the initial state of grammar must be labeled with 'S'
    map_label_to_state = {"S": add_new_state_to_automata()}

    def get_state_for_rule(name):
        try:
            return map_label_to_state[name]
        except KeyError:
            map_label_to_state[name] = add_new_state_to_automata()
            return map_label_to_state[name]

    for line in grammar:
        grammar_label, rules = filter_grammar_line(line)
        new_state = get_state_for_rule(grammar_label)
        for label, rule in rules:
            to_state = get_state_for_rule(rule)
            add_transition_to_automata(new_state, label, to_state)
    add_terminal_label_to_state(get_state_for_rule(""), grammar_name)
    join_states(0, get_state_for_rule("S"))


def join_states(state1, state2):
    for key in automata[state2].keys():
        if key == "is_terminal":
            add_terminal_label_to_state(state1, automata[state2][key])
            continue
        try:
            for transition in automata[state2][key]:
                add_transition_to_automata(state1, key, transition)
        except TypeError:
            add_transition_to_automata(state1, key, key)


def remove_epsilon_transitions():
    seen = set()

    def remove_epsilon(state):
        if state in seen:
            return
        seen.add(state)
        try:
            for transition in automata[state][""].copy():
                remove_epsilon(transition)
                join_states(state, transition)
            del automata[state][""]
        except KeyError:
            return

    for state in automata:
        remove_epsilon(state)


def eliminate_non_determinism():
    map_new_states = {}

    def eliminate(state):
        for label in state.keys():
            if label == "is_terminal":
                continue
            if len(state[label]) > 1:
                new_label = str(sorted(list(state[label])))
                new_state = map_new_states.get(new_label)
                if not new_state:
                    new_state = add_new_state_to_automata()
                    map_new_states[new_label] = new_state
                    for transition in state[label]:
                        join_states(new_state, transition)
                    eliminate(automata[new_state])
                state[label] = new_state
            else:
                state[label] = state[label].pop()

    for state in automata.copy().keys():
        print(state, "*" * 50)
        print_automata()
        eliminate(automata[state])


while True:
    try:
        token = input()
        if not token:
            break
        add_token_to_automata(token)
    except EOFError:
        break

label = ""
grammar = []
while True:
    try:
        line = input()
        if not line:
            add_grammar_to_automata(label, grammar)
            grammar, label = [], ""
            continue
        if not label:
            label = line
        else:
            grammar.append(line)
    except EOFError:
        if grammar:
            add_grammar_to_automata(label, grammar)
        break


def print_automata():
    for state, value in automata.items():
        print(state, ":", value)


print_automata()
remove_epsilon_transitions()
print_automata()
eliminate_non_determinism()
print_automata()

