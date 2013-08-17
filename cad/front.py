from pyx import *
text.set(mode="latex") 
#text.preamble(r"\usepackage{ulem}")  # underlining text...
#text.preamble("\usepackage{anyfontsize}")
text.preamble(r"\renewcommand{\familydefault}{\sfdefault}")
#text.preamble(r"\usepackage{times}")

attrs = [style.linewidth(0.001), style.linecap.square]

def draw_mounting_hole(canvas, x, y):
    c.stroke(path.circle(x, y, .3/2.), attrs)

def draw_lcd(canvas, x, y):
    lcd_x = 7.13+0.05
    lcd_y = 2.63+0.05

    holes_x = 7.5
    holes_y = 3.1

    canvas.stroke(path.rect(x-lcd_x/2., y-lcd_y/2., lcd_x, lcd_y), attrs)
    #canvas.stroke(path.line(7, y-lcd_y/2., 7, y-lcd_y/2.-2.15), attrs)
    draw_mounting_hole(canvas, x-holes_x/2., y+holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y+holes_y/2.)
    draw_mounting_hole(canvas, x-holes_x/2., y-holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y-holes_y/2.)

def draw_navigation(canvas, x, y):
    buttons_diameter = 3.5+0.1
    holes_x = 3.2
    holes_y = 3.3

    canvas.stroke(path.circle(x, y, buttons_diameter/2.), attrs)
    draw_mounting_hole(canvas, x-holes_x/2., y+holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y+holes_y/2.)
    draw_mounting_hole(canvas, x-holes_x/2., y-holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y-holes_y/2.)

    #canvas.text(x, y + buttons_diameter/2.+0.5, "ON", [trafo.scale(2), text.halign.boxcenter, text.vshift.middlezero, color.rgb.red])
    #canvas.text(x, y - buttons_diameter/2.-0.5, "OFF", [trafo.scale(2), text.halign.boxcenter, text.vshift.middlezero, color.rgb.red])

def draw_usb_socket(canvas, x, y):
    socket_diameter = 2.36
    holes_x = 1.9
    holes_y = 2.4

    canvas.stroke(path.circle(x, y, socket_diameter/2.), attrs)
    draw_mounting_hole(canvas, x-holes_x/2., y+holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y-holes_y/2.)

def draw_led(canvas, x, y):
    led_diameter = 0.6
    canvas.stroke(path.circle(x, y, led_diameter/2.), attrs)

c = canvas.canvas()
c.stroke(path.rect(0.5, 0, 9, 10), attrs)

draw_lcd(c, 5, 8)
draw_navigation(c, 7, 8-5.5)
draw_usb_socket(c, 2, 8-5.5) 
draw_led(c, (7+2)/2., 8-5.5)

c.writePDFfile("front")

