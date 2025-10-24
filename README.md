<a id="readme-top"></a>

<div align="center">
  <h1>🐫 Camel Up</h1>
  <p>A Python implementation of the board game Camel Up with AI probability analysis</p>

  [![Python][Python]][Python-url]
  [![Colorama][Colorama]][Colorama-url]
</div>

---

## Table of Contents

<details>
  <summary>Expand</summary>a
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#game-overview">Game Overview</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#algorithms-explained">Algorithms Explained</a></li>
    <li><a href="#how-to-run">How To Run</a></li>
    <li><a href="#game-mechanics">Game Mechanics</a></li>
    <li><a href="#code-examples">Code Examples</a></li>
    <li><a href="#key-features">Key Features</a></li>
  </ol>
</details>

---

## About The Project

**Camel Up** is a digital implementation of the popular board game where players make strategic bets on which colored camels will finish in first and second place during a race. The project combines game simulation with sophisticated **probability analysis** using two different approaches:

1. **Enumerative Analysis** - Calculates *exact* probabilities by testing every possible dice roll sequence
2. **Experimental Analysis** - Estimates probabilities using Monte Carlo simulation with random trials

This project is perfect for understanding game theory, probability calculations, and algorithm design.

### Live Gameplay Example
```
🌴 p  g  y  r  b     |🏁    ← Red camel is in 1st place (rightmost position)
🌴          g        |🏁    ← Green camel is stacked on top of Yellow
🌴 p  y  r  b        |🏁    ← Other positions
```

---

## Game Overview

### The Game Rules (Simplified)

**Setup:**
- 5 colored camels (Red, Blue, Green, Yellow, Purple) start at random positions on a 16-space track
- Each camel color has betting tickets worth [5, 3, 2, 2] coins
- Players start with 3 coins each

**Turn Structure:**
- Players alternate turns, choosing to either:
  - **BET (B)**: Place a betting ticket on a camel color
  - **ROLL (R)**: Shake the pyramid to roll a die

**Rolling Dice:**
- Rolling a die shows a color and value (1, 2, or 3)
- That camel moves that many spaces forward
- **IMPORTANT**: Any camel stacked on top moves with it!

**Stacking:**
- When a camel is passed by another camel, it gets stacked on top
- Stacked camels move together as a group

**Leg End:**
- When all 5 dice have been rolled, the leg ends
- 1st place camel: Correct bettors win the ticket value
- 2nd place camel: Correct bettors win 1 coin
- Wrong bet: Lose 1 coin

**Win a Die Roll:** Earn 1 coin for rolling (incentive to roll vs. bet)

---

## Project Structure

```
camel_up/
├── CamelUpGame.py          # Main game controller & player interactions
├── CamelUpBoard.py         # Board state, camel movement & probability algorithms
├── CamelUpPlayer.py        # Player data model (money, bets)
├── getAIMove.py            # AI decision-making utilities (optional extension)
├── demos/
│   └── deepcopy_demo.py    # Educational demo on Python deep copying
└── README.md               # This file
```

### File Responsibilities

| File | Purpose | Key Methods |
|------|---------|------------|
| `CamelUpGame.py` | Game orchestration & UI | `play_1_leg()`, `get_player_move()`, `leg_payouts_and_results()` |
| `CamelUpBoard.py` | Game state & algorithms | `move_camel()`, `run_enumerative_leg_analysis()`, `run_experimental_leg_analysis()` |
| `CamelUpPlayer.py` | Player state | `win_money()`, `add_bet()`, `reset_tickets()` |
| `demos/deepcopy_demo.py` | Learning resource | Demo of state preservation via deep copy |

---

## Algorithms Explained

This section explains the core algorithms. **Don't worry if you haven't worked on this in a while** — these explanations start from scratch!

### 1. Camel Movement Algorithm ⬆️

**What it does:** When a die is rolled (e.g., Red-2), move the red camel 2 spaces forward, along with any camels stacked on top.

**The Challenge:** Camels can stack on top of each other. If a camel moves, ALL camels riding on top move with it.

