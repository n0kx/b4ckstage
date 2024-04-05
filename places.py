galactic_unicorn = None
graphics = None

def init():
    draw()

def draw(time="30"):
    time_int = int(time)
    
    graphics.set_pen(graphics.create_pen(0, 0, 0))
    graphics.clear()
    
    if time_int > 0: # There is time remaining
        graphics.set_pen(graphics.create_pen(2, 169, 247)) #indigo
        graphics.text("PLACES IN", 4, -1, -1, 1)
        
        if time_int <= 5:
            graphics.set_pen(graphics.create_pen(255, 0, 0)) #red
        else:
            graphics.set_pen(graphics.create_pen(255, 110, 33)) #orange
        
        position = 22 if time_int >= 10 else 24
        
        graphics.text(time, position, 5, -1, 1)
    else: # No time remaining
        graphics.set_pen(graphics.create_pen(2, 169, 247)) #indigo
        graphics.text("PLACES!", 11, 2, -1, 1)
    
    galactic_unicorn.update(graphics)