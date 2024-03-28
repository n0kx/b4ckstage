galactic_unicorn = None
graphics = None

def init():
    draw()

@micropython.native  # noqa: F821
def draw(time="30"):
    #graphics.set_font("bitmap8")
    graphics.set_pen(graphics.create_pen(0, 0, 0))
    graphics.clear()
    graphics.set_pen(graphics.create_pen(0, 255, 0)) #green
    graphics.text("PLACES IN", 4, -1, -1, 1)
    graphics.set_pen(graphics.create_pen(255, 0, 0)) #red
    graphics.text(time, 22, 5, -1, 1)
    galactic_unicorn.update(graphics)
