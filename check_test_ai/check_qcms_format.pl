% Prédicat pour vérifier si la chaîne d'entrée correspond au format QCM
check_qcms_format(QCMStr, NumQuestions, NumProps) :-
    % Séparer la chaîne QCM en questions individuelles
    split_string(QCMStr, "+", "", QuestionList),
    % Vérifier si le nombre de questions correspond
    length(QuestionList, NumQuestions),
    % Vérifier le format de chaque question
    maplist(check_question_format(NumProps), QuestionList),
    % Si tout est correct, afficher true
    format('True~n').
check_qcms_format(_, _, _) :-
    % Si une vérification échoue, afficher false
    format('False~n').
    %, fail.

% Prédicat pour vérifier le format de chaque question individuelle
check_question_format(NumProps, Question) :-
    % Séparer la chaîne de question en question et propositions
    split_string(Question, "*", "", [Q|Props]),
    % Vérifier si le nombre de propositions correspond
    length(Props, NumProps),
    % Optionnellement, vérifier que la partie question n'est pas vide
    not(Q = "").

% Prédicat auxiliaire pour diviser les chaînes sans champs vides
split_string(Str, Delim, SubStrings) :-
    split_string(Str, Delim, "", SubStrList),
    exclude(=(""), SubStrList, SubStrings).
