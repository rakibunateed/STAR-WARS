import turtle
import math

def _make_ship_shape(screen):
    """
    Register a custom 'fighter' polygon that looks like a real jet fighter
    viewed from above: swept wings, fuselage, and rear fins.
    Coordinates are (x, y) pairs — turtle shapes use a polygon outline.
    """

    ship_coords = (

        ( 0,   24),
        ( 4,   14),
        (20,    0),
        (10,  -10),
        (12,  -22),
        ( 5,  -18),
        ( 0,  -14),
        (-5,  -18),
        (-12, -22),
        (-10, -10),
        (-20,   0),
        (-4,   14),
    )
    screen.register_shape("fighter", ship_coords)

    glow_coords = (
        ( 0,  5), ( 3,  3), ( 4,  0), ( 3, -3),
        ( 0, -5), (-3, -3), (-4,  0), (-3,  3),
    )
    screen.register_shape("glow", glow_coords)


class Player:
    SPEED          = 14
    BASE_SHOOT_COOLDOWN = 7
    RADIUS         = 18
    BOUNDARY_X     = 360

    def __init__(self):
        screen = turtle.Screen()
        _make_ship_shape(screen)

        self._thruster = turtle.Turtle()
        self._thruster.speed(0)
        self._thruster.shape("glow")
        self._thruster.color("#ff6600")
        self._thruster.shapesize(1.4, 1.0)
        self._thruster.penup()
        self._thruster.setheading(90)
        self._thruster.goto(0, -242)

        self._light_r = turtle.Turtle()
        self._light_r.speed(0); self._light_r.shape("circle")
        self._light_r.color("#ff0055"); self._light_r.shapesize(0.18, 0.18)
        self._light_r.penup(); self._light_r.goto(20, -220)

        self._light_l = turtle.Turtle()
        self._light_l.speed(0); self._light_l.shape("circle")
        self._light_l.color("#00ff99"); self._light_l.shapesize(0.18, 0.18)
        self._light_l.penup(); self._light_l.goto(-20, -220)

        self._t = turtle.Turtle()
        self._t.speed(0)
        self._t.shape("fighter")
        self._t.color("#00ccff", "#005588")
        self._t.shapesize(1.7, 1.7)
        self._t.penup()
        self._t.setheading(90)
        self._t.goto(0, -220)

        self._canopy = turtle.Turtle()
        self._canopy.speed(0); self._canopy.shape("circle")
        self._canopy.color("#aaeeff"); self._canopy.shapesize(0.3, 0.2)
        self._canopy.penup(); self._canopy.goto(0, -212)

        self._left  = False
        self._right = False
        self._cd    = 0
        self.alive  = True
        self._pulse = 0

    # ── Controls ──
    def start_left(self):  self._left  = True
    def stop_left(self):   self._left  = False
    def start_right(self): self._right = True
    def stop_right(self):  self._right = False

    # ── Update  ──
    def update(self, level=1):
        x = self.x()
        if self._left  and x > -self.BOUNDARY_X: x -= self.SPEED
        if self._right and x <  self.BOUNDARY_X: x += self.SPEED

        if x != self.x():
            self._t.setx(x)
            self._thruster.setx(x)
            self._canopy.setx(x)
            self._light_r.setx(x + 20)
            self._light_l.setx(x - 20)

        self._pulse = (self._pulse + 1) % 8
        if self._pulse == 0:
            self._thruster.color("#ffaa00")
        elif self._pulse == 4:
            self._thruster.color("#ff4400")

        cooldown = max(2, self.BASE_SHOOT_COOLDOWN - (level - 1))
        if self._cd > 0:
            self._cd -= 1
            return False
        self._cd = cooldown
        return True  # fire!

    def x(self): return self._t.xcor()
    def y(self): return self._t.ycor()

    def _all_parts(self):
        return [self._t, self._thruster, self._canopy,
                self._light_r, self._light_l]

    def hide(self):
        self.alive = False
        for p in self._all_parts(): p.hideturtle()

    def show(self):
        self.alive = True
        self._t.goto(0, -220)
        self._thruster.goto(0, -242)
        self._canopy.goto(0, -212)
        self._light_r.goto(20, -220)
        self._light_l.goto(-20, -220)
        for p in self._all_parts(): p.showturtle()

    def reset(self):
        self._left = self._right = False
        self._cd   = 0
        self.alive = True
        self.show()
