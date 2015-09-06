import math
import decimal

def orbital_velocity(planet_radius,GM):
	altitude=decimal.Decimal(raw_input('how high above the surface of the planet are you?>	'))
	
	#velocity(m/s)=sqrt(GM*((2/altitude)-(1/planer_radius)))
	
	a=decimal.Decimal(altitude)+planet_radius
	gm=decimal.Decimal(GM)
	
	velocity = decimal.Decimal(math.sqrt(gm/a))
	print format(velocity,'.2f'),'m/s'
	
	
orbital_velocity(600000,3.52*10**12)




def deltaVinclination(initial_velocity,change_in_angle):
	