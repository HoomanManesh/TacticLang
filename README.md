# TacticLang


A soccer-inspired programming language where coding constructs map to football tactics, so writing and reading code feels like drawing up plays and narrating a match.



🚀 Features

Soccer-themed syntax 
  - `pass` (`+`), `passBack` (`–`), `cross` (`*`), `crossBack` (`/`), `feint` (`%`)  
  - `kickoff(init; cond; update){…}` loops  
  - `when(cond){…}`, `otherwiseIf(cond){…}`, `otherwise{…}` conditionals  
  - `commentatorSay(expr);` prints play-by-play lines  

Built-in helpers  
  - `startMatch();` picks a random formation  
  - `randomStep()` → random minute 1–45  

Audio integration 
  - Launch your stadium ambience MP3 via `startMatch();`  

Error handling
  - Clear syntax errors with line numbers  
  - Catches runtime exceptions and reports them  

---

🛠 Getting Started

Prerequisites

Python 3.8+  
- (Optional) A media player registered for `.mp3` if you use the audio feature  

Installation

1. Clone the repo  
   ```bash
   git clone https://github.com/HoomanManesh/HoomanManesh.github.io.git
   cd HoomanManesh.github.io/TactiCLang
2. Ensure your MP3 (e.g. soccer-stadium.mp3) lives here if you want ambience.

3. Make the interpreter executable

bash
Always show details

Copy
chmod +x interpreter.py


▶️ Usage
Save your TacticLang source in a .tac file, for example HelloWorld.tac:

tactica
Always show details

Copy
commentatorSay("Hello, TactiCLang World!");
Then run:

bash
Always show details

Copy
python interpreter.py HelloWorld.tac
You should see:

yaml
Always show details

Copy
🎙️ Commentator: Hello, TactiCLang World!
📖 Language Overview
Key Statements
ebnf
Always show details

Copy
<startMatchStmt>   -> startMatch();  
<varDecl>          -> let x = expr;  
<printStmt>        -> commentatorSay(expr);  
<loopStmt>         -> kickoff(init; cond; update){ … }  
<ifElseStmt>       -> when(cond){…} {otherwiseIf(cond){…}} [otherwise{…}]
Soccer-Ops
TactiCLang	Python
pass	+
passBack	-
cross	*
crossBack	/
feint	%

📂 Examples
HelloWorld.tac – prints a greeting

Arithmetic.tac – demos +, -, *, /, %

LoopDemo.tac – for-loop via kickoff

IfElseDemo.tac – when/otherwiseIf/otherwise

FizzBuzz.tac – “tiki/taka/tikitaka” from 1–100

FootballSummary.tac – concise match recap

PenaltyShootout.tac – simulates spot kicks

StartingXI.tac – lists players 1–11 and picks a captain

🤝 Contributing
Fork the repo

Create a feature branch (git checkout -b feature/my-feature)

Commit your changes (git commit -am 'Add my feature')

Push to the branch (git push origin feature/my-feature)

Open a Pull Request

📜 License
This project is released under the MIT License. See LICENSE for details.

Designed and developed by Hooman Manesh 