**Data Structure:**
```python
# Track is a list of 16 positions
# Each position contains a list of camels (top to bottom)
track = [
    [],           # Position 0: Empty
    ['r'],        # Position 1: Red camel alone
    ['y', 'b'],   # Position 2: Yellow on bottom, Blue stacked on top
    ['g'],        # Position 3: Green camel
    # ... more positions
]
```

**Algorithm Steps:**

```python
def move_camel(self, die: tuple[str, int]) -> list[list[str]]:
    """Move a camel and all camels stacked on top of it"""
    color, roll = die  # Example: ('r', 2)

    # Step 1: Find the camel's current position
    for position in range(len(self.track)):
        for i in range(len(self.track[position])):
            if self.track[position][i] == color:

                # Step 2: Move the camel and everything on top of it
                #  (i is the index of our camel, everything from i onwards goes with it)
                for k in range(i, len(self.track[position])):
                    new_position = position + roll
                    if new_position < 16:
                        self.track[new_position].append(self.track[position][k])

                # Step 3: Remove the camel(s) from the old position
                self.track[position] = self.track[position][:i]
                return self.track
```

**Example:**
```
Before: Position 2 has ['y', 'b']  (Blue stacked on Yellow)
Roll:   Red-2 is rolled (Red is at position 1)
After:  Red moves from position 1 to position 3
Result: Red now in position 3 alone

If Yellow at position 2 rolled 2:
Before: track[2] = ['y', 'b']
After:  track[2] = []  (Yellow and Blue removed)
        track[4] = ['y', 'b']  (Both move together)
```

---

### 2. Probability Analysis: Enumerative Approach 🔢

**What it does:** Calculate the *exact* probability that each camel finishes 1st or 2nd by testing EVERY POSSIBLE dice sequence.

**Why it's useful:** Helps players make optimal betting decisions. "Should I bet on Red? Red has a 45% chance to win!"

**The Algorithm (4 Steps):**

#### Step 1: Generate All Possible Dice Sequences

```python
def get_all_dice_roll_sequences(self) -> set:
    """Generate all possible ways the remaining dice could be rolled"""
    # Example: If pyramid has {r, b, g} (3 dice remaining)
    # We need all permutations (order) × all value combinations (1,2,3 each)

    # Color orders: (r,b,g), (r,g,b), (b,r,g), (b,g,r), (g,r,b), (g,b,r) = 6 permutations
    color_orders = permutations(['r', 'b', 'g'])

    # Roll values: Each die can be 1, 2, or 3
    # So: (1,1,1), (1,1,2), (1,1,3), ..., (3,3,3) = 3^3 = 27 combinations
    rolls = product([1,2,3], repeat=3)

    # Combine: For EACH color order × roll combination
    # Result: 6 × 27 = 162 total possible sequences

    all_sequences = {
        (('r', 1), ('b', 2), ('g', 3)),
        (('r', 1), ('b', 2), ('g', 1)),
        (('r', 1), ('b', 3), ('g', 2)),
        # ... 159 more sequences
    }
```

**Math:** If you have N dice remaining:
- Permutations of colors: N!
- Combinations of rolls: 3^N
- **Total sequences: N! × 3^N**

Example: 3 dice → 6 × 27 = **162 sequences**

#### Step 2: Simulate Each Sequence

```python
# For EACH of the 162 possible sequences:
for sequence in all_sequences:
    # Make a copy of the board (don't modify the original!)
    board_copy = deepcopy(self.track)

    # Play out this entire sequence of rolls
    for roll in sequence:
        board_copy = move_camel(board_copy, roll)

    # Get the final 1st and 2nd place finishers
    first, second = get_rankings(board_copy)

    # Record that this sequence led to first=X, second=Y
    win_counts[first][0] += 1      # first place count
    win_counts[second][1] += 1     # second place count
```

**Why deepcopy?** We need a fresh copy of the board for each sequence. Otherwise, moving camels in one simulation affects the next!

#### Step 3: Count Results

