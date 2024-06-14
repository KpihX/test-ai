:- consult('sent_to_svc.pl').
:- consult('text_to_sent.pl').

text_to_svc(Text, SVCList) :-
    text_to_sentences(Text, Sentences),
    sentences_to_svc(Sentences, SVCList).

sentences_to_svc([], []).
sentences_to_svc([Sentence | Rest], SVCList) :-
    split_string(Sentence, " ", "", WordList),
    parse_sentence(WordList, Subject, Verb, Complement),
    sentences_to_svc(Rest, RestSVCList),
    append([[Subject, Verb, Complement]], RestSVCList, SVCList).

% Exemple d'utilisation
example_svc :-
    Text = "John eats an apple. Mary sees the dog. The cat likes meat.",
    text_to_svc(Text, SVCList),
    write("Liste des triplets Sujet-Verbe-Complément :"), nl,
    write_svc_list(SVCList).

write_svc_list([]).
write_svc_list([SVC | Rest]) :-
    write(SVC), nl,
    write_svc_list(Rest).

% Test individuel pour text_to_sentences/2
test_text_to_sentences :-
    Text = "John eats an apple. Mary sees the dog. The cat likes meat.",
    text_to_sentences(Text, Sentences),
    write("Phrases extraites :"), nl,
    write_sentences(Sentences).

% Test individuel pour parse_sentence/4
test_parse_sentence :-
    Sentence = "John eats an apple",
    split_string(Sentence, " ", "", WordList),
    parse_sentence(WordList, Subject, Verb, Complement),
    write("Sujet : "), write(Subject), nl,
    write("Verbe : "), write(Verb), nl,
    write("Complément : "), write(Complement), nl.