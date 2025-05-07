// Soccer Match Summary (no guaranteed tie)
startMatch();

// 1) Randomize how many goals each team scores (0–5)
let homeGoals = randomStep() feint 6;
let awayGoals = randomStep() feint 6;

// 2) Announce each goal at its own random minute
//    (minutes 1–90)
kickoff(i = 1; i <= homeGoals; i++) {
  let m = randomStep() pass 45;      
  commentatorSay("Goal! Home at minute " pass m);
}
kickoff(j = 1; j <= awayGoals; j++) {
  let m = randomStep() pass 45;      
  commentatorSay("Goal! Away at minute " pass m);
}

// 3) Final score summary
commentatorSay(
  "Full-time Final Score: " pass homeGoals pass "-" pass awayGoals
);
