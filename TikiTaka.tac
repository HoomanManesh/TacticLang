startMatch();


// FizzBuzz in TacticaLang: tiki (3), taka (5), tikitaka (both)
kickoff(i = 1; i <= 100; i++) {
  when (i feint 15 == 0) {
    commentatorSay("TikiTaka");
  }
  otherwiseIf (i feint 3 == 0) {
    commentatorSay("Tiki");
  }
  otherwiseIf (i feint 5 == 0) {
    commentatorSay("Taka");
  }
  otherwise {
    commentatorSay(i);
  }
}
