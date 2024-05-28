% Définition de la grammaire avec DCG
sentence --> subject, predicate.
subject --> noun_phrase.
predicate --> verb_phrase.

noun_phrase --> determiner, noun.
noun_phrase --> proper_noun.

verb_phrase --> verb.
verb_phrase --> verb, noun_phrase.

determiner --> [the].
determiner --> [a].

noun --> [apple].
noun --> [book].
noun --> [cat].
noun --> [dog].

verb --> [eats].
verb --> [reads].
verb --> [chases].
verb --> [sleeps].

proper_noun --> [john].
proper_noun --> [mary].
proper_noun --> [susan].

% Vérifie si une phrase est cohérente
check_sentence(Sentence) :-
    atom_string(SentenceAtom, Sentence),
    split_string(SentenceAtom, " ", "", SentenceList),
    phrase(sentence, SentenceList).

% Vérifie si deux phrases peuvent se suivre logiquement
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

% Vérifie si une phrase commence par un mot donné
starts_with(Sentence, Word) :-
    atom_string(SentenceAtom, Sentence),
    split_string(SentenceAtom, " ", "", SentenceList),
    SentenceList = [FirstWord | _],
    atom_string(Word, FirstWord).

% Vérifie si une phrase se termine par un mot donné
ends_with(Sentence, Word) :-
    atom_string(SentenceAtom, Sentence),
    split_string(SentenceAtom, " ", "", SentenceList),
    last(SentenceList, LastWord),
    atom_string(Word, LastWord).

% Exemple d'utilisation
% ?- check_sentence("john eats an apple").
% ?- check_questions("Bonjour.", "Comment ça va ?").
