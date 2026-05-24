import turtle


_POOL_SIZE = 20
_pool: list = []
_active: list = []

def _init_pool():
    """Pre-create all bullet turtles once at game start."""
    for _ in range(_POOL_SIZE):
        t = turtle.Turtle()
        t.speed(0)
        t.shape("square")
        t.color("#00ffff")
        t.shapesize(stretch_wid=0.25, stretch_len=1.2)
        t.penup()
        t.setheading(90)
        t.hideturtle()
        t.goto(2000, 2000)
        _pool.append(t)

def init_bullet_pool():
    _init_pool()


class Bullet:
    BASE_SPEED = 18
    RADIUS     = 6

    def __init__(self, x, y, level=1):
        self.active = True
        self.x = x
        self.y = y
        self.speed = min(self.BASE_SPEED + (level - 1) * 2, 32)
        if _pool:
            self._t = _pool.pop()
        else:
            self._t = turtle.Turtle()
            self._t.speed(0)
            self._t.shape("square")
            self._t.color("#00ffff")
            self._t.shapesize(stretch_wid=0.25, stretch_len=1.2)
            self._t.penup()
            self._t.setheading(90)

        self._t.goto(x, y)
        self._t.showturtle()
        _active.append(self)

    def update(self):
        if not self.active:
            return
        self.y += self.speed
        self._t.sety(self.y)
        if self.y > 310:
            self.destroy()

    def destroy(self):
        if not self.active:
            return
        self.active = False
        self._t.hideturtle()
        self._t.goto(2000, 2000)
        _pool.append(self._t)
        if self in _active:
            _active.remove(self)