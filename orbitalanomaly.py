from decimal import *
from math import *
from numpy import average, pi
#from kerbalformulae import planets, au

##############################################################################
#### This is meant to be used to help put satellites in synchronous orbits ###
#### and to determine satellite locations at a particular moment. ############
#### can also be used to determine planet locations ##########################
##############################################################################



# \ = continued line
##############################################################################
######################## 		Function Area		 #########################

#def eccentricAnomaly(V,e):
#	n=Decimal(e)+Decimal(cos(V))
#	d=Decimal(1)+Decimal(e)*Decimal(cos(V))
#	E=float(acos(n/d))
#	return E









#def flightpathangle(V,e):
#	E=1+Decimal(e)*Decimal(cos(V))
#	E=(Decimal(e)*Decimal(sin(V)))/Decimal(E)
#	E=Decimal(atan(E))
#	return E

#def meanAnomaly(e,E):
#	M=Decimal(E)-Decimal(e)*Decimal(sin(E))
#	return M
#	#M=E-esin(E)




def position(M,n,f,s): #answer is in radians
	M = float(n*s)+ float(M)
	return M

	
#def trueAnomaly(a,e,pe):
#	V=Decimal(a)*(Decimal(1)-Decimal(e**2))/Decimal(pe)
#	V=V-1
#	V=Decimal(V)/Decimal(e)
#	V=Decimal(acos(V))
#	return eccentricAnomaly(V,e)
#	#V=(((Decimal(a)*(Decimal(1)-Decimal(e**2)))		\\
	#/Decimal(pe))-Decimal(1))/Decimal(e)


		
#def eccentricity(ap,pe,a):
#	ea=Decimal(1)-(Decimal(ap)/Decimal(a))
#	ep=(Decimal(pe)/Decimal(a))-Decimal(1)
#	return ep
#	return trueAnomaly(a,ep,pe)


def timeinflight(V,e,a):
	#V - esin(V)*sqrt(a^3/mu)
	srt = pow(a,3) / planets['Sun']['mu']
	print srt
	print 'V: ',V
	print 'e: ',e
	print 'a: ',a
	print 'sin(v): ',sin(V)
	TOF = float(V - (e*sin(V)) * sqrt(srt))
	return TOF
	
######################## 		Function Area		 #########################
##############################################################################

##############################################################################
######################## 		Testing Area		 #########################

########
mu_earth=3530
#float(3.986004418e5)

#a = 26500

#n = meanMotion(mu_earth,a)

#f = radians(5)

#e = Decimal(0.6)

#E = eccentricAnomaly(f,e)

#M = meanAnomaly(e,E)

#time = 60

#position = position (M,n,f,time)

#print position, 'radians', '\n'

########
#print degrees(position), 'degrees'

#print f,'radians','\n', n,'radians/sec'

#def flighttime(planetA,planetB):
#	radiusA = Decimal(planets[planetA.capitalize()]['Ap'] + planets[planetA.capitalize()]['Po'])/Decimal(au)
#	radiusB = Decimal(planets[planetB.capitalize()]['Ap'] + planets[planetB.capitalize()]['Po'])/Decimal(au)


#	V = float(trueAnomaly(a, e, radiusA))
#	radiusA = float(radiusA)
#	radiusB = float(radiusB)


#	tup = (radiusA,radiusB)
#	a = float(average(tup))
#	e = float(eccentricity(radiusA, radiusB, a))
#	E = float(eccentricAnomaly(V,e))
#	answer = timeinflight(V,e,a)
#	return answer
	
#print flighttime('Kerbin','Duna')	


#velocity at apogee or perigee


	
	
######################## 		Testing Area		 #########################
##############################################################################

def eccentricity(ap,pe):
	e = float(ap - pe)/float(ap + pe)
	return e

def orbitalperiod(mu,a):
	factor = float(a**3)/float(mu_earth)
	time = pi*2*sqrt(factor) # result in seconds
	return time
	
def velocity(mu,altit,body_radius,semi_major_axis):
	mu = mu
	alt = altit
	r=alt+body_radius
	a = semi_major_axis
	factor1 = float(2)/float(r)
	factor2 = float(1)/float(a)
	velocity = sqrt( mu * (factor1 - factor2))
	return velocity

def semimajoraxis(ap,pe):
	a=Decimal(ap+pe)/Decimal(2)
	return a
#	planet = raw_input('Which planet are you circling?>		')
#	return eccentricity(ap,pe,a), meanMotion(planet,a)

def eccentricanomaly(inital_position,mean_anomaly,eccent):
	eo = inital_position
	e = eccent
	m = mean_anomaly
	n = eo - e*sin(eo) - m
	d = 1 - e*cos(eo)
	E = eo - float(n)/float(d)
	return E

def true_anomaly(eccentric_anomaly,eccent):
	E = eccentric_anomaly
	e = eccent
	n = cos(E) - e
	d = 1 - e * cos(E)
	v = float(acos(n/d))
	return v

def flightpath(eccent, trueanomaly):
	'''flight-path angle'''
	e = eccent
	v = trueanomaly
	n = e * sin(v)
	d = 1 + e * cos(v)
	f = atan(n/d)
	return f

def altitude(semi_major_axis, eccent, eccentric_anomaly,body_radius):
	a = float(semi_major_axis)
	e = eccent
	E = float(eccentric_anomaly)
	alt = (a * (1 - e * cos(E))) - float(body_radius) # in km's
	return alt

def meanAnomalytime(meanmotion,time):
	m = meanmotion * time
	return m

def meanMotion(planet,a):
#	n=Decimal(sqrt(Decimal(planets[planet]['mu'])/(a**3)))
	factor= float(mu_earth)/float(a**3)
	n=sqrt(factor)
	return n



#Ra = 7778
#Rp = 6778
#body_radius= 6378#km

def altitudecalc(Ra,Rp,body_radius):
	a = semimajoraxis(Ra,Rp)
	e = eccentricity(Ra,Rp)
	mean_motion= meanMotion('Earth',a)
	period = orbitalperiod('Earth',a)
	apogeetime = float(period)/float(2)
	print 'a: ',a
	print 'e: ',e
	print 'Mean Motion: ',mean_motion
	print 'orbital period:	', period
	print 'apogee time: ', apogeetime
	
	for moment in range(0,int(period)):
		fd=open('testcase.csv','a')
		mean_anomaly = meanAnomalytime(mean_motion,moment)
		print 'Mean anomaly:	', mean_anomaly
		E = eccentricanomaly(mean_anomaly,mean_anomaly,e)
		print 'Eccentric anomaly:	',E
		tranom = true_anomaly(E,e)
		print 'True anomaly:	',tranom
#		flightpath = flightpath(e, tranom)
#		print 'flightpath:	',flightpath
		current_altitude = altitude(a,e,E,body_radius)
		print 'altitude: ', current_altitude
		current_velocity = velocity(mu_earth,current_altitude,body_radius,a)
		print 'velocity: ',current_velocity,'\n'
		myCsvRow = '%f,%f,%f\n' % (moment,current_altitude,current_velocity)
		fd.write(myCsvRow)
		fd.close()


