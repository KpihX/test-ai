% Knowledge base for nouns, pronouns, verbs(transitive and intransitive)
proper_noun(mary,marys).
proper_noun(henry,henrys).

intransitive_verb(runs,run).
intransitive_verb(sits,sit).

transitive_verb(gives,give).
transitive_verb(reads,read).


:-consult('kb_nouns').
:-consult('kb_pronouns').
:-consult('kb_determiners').


sentence(sentence(NP,VP)) --> noun_phrase(Num,NP), verb_phrase(Num,VP).

noun_phrase(Num,noun_phrase(PN)) --> proper_noun(Num,PN).
noun_phrase(Num,NP) -->
   determiner(Det),
   noun(Num,N),
   rel(Num,Rel),
   {build_np(Det,N,Rel,NP)}. /* embedded Prolog goal */

/* Prolog rules eor build_np */
build_np(Det,N,rel(nil),noun_phrase(Det,N)).
build_np(Det,N,rel(RP,VP),noun_phrase(Det,N,rel(RP,VP))).

verb_phrase(Num,verb_phrase(TV,NP)) -->
              transitive_verb(Num,TV), 
              noun_phrase(_,NP).
verb_phrase(Num,verb_phrase(IV)) --> intransitive_verb(Num,IV).

rel(_Num,rel(nil)) --> [].
rel(Num,rel(RP,VP)) -->
             relative_pronoun(RP), verb_phrase(Num,VP).

proper_noun(sing,proper_noun(PN)) --> [PN], {proper_noun(PN,_X)}.
proper_noun(plu,proper_noun(PN)) --> [PN], {proper_noun(_X,PN)}.


relative_pronoun(relative_pronoun(RPN)) --> [RPN], {relative_pronoun(RPN)}.


intransitive_verb(sing,intransitive_verb(IV)) -->[IV], {intransitive_verb(IV,_X)}.
intransitive_verb(plu,intransitive_verb(IV)) --> [IV], {intransitive_verb(_X,IV)}.


determiner(determiner(DET)) --> [DET], {determiner(DET)}.

noun(sing,noun(N)) --> [N], {noun(N,_X)}.
noun(plu,noun(N)) --> [N], {noun(_X,N)}.

transitive_verb(sing,transitive_verb(TV)) --> [TV], {transitive_verb(TV,_X)}.
transitive_verb(plu,transitive_verb(TV)) --> [TV], {transitive_verb(_X,TV)}.

:- ['read_line'].

parse :- write('Enter English input: '),
         read_line(Input),
         trim_period(Input,I),
         nl,
         sentence(Parse_form,I,[]),
         write(Parse_form), 
         nl, nl.

trim_period([.],[]).     
trim_period([X|R],[X|T]) :- trim_period(R,T).
