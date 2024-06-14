% Règles pour la structure de base d'une phrase
sentence(S) :- subject(S), predicate(S).
subject(S) :- noun_phrase(S).
predicate(S) :- verb_phrase(S).

% Règles pour les phrases nominales
noun_phrase(NP) :- determiner(NP), noun(NP).
noun_phrase(NP) :- proper_noun(NP).

% Règles pour les phrases verbales
verb_phrase(VP) :- verb(VP).
verb_phrase(VP) :- verb(VP), noun_phrase(VP).

% Déterminants en anglais
determiner(the).
determiner(a).

% Noms en anglais
noun(apple).
noun(book).
noun(cat).
noun(dog).

% Verbes en anglais
verb(eats).
verb(reads).
verb(chases).
verb(sleeps).

% Noms propres en anglais
proper_noun(john).
proper_noun(mary).
proper_noun(susan).

% Fonction de vérification de la cohérence d'une phrase
check_sentence(Sentence) :-
    atom_chars(Sentence, Chars),
    phrase(sentence(S), Chars),
    !,
    write('La phrase est cohérente.').
check_sentence(_) :-
    write('La phrase est incohérente.').

% Exemple d'utilisation
% check_sentence("John eats an apple.").
