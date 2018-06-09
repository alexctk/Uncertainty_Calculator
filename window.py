from tkinter import *
import calc as c

# GUI using tkinter

root = Tk() # holds window with all other widgets

frame = Frame(root) # widget container, responsible for arranging other widgets
frame.pack()

bottomframe = Frame(root)
bottomframe.pack(side = "bottom")

# Widget syntax: variable_name = Widget_type(parent_widget, option1, option2, ...)

# text box
text_entry = Entry(frame, width = 20) # entry type widget
text_entry.pack(side = "left") # widget placement

# take string input and pass to calc module
# obtain result from calc module
def compute():
    text_input = text_entry.get()
    result = c.eval_input(text_input)
    print(result)
    result_label.configure(text=result.format(result))

compute = Button(frame, text = " calculate ", command = compute)
compute.pack(side='left', padx=4)

result_label = Label(frame, width = 20)
result_label.pack(side = "left")

quit_button = Button(bottomframe, text = "Quit", command=frame.quit)
quit_button.pack(side = "bottom")

root.mainloop()
