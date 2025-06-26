# Gomoku AI Game with Heuristic Flip Mechanics

**Author**: David Chung  
**Course**: 15-112: Fundamentals of Programming  
**Institution**: Carnegie Mellon University  
**Technologies**: Python · `cmu_112_graphics` · Custom AI · Heuristics · Game Design  

## 🎯 Overview

This project is a two-player **Gomoku game with AI integration**, developed as the final term project for Carnegie Mellon's 15-112 course. Players compete on a dynamically resizable board, where the objective is to connect four consecutive pieces. The game supports **AI vs. Player**, **Player vs. Player**, and a unique **flip mode** where the column of a placed piece is reversed each turn to add an additional layer of strategy.

The AI opponent uses a heuristic evaluation function to choose optimal moves and improves over time through state analysis.

## 🧠 Features

- 🤖 **AI Opponent**: Custom-built AI logic simulates opponent moves and prioritizes high-scoring positions.
- 🔄 **Flip Mode**: Optional game mechanic that flips the board column after a piece is placed—forcing players to adapt.
- 🧑‍🤝‍🧑 **Multiplayer Support**: Toggle between player-vs-AI and two-player mode.
- 🎨 **Graphical Interface**: Built with `cmu_112_graphics` for smooth animations, hover previews, and status messaging.
- ⚙️ **Scalable Grid**: Players can increase or decrease the board size during gameplay.
- 🏁 **Victory Conditions**: Win by connecting four or more consecutive pieces in any direction; draw if the board fills.


## 🗂️ Project Structure

```
gomoku/
├── main.py                  # Game engine and animation loop
├── aibot.py                 # AI logic and evaluation functions
├── boardMethods.py          # Game logic, win-checking, flipping mechanics
├── grid_board.py            # Board rendering and interaction
├── human_player.py          # Player interaction logic
├── aiTester.py              # Test environment for AI-vs-AI simulation
├── cmu_112_graphics.py      # Custom graphics library from CMU 15-112
```

## 📌 Gameplay Controls

| Key/Mouse | Action                          |
|-----------|---------------------------------|
| Mouse     | Hover/pick position to place    |
| `r`       | Restart game                    |
| `Up`      | Increase board size             |
| `Down`    | Decrease board size             |
| `s`       | Save/update AI state (optional) |
| `p`       | Pause/unpause timer loop        |

## 🚀 How to Run

```bash
pip install cmu_112_graphics
python main.py
```

At launch, you'll be prompted to choose:
1. **Player mode**: Single or two-player
2. **Flip mode**: Enable or disable board flipping


## 🤖 AI Strategy (In Depth)

The AI in this Gomoku implementation is designed with **speed, adaptability, and strategic foresight** in mind. Here's a breakdown of its inner workings:

- ⚡ **Memoization**:
  - The AI uses a hash map (`seenStates`) to **cache previously evaluated board states**, reducing redundant calculations and accelerating decision-making in complex boards.

- 🧠 **Heuristic Scoring**:
  - Evaluates each possible move using a custom `scoreBoard()` function.
  - Scores are weighted based on:
    - Length of potential streaks (e.g., 2-in-a-row, 3-in-a-row)
    - Blocking opponent from connecting four
    - Simulated opponent moves (minimax-inspired)
    - Board symmetry and center control

- 📉 **Move Pruning**:
  - To reduce the search space, the AI uses `getNearbyMoves()` to only consider positions within a certain distance of current pieces—leading to **O(k)** efficiency rather than O(n²).

- 🔁 **Flip Prediction**:
  - When flip mode is enabled, the AI simulates the flipped board state **before** evaluating a move, ensuring decisions remain optimal even with unpredictable reversals.

- ♻️ **Post-Game Learning (Prototype)**:
  - A placeholder method `updateData()` is triggered at the end of each game—paving the way for future enhancements like reinforcement learning or persistent scoring systems.

This hybrid of heuristic evaluation, smart pruning, and memoization creates a responsive AI that plays effectively while maintaining a fast, fluid user experience.


- Uses a **heuristic evaluation function** based on proximity, threats, and potential wins.
- Evaluates potential blocking and scoring moves using a scoring model weighted by:
  - Consecutive piece length
  - Blocking opponent streaks
  - Nearby empty cells
- Optional AI state persistence feature for long-term improvement (via `updateData()`).

## 💡 Learning Outcomes

This project demonstrates:
- OOP design with reusable modules (`player`, `gridBoard`, `boardMethods`)
- Recursive and heuristic-based AI development
- Game animation loop architecture via `cmu_112_graphics`
- Algorithmic thinking for win-checking and board manipulation