```python
# After simulating all 162 sequences, count:
# win_counts = {
#     'r': [45, 28],    # Red was 1st in 45 sequences, 2nd in 28
#     'b': [38, 40],    # Blue was 1st in 38 sequences, 2nd in 40
#     'g': [35, 32],    # Green was 1st in 35 sequences, 2nd in 32
#     'y': [22, 31],
#     'p': [22, 31]
# }
```

#### Step 4: Calculate Probabilities

```python
total_sequences = 162

probabilities = {
    'r': (45/162, 28/162),   # (27.8%, 17.3%)
    'b': (38/162, 40/162),   # (23.5%, 24.7%)
    'g': (35/162, 32/162),   # (21.6%, 19.8%)
    'y': (22/162, 31/162),   # (13.6%, 19.1%)
    'p': (22/162, 31/162)    # (13.6%, 19.1%)
}
```

**Complexity:**
- Time: O(N! × 3^N × 16 × 5) where N = dice remaining
- Accurate but slow for larger N (6 dice = 518,400 sequences!)

---

### 3. Probability Analysis: Experimental Approach 🎲

**What it does:** Estimate probabilities by running random simulations (Monte Carlo method).

**Why it's useful:** Much faster than enumerative for large N, gives approximate answers quickly.

**The Algorithm (3 Steps):**

```python
def run_experimental_leg_analysis(self, trials: int) -> dict:
    """Run 'trials' random simulations, count results"""

    # Get all possible sequences (same as enumerative)
    all_sequences = list(self.get_all_dice_roll_sequences())
    # all_sequences = [162 sequences] (or however many)

    win_counts = {'r': [0, 0], 'b': [0, 0], ...}

    # Run 'trials' times (default: 5000)
    for i in range(trials):

        # Step 1: Pick a random sequence from all possibilities
        sequence = random.choice(all_sequences)
        # Example: (('r', 2), ('b', 1), ('g', 3))

        # Step 2: Simulate that sequence
        board_copy = deepcopy(self.track)
        for roll in sequence:
            board_copy = move_camel(board_copy, roll)

        # Step 3: Count the results
        first, second = get_rankings(board_copy)
        win_counts[first][0] += 1
        win_counts[second][1] += 1

    # After 5000 trials:
    # win_counts = {'r': [1200, 850], 'b': [950, 1100], ...}

    # Convert to percentages
    return {
        'r': (1200/5000, 850/5000),  # (24.0%, 17.0%)
        'b': (950/5000, 1100/5000),  # (19.0%, 22.0%)
        # ...
    }
```

**Why it works:**
- By random sampling, we approximate the true distribution
- More trials → more accurate
- 5000 trials usually gives ±2% accuracy

**Complexity:**
- Time: O(trials × 16 × 5) — much faster than enumerative!
- Approximate but quick for any N

---

### 4. Get Rankings Algorithm 🏆

**What it does:** Look at the final board state and find which camel is 1st and which is 2nd.

**Key insight:** The rightmost position (position 15) has the leader. Among camels at the same position, the topmost camel is ahead.

```python
def get_rankings(self, track: list[list[str]]) -> tuple[str, str]:
    """Find the 1st and 2nd place camels"""
    camels_found = []

    # Scan from right to left (position 15 → 0)
    for position_index in range(len(track) - 1, -1, -1):
        position = track[position_index]

        # Within each position, scan top to bottom
        for camel_index in range(len(position) - 1, -1, -1):
            camels_found.append(position[camel_index])

            # Stop when we have 1st and 2nd place
            if len(camels_found) == 2:
                return tuple(camels_found)

    # Edge case: not enough camels (shouldn't happen)
    return None
```

**Example:**
```
Board state (right to left):
Position 15: ['b']          ← Blue is rightmost
Position 14: []
Position 13: ['r', 'g']     ← Red on bottom, Green on top
Position 12: ['y']

Scan:
1. Position 15, camel 'b' → camels_found = ['b']
2. Position 13, camel 'g' (top) → camels_found = ['b', 'g']
3. Found 2 camels! Return ('b', 'g')

Result: Blue is 1st, Green is 2nd
```

---

## How To Run

### Prerequisites
```bash
pip install colorama
```

### Play a Game
```bash
python CamelUpGame.py
```

You'll be prompted:
```
p1- (B)et or (R)oll? r
```

