# Script Name: kerbalformulae.py
# Author: Milo Sanu	
# Created: 2/15/15
# Last Modified:
# Version: 2.0
# Modifications:
# Description: This script provides the user with mission planning data. Data includes
#				maneuver deltaV's and time spent of dark side of celestial bodies. 

from math import sin,cos,sqrt,pi
from decimal import Decimal, getcontext
from functools import partial


# 20115 char 463 lines ######################################################
######################## 		Constants     		 #########################

gravity_constant = 6.67384*pow(10,-11)
deltaVtakeoff  = 4620 #m/s
getcontext().prec = 4

planets = {
'Sun':{'mu':1.1723328*pow(10,18),'radius': 261600000,'Ap':0,'Po':0, 'Incline':0,'Parent':'Sun','Moons':'Moho\nEve\nKerbin\nDuna\nDres\nJool\nEeloo'},
'Moho':{'mu':1.6860938*pow(10,11),'radius':250000,'Ap':6315765980,'Po':4210510628, 'Incline':7,'Parent':'Sun','Moons':'No Moons Available'},
'Eve':{'mu':8.1717302*pow(10,12),'radius':700000,'Ap':9931011387,'Po':9734357701, 'Incline':2.1,'Parent':'Sun','Moons':'Gilly'},
'Kerbin':{'mu':3.52316*pow(10,12),'radius':600000,'Ap':13599840256,'Po':13599840256, 'Incline':0,'Parent':'Sun','Moons':'Mun\nMinmus'},
'Duna':{'mu':3.0136321*pow(10,11),'radius':320000,'Ap':21783189163,'Po':19669121365, 'Incline':.06,'Parent':'Sun','Moons':'Ike'},
'Dres':{'mu':2.1484489*pow(10,10),'radius':138000,'Ap':46761053522,'Po':34917642884, 'Incline':5,'Parent':'Sun','Moons':'No Moons Available'},
'Jool':{'mu':2.82528*pow(10,14),'radius':6000000,'Ap':72212238387,'Po':65334882253, 'Incline':1.304,'Parent':'Sun','Moons':'Laythe\nVall\nTylo\nBop\nPol'},
'Eeloo':{'mu':7.4410815*pow(10,10),'radius':210000,'Ap':113549713200,'Po':66687926800,'Incline':6.15, 'Parent':'Sun','Moons':'No Moons Available'},
'Gilly':{'mu':8.28945*pow(10,6),'radius':13000,'Ap':48825000,'Po':14175000, 'Incline':12,'Parent':'Eve','Moons':'No Moons Available'},
'Mun':{'mu':6.5138398*pow(10,10),'radius':200000,'Ap':12000000,'Po':12000000, 'Incline':0,'Parent':'Kerbin','Moons':'No Moons Available'},
'Minmus':{'mu':1.7658*pow(10,9),'radius':60000,'Ap':47000000,'Po':47000000, 'Incline':6,'Parent':'Kerbin','Moons':'No Moons Available'},
'Ike':{'mu':1.8568368*pow(10,10),'radius':130000,'Ap':3296000,'Po':3104000, 'Incline':.2,'Parent':'Duna','Moons':'No Moons Available'},
'Laythe':{'mu':1.962*pow(10,12),'radius':500000,'Ap':27184000,'Po':27184000, 'Incline':0,'Parent':'Jool','Moons':'No Moons Available'},
'Vall':{'mu':2.074815*pow(10,11),'radius':300000,'Ap':43152000,'Po':43152000, 'Incline':0,'Parent':'Jool','Moons':'No Moons Available'},
'Tylo':{'mu':2.82528*pow(10,12),'radius':600000,'Ap':68500000,'Po':68500000, 'Incline':.025,'Parent':'Jool','Moons':'No Moons Available'},
'Bop':{'mu':2.4868349*pow(10,9),'radius':65000,'Ap':158697500,'Po':98302500, 'Incline':15,'Parent':'Jool','Moons':'No Moons Available'},
'Pol':{'mu':721702080,'radius':44000,'Ap':210624206,'Po':149155794, 'Incline':4.25,'Parent':'Jool','Moons':'No Moons Available'},
}

######################## 		Constants     		 #########################
##############################################################################

##############################################################################
######################## 		Function Area		 #########################

def circlegraph(radius,angle):
	'''Provides X and Y coordinates to a circle'''
	angle = float(angle)*float(pi/180)
	x=radius*cos(angle)
	if angle >= pi:
		y=radius*sin(angle)
	return x,y

