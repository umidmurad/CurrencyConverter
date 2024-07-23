"""
User interface for module currency

When run as a script, this module prompts the user for two currencies and amount.
It prints out the result of converting the first currency to the second.

Author: Umid Muradli
Date:   7/7/2024
"""

import currency

src = input('3-letter code for original currency: ')
dst = input('3-letter code for the new currency: ')
amt = input('Amount of the original currency: ')

amtFloat = float(amt)

result = currency.exchange(src,dst,amtFloat)
# Round up the result 
roundedResult = round(result, 3)
# Convert the numerical values to strings
resultStr = str(roundedResult)

print('You can exchange ' + amt +' ' + src + ' for ' + resultStr +' '+ dst + '.')
