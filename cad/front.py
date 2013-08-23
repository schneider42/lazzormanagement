from pyx import *
text.set(mode="latex") 
#text.preamble(r"\usepackage{ulem}")  # underlining text...
#text.preamble("\usepackage{anyfontsize}")
text.preamble(r"\renewcommand{\familydefault}{\sfdefault}")
#text.preamble(r"\usepackage{times}")

attrs = [style.linewidth(0.001), style.linecap.square]
attrs_helper = attrs + [color.rgb.red]

def draw_mounting_hole(canvas, x, y):
    c.stroke(path.circle(x, y, .3/2.), attrs)

def draw_plate_hole(canvas, x, y):
    c.stroke(path.circle(x, y, .65/2.), attrs)

def draw_lcd(canvas, x, y):
    lcd_x = 7.13+0.05
    lcd_y = 2.63+0.05

    holes_x = 7.5
    holes_y = 3.1

    board_x = 8.5
    board_y = 5.6

    board_y_offset = board_y - 2.45

    canvas.stroke(path.rect(x-lcd_x/2., y-lcd_y/2., lcd_x, lcd_y), attrs)
    canvas.stroke(path.rect(x-board_x/2., y-board_y_offset, board_x, board_y), attrs_helper)
    draw_mounting_hole(canvas, x-holes_x/2., y+holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y+holes_y/2.)
    draw_mounting_hole(canvas, x-holes_x/2., y-holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y-holes_y/2.)

def draw_navigation(canvas, x, y):
    buttons_diameter = 3.4+0.1
    holes_x = 3.2
    holes_y = 3.3
    board_x = 4.00
    board_y = 4.63

    board_y_offset = board_y - 1.995

    canvas.stroke(path.circle(x, y, buttons_diameter/2.), attrs)
    canvas.stroke(path.rect(x-board_x/2., y-board_y_offset, board_x, board_y), attrs_helper)
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
    front_x = 2.58
    front_y = 3.08

    canvas.stroke(path.circle(x, y, socket_diameter/2.), attrs)
    draw_mounting_hole(canvas, x-holes_x/2., y+holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y-holes_y/2.)
    canvas.stroke(path.rect(x-front_x/2., y-front_y/2, front_x, front_y), attrs_helper)

def draw_led(canvas, x, y):
    led_diameter = 0.6
    canvas.stroke(path.circle(x, y, led_diameter/2.), attrs)

def draw_plate(canvas, x, y):
    plate_x = 14.0
    plate_y = 20.8+0.65
    holes_r = 0.65/2.

    holes_x1 = 14.0/2.-2.65-holes_r
    holes_y1 = 10.4+holes_r-0.16-holes_r

    holes_x2 = 14.0/2.-0.17-holes_r
    holes_y2 = 0

    draw_plate_hole(canvas, x+holes_x2, y + holes_y2)
    draw_plate_hole(canvas, x-holes_x2, y + holes_y2)
    
    draw_plate_hole(canvas, x-holes_x1, y + holes_y1)
    draw_plate_hole(canvas, x-holes_x1, y - holes_y1)
    draw_plate_hole(canvas, x+holes_x1, y + holes_y1)
    draw_plate_hole(canvas, x+holes_x1, y - holes_y1)

    canvas.stroke(path.rect(x-plate_x/2., y-plate_y/2, plate_x, plate_y), attrs)

def draw_amp_meter(canvas, x, y):
    meter_diameter = 3.8 + 0.3

    holes_x = 3.67-0.27
    holes_y = (4.5/2.-0.62+0.27/2.)*2

    front_x = 4.5
    front_y = 4.5
    front_y_offset = front_y - .45-3.8/2

    canvas.stroke(path.circle(x, y, meter_diameter/2.), attrs)
    draw_mounting_hole(canvas, x-holes_x/2., y-holes_y/2.)
    draw_mounting_hole(canvas, x+holes_x/2., y-holes_y/2.)
    canvas.stroke(path.rect(x-front_x/2., y-front_y_offset, front_x, front_y), attrs_helper)


def draw_main_switch(canvas, x, y):
    socket_diameter = 2.2+0.1
    front_x = 3.0
    front_y = 4.0

    canvas.stroke(path.circle(x, y, socket_diameter/2.), attrs)
    canvas.stroke(path.rect(x-front_x/2., y-front_y/2, front_x, front_y), attrs_helper)

c = canvas.canvas()
draw_plate(c, 0, 0)
#c.stroke(path.rect(0.5, 0, 9, 10), attrs)


assembly_x = 0
assembly_y = 0

draw_lcd(c, assembly_x, assembly_y)
draw_navigation(c, assembly_x+2, assembly_y-5.5)
draw_usb_socket(c, assembly_x-3, assembly_y-5.5) 
#draw_led(c, (2*assembly_x+2-3)/2., assembly_y-5.5)
draw_amp_meter(c, -3, assembly_y+6)
draw_main_switch(c, 3, assembly_y+6)
c.writePDFfile("front")
c.writeEPSfile("front")