def sphere_of_influence(planet):
	''' This function calculates the effective sphere of influence of a planet'''
	massPlanet = Decimal(planets[planet.capitalize()]['mu']) / Decimal(6.67384*pow(10,-11))
	massSun = Decimal(planets[planets[planet]['Parent']]['mu']) / Decimal(6.67384*pow(10,-11))
	average = Decimal(planets[planet.capitalize()]['Ap'] + planets[planet.capitalize()]['Po']) / Decimal(2)
	exponent = Decimal(2)/Decimal(5)
	soi = Decimal(average)*(Decimal(massPlanet)/Decimal(massSun))**exponent
	return soi.__float__()

#Input is degree change 
def inclination_change(velocity,degree_change): #ic
	'''Delivers the deltaV needed to execute an inclination change of X at a
	particular altitude
	velocity ==> V in meters per second
	degree_change ==> X in degrees
	'''
	angle = Decimal(degree_change)/Decimal(2)*Decimal(.0175)
	deltaV=2*velocity*sin(angle)
	return deltaV #in m/s

#Input in excel sheet is Orbiting Body and Altitude	
def orbital_velocity(mu,distance): #ov
	''' Determines average orbital velocity '''
	factor=Decimal(mu)/Decimal(distance)
	velocity = sqrt(factor)
	return velocity.__float__() # in m/s

def orbital_period(mu,distance): #op
	'''Determines the orbital period in terms of total seconds'''
	factor=Decimal(pow(distance,3))/Decimal(mu)
	time = 2 * pi * sqrt(factor)
	return time.__float__() # in seconds

def escape_velocity(mu,planet_radius): #ev
	'''Determines the escape velocity of the parent body'''
	factor=(Decimal(2)*Decimal(mu))/Decimal(planet_radius)
	esp_velocity= sqrt(factor)
	return esp_velocity.__float__()

#pt
# delta V, slightly off. May just be a rounding error 
# consider breaking this function up that you can provide and outline for
# deltaV use. 
def planet_transfer(origin_body,target_body,origin_body_orbit,target_body_orbit):
	''' This function attempts to calculate the amount of DeltaV required for a 
	planetary transfer in KSP. It's last step assumes that you'll be entering at 
	75% of the SOI of your target planet. Therefore, the hohmann transfer to 
	your desired orbit is also included in the total calculation'''

	## determine what the origin and target planet are
	## determine the orbits around origin and target planet

	target_body_SOI_entry = Decimal(sphere_of_influence(target_body))*Decimal(.75)

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

	factor = [Decimal(2)/ Decimal(distance1),Decimal(2)/ Decimal(distance1 + distance2)]
	VexitSOI = sqrt( Decimal(planets['Sun']['mu']) * Decimal(factor[0].__float__() - factor[1].__float__()))

	## determine what your velocity will be when entering the target SOI
	factor = [Decimal(2)/ Decimal(distance2),Decimal(2)/ Decimal(distance1 + distance2)]
	VentrySOI = sqrt( Decimal(planets['Sun']['mu']) * Decimal(factor[0].__float__() - factor[1].__float__())) 

	Vexit = abs(float(VexitSOI - orig_planet_velocity))
	Ventry = float(VentrySOI - tar_planet_velocity)
	
	origin_body,target_body = planets[origin_body],planets[target_body]
	
	#determine velocity just after injection burn
	factor = [Decimal(Vexit**2) / Decimal(2), Decimal(origin_body['mu']) / Decimal(semimajor_axis_origin)]
	VelocityInjection = sqrt ( 2 * Decimal(factor[0].__float__() + factor[1].__float__()))

	#determine velocity of hyberpolic orbit over target planet
	factor = [Decimal(Ventry**2) / Decimal(2),Decimal(target_body['mu']) / Decimal(semimajor_axis_target)]
	HyperbolicVelocity = sqrt ( 2 * Decimal(factor[0].__float__() + factor[1].__float__()))

	## determine deltaV for injection and capture

	deltaVinjection =  Decimal(VelocityInjection - semimajor_axis_origin_velocity)
	deltaVcapture = Decimal(HyperbolicVelocity - semimajor_axis_target_velocity)

	target_body_orbit = Decimal(target_body_orbit)
	## hohmann transfer from heigh of hyperbolic entry to desired orbit
	ht = hohmann_transfer(target_body_SOI_entry,target_body_orbit,target_body['radius'],target_body['mu'])

	## add the deltaV's together

	deltaVtransfer= float(deltaVinjection + deltaVcapture) + ht


	print "Velocity of origin planet around Kerbol: %.2f \nVelocity of target planet around Kerbol:%.2f \n\
Velocity after exiting origin SOI:%.2f \nVelocity before entering origin SOI:%.2f \nVelocity before exiting origin SOI:%.2f\n\
Velocity after entering target SOI:%.2f \nVelocity after injection burn:%.2f \nHyperbolicVelocity:%.2f \n\
deltaV required for Capture:%.2f \ndeltaV required for injection:%.2f \nhohmann transfer to desired orbit: %.2f \n\
SOI entry: %.2f \ndeltaV:%.2f" % (orig_planet_velocity,tar_planet_velocity,VexitSOI,VentrySOI,Vexit,Ventry,VelocityInjection,HyperbolicVelocity,deltaVcapture,deltaVinjection,ht,target_body_SOI_entry,deltaVtransfer)
	
	return deltaVtransfer

