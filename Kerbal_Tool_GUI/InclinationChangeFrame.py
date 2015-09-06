from Tkinter import *

root=Tk()

mainframe = Frame(root)
mainframe.pack()

######## design the frame from the top and work clockwise #########

topLabel = Label(mainframe, text = 'Inclination Change')
resultslabel = Label(mainframe,text = 'Ascent: 4600 \n Inclination Change: 200 \n Moon Transfer: 800 \n Capture: 300 \n Hohmann Transfer to 40KM: 500',bd = 1,relief=SUNKEN,anchor=W)
add_maneuverButton = Button(mainframe,text = 'Add Maneuver')
mainmenuButtion = Button(mainframe,text = 'Main Menu')

degree_change = Label(mainframe, text = 'Number of degrees to change inclincation by:')
altitude = Label(mainframe, text = 'Altitude, in Km:')
altitudeInput = Entry(mainframe)
degree_changeInput = Entry(mainframe)


var = StringVar(mainframe)
var.set("Kerbin") # initial value
parent_body = Label(mainframe, text = 'orbiting body') 
parent_body_input = OptionMenu(mainframe, var,"Kerbin", "Moho", "Eve", "Jool","Dres","Eeloo")



topLabel.grid( row = 0, columnspan = 15 ) 
resultslabel.grid( row = 2, rowspan = 4, column = 10, columnspan = 4)
add_maneuverButton.grid( row = 6, column = 10, columnspan = 4)
mainmenuButtion.grid( row = 6, column = 1, columnspan = 2)
parent_body.grid( row = 2, column = 1, columnspan = 4)
parent_body_input.grid( row = 2, column = 6, columnspan = 2)
altitude.grid(row = 3, column = 1, columnspan = 4)
altitudeInput.grid(row = 3, column = 6, columnspan = 2)
degree_change.grid( row = 4, column = 1, columnspan = 4 )
degree_changeInput.grid( row = 4, column = 6, columnspan = 2 )


add_maneuverButton.grid( row = 5, column = 2 )
mainmenuButtion.grid( row = 5, column = 0, columnspan = 2)

root.mainloop()