from math import sin,cos,radians,pi,degrees
	
def py_theorem(d,ang):
	''' Given a displacement (d) - meters - and angle - degrees, will return vertical and lateral distance '''
	dn = d * sin(radians(ang))
	de = d * cos(radians(ang))
	return dn,de
	

#	ne = ["latitude","longitude"]
#	coordinates=[]
#	for i in ne:
#		coordinates.append(int(raw_input("What is your "+i+" in degrees?\n>")))

def central_pt(Lat, Long, d, r):
	''' Provide current location (Lat, Long), desired displacement (d),
	 and radius (r) of landed body in meters'''
	ang = [x for x in xrange(0,360,45)]
	landings=[]
	for i in ang:
		landings.append(target_landing(Lat, Long, d, i, r))
	return landings
	
def target_landing(Lat, Long, d, ang, r):
	''' Provide current location(Lat, Long), displacement (d) of next landing, angle (ang) from current location
	landed body radius in meters (r) '''
	deltLat = float(py_theorem(d,ang)[0])/float(r)
	deltLong = float(py_theorem(d,ang)[1])/float(r) * cos(radians(Lat)) 
	lat2 = Lat + degrees(deltLat)
	long2 = Long + degrees(deltLong)
	return lat2,long2

#print target_landing(10.18,-10.12,500,78.69,200000)
position = [central_pt(10.18,-10.12, 500, 200000)]

compass_dir = [
'East',
'North-East',
'North',
'North-West',
'West',
'South-West',
'South',
'South-East']

for item in range(len(compass_dir)):
	print compass_dir[item],'ward landing:\n','Lat: ',round(position[0][item][0],4),'Long: ',round(position[0][item][1],4)