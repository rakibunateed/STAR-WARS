# ⚡ STAR WARS — Python Space Shooter Game

A fully object-oriented 2D arcade space shooter built with Python Turtle Graphics. No external libraries required — just Python 3.8+.

---

## 🗂 Project Structure

```
space_shooter/
│
├── main.py        ← Entry point — run this file
├── game.py        ← Game loop, collisions, state machine
├── player.py      ← Player ship + shooting cooldown
├── enemy.py       ← Enemy ships with zigzag AI
├── bullet.py      ← Laser bolt logic
├── scoreboard.py  ← HUD: score, lives, level
├── lifeup.py      ← Collectible heart life powerup
└── effects.py     ← Scrolling star field + explosion particles
```

---

## 🎮 How to Play

```bash
cd space_shooter
python main.py
```

| Key | Action |
|-----|--------|
| `←` / `→` or `A` / `D` | Move ship |
| `Automatic` | Shoot |
| `Enter` | Start / Restart |

---

## 🏆 Rules

- Destroy enemies before they reach the bottom.
- Each kill = **+100 points**.
- An enemy reaching the bottom costs **1 life**.
- You start with **5 lives**. Lose them all → Game Over.
- Each time you level up, a pink ♥ heart drops from the top — fly into it to collect an extra life!
- Every **500 points** advances you one level (enemies get faster + more).
- Bullet speed and fire rate also increase with each level.

---

## 📸 Screenshots

<img width="801" height="629" alt="Screenshot 2026-05-23 215314" src="https://github.com/user-attachments/assets/3f249b76-ee8a-404f-98ce-8f64e6678b1d" />
<img width="803" height="630" alt="Screenshot 2026-05-23 215359" src="https://github.com/user-attachments/assets/2af5031d-e0aa-4e07-8338-be04261add1b" />
<img width="800" height="631" alt="Screenshot 2026-05-23 215410" src="https://github.com/user-attachments/assets/48416bbd-0fc2-477a-9429-a0aac02d518e" />



---

## 🧱 OOP Design

| Class | Responsibility |
|-------|---------------|
| `Game` | Window, game loop, collisions, state transitions |
| `Player` | Ship movement, shooting, bullet list ownership |
| `Enemy` | Descent, zigzag movement, self-destruction |
| `Bullet` | Upward travel, off-screen deactivation |
| `Scoreboard` | HUD rendering (score, lives, level, high score) |
| `StarField` | Parallax scrolling background |
| `Explosion` | Short-lived particle burst on enemy death |

---

## 📦 Requirements

- Python **3.8** or newer  
- `turtle` module (included in the Python standard library)  
- No `pip install` needed!

---


## 👨‍💻 Author

### Rakibun Ateed

- GitHub: [@rakibunateed](https://github.com/rakibunateed?utm_source=chatgpt.com)

---
