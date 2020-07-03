import tkinter
import pygame

root = tkinter.Tk()

TITLE = "Display Gamepads"
WIDTH = 600
HEIGHT = 400

root.title(TITLE)
root.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+400+10")

pygame.init()

joysticks = []
joystick_names = []
for i in range(pygame.joystick.get_count()):
    j = pygame.joystick.Joystick(i)
    j.init()
    joysticks.append(j)
    joystick_names.append(j.get_name())

selected_joystick_name = tkinter.StringVar(root)
selected_joystick_name.set(joystick_names[0])

joystick = joysticks[0]

def update_joystick(name):
    for j in joysticks:
        if j.get_name() == name:
            joystick = j
            reset_boxes()
            break

dropdown = tkinter.OptionMenu(root, selected_joystick_name,
                              *joystick_names,
                              command=update_joystick)
dropdown.place(x=20, y=10)

digital_inputs = []
analog_inputs = []
hat_inputs = []

class Value(tkinter.Label):
    def __init__(self, master, text, horizontal, vertical):
        self.v = tkinter.StringVar()
        super().__init__(master, textvariable=self.v)
        self.place(x=horizontal, y=vertical)
        self.text = text
        self.v.set(self.text)
    def Set(self, value):
        self.v.set(self.text + value)
        
def reset_boxes():
    global digital_inputs
    global analog_inputs
    global hat_inputs
    for i in range(len(digital_inputs)):
        digital_inputs[i].destroy()
    for i in range(len(analog_inputs)):
        analog_inputs[i].destroy()
    for i in range(len(hat_inputs)):
        hat_inputs[i].destroy()
    digital = Value(root, "Digital Inputs", 20, 60)
    digital = Value(root, "Analog Inputs", 160, 60)
    digital = Value(root, "Hat Inputs", 320, 60)
    digital_inputs = []
    analog_inputs = []
    hat_inputs = []
    for i in range(joystick.get_numbuttons()):
        y = 90 + i * 20
        v = Value(root, "Index " + str(i) + ": ", 20, y)
        v.Set("false")
        digital_inputs.append(v)
    for i in range(joystick.get_numaxes()):
        y = 90 + i * 20
        v = Value(root, "Index " + str(i) + ": ", 160, y)
        v.Set("0.0")
        analog_inputs.append(v)
    for i in range(joystick.get_numhats()):
        y = 90 + i * 20
        v = Value(root, "Index " + str(i) + ": ", 320, y)
        v.Set("0.0")
        hat_inputs.append(v)
def update_inputs():
    pygame.event.pump()
    for i in range(len(digital_inputs)):
        digital_inputs[i].Set(str(joystick.get_button(i)))
    for i in range(len(analog_inputs)):
        val = joystick.get_axis(i)
        if val != 0.0:
            analog_inputs[i].Set(str(round(val, 3)))
    for i in range(len(hat_inputs)):
        val = joystick.get_hat(i)
        hat_inputs[i].Set(str(val))
    root.after(30, update_inputs)

reset_boxes()

root.after(30, update_inputs)
root.mainloop()
