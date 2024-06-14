% Determiners
det(the).
det(a).
det(an).

% Common Nouns
noun(dog).
noun(cat).
noun(man).
noun(woman).

% Proper Nouns
proper_noun(john).
proper_noun(mary).

% Verbs
verb(eats).
verb(likes).
verb(sees).

% Complements (objects of verbs)
comp(apple).
comp(meat).
comp(with, the, cat).

% Noun Phrase
np([Det, Noun]) --> [Det], {det(Det)}, [Noun], {noun(Noun)}.
np([ProperNoun]) --> [ProperNoun], {proper_noun(ProperNoun)}.

% Verb Phrase
vp([Verb, Comp]) --> [Verb], {verb(Verb)}, [Comp], {comp(Comp)}.
vp([Verb, Det, Comp]) --> [Verb], {verb(Verb)}, [Det], {det(Det)}, [Comp], {comp(Comp)}.

% Sentence
s([NP, VP]) --> np(NP), vp(VP).


% Main parser
parse_sentence(Sentence, Subject, Verb, Complement) :-
    phrase(s([NP, VP]), Sentence),
    find_subject(NP, Subject),
    find_verb(VP, Verb),
    find_comp(VP, Complement).

% Find the subject
find_subject([Det, Noun], [Det, Noun]) :- det(Det), noun(Noun).
find_subject([ProperNoun], [ProperNoun]) :- proper_noun(ProperNoun).

% Find the verb
find_verb([Verb | _], Verb) :- verb(Verb).

% Find the complement
find_comp([_, Comp], Comp) :- comp(Comp).
find_comp([_, Det, Comp], [Det, Comp]) :- det(Det), comp(Comp).

% Example usage
parse_and_display(Sentence) :-
    parse_sentence(Sentence, Subject, Verb, Complement),
    format('Subject: ~w~n', [Subject]),
    format('Verb: ~w~n', [Verb]),
    format('Complement: ~w~n', [Complement]).
