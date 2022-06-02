# Do not modify these lines
__winc_id__ = 'd0d3cdcefbb54bc980f443c04ab3a9eb'
__human_name__ = 'operators'

# Add your code after this line

# The language spoken the most in Switzerland is the same as in Spain.
spain_mostspoken_language = "Catalan"
switzerland_mostspoken_language = "German"
print(switzerland_mostspoken_language == spain_mostspoken_language)

# The most prevalent religion in Switzerland is the same as in Spain.
spain_prevalent_religion = "Roman Catholic"
switzerland_prevalent_religion = "Roman Catholic"
print(switzerland_prevalent_religion == spain_prevalent_religion)

# The name length of Spain's capital does not equal that of Switzerland.
spain_capital = "Madrid"
switzerland_capital = "Bern"
print(len(spain_capital) != len(switzerland_capital))

# Switzerland's GDP is greater than Spain's GDP.
spain_gdp = 1.95
switzerland_gdp = 1.11
print(switzerland_gdp > spain_gdp)

# The population growth is less than 1% in Switzerland and Spain.
spain_population_growth = 0.13
switzerland_population_growth = 0.65
print(spain_population_growth and switzerland_population_growth < 1)

# At least one of the two countries has a population count of over 10 million.
spain_population = 47163418
switzerland_population = 8508698
print(spain_population > 10000000 or switzerland_population > 10000000)

# Exactly one of the two countries has a population count of over 10 million.
print(spain_population > 10000000 and switzerland_population < 10000000 or spain_population < 10000000 and switzerland_population > 10000000 )