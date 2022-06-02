# Do not modify these lines
__winc_id__ = '62311a1767294e058dc13c953e8690a4'
__human_name__ = 'casting'

# Add your code after this line

# part 1
leek_price = 2
l = 'Leek is ' + str(leek_price) + ' euro per kilo.'
print(l)

# part 2
leek_order = 'leek 4'

leek_number = int(leek_order[leek_order.find('4'):])

sum_total = leek_number * leek_price
print(sum_total)

# part 3
broccoli_price = 2.34
broccoli_order = "broccoli 1.6"
broccoli_number = float(broccoli_order[broccoli_order.find('1.6'):])

sum_total_broccoli = broccoli_price * broccoli_number

b = str(broccoli_number) + 'kg broccoli costs ' + str(round(sum_total_broccoli, 2)) + 'e'
print(b)
