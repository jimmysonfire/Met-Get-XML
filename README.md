# Met-Get-XML
A small python module that uses the Met Office API and searches the Met Office Location list and returns today's and tonight's forecast.

You must provide your own API key from https://www.metoffice.gov.uk/datapoint and then paste it into the <API KEY> line.

The code gets the met office forecast location list and attempts to match location names and unitary authority names to a location input by the user. 
Upon retrieving the forecast from the Met Office the reponse is parsed and todays date selected and its subelements parsed, matched to definitions and then printed to Standard Output.
