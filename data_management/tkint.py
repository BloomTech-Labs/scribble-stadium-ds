from tkinter import *

#run function when button is pressed
def button_test ():
    print ('hello')


root = Tk()

myButton = Button( root, text = 'button' )
myButton['command'] = button_test
myButton.pack()
myLabel = Label(root, text = 'strings')
myLabel.pack()



root.mainloop()

