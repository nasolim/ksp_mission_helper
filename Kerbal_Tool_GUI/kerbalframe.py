from Tkinter import *
import kerbalformulae

mainLabel = '''
Welcome to my Kerbal orbital mechanics and flight planning software. 
This program was built to help those Kerbal scientists who were on the barely 
brink of passing Professor Wernher von Kerman Rocket Science course.'''

root=Tk()

topframe=Frame(root)
topframe.pack()
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

#button1 = Button(topframe,text = 'Button 1', fg = 'red')
#button2 = Button(bottomframe,text = 'Button 2', fg = 'blue')


#frame=Frame(root)

topLabel = Label(topframe, text = '''
Welcome to my Kerbal orbital mechanics and flight planning software. 
This program was built to help those Kerbal scientists who were on the barely 
brink of passing Professor Wernher von Kerman Rocket Science course.''')

button1 = Button(bottomframe,text = 'Inclination Transfer')
button2 = Button(bottomframe,text = 'Orbital Velocity')
button3 = Button(bottomframe,text = 'Hohmann Transfer')
button4 = Button(bottomframe,text = 'Moon Transfer')
button5 = Button(bottomframe,text = 'Planetary Transfer')
button6 = Button(bottomframe,text = 'Escape Velocity')

#button1.pack()
#button2.pack()
#button3.pack()
#button4.pack()
#button5.pack()
#button6.pack()


topLabel.pack(fill=X)
button1.grid(row = 1, column = 1)
button2.grid(row = 1, column = 2)
button3.grid(row = 2, column = 1)
button4.grid(row = 2, column = 2)
button5.grid(row = 3, column = 1)
button6.grid(row = 3, column = 2)


root.mainloop()