#mt
def moon_transfer(parent_body,moon,parent_orbit,moon_orbit):
	'''DeltaV needed to transfer to a moon of the parent body'''
	mu= planets[parent_body]['mu']
	
	original_majoraxis = planets[parent_body]['radius'] + parent_orbit
	
	initial_velocity = sqrt(Decimal(mu)/Decimal(original_majoraxis))
	
	transfer_majoraxis = Decimal(original_majoraxis + moon_orbit)/Decimal(2)
	
	factor = [Decimal(2) / Decimal(original_majoraxis),Decimal(1) / Decimal(transfer_majoraxis)]
	transfer_velocity = sqrt(mu*(factor[0].__float__()-factor[1].__float__()))

	deltaV_A = transfer_velocity - initial_velocity
	return deltaV_A

#ht
def hohmann_transfer(original_orbit,final_orbit,planetradius,planetmu):
	'''Returns DeltaV needed to perform desired Hohmann Transfer manuever'''
	mu = Decimal(planetmu)
	originalDistance = original_orbit + planetradius
	finalDistance = final_orbit + planetradius
	transfer_majoraxis = Decimal(originalDistance + finalDistance)/Decimal(2)
	initialvelocity = orbital_velocity(mu,originalDistance)
	finalvelocity = orbital_velocity(mu,finalDistance)
	factor1 = Decimal(2)/Decimal(originalDistance)
	factor2 = Decimal(1)/Decimal(transfer_majoraxis)
	factor3 = Decimal(2)/Decimal(finalDistance)
	transfervelocitybegin = Decimal(sqrt(Decimal(mu)*Decimal((factor1-factor2))))
	transfervelocitybegin = Decimal(sqrt(Decimal(mu)*Decimal((factor1-factor2))))
	transfervelocityfinal = Decimal(sqrt(Decimal(mu)*Decimal((factor3-factor2))))
	deltaA = Decimal(transfervelocitybegin) - Decimal(initialvelocity)
	deltaB = Decimal(finalvelocity) - Decimal(transfervelocityfinal)
	deltaTransfer = float(Decimal(deltaA) + Decimal(deltaB))
	return abs(deltaTransfer)

#td
def timeindarkness(planet,distance):
	'''Determines how long, in minutes, a satellite will be in the shadow of its parent body'''
	C=Decimal(planet)/Decimal(distance)
	#Arc length, C in radians	-	http://www.mathopenref.com/arclength.html
	length=Decimal(distance)*Decimal(C)*Decimal(2)
	
	velocity=orbital_velocity(planets[planet.capitalize()]['mu'],distance)
	
	time = Decimal(length)/Decimal(velocity)
	time = Decimal(time)/Decimal(60)
	return time # in minutes


def landing(displacement,planet,mu):
	'''Calculates the deltaV needed to land on a vacuum planet'''
	surface_gravity=float(mu)/float(pow(planets[planet.capitalize()]['radius'],2))
	time_seconds=sqrt((2*displacement)/surface_gravity)
	orbitalVelocity = orbital_velocity(mu,displacement)
	#from my landing path to the surface. 
	deltaVforLanding = float(.5*surface_gravity*time_seconds)# + orbitalVelocity
	print deltaVforLanding
	descent_deltaV=deltaVforLanding - orbitalVelocity
	print 'Descent time from %s meters: %s seconds' % (displacement,time_seconds)
	return descent_deltaV
######################## 		Function Area		 #########################
##############################################################################

##############################################################################
################################# Calling Area ###############################

def altitude_q():
	txt ='What is Your Altitude, in Km?\n> '
	altitude = float(raw_input(txt))*1000
	return altitude
	
def orbiting_body(relation):
	txt = '\nWhat body are you '+relation+'?\n'+planets['Sun']['Moons']+'\n> '
	body = raw_input(txt)
	planet = planets[body.capitalize()]
	return body, planet

def ic():
	body,planet = orbiting_body('orbiting')
	mu = planet['mu']
	altitude = altitude_q()
	distance = planet['radius'] + altitude
	velocity = orbital_velocity(mu,distance)
	txt ='How many degrees would you like to change your orbit by?\n> '
	inclin_delta = raw_input(txt)
	return inclination_change(velocity,inclin_delta)

def ov():
	body,planet = orbiting_body('orbiting')
	mu = planet['mu']
	altitude = altitude_q()
	distance = float(planet['radius'] + altitude)
	velocity = orbital_velocity(mu,distance)
	return velocity
	
