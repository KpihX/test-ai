% Prédicat principal pour transformer un texte en liste de phrases
text_to_sentences(Text, Sentences) :-
    % Remplacer les sauts de ligne par des espaces
    replace_newlines(Text, CleanedText),
    % Diviser le texte en phrases en utilisant la ponctuation comme délimiteur
    split_string(CleanedText, ".!?", "", RawSentences),
    % Filtrer les phrases vides et nettoyer les espaces superflus
    filter_empty_sentences(RawSentences, FilteredSentences),
    trim_sentences(FilteredSentences, Sentences).

% Prédicat pour remplacer les sauts de ligne par des espaces
replace_newlines(Text, CleanedText) :-
    split_string(Text, "\n", "", Lines),
    atomics_to_string(Lines, " ", CleanedText).

% Prédicat pour filtrer les phrases vides
filter_empty_sentences([], []).
filter_empty_sentences([Sentence | Rest], FilteredSentences) :-
    (   Sentence = ""
    ->  filter_empty_sentences(Rest, FilteredSentences)
    ;   FilteredSentences = [Sentence | Tail],
        filter_empty_sentences(Rest, Tail)
    ).

% Prédicat pour supprimer les espaces superflus en début et fin de phrase
trim_sentences([], []).
trim_sentences([Sentence | Rest], [TrimmedSentence | TrimmedRest]) :-
    string_chars(Sentence, Chars),
    trim_chars(Chars, TrimmedChars),
    string_chars(TrimmedSentence, TrimmedChars),
    trim_sentences(Rest, TrimmedRest).

% Prédicat auxiliaire pour supprimer les espaces en début et fin de liste de caractères
trim_chars(Chars, TrimmedChars) :-
    remove_leading_spaces(Chars, LeadingTrimmedChars),
    reverse(LeadingTrimmedChars, Reversed),
    remove_leading_spaces(Reversed, ReversedTrimmedChars),
    reverse(ReversedTrimmedChars, TrimmedChars).

% Prédicat auxiliaire pour supprimer les espaces en début de liste de caractères
remove_leading_spaces([' ' | Rest], TrimmedChars) :- remove_leading_spaces(Rest, TrimmedChars).
remove_leading_spaces(Chars, Chars).

% Exemple d'utilisation
example :-
    Text = "Ceci est la première phrase. Voici la deuxième phrase ! Et enfin, la troisième phrase ?",
    text_to_sentences(Text, Sentences),
    write("Phrases extraites :"), nl,
    write_sentences(Sentences).

% Prédicat pour afficher les phrases
write_sentences([]).
write_sentences([Sentence | Rest]) :-
    writeln(Sentence),
    write_sentences(Rest).