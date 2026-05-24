import turtle
import math
import random

from player     import Player
from enemy      import Enemy
from bullet     import Bullet, init_bullet_pool
from scoreboard import Scoreboard
from effects    import StarField, Explosion
from lifeup     import LifeUp, init_lifeup_pool
import enemy  as enemy_module

W, H = 800, 600

PTS_KILL   = 100
ENEMY_BASE = 4

def spawn_interval(level):
    return max(18, 70 - (level - 1) * 8)

class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("⚡ STAR WARS")
        self.screen.bgcolor("black")
        self.screen.setup(W, H)
        self.screen.tracer(0)

        init_bullet_pool()
        enemy_module.init_enemy_pool()
        init_lifeup_pool()

        self.stars       = StarField()
        self.sb          = Scoreboard()
        self.player      = Player()
        self.bullets:    list[Bullet]    = []
        self.enemies:    list[Enemy]     = []
        self.explosions: list[Explosion] = []
        self.lifeups:    list[LifeUp]    = []

        self._enemy_timer  = 0
        self._lifeup_timer = 0

        self.ui = turtle.Turtle()
        self.ui.hideturtle()
        self.ui.speed(0)
        self.ui.penup()

        self._state = "attract"
        self._frame = 0
        self._last_level = 1

        self._setup_controls()
        self._draw_attract()
        self.screen.update()

        self._loop()
        turtle.done()

    # ── Controls ───
    def _setup_controls(self):
        s = self.screen
        s.onkeypress(self.player.start_left,   "Left")
        s.onkeyrelease(self.player.stop_left,  "Left")
        s.onkeypress(self.player.start_right,  "Right")
        s.onkeyrelease(self.player.stop_right, "Right")
        s.onkeypress(self.player.start_left,   "a")
        s.onkeyrelease(self.player.stop_left,  "a")
        s.onkeypress(self.player.start_right,  "d")
        s.onkeyrelease(self.player.stop_right, "d")
        s.onkeypress(self._enter,              "Return")
        s.listen()

    def _enter(self):
        if self._state in ("attract", "gameover"):
            self._start()

    # ── State transitions ──
    def _start(self):
        self.ui.clear()
        self.sb.reset()
        self.player.reset()

        for b in self.bullets:   b.destroy()
        for e in self.enemies:   e.destroy()
        for ex in self.explosions: ex.cleanup()
        for lu in self.lifeups:  lu.destroy()
        self.bullets.clear()
        self.enemies.clear()
        self.explosions.clear()
        self.lifeups.clear()

        self._frame        = 0
        self._enemy_timer  = 0
        self._lifeup_timer = 0
        self._last_level   = 1

        for i in range(ENEMY_BASE):
            e = Enemy(1)
            e._t.goto(e.x, 290 + i * 70)
            e.y = 290 + i * 70
            self.enemies.append(e)

        self._state = "playing"

    def _game_over(self):
        self._state = "gameover"
        self.player.hide()
        for e in self.enemies:  e.destroy()
        for lu in self.lifeups: lu.destroy()
        self.enemies.clear()
        self.lifeups.clear()
        self._draw_gameover()

    # ── Main loop ──
    def _loop(self):
        self._frame += 1
        self._update()
        self.screen.update()
        self.screen.ontimer(self._loop, 16)

    # ── Update ──
    def _update(self):
        self.stars.update()

        if self._state != "playing":
            return

        if self.player.update(self.sb.level):
            b = Bullet(self.player.x(), self.player.y() + 24, self.sb.level)
            self.bullets.append(b)

        for b in self.bullets:
            b.update()
        self.bullets = [b for b in self.bullets if b.active]

        for e in self.enemies:
            e.update()

        for lu in self.lifeups:
            lu.update()
        self.lifeups = [lu for lu in self.lifeups if lu.active]

        self.explosions = [ex for ex in self.explosions if ex.update()]

        self._collide()

        if self._state != "playing":
            return

        # ── Enemy spawn ──
        level = self.sb.level
        target_on_screen = ENEMY_BASE + (level - 1) * 2

        self._enemy_timer -= 1
        if self._enemy_timer <= 0:
            self._enemy_timer = spawn_interval(level)
            if len(self.enemies) < target_on_screen:
                en = Enemy(level)

                en.y = 290 + random.randint(0, 180)
                en._t.sety(en.y)
                self.enemies.append(en)

        while len(self.enemies) < max(1, target_on_screen // 2):
            en = Enemy(level)
            en.y = 290 + random.randint(0, 180)
            en._t.sety(en.y)
            self.enemies.append(en)

        # ── Level-up check ──
        if self.sb.check_level_up():
            new_level = self.sb.level
            self.sb.draw()

            lu = LifeUp()
            self.lifeups.append(lu)
            self._last_level = new_level

        # ── Life powerup timer ──
        self._lifeup_timer -= 1
        if self._lifeup_timer <= 0:
            self._lifeup_timer = 60 * 30
            lu = LifeUp()
            self.lifeups.append(lu)

    # ── Collision detection ──
    def _collide(self):
        dead_e  = set()
        dead_b  = set()
        dead_lu = set()
        hud_dirty = False

        for ei, e in enumerate(self.enemies):
            for bi, b in enumerate(self.bullets):
                if bi in dead_b:
                    continue
                if math.hypot(b.x - e.x, b.y - e.y) < e.RADIUS + b.RADIUS:
                    dead_b.add(bi)
                    dead_e.add(ei)
                    self.explosions.append(Explosion(e.x, e.y))
                    self.sb.add(PTS_KILL)
                    hud_dirty = True
                    break

            if ei not in dead_e and e.escaped():
                dead_e.add(ei)
                self.sb.lose_life()
                hud_dirty = True
                if self.sb.lives <= 0:
                    if hud_dirty: self.sb.draw()
                    self._game_over()
                    return

            if (ei not in dead_e and
                    math.hypot(e.x - self.player.x(),
                               e.y - self.player.y()) < e.RADIUS + self.player.RADIUS):
                dead_e.add(ei)
                self.explosions.append(Explosion(self.player.x(), self.player.y()))
                self.sb.lose_life()
                hud_dirty = True
                if self.sb.lives <= 0:
                    if hud_dirty: self.sb.draw()
                    self._game_over()
                    return

        for li, lu in enumerate(self.lifeups):
            if math.hypot(lu.x - self.player.x(),
                          lu.y - self.player.y()) < lu.RADIUS + self.player.RADIUS:
                dead_lu.add(li)
                self.sb.gain_life()
                hud_dirty = True

        if hud_dirty:
            self.sb.draw()

        for i in dead_e:  self.enemies[i].destroy()
        for i in dead_b:  self.bullets[i].destroy()
        for i in dead_lu: self.lifeups[i].destroy()
        self.enemies  = [e  for i, e  in enumerate(self.enemies)  if i not in dead_e]
        self.bullets  = [b  for i, b  in enumerate(self.bullets)  if i not in dead_b]
        self.lifeups  = [lu for i, lu in enumerate(self.lifeups)  if i not in dead_lu]

    # ── UI overlays ──
    def _draw_attract(self):
        self.ui.clear()
        self.ui.goto(0, 90)
        self.ui.color("#00ccff")
        self.ui.write("⚡  STAR WARS  ⚡",
                      align="center", font=("Courier", 26, "bold"))

        self.ui.goto(0, 25)
        self.ui.color("lime green")
        self.ui.write("← →  or  A D  —  Move",
                      align="center", font=("Courier", 12, "normal"))

        self.ui.goto(0, -10)
        self.ui.color("#ff44aa")
        self.ui.write("♥  Collect hearts to gain extra lives!",
                      align="center", font=("Courier", 12, "normal"))
        self.ui.goto(0, -45)
        self.ui.color("gold")
        self.ui.write(f"🏆  ALL-TIME BEST:  {self.sb.high_score:,}",
                      align="center", font=("Courier", 13, "bold"))
        self.ui.goto(0, -115)
        self.ui.color("#00ccff")
        self.ui.write("Press  ENTER  to Start",
                      align="center", font=("Courier", 16, "bold"))

    def _draw_gameover(self):
        self.ui.clear()
        self.ui.goto(0, 60)
        self.ui.color("#ff3333")
        self.ui.write("GAME OVER",
                      align="center", font=("Courier", 34, "bold"))
        self.ui.goto(0, 0)
        self.ui.color("white")
        self.ui.write(f"SCORE:  {self.sb.score:,}",
                      align="center", font=("Courier", 16, "normal"))
        self.ui.goto(0, -35)
        self.ui.color("gold")
        self.ui.write(f"BEST:   {self.sb.high_score:,}",
                      align="center", font=("Courier", 16, "normal"))
        self.ui.goto(0, -80)
        self.ui.color("#00ccff")
        self.ui.write("Press  ENTER  to Play Again",
                      align="center", font=("Courier", 14, "bold"))
