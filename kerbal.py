from decimal import *
getcontext().prec = 4
## Data Input ##

## Data Calculation ##

def hoursToSeconds(periodHours):
	seconds=periodHours*3600
	return seconds
	
def minutesToSeconds(periodMinutes):
	seconds=periodMinutes*60
	return seconds
	
def orbitinSeconds(hours,minutes,periodSeconds):
	seconds=hours+minutes+periodSeconds
	print 'total seconds:',seconds
	
def degreesBWSats(satCount):
	degrees=Decimal(359)/Decimal(satCount)
#	degreesremainder=359%satCount
#	total=degrees+degreesremainder
	print 'degrees between sats:', degrees
	
def secondsfor1degree():
	intSeconds=TS/359
	remainderSeconds=TS%359
	total=intSeconds+remainderSeconds
	print total

def differenceInPeriodsforDesiredResult():
	
	
def period_you_need_to_achieve_goal():


## Data Translation ##


## Information Return ##


periodHours=int(raw_input("what is your desired orbit's hourly period>	"))
periodMinutes=int(raw_input("what are the minutes for that period>	"))
periodSeconds=int(raw_input("what are the seconds for that period>	"))
satCount=int(raw_input("How many Satellites would you like to insert to this orbit>	"))

hours=hoursToSeconds(periodHours)

minutes=minutesToSeconds(periodMinutes)

print orbitinSeconds(hours,minutes,periodSeconds)

print degreesBWSats(satCount)
