#from kerbalformulae import orbital_velocity,ov, planets
from decimal import Decimal
import math
import numpy


#def landing(displacement,planet,mu):
#	surface_gravity=mu/(math.pow(planets[planet.capitalize()]['radius'],2))
#	time_seconds=math.sqrt((2*displacement)/surface_gravity)
#	orbitalVelocity = orbital_velocity(mu,displacement)
#	finalVelocity = float(.5*surface_gravity*time_seconds) + orbitalVelocity
#	descent_deltaV=finalVelocity - orbitalVelocity
#	print 'Descent time from %s meters: %s seconds' % (displacement,time_seconds)
#	return descent_deltaV


planets = {
'Sun':{'mu':1.1723328*pow(10,18),'radius': 261600000,'Ap':0,'Po':0, 'Incline':0,'Parent':'Sun'},
'Moho':{'mu':168609380000,'radius':250000,'Ap':6315765980,'Po':4210510628, 'Incline':7,'Parent':'Sun'},
'Eve':{'mu':8171730200000,'radius':700000,'Ap':9931011387,'Po':9734357701, 'Incline':2.1,'Parent':'Sun'},
'Kerbin':{'mu':3523160000000,'radius':600000,'Ap':13599840256,'Po':13599840256, 'Incline':0,'Parent':'Sun'},
'Duna':{'mu':301363210000,'radius':320000,'Ap':21783189163,'Po':19669121365, 'Incline':.06,'Parent':'Sun'},
'Dres':{'mu':21484489000,'radius':138000,'Ap':46761053522,'Po':34917642884, 'Incline':5,'Parent':'Sun'},
'Jool':{'mu':282528000000000,'radius':6000000,'Ap':72212238387,'Po':65334882253, 'Incline':1.304,'Parent':'Sun'},
'Eeloo':{'mu':74410815000,'radius':210000,'Ap':113549713200,'Po':66687926800,'Incline':6.15, 'Parent':'Sun'},
'Gilly':{'mu':8289450,'radius':13000,'Ap':48825000,'Po':14175000, 'Incline':12,'Parent':'Eve'},
'Mun':{'mu':65138398000,'radius':200000,'Ap':12000000,'Po':12000000, 'Incline':0,'Parent':'Kerbin'},
'Minmus':{'mu':1765800000,'radius':60000,'Ap':47000000,'Po':47000000, 'Incline':6,'Parent':'Kerbin'},
'Ike':{'mu':18568368000,'radius':130000,'Ap':3296000,'Po':3104000, 'Incline':.2,'Parent':'Duna'},
'Laythe':{'mu':1962000000000,'radius':500000,'Ap':27184000,'Po':27184000, 'Incline':0,'Parent':'Jool'},
'Vall':{'mu':207481500000,'radius':300000,'Ap':43152000,'Po':43152000, 'Incline':0,'Parent':'Jool'},
'Tylo':{'mu':2825280000000,'radius':600000,'Ap':68500000,'Po':68500000, 'Incline':.025,'Parent':'Jool'},
'Bop':{'mu':2486834900,'radius':65000,'Ap':158697500,'Po':98302500, 'Incline':15,'Parent':'Jool'},
'Pol':{'mu':721702080,'radius':44000,'Ap':210624206,'Po':149155794, 'Incline':4.25,'Parent':'Jool'},
}

def eccentricity(ap,pe,a):
	ea=float(1)-float(ap/a)
	ep=float(pe/a)-float(1)
	return ep
	
	
def semimajoraxis(ap,pe):
	a=float((ap+pe)/2)
	return a
#	planet = raw_input('Which planet are you circling?>		')
#	return eccentricity(ap,pe,a), meanMotion(planet,a)

def orbital_velocity(mu,distance): #ov
	''' Determines average orbital velocity '''
	factor=float(mu/distance)
	velocity = math.sqrt(factor)
	return velocity # in m/s

def orbiting_body():
	txt = '\nWhat is the Orbiting Body?\n'+str(planets.keys())+'\n> '
	planet = raw_input(txt)
	return planet

def semiMinoraxis(ap,pe):
	major_axis = semimajoraxis(ap,pe)
#	print "major axis: %s" %(major_axis)
	semi_major_axis = Decimal(major_axis) / Decimal(2)
	print "semi major axis: %.2f" %(semi_major_axis)
	eccent = eccentricity(ap,pe,semi_major_axis)
	print "eccentricity: %.2f" %(eccent)
	variable = Decimal(1) - Decimal(eccent ** 2)
#	print "variable: %s" %(variable)
	semi_minor_axis = Decimal(semi_major_axis) * Decimal(math.sqrt(variable))
	print "semi_minor_axis: %.2f" %(semi_minor_axis)


def testlanding():
#	apogee = float(raw_input('what is your descent Ap, in Km?\n> '))*1000
#	pergee = float(raw_input('what is your descent Pe, in Km?\n> '))*1000
#	descentheight = float(raw_input('what is your height before descent,in Km?\n> '))*1000
#	alt_terrain = float(raw_input('what is the height of the terrain,in Km?\n> '))*1000
#	planet = orbiting_body()
	radius = int(planets[planet]['radius'])
	print 'radius:	', radius
	Ap=apogee+radius
	print 'Ap:	',Ap
	Po=pergee+radius
	print 'Po:	',Po
	tup = (Ap,Po)
	semiMinoraxis(Ap,Po)
	mu = planets[planet]['mu']
	if semiMinoraxis <= (.5*radius):
		print 'this wont result in a landing'
	else:
		print 'the semi minor is less than the radius'
		orbit=numpy.average(tup)
		print orbit
		orbitalvelocity = orbital_velocity(mu,(orbit+radius))
		print 'orbitalvelocity:	',orbitalvelocity
		surface_gravity=float(mu)/float(pow(planets[planet.capitalize()]['radius'],2))
		print 'g: ',surface_gravity
#		time_seconds=math.sqrt((2*descentheight)/surface_gravity)
#		print 'time: ',time_seconds
#		landing = float(.5*surface_gravity*time_seconds)
		landing= math.sqrt((orbitalvelocity**2) + 2 * (-surface_gravity) * (alt_terrain-descentheight))
		print 'landing: ',landing
		landing = orbitalvelocity + landing
		print 'V needed for landing: ',landing
		return landing


apogee=37600
pergee=-190100
descentheight=34705
alt_terrain=0
planet='Mun'

print testlanding()

######################################






