"""
Converting the average daily temperatures for several planets 
from Kelvin to Farenheit --- Version 4
"""


# Initialize temperatures for various planets
# http://www.smartconversion.com/otherInfo/Temperature_of_planets_and_the_Sun.aspx
MERCURY_KELVIN = 440
VENUS_KELVIN = 737
MARS_KELVIN = 210

# Compute temperature in Farenheit
def kelvin_to_celsius(temp_kelvin):
    """
    Given a floaring point temperature temp in Kelvin,
    return the corresponding temperature in Celsius
    """
    return temp_kelvin - 275.15

def kelvin_to_farenheit(temp_kelvin):
    """
    Given a floating point temperature temp in Kelvin,
    return the corresponding temperature in Farenheit
    """
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    return temp_celsius * 9 / 5 + 32

mercury_farenheit = kelvin_to_farenheit(MERCURY_KELVIN)
venus_farenheit = kelvin_to_farenheit(VENUS_KELVIN)
mars_farenheit = kelvin_to_farenheit(MARS_KELVIN)

# Print out results
def print_temp_farenheit(planet, temp_farenheit):
    """
    Print out the average daily temps in Farenheit
    """
    print("The daily average temperature on", planet, "is", temp_farenheit, "Farenheit")
    
print_temp_farenheit("Mercury", mercury_farenheit)
print_temp_farenheit("Venus", venus_farenheit)
print_temp_farenheit("Mars", mars_farenheit)

# Output
##The daily average temperature on Mercury is 328.73 Farenheit
##The daily average temperature on Venus is 863.33 Farenheit
##The daily average temperature on Mars is -85.27 Farenheit