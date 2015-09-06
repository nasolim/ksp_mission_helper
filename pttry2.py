from kerbalformulae import *
from decimal import *
from math import *


def sphere_of_influence(planet):
	''' This function calculates the effective sphere of influence of a planet'''
	massPlanet = Decimal(planets[planet.capitalize()]['mu']) / Decimal(6.67384*pow(10,-11))
	massSun = Decimal(planets[planets[planet]['Parent']]['mu']) / Decimal(6.67384*pow(10,-11))
	average = Decimal(planets[planet.capitalize()]['Ap'] + planets[planet.capitalize()]['Po']) / Decimal(2)
	exponent = Decimal(2)/Decimal(5)
	soi = Decimal(average)*(Decimal(massPlanet)/Decimal(massSun))**exponent
	return soi


def planet_transfer(origin_body,target_body,origin_body_orbit,target_body_orbit):
	''' This function attempts to calculate the amount of DeltaV required for a 
	planetary transfer in KSP. It's last step assumes that you'll be entering at 
	75% of the SOI of your target planet. Therefore, the hohmann transfer to 
	your desired orbit is also included in the total calculation'''

	## determine what the origin and target planet are

	## determine the orbits around origin and target planet

	target_body_SOI_entry = Decimal(sphere_of_influence(target_body.capitalize()))*Decimal(.75)

	semimajor_axis_origin = origin_body_orbit + planets[origin_body]['radius']
	semimajor_axis_target = target_body_SOI_entry + planets[target_body]['radius']

	## determine orbital velocity of planets around the sun

	distance1 = Decimal(planets[origin_body]['Ap']+planets[origin_body]['Po']) / Decimal(2)
	distance2 = Decimal(planets[target_body]['Ap']+planets[target_body]['Po']) / Decimal(2)

	orig_planet_velocity = float(orbital_velocity(planets[planets[origin_body]['Parent']]['mu'],distance1))
	tar_planet_velocity = float(orbital_velocity(planets[planets[target_body]['Parent']]['mu'],distance2))


	## determine orbital velocity of craft about target and origin

	semimajor_axis_origin_velocity = float(orbital_velocity(planets[origin_body]['mu'],semimajor_axis_origin))
	semimajor_axis_target_velocity = float(orbital_velocity(planets[target_body]['mu'],semimajor_axis_target))

	## determine what your velocity will be when exiting the origin SOI
	factor1 = Decimal(2)/ Decimal(distance1)
	factor2 = Decimal(2)/ Decimal(distance1 + distance2)

	VexitSOI = sqrt( Decimal(planets['Sun']['mu']) * Decimal(factor1 - factor2))



	## determine what your velocity will be when entering the target SOI
	factor1 = Decimal(2)/ Decimal(distance2)
	factor2 = Decimal(2)/ Decimal(distance1 + distance2)
	VentrySOI = sqrt( Decimal(planets['Sun']['mu']) * Decimal(factor1 - factor2)) 

	Vexit = abs(float(VexitSOI - orig_planet_velocity))
	Ventry = float(VentrySOI - tar_planet_velocity)

	#determine velocity just after injection burn
	factor1 = Decimal(Vexit**2) / Decimal(2)
	factor2	= Decimal(planets[origin_body]['mu']) / Decimal(semimajor_axis_origin)
	VelocityInjection = sqrt ( 2 * Decimal(factor1 + factor2))

	#determine velocity of hyberpolic orbit over target planet

	factor1 = Decimal(Ventry**2) / Decimal(2)
	factor2	= Decimal(planets[target_body]['mu']) / Decimal(semimajor_axis_target)
	HyperbolicVelocity = sqrt ( 2 * Decimal(factor1 + factor2))

	## determine deltaV for injection and capture

	deltaVinjection =  float(VelocityInjection - semimajor_axis_origin_velocity)
	deltaVcapture = float(HyperbolicVelocity - semimajor_axis_target_velocity)

	## hohmann transfer from heigh of hyperbolic entry to desired orbit
	ht = hohmann_transfer(target_body_SOI_entry,target_body_orbit,target_body.capitalize())

	## add the deltaV's together

	deltaV= float(deltaVinjection + deltaVcapture) + ht


	print 'Velocity of origin planet around Kerbol: %.2f' % (orig_planet_velocity)
	print 'Velocity of target planet around Kerbol:%.2f' % (tar_planet_velocity)
	print 'Velocity after exiting origin SOI:%.2f' % (VexitSOI)
	print 'Velocity before entering origin SOI:%.2f' % (VentrySOI)
	print 'Velocity before exiting origin SOI:%.2f' % (Vexit)
	print 'Velocity after entering target SOI:%.2f' % (Ventry)
	print 'Velocity after injection burn:%.2f' % (VelocityInjection)
	print 'HyperbolicVelocity:%.2f' % (HyperbolicVelocity)
	print 'deltaV required for Capture:%.2f' % (deltaVcapture)
	print 'deltaV required for injection:%.2f' % (deltaVinjection)
	print 'hohmann transfer to desired orbit: %.2f' % (ht)
	print 'SOI entry: %.2f'  % (target_body_SOI_entry)
	print 'deltaV:%.2f' % (deltaV)

print planet_transfer('Kerbin','Duna',100000,100000)

#print float(sphere_of_influence('Mun'))