% Prédicat pour vérifier si la chaîne d'entrée est sous la forme 'str1*...*strn', 
% avec n quelconque, et chaque stri non vide et se terminant par un point
check_facts_format(Str) :-
    % Séparer la chaîne en sous-chaînes basées sur l'étoile
    split_string(Str, "\n", "", SubStrList),
    % Vérifier que chaque sous-chaîne est non vide et se termine par un point
    maplist(string_ends_with_period_and_not_empty, SubStrList),
    % Si tout est correct, afficher true
    format('True~n').

check_facts_format(_) :-
    % Si une vérification échoue, afficher false
    format('False~n').

% Prédicat auxiliaire pour vérifier si une chaîne se termine par un point et n'est pas vide
string_ends_with_period_and_not_empty(Str) :-
    not(Str = ""),
    string_ends_with(Str, ".").

% Prédicat auxiliaire existant pour vérifier si une chaîne se termine par un certain caractère
string_ends_with(Str, End) :-
    sub_string(Str, _, Length, 0, End),
    Length > 0.