Enter `r` to roll the dice or `b` to place a bet.

### View Probability Analysis
```bash
python CamelUpBoard.py
```

This will:
1. Show the board state
2. Calculate exact (enumerative) probabilities
3. Run 5000 simulated trials and show estimated probabilities
4. Compare the two approaches

### Run Deepcopy Demo
```bash
python demos/deepcopy_demo.py
```

Learn why `deepcopy` is essential for preserving board state.

---

## Game Mechanics

### Betting Tickets

Each camel has 4 betting tickets worth [5, 3, 2, 2]:
- Place a bet on Red → win the ticket value if Red finishes 1st
- If Red finishes 2nd instead → win 1 coin (consolation prize)
- If Red doesn't place → lose 1 coin

### Expected Value (EV)

The game calculates EV to help you decide which camel to bet on:

```
EV = (prob_1st × ticket_value) + (prob_2nd × 1) - (prob_3rd+ × 1)
```

**Example:**
- Red has 30% to win, 20% to place 2nd, 50% to not place
- Betting Red worth 5 coins:
- EV = (0.30 × 5) + (0.20 × 1) - (0.50 × 1)
- EV = 1.50 + 0.20 - 0.50 = **1.20 coins**

Positive EV = Good bet! Negative EV = Bad bet!

### Camel Stacking

When a camel is overtaken, it stacks on the winner:

```
Roll: Yellow moves from position 5 to position 7, where Red is

Before:
Position 5: ['y', 'p']     ← Yellow on bottom, Purple on top
Position 7: ['r']         ← Red alone

After (Yellow rolls 2):
Position 5: []            ← Empty
Position 7: ['r', 'y', 'p'] ← All three together! Red on bottom
```

This creates complex strategic situations!

---

## Code Examples

### Example 1: Simulate One Move

```python
from CamelUpBoard import CamelUpBoard
from colorama import Back, Style

# Create board
styles = {
    "r": Back.RED + Style.BRIGHT,
    "b": Back.BLUE + Style.BRIGHT,
    # ... etc
}
board = CamelUpBoard(styles)

# Roll a die (randomly chooses color and value)
die = board.shake_pyramid()  # Returns ('r', 2)

# Move the camel
board.move_camel(die)

# Show the board
board.print([player1, player2])
```

### Example 2: Get Exact Probabilities

```python
# Get exact probabilities for current board state
probabilities = board.run_enumerative_leg_analysis()

# probabilities = {
#     'r': (0.278, 0.173),  # Red: 27.8% to win, 17.3% to place
#     'b': (0.235, 0.247),
#     'g': (0.216, 0.198),
#     'y': (0.136, 0.191),
#     'p': (0.136, 0.191)
# }

for color, (prob_1st, prob_2nd) in probabilities.items():
    print(f"{color}: 1st={prob_1st:.1%}, 2nd={prob_2nd:.1%}")
```

### Example 3: Calculate Betting Advice

```python
# Get probabilities
enum_probs = board.run_enumerative_leg_analysis()

# Calculate EV for a bet
ticket_value = 5  # Top Red ticket is worth 5
prob_1st = enum_probs['r'][0]
prob_2nd = enum_probs['r'][1]

ev = ticket_value * prob_1st + 1 * prob_2nd - 1 * (1 - prob_1st - prob_2nd)
print(f"Red ticket (value={ticket_value}): EV = {ev:.2f}")

if ev > 0:
    print("Good bet!")
else:
    print("Bad bet.")
```

---

## Key Features

✅ **Exact Probability Calculation** - Enumerate all possible outcomes
✅ **Approximate Probability Calculation** - Fast Monte Carlo simulation
✅ **Camel Stacking** - Complex movement with multiple camels
✅ **Betting System** - Strategic decision-making based on probabilities
✅ **Colored Terminal Output** - Beautiful board visualization
✅ **AI Advice** - Shows EV for each betting option
✅ **Educational** - Learn game theory, probability, algorithms

---

## Common Gotchas

### Gotcha 1: Why Use `deepcopy`?

When simulating sequences, you MUST use `deepcopy` to preserve board state:

