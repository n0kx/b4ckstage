galactic_unicorn = None
graphics = None

def init():
    #graphics.set_font("bitmap8")
    graphics.set_pen(graphics.create_pen(0, 0, 0))
    graphics.clear()
    graphics.set_pen(graphics.create_pen(145, 0, 164)) #purple
    graphics.text("BACKSTAGE", 2, -1, -1, 1)
    graphics.set_pen(graphics.create_pen(255, 255, 255)) #white
    graphics.text("by n0kx", 10, 5, -1, 1)
    galactic_unicorn.update(graphics)
