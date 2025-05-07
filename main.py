import json
from collections import deque

def postfix(expresie):
    ordine = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
    expresie_postfixata = []
    stiva_operatori = []

    expresie_concat = []
    for i in range(len(expresie)):
        caracter = expresie[i]
        expresie_concat.append(caracter)
        if i + 1 < len(expresie):
            urmatorul = expresie[i + 1]
            if (caracter not in '(|' and urmatorul not in ')*+?|') or (caracter in ')*+?' and urmatorul not in ')*+?|'):
                expresie_concat.append('.')
    expresie = ''.join(expresie_concat)

    for caracter in expresie:
        if caracter == '(':
            stiva_operatori.append(caracter)
        elif caracter == ')':
            while stiva_operatori[-1] != '(':
                expresie_postfixata.append(stiva_operatori.pop())
            stiva_operatori.pop()
        elif caracter in ordine:
            while stiva_operatori and stiva_operatori[-1] != '(' and ordine[caracter] <= ordine[stiva_operatori[-1]]:
                expresie_postfixata.append(stiva_operatori.pop())
            stiva_operatori.append(caracter)
        else:
            expresie_postfixata.append(caracter)

    while stiva_operatori:
        expresie_postfixata.append(stiva_operatori.pop())

    return ''.join(expresie_postfixata)


class Stare:
    def __init__(self):
        self.tranzitii = []
        self.epsilon = []


def construieste_NFA(postfix):
    stiva = []

    for caracter in postfix:
        if caracter == '.':
            nfa2 = stiva.pop()
            nfa1 = stiva.pop()
            nfa1['final'].epsilon.append(nfa2['initial'])
            stiva.append({'initial': nfa1['initial'], 'final': nfa2['final']})
        elif caracter == '|':
            nfa2 = stiva.pop()
            nfa1 = stiva.pop()
            initial = Stare()
            final = Stare()
            initial.epsilon.extend([nfa1['initial'], nfa2['initial']])
            nfa1['final'].epsilon.append(final)
            nfa2['final'].epsilon.append(final)
            stiva.append({'initial': initial, 'final': final})
        elif caracter == '*':
            nfa = stiva.pop()
            initial = Stare()
            final = Stare()
            initial.epsilon.extend([nfa['initial'], final])
            nfa['final'].epsilon.extend([nfa['initial'], final])
            stiva.append({'initial': initial, 'final': final})
        elif caracter == '+':
            nfa = stiva.pop()
            initial = Stare()
            final = Stare()
            initial.epsilon.append(nfa['initial'])
            nfa['final'].epsilon.extend([nfa['initial'], final])
            stiva.append({'initial': initial, 'final': final})
        elif caracter == '?':
            nfa = stiva.pop()
            initial = Stare()
            final = Stare()
            initial.epsilon.extend([nfa['initial'], final])
            nfa['final'].epsilon.append(final)
            stiva.append({'initial': initial, 'final': final})
        else:
            initial = Stare()
            final = Stare()
            initial.tranzitii.append((final, caracter))
            stiva.append({'initial': initial, 'final': final})

    return stiva.pop()


def acces_prin_e(stari):
    stari_accesibile = set(stari)
    stiva = list(stari)

    while stiva:
        stare = stiva.pop()
        for eps_stare in stare.epsilon:
            if eps_stare not in stari_accesibile:
                stari_accesibile.add(eps_stare)
                stiva.append(eps_stare)
    return stari_accesibile


def simuleaza_NFA(nfa, string):
    curent = acces_prin_e({nfa['initial']})

    for simbol in string:
        urmator = set()
        for stare in curent:
            for tranzitie in stare.tranzitii:
                if tranzitie[1] == simbol:
                    urmator.add(tranzitie[0])
        curent = acces_prin_e(urmator)
        if not curent:
            return False

    return nfa['final'] in curent


class DFAState:
    def __init__(self, stari_nfa):
        self.stari_nfa = frozenset(stari_nfa)
        self.transitions = {}
        self.is_final = False


def nfa_to_dfa(nfa):

    simboluri = set()
    stari_nfa = set()

    def colecteaza_stari(stare):
        if stare in stari_nfa:
            return
        stari_nfa.add(stare)
        for s, simbol in stare.tranzitii:
            simboluri.add(simbol)
            colecteaza_stari(s)
        for s in stare.epsilon:
            colecteaza_stari(s)

    colecteaza_stari(nfa['initial'])
    simboluri.discard('')

    stari_initiale_prin_e = frozenset(acces_prin_e({nfa['initial']}))
    stari_dfa = {}
    dfa_initial = DFAState(stari_initiale_prin_e)
    dfa_initial.is_final = nfa['final'] in stari_initiale_prin_e
    stari_dfa[stari_initiale_prin_e] = dfa_initial

    queue = deque([dfa_initial])

    while queue:
        stare_dfa = queue.popleft()
        for simbol in simboluri:
            urm_nfa = set()
            for stare_nfa_compusa in stare_dfa.stari_nfa:
                for next, tranz in stare_nfa_compusa.tranzitii:
                    if tranz == simbol:
                        urm_nfa.update(acces_prin_e({next}))
            if not urm_nfa:
                continue
            stare_noua_de_adaugat = frozenset(urm_nfa)
            if stare_noua_de_adaugat not in stari_dfa:
                new_dfa = DFAState(stare_noua_de_adaugat)
                new_dfa.is_final = nfa['final'] in stare_noua_de_adaugat
                stari_dfa[stare_noua_de_adaugat] = new_dfa
                queue.append(new_dfa)
            stare_dfa.transitions[simbol] = stari_dfa[stare_noua_de_adaugat]

    return dfa_initial


def simuleaza_DFA(dfa_initial, string):
    curent = dfa_initial
    for simbol in string:
        if simbol not in curent.transitions:
            return False
        curent = curent.transitions[simbol]
    return curent.is_final


def ruleaza_teste():
    with open('teste.json', 'r') as file:
        teste = json.load(file)

    for test in teste:
        print(f"\nTest: {test['name']}")
        print(f"Regex: {test['regex']}")

        try:
            post = postfix(test['regex'])
            print(f"Postfix: {post}")

            nfa = construieste_NFA(post)

            print("Testare NFA:")
            for string in test['test_strings']:
                input = string['input']
                expected = string['expected']
                rezultat = simuleaza_NFA(nfa, input)
                print(f"  '{input}': {expected} -> {rezultat}")

            print("Testare DFA:")
            dfa = nfa_to_dfa(nfa)
            for string in test['test_strings']:
                input = string['input']
                expected = string['expected']
                rezultat = simuleaza_DFA(dfa, input)
                print(f"  '{input}': {expected} -> {rezultat}")



        except Exception as e:
            print(f"Eroare: {str(e)}")


if __name__ == "__main__":
    ruleaza_teste()
