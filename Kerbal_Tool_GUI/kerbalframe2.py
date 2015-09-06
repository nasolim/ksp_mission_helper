from Tkinter import *

root=Tk()

mainframe = Frame(root)
mainframe.pack()

topLabel = Label(mainframe, text = 'Tool Name')
infolabel = Label(mainframe,text = 'Ascent: 4600 \n Inclination Change: 200 \n Moon Transfer: 800 \n Capture: 300 \n Hohmann Transfer to 40KM: 500',bd = 1,relief=SUNKEN,anchor=W)
add_maneuverButton = Button(mainframe,text = 'Add Maneuver')
mainmenuButtion = Button(mainframe,text = 'Main Menu')

var = StringVar(mainframe)
var.set("Kerbin") # initial value


label_1 = Label(mainframe, text = 'Orbiting Body')
label_1Input = OptionMenu(mainframe, var,"Kerbin", "Moho", "Eve", "Jool","Dres","Eeloo")
label_2 = Label(mainframe, text = 'Altitude above Sea Level') 
label_3 = Label(mainframe, text = 'Target Body')
label_4 = Label(mainframe, text = 'Altitude above Sea Level')


topLabel.grid( row = 0, columnspan = 4 ) 
infolabel.grid( row = 1, rowspan = 4, column = 2, columnspan = 2)

label_1.grid( row = 1, column = 0)
label_1Input.grid( row = 1, column = 1)
label_2.grid( row = 2, column = 0, columnspan = 2 )
label_3.grid( row = 3, column = 0, columnspan = 2 )
label_4.grid( row = 4, column = 0, columnspan = 2 )


add_maneuverButton.grid( row = 5, column = 2 )
mainmenuButtion.grid( row = 5, column = 0, columnspan = 2)

root.mainloop()