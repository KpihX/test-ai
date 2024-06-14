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

% Fonction de vérification de la cohérence de deux questions
check_questions(Question1, Question2) :-
    check_sentence(Question1),
    check_sentence(Question2),
    can_follow(Question1, Question2),
    !,
    write('Les questions sont cohérentes.').
check_questions(_, _) :-
    write('Les questions ne sont pas cohérentes.').

% Règles de logique pour les questions
can_follow(Q1, Q2) :-
    % Exemple : "Bonjour" peut être suivi de "Comment ça va ?"
    (ends_with(Q1, "Bonjour."), starts_with(Q2, "Comment")).
    % Ajoutez d'autres règles logiques selon vos besoins.

% Vérifie si une phrase commence par un mot donné
starts_with(Sentence, Word) :-
    atom_chars(Sentence, Chars),
    atom_chars(Word, WordChars),
    append(WordChars, _, Chars).

% Vérifie si une phrase se termine par un mot donné
ends_with(Sentence, Word) :-
    atom_chars(Sentence, Chars),
    atom_chars(Word, WordChars),
    append(_, WordChars, Chars).

% Fonction de vérification de la cohérence d'une phrase
check_sentence(Sentence) :-
    atom_chars(Sentence, Chars),
    phrase(sentence(S), Chars),
    !.
check_sentence(_) :-
    fail.

% Exemple d'utilisation
% ?- check_questions("Bonjour.", "Comment ça va ?").
