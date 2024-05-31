% Prédicat pour vérifier si la chaîne d'entrée est sous la forme 'souschaine1*souschaine2'
check_qro_format(Str) :-
    % Séparer la chaîne en deux sous-chaînes basées sur l'étoile
    split_string(Str, "*", "", SubStrList),
    % Vérifier qu'il y a exactement deux sous-chaînes
    length(SubStrList, 2),
    % Extraire les sous-chaînes
    nth0(0, SubStrList, Subchain1),
    nth0(1, SubStrList, Subchain2),
    % Vérifier que souschaine1 se termine par un point d'interrogation
    string_ends_with(Subchain1, "?"),
    % Vérifier que les sous-chaînes ne sont pas vides
    not(Subchain1 = ""),
    not(Subchain2 = ""),
    % Si tout est correct, afficher true
    format('True~n').

check_qro_format(_) :-
    % Si une vérification échoue, afficher false
    format('False~n').
    %, fail.

% Prédicat auxiliaire pour vérifier si une chaîne se termine par un certain caractère
string_ends_with(Str, End) :-
    sub_string(Str, _, Length, 0, End),
    Length > 0.
