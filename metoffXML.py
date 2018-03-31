##############################################################################
# James Lloyd-Addecott 29/03/2018
#
# Requests library used in accordance with Apache 2 license.
# Requests is available at http://http://docs.python-requests.org/en/master/
# Apache 2 license can be viewed at https://opensource.org/licenses/Apache-2.0
#
###############################################################################
# Setup some constants
import xml.etree.ElementTree as et
import urllib.request as u
import datetime
#
# You will need to supply your own API key from the Met office
# It's easy to register for a key at https://www.metoffice.gov.uk/datapoint
#
apiKey = '<API KEY>'
locationsUrl = 'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/sitelist?res=daily&'
allLocations = locationsUrl + apiKey
fcUrl = 'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/'

# Get the XML locations list
xmlLocationTree = et.ElementTree(file = u.urlopen(allLocations))
xmlLocationRoot = xmlLocationTree.getroot()

# Ask for location and return similar

askForLocation = input('Please enter a location: ').capitalize()

for location in xmlLocationRoot.findall('Location'):
    locId = location.get('id')
    locname = location.get('name')
    locuAA = location.get('unitaryAuthArea')

    if locname == askForLocation or locuAA == askForLocation:
        print(locId, locname)

# Ask for location choice and get forecast.

chosenLocation = input('Please enter your chosen location id: ')
forecastUrl = fcUrl + chosenLocation + "?res=daily&" + apiKey
print("Getting forecast now.....")
xmlForecast = et.ElementTree(file = u.urlopen(forecastUrl))
print("Forecast retrieved")
xmlForecastRoot = xmlForecast.getroot()

fcPeriod = xmlForecastRoot[1][0][1].items()
fcToday = xmlForecastRoot[1][0][1][0].items()
fcTonight = xmlForecastRoot[1][0][1][1].items()
fcParams = {'FDm':('C','Feels Like Day Max Temp.'),'FNm':('C','Feels Like Night Min Temp'),
            'Dm':('C','Day Max Temp'), 'Nm':('C','Night Min Temp'),'Gn':('mph','Wind Gust Day'),
            'Gm':('mph','Wind Gust night'),'Hn':('%','Humidity Noon'),'Hm':('%','Humidity Midnight'),
            'V':('','Visibility'),'D':('','Wind Direction'),'S':('mph','Wind Speed'), 'U':('','Max UV Index'), 'W':('Weather Type'),
            'PPd':('%','Precipitation Probably Day'),'PPn':('%','Precipitation Probability Night')}

# Manually create the WX elements from the forecast as the xml seems to contain a list and another list or
# possibly a tuple nested within a list for each element.
# Test that this returns the forecast dates and the forecasts for day and night.

fcPeriodDict = dict(fcPeriod)
fcPeriodDict['value'] = datetime.date.today()
fcTodayDict = dict(fcToday)
fcTonightDict = dict(fcTonight)

# Display the Forecast.
print("Todays (" + str(fcPeriodDict['value']) +") daytime forecast: \n" )
for k in fcTodayDict.keys():
    fcVal = fcTodayDict.get(k)
    paramUnits = fcParams.get(k)[0]
    paramText = fcParams.get(k)[1]
    print(paramText,fcVal,paramUnits)
print("\n""Tonights (" + str(fcPeriodDict['value']) +") forecast: \n" )
for k in fcTonightDict.keys():
    fcVal = fcTonightDict.get(k)
    paramUnits = fcParams.get(k)[0]
    paramText = fcParams.get(k)[1]
    print(paramText,fcVal,paramUnits)

