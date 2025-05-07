# Regex_To_NFA_To_DFA

Regex_To_NFA_To_DFA este un proiect scris în Python, care transformă o expresie regulată în forma postfixată, folosind algoritmul Shunting Yard. Mai apoi, din forma postfixată se construiește un NFA, utilizând algoritmul lui Thompson. La final, NFA-ul este transformat în DFA, aplicând Subset Construction. 


## Regex » Forma postfixată

* Reținem într-un dicționar eventualele simboluri, alături de prioritățile lor. Ordinea priorităților este următoarea: stelare ( * ), repetare de una sau mai multe ori ( + ),  
prezență opțională ( ? ), concatenare ( . ) și alternare ( | ).

* Deoarece în expresiile primite ca input este posibil ca simbolul concatenării să nu apară explicit, îl vom adăuga noi unde este cazul. Ca de exemplu: între două litere, după un operator singular, între două parenteze, etc. Așadar în loc de "ab", algoritmul va prelucra "a.b".

* După ce expresia este gata de prelucrat, vom aplica algoritmul Shunting Yard.

* În funcție de caracterul primit, vom lua decizia de prelucrare, folosindu-ne de o stivă. Dacă caracterul curent este "(", îl inserăm în stivă. Pentru ")" scoatem operatorii din stivă până la "(" și adăugăm la finalul string-ului care reține expresia finală. Literele se adaugă direct la expresia finală. Restul operatorilor scot de pe stivă pe cei cu prioritate mai mare sau egală, aceștia fiind adăgați la expresia finală. După ce toți operatorii cu prioritate mai mare au fost eliminați de pe stivă, simbolul curent este introdus.

* La finalul parcurgerii expresiei regulate, și după golirea stivei, string-ul în care reținem expresia finală va conține exact Regex-ul inițial în forma postfixată.


## Formă postfixată » NFA

* Acest cod construiește un Automat Finit Nedeterminist (NFA), utilizând metoda lui Thompson. Această metodă este eficientă și modulară, permițând construcția NFA-ului prin combinarea sub-automatelor corespunzătoare subexpresiilor.

* Fiecare caracter din expresia postfixată este procesat și se urmăresc pașii:

     1. Dacă este un simbol din alfabet, pe stivă se încarcă un NFA simplu cu două stări și o tranziție.
     2. Dacă este un operator, se scot de pe stivă unul sau două NFA-uri în funcție de operație (unul pentru '*', '+', '?' și două pentru '.' sau '|' ). NFA-urile eliminate sunt prelucrate în funcție de operația corespunzătoare, iar NFA-ul returnat este introdus în stivă.
     3. La final, stiva conține un singur automat, care este fix NFA-ul corespunzator Expresiei postfixate din input.


## NFA » DFA

* Acest cod implementează algoritmul subset construction pentru a converti un Automat Finit Nedeterminist (NFA) într-un Automat Finit Determinist (DFA) echivalent.

* La început este nevoie să cunoaștem simbolurile din NFA, așadar o varintă ar fi să parcurgem NFA-ul și să reținem literele din alfabet pe care le-am întâlnit.

* Starea inițială a DFA-ului este compusă din starea inițială a NFA-ului și toate stările care pot fi accesate din starea inițială prin lambda-mișcări.

* Folosind o coadă, procesăm toate stările nou create. Pentru fiecare simbol, calculăm următoarea stare. Dacă starea nu există deja, o construim și o adăugăm în coadă.

* O stare în DFA este finală, dacă conține cel puțin o stare finală din NFA.



## Structura codului

* Fiecare etapă de mai sus este cuprinsă în funcții independente. Pe lângă aceste funcții apar și câteva funcții ajutătoare, pentru testare, atât a NFA-ului, cât si a DFA-ului.

* Datele sunt testate cu ajutorul testelor din fișierul teste.json, atașate repository-ului.

## Instrucțiuni de rulare

* Rulează fișierul main.py, rezultatele vor fi afișate în consolă.
* Fișierul teste.json trebuie să se afle în același director cu celelalte fișiere.
