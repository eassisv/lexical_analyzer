import sys, json

if len(sys.argv) < 2:
    print("Needs a glc as argument")

f = open(sys.argv[1], "r")
lines = f.readlines()
f.close()
rules = []

lines = map(lambda line: line.strip(), lines)
lines = filter(lambda line: len(line), lines)
lines = list(lines)


for index, line in zip(range(len(lines)), lines):
    rule_len = len(line.split()) - 2
    rule_name = line.split(maxsplit=1)[0]
    rules.append(dict(len=rule_len, name=rule_name, rule=line))

print(rules)
f = open("glc_info.json", "w")
json.dump(rules, f, indent=2)
