all_used_terms = set()


def get_rules(n: int, isInput=True, rule=None):
    rules = []

    for _ in range(n):
        dic = {}
        if isInput:
            rule = input().lower()
        if rule[0:3] == "and":
            count = rule.count("and")
            for _ in range(count):
                dic = {}
                dic["type"] = "pure"
                index = rule.find("and")
                index2 = rule.find("and", index + 3)
                if index2 != -1:
                    dic["term"] = rule[index + 4:index2 - 1]
                    rule = rule[index2:]
                else:
                    dic["term"] = rule[index + 4:]

                all_used_terms.add(dic["term"])
                rules.append(dic)

        elif rule[0:2] == "or":
            count = rule.count("or ")
            dic["type"] = "or"
            for _ in range(1, count + 1):
                index = rule.find("or ", 3)
                if index != -1:
                    temp = rule[3: index - 1]
                else:
                    temp = rule[3:]
                dic["term" + str(_)] = temp
                all_used_terms.add(temp)
                rule = rule[index:]
            rules.append(dic)

        elif rule[0:2] == "if":
            dic["type"] = "if"
            index = rule[3:].find("then")
            dic["term"] = rule[3:index + 2]
            all_used_terms.add(dic["term"])
            dic["term2"] = rule[index + 8:]
            all_used_terms.add(dic["term2"])
            rules.append(dic)

        else:
            dic["type"] = "pure"
            dic["term"] = rule
            all_used_terms.add(dic["term"])
            rules.append(dic)
    return rules


# inputs
number_of_rules = int(input())
user_rules = get_rules(number_of_rules)
given_result = input().lower()

n = len(all_used_terms)
list_sentences = list(all_used_terms)
all_used_terms = set()
state = 0
satisfying_rules = []


def check_rules(boolean_sentences):
    for rule in user_rules:
        if rule["type"] == "pure":
            index = list_sentences.index(rule["term"])
            if not boolean_sentences[index]:
                return
        elif rule["type"] == "if":
            index = list_sentences.index(rule["term"])
            index2 = list_sentences.index(rule["term2"])
            if boolean_sentences[index] and not boolean_sentences[index2]:
                return
        else:
            for _ in range(1, len(rule)):
                index = list_sentences.index(rule["term" + str(_)])
                if boolean_sentences[index]:
                    break
            else:
                return

    else:
        satisfying_rules.append(boolean_sentences)


for i in range(2 ** n):
    bin_state = bin(state)
    str_bin_state = str(bin_state)[2:]
    str_bin_state = (n - len(str_bin_state)) * "0" + str_bin_state
    boolean_sentences = [bool(int(i)) for i in str_bin_state]
    check_rules(boolean_sentences)
    state += 1

parse_results = get_rules(1, False, given_result)
terms_result = list(all_used_terms)
_type = parse_results[0]["type"]


for item in terms_result:
    if item not in list_sentences:
        if _type == "pure":
            print("False")
            break
    else:
        index = list_sentences.index(item)
        for j in range(len(satisfying_rules)):
            if not satisfying_rules[j][index]:
                if _type == "pure":
                    print("False")
                    exit()
        else:
            if _type == "or":
                print("True")
                break
else:
    if _type == "pure":
        print("True")
    else:
        print("False")

