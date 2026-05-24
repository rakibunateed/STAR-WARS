import turtle
import os

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.dat")

def _load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def _save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except OSError:
        pass


class Scoreboard:
    MAX_LIVES = 9

    def __init__(self):
        self.score      = 0
        self.high_score = _load_highscore()
        self.lives      = 5
        self.level      = 1

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()
        self.draw()

    def add(self, pts):
        self.score += pts
        if self.score > self.high_score:
            self.high_score = self.score
            _save_highscore(self.high_score)

    def gain_life(self):
        if self.lives < self.MAX_LIVES:
            self.lives += 1

    def lose_life(self):
        self.lives -= 1

    def reset(self):
        self.score = 0
        self.lives = 5
        self.level = 1

    def check_level_up(self):
        target = 1 + self.score // 500
        if target > self.level:
            self.level = target
            return True
        return False

    def draw(self):
        self.pen.clear()

        self.pen.goto(-370, 265)
        self.pen.color("cyan")
        self.pen.write(f"SCORE: {self.score:06d}", font=("Courier", 13, "bold"))

        self.pen.goto(-60, 265)
        self.pen.color("gold")
        self.pen.write(f"BEST: {self.high_score:06d}", font=("Courier", 13, "bold"))

        self.pen.goto(270, 265)
        self.pen.color("lime green")
        self.pen.write(f"LVL {self.level}", font=("Courier", 13, "bold"))

        self.pen.goto(-370, -280)
        self.pen.color("#ff44aa")
        hearts = "♥ " * self.lives
        self.pen.write(hearts, font=("Courier", 15, "bold"))
