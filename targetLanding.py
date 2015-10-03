# Script Name: targetLanding.py
# Author: Milo Sanu	
# Created: 10/3/15
# Last Modified:
# Version: 1.0
# Modifications:
# Description: Script which provides the user with coordinates that are a predetermined 
# distance from the original landing site. 

from math import sin,cos,radians,pi,degrees
from kerbalformulae import orbiting_body
	
def py_theorem(d,ang):
	''' Given a displacement (d) - meters - and angle - degrees;
	 Return vertical and lateral distance '''
	dn = d * sin(radians(ang))
	de = d * cos(radians(ang))
	return dn,de

def perimeter_landing(Lat, Long, d, r):
	''' Provide current location (Lat, Long), desired displacement (d),
	 and radius (r) of landed body in meters
	 Returns Coordinate'''
	ang = [x for x in xrange(0,360,45)]
	landings=[new_position(Lat, Long, d, i, r) for i in ang]
	return landings
	
def new_position(Lat, Long, d, ang, r):
	''' Provide current location(Lat, Long), displacement (d) of next landing, angle (ang) from current location
	landed body radius in meters (r). 0 degree ang is East, 90 degree is North '''
	deltLat = float(py_theorem(d,ang)[0])/float(r)
	deltLong = float(py_theorem(d,ang)[1])/float(r) * cos(radians(Lat)) 
	lat2 = Lat + degrees(deltLat)
	long2 = Long + degrees(deltLong)
	return lat2,long2

compass_dir = [
'East',
'North-East',
'North',
'North-West',
'West',
'South-West',
'South',
'South-East']

def epicenter():
	latitude = float(raw_input('What is your Latitude?\n>'))
	longitude = float(raw_input('What is your Longitude?\n>'))
	displacement = float(raw_input('How far from your current location would you like to be?\n>'))
	body,celestial_radius = orbiting_body('parked on')
	position = [perimeter_landing(latitude,longitude, displacement, celestial_radius['radius'])]
	for item in range(len(compass_dir)):
		print compass_dir[item],'landing:\n','Lat: ',round(position[0][item][0],4),'Long: ',round(position[0][item][1],4)
