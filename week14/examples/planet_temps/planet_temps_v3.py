"""
Converting the average daily temperatures for several planets 
from Kelvin to Farenheit --- Version 3
"""


# Initialize temperatures for various planets
# http://www.smartconversion.com/otherInfo/Temperature_of_planets_and_the_Sun.aspx
mercury = 440
venus = 737
mars = 210

# Compute temperature in Farenheit
def compute_celsius(temp):
    """
    Given a floaring point temperature temp in Kelvin,
    return the corresponding temperature in Celsius
    """
    return temp - 275.15

def compute_farenheit(temp):
    """
    Given a floating point temperature temp in Kelvin,
    return the corresponding temperature in Farenheit
    """
    temp_celsius = compute_celsius(temp)
    return temp_celsius * 9 / 5 + 32

mercury_result = compute_farenheit(mercury)
venus_result = compute_farenheit(venus)
mars_result = compute_farenheit(mars)

# Print out results
def print_temp(planet, temp):
    """
    Print out the average daily temps
    """
    print("The daily average temperature on", planet, "is", temp, "Farenheit")
    
print_temp("Mercury", mercury_result)
print_temp("Venus", venus_result)
print_temp("Mars", mars_result)

# Output
##The daily average temperature on Mercury is 328.73 Farenheit
##The daily average temperature on Venus is 863.33 Farenheit
##The daily average temperature on Mars is -85.27 Farenheit