def ev():
	body,planet = orbiting_body('orbiting')
	ev = escape_velocity(planet['mu'],planet['radius'])
	return body,ev
	
def pt():
	bodyA,planetA = orbiting_body('departing from')
	bodyB,planetB = orbiting_body('arriving at')
	txt = "\nWhat is your orbit around %s, in Km:\n> " %(bodyA.capitalize())
	orbitA = float(raw_input(txt))*1000
	txt = "\nWhat is your orbit around %s, in Km: \n> " %(bodyB.capitalize())
	orbitB = float(raw_input(txt))*1000	
	answer = planet_transfer(bodyA.capitalize(),bodyB.capitalize(),orbitA,orbitB)
	return answer
	
def ht():
	body,planet = orbiting_body('orbiting')
	txt = "What is your current orbit, in Km?\n> "
	original_orbit = float(raw_input(txt))*1000
	txt = "What is your target orbit, in Km?\n> "
	final_orbit = float(raw_input(txt))*1000
	return hohmann_transfer(original_orbit,final_orbit,planet['radius'],planet['mu'])
	
def td():
	txt = '\nwhat is your expected orbit, in Km? \n> '
	distance = int(raw_input(txt))*1000
	txt = 'What is the parent body?\n'+str(planets.keys())+'\n> '
	planet = raw_input(txt)
	return float(timeindarkness(planet['radius'],distance))

def mt():
	parent = orbiting_body()
	sat_list = ''
	sat_list = planets[parent.capitalize()]['Moons']
	
	if sat_list != 'No Moons Available':
		txt = '\nwhat is your orbit around %s, in Km? \n> ' % (parent.capitalize())
		parent_orbit = int(raw_input(txt))*1000
	
		txt = 'What satellite are you looking to transfer to:\n' + sat_list + '\n> '
		moon = raw_input(txt)
	
		moon_orbit = Decimal(planets[moon.capitalize()]['Ap'] + planets[moon.capitalize()]['Po'])/Decimal(2)
	
		return moon_transfer(parent.capitalize(),moon.capitalize(),parent_orbit,moon_orbit)
	else: return 'No Moons Available'
			
def lg():
	planet = orbiting_body()
	mu = planets[planet.capitalize()]['mu']
	altitude = altitude_q()
	return landing(altitude,planet,mu)

def main():
	'''Navigation function. Not case sensitive.'''
	
	print "	    Utility					Description   "
	print "---------------------		----------------------------------------------------------	"
	print "Escape Velocity			 Determine the escape velocity of a celestial body."
	print "Inclination Change		 Determine deltaV needed to perform an inclination change."
	print "Orbital Velocity		 Determine orbit velocity of an orbit."
	print "Landing				 Determine deltaV required to land on a planet."
	print "Planet Transfer			 Determine deltaV required to transfer to a new planet."
	print "Hohmann Transfer		 Determine deltaV required to change orbit."
	print "Moon Transfer			 Determine deltaV required to reach a moon. "
	print "Battery Requirements		 Determine amount of time in darkness for a specific orbit. "
	print "Quit"
	
	txt = raw_input(">	")

	txt = txt.lower()
	if txt == 'inclination change':
		answer = ic()
		return 'deltaV required: %.2f m/s' % (answer)
	elif txt == 'orbital velocity':
		answer = ov()
		return '%.2f m/s' % (answer)
	elif txt == 'landing':
		answer = lg()
		return 'DeltaV needed to land: %.2f m/s' % (answer)
	elif txt == 'moon transfer':
		answer = mt()
		if answer == 'No Moons Available':
			return answer
		else:
			return 'deltaV required: %.2f m/s' % (answer)	
	elif txt == 'escape velocity':
		answer = ev()
		return 'Velocity required to escape %s is %.2f m/s' % (answer[0].capitalize(),answer[1])
	elif txt == 'planet transfer':
		answer =  pt()
		return 'deltaV required: %.2f m/s' % (answer)
	elif txt == 'hohmann transfer':
		answer = ht()
		return ' delta V required for maneuver: %.2f m/s ' % (answer)
	elif txt == 'battery requirements':
		answer = td()
		return '%.2f mintues in darkness' % (answer)
	elif txt == 'quit':
		return 'Quitting'
	else:
		return "I dont know what you're looking for. Please try again"


def run():
	print '''
Welcome to my Kerbal orbital mechanics and flight planning software. 
This program was built to help those Kerbal scientists who were barely
passing Professor Wernher von Kerman Rocket Science course.
	'''
	
	status=''

	while status != 'Quitting':
		status = main()
		print '\n****	' + status + '	****\n'
print 'To start script, execute .run()'
#run()

################################# Calling Area ###############################
##############################################################################

########################################################
##################### Testing Area #####################


##################### Testing Area #####################
########################################################


