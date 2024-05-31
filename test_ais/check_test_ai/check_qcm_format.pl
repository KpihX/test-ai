% Prédicat pour vérifier si la chaîne d'entrée correspond au format spécifié
check_qcm_format(Str, NumProps) :-
    % Séparer la chaîne en sous-chaînes basées sur l'étoile
    split_string(Str, "*", "", SubStrList),
    % Calculer le nombre attendu de sous-chaînes
    ExpectedLength is NumProps + 2,
    % Vérifier si le nombre de sous-chaînes est correct
    length(SubStrList, ExpectedLength),
    % Extraire la première sous-chaîne
    nth0(0, SubStrList, FirstSubStr),
    % Vérifier que la première sous-chaîne se termine par un point d'interrogation
    string_ends_with(FirstSubStr, "?"),
    % Extraire la deuxième sous-chaîne
    nth0(1, SubStrList, SecondSubStr),
    % Vérifier que la deuxième sous-chaîne est un entier valide
    is_integer_in_range(SecondSubStr, NumProps),
    % Vérifier que toutes les sous-chaînes ne sont pas vides
    maplist(not_empty, SubStrList),
    % Si tout est correct, afficher true
    format('True~n').

check_qcm_format(_, _) :-
    % Si une vérification échoue, afficher false
    format('False~n').
    %, fail.

% Prédicat auxiliaire pour vérifier si une chaîne se termine par un certain caractère
string_ends_with(Str, End) :-
    sub_string(Str, _, Length, 0, End),
    Length > 0.

% Prédicat auxiliaire pour vérifier qu'une chaîne n'est pas vide
not_empty(Str) :-
    not(Str = "").

% Prédicat auxiliaire pour vérifier si une chaîne représente un entier dans une plage donnée
is_integer_in_range(Str, RangeEnd) :-
    % Convertir la chaîne en entier
    number_string(Int, Str),
    % Vérifier si l'entier est dans la plage [1, RangeEnd]
    between(1, RangeEnd, Int).
