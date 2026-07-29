"""
Converting the average daily temperatures for several planets 
from Kelvin to Farenheit --- Version 6
"""

# Important constants
ZERO_KELVIN_IN_CELSIUS = -275.15
ZERO_CELSIUS_IN_FARENHEIT = 32
CELSIUS_TO_FARENHEIT_SCALING = 9 / 5

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
    return temp_kelvin + ZERO_KELVIN_IN_CELSIUS

def kelvin_to_farenheit(temp_kelvin):
    """
    Given a floating point temperature temp in Kelvin,
    return the corresponding temperature in Farenheit
    """
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    return temp_celsius * CELSIUS_TO_FARENHEIT_SCALING + ZERO_CELSIUS_IN_FARENHEIT


# Print out results
def print_temp_farenheit(planet, temp_farenheit):
    """
    Print out the average daily temps in Farenheit
    """
    print("The daily average temperature on", planet, "is", temp_farenheit, "Farenheit")

    
# Compute and print results
def compute_and_print_temperatures():
    """
    Compute the temeperatues for three planets in Farenheit
    """
    mercury_farenheit = kelvin_to_farenheit(MERCURY_KELVIN)
    venus_farenheit = kelvin_to_farenheit(VENUS_KELVIN)
    mars_farenheit = kelvin_to_farenheit(MARS_KELVIN)

    print_temp_farenheit("Mercury", mercury_farenheit)
    print_temp_farenheit("Venus", venus_farenheit)
    print_temp_farenheit("Mars", mars_farenheit)

compute_and_print_temperatures()

# Output
##The daily average temperature on Mercury is 328.73 Farenheit
##The daily average temperature on Venus is 863.33 Farenheit
##The daily average temperature on Mars is -85.27 Farenheit