```python
# ❌ WRONG - This mutates the original board!
board_copy = self.track
for roll in sequence:
    move_camel(board_copy, roll)

# ✅ CORRECT - Creates independent copy
board_copy = deepcopy(self.track)
for roll in sequence:
    move_camel(board_copy, roll)
```

### Gotcha 2: Camel Movement with Stacking

When moving a camel, ALL camels on top move with it:

```python
# Position 3 has ['red', 'blue', 'green']
# (red on bottom, green on top)

# When red rolls 2:
# Move EVERYTHING from red's index onwards
for k in range(i, len(self.track[position])):  # i=0, so includes all
    # Move red, blue, AND green
    self.track[new_position].append(self.track[position][k])
```

### Gotcha 3: Probability Complexity

Number of sequences explodes as dice remain:
- 1 die: 3 sequences
- 2 dice: 2! × 3² = 18 sequences
- 3 dice: 3! × 3³ = 162 sequences
- 4 dice: 4! × 3⁴ = 1,296 sequences
- 5 dice: 5! × 3⁵ = 14,400 sequences ⚠️

This is why experimental (Monte Carlo) analysis becomes practical!

---

## What Each File Does

### CamelUpGame.py (Game Controller)
- **Purpose:** Orchestrates the turn-based gameplay
- **Key methods:**
  - `play_1_leg()` - Main game loop
  - `get_player_move()` - Prompts for Bet/Roll
  - `get_player_bet()` - Shows AI advice and takes bet
  - `leg_payouts_and_results()` - Awards winnings
- **Uses:** CamelUpBoard, CamelUpPlayer

### CamelUpBoard.py (Game Logic)
- **Purpose:** Manages board state and probabilities
- **Key methods:**
  - `move_camel()` - Moves camel and stacked camels
  - `shake_pyramid()` - Rolls a random die
  - `get_rankings()` - Finds 1st and 2nd place
  - `run_enumerative_leg_analysis()` - Exact probabilities (slow)
  - `run_experimental_leg_analysis()` - Approx probabilities (fast)
- **Advanced:** `get_all_dice_roll_sequences()` uses `itertools.permutations` and `itertools.product`

### CamelUpPlayer.py (Player Model)
- **Purpose:** Represents a player
- **Tracks:** Money (coins), current bets

---

## Frequently Asked Questions

**Q: Why does it take so long to calculate probabilities with 5 dice?**
A: Because there are 14,400 possible sequences to simulate. That's why `experimental_leg_analysis` is useful — it samples 5,000 random sequences instead, much faster!

**Q: Can I play multiple legs?**
A: Currently, `play_1_leg()` plays one leg only. You'd need to modify `CamelUpGame.py` to add a loop that calls `play_1_leg()` multiple times and resets bets.

**Q: Why can't a camel move past position 15?**
A: The track has 16 positions (0-15). Position 15 is the finish line. Currently, if a camel would overshoot, it's capped at position 15.

**Q: How do I make the AI make moves automatically?**
A: `getAIMove.py` has utilities for this. You'd need to implement recursive game tree search to evaluate which moves maximize expected winnings.

---

## Improvements / TODOs

- [ ] Randomize starting camel positions (currently fixed at positions 0-2)
- [ ] Handle camels reaching the finish line (position 15+)
- [ ] Implement full AI player that makes optimal moves
- [ ] Play multiple legs with running score
- [ ] Save game state and load previous games
- [ ] Add unit tests

---

## Learning Resources

- **Game Tree Search:** See `getAIMove.py` for recursive minimax approach
- **Deepcopy:** See `demos/deepcopy_demo.py` for detailed explanation
- **Probability:** See `CamelUpBoard.py` for Monte Carlo simulation
- **Itertools:** Used for `permutations()` and `product()` in probability calculations

---

<p align="center">
  Made with 🐫 for learning algorithm design
</p>

---

<!-- Badge links -->
[Python]: https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[Colorama]: https://img.shields.io/badge/Colorama-Terminal%20Colors-4CAF50?style=for-the-badge
[Colorama-url]: https://pypi.org/project/colorama/
