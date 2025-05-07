// Soccer Match Summary (unique, chronological goals, zero-based loops)
startMatch();

// 1) Randomize how many goals each team scores (0–5)
let homeGoals = randomStep() feint 6;
let awayGoals = randomStep() feint 6;

// (Interpreter will inject these Python lines right here:)
// homeMinutes = sorted(random.sample(range(1,91), homeGoals))
// awayMinutes = sorted(random.sample(range(1,91), awayGoals))

// 2) Announce home goals (i = 0 … homeGoals-1)
kickoff(i = 0; i < homeGoals; i++) {
    commentatorSay("Goal! Home at minute " pass homeMinutes[i]);
}

// 3) Announce away goals (j = 0 … awayGoals-1)
kickoff(j = 0; j < awayGoals; j++) {
    commentatorSay("Goal! Away at minute " pass awayMinutes[j]);
}

// 4) Final score summary
commentatorSay(
  "Full-time Final Score: " pass homeGoals pass "-" pass awayGoals
);
