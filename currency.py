"""
Module for currency exchange

This module provides several string parsing functions to implement a simple
currency exchange routine using an online currency service. The primary function
in this module is exchange().

Author: Umid Muradli
Date:   7/7/2024
"""

import introcs
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

APIKEY = os.getenv('APIKEY')
if not APIKEY:
    raise ValueError("No API key found. Please set the APIKEY environment variable.")

def before_space(s):
    """
    Returns the substring of s up to, but not including, the first space.

    Example: before_space('Hello World') returns 'Hello'

    Parameter s: the string to slice
    Precondition: s is a string with at least one space in it
    """

    result = ""
    position = introcs.find_str(s, " ")
    assert position != -1
    result = s[:position]

    return result


def after_space(s):
    """
    Returns the substring of s after the first space

    Example: after_space('Hello World') returns 'World'

    Parameter s: the string to slice
    Precondition: s is a string with at least one space in it
    """

    result = ""
    position = introcs.find_str(s, " ")
    assert position != -1
    result = s[position+1 :]

    return result


def first_inside_quotes(s):
    """
    Returns the first substring of s between two (double) quote characters

    Note that the double quotes must be part of the string.  So "Hello World" is a 
    precondition violation, since there are no double quotes inside the string.

    Example: first_inside_quotes('A "B C" D') returns 'B C'
    Example: first_inside_quotes('A "B C" D "E F" G') returns 'B C', because it only 
    picks the first such substring.

    Parameter s: a string to search
    Precondition: s is a string with at least two (double) quote characters inside
    """

    result = ""
    #Find the first quote mark
    firstPos = introcs.find_str(s, '"')

    #Ensure quote mark actually exists
    assert firstPos != -1
    #Find the second quote mark
    secondPos = introcs.find_str(s, '"', start = firstPos+1)

    #Ensure second quote mark actually exists
    assert secondPos != -1

    result = s[firstPos+1 : secondPos]
    return result


def get_src(json):
    """
    Returns the src value in the response to a currency query.

    Given a JSON string provided by the web service, this function returns the string
    inside string quotes (") immediately following the substring '"src"'. For example,
    if the json is
        
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'

    then this function returns '2 United States Dollars' (not '"2 United States Dollars"'). 
    On the other hand if the json is 
        
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'

    then this function returns the empty string.

    The web server does NOT specify the number of spaces after the colons. The JSON
        
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
        
    is also valid (in addition to the examples above).

    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
    """
    
    result = ""
    
    #Look for 'src'
    srcPOS = introcs.find_str(json, '"src"')
    #Make a copy of Json , add 5 because of length of src
    copyJson = json[srcPOS+5:]
    result = first_inside_quotes(copyJson)
    return result


def get_dst(json):
    """
    Returns the dst value in the response to a currency query.

    Given a JSON string provided by the web service, this function returns the string
    inside string quotes (") immediately following the substring '"dst"'. For example,
    if the json is
        
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'

    then this function returns '1.772814 Euros' (not '"1.772814 Euros"'). On the other
    hand if the json is 
        
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'

    then this function returns the empty string.

    The web server does NOT specify the number of spaces after the colons. The JSON
        
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
        
    is also valid (in addition to the examples above).

    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
    """

    result = ""
    
    #Look for 'dst'
    srcPOS = introcs.find_str(json, '"dst"')
    #Make a copy of Json , add 5 because of length of dst
    copyJson = json[srcPOS+5:]
    result = first_inside_quotes(copyJson)
    return result


def has_error(json):
    """
    Returns True if the response to a currency query encountered an error.

    Given a JSON string provided by the web service, this function returns True if the
    query failed and there is an error message. For example, if the json is
        
        '{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}'

    then this function returns True (It does NOT return the error message 
    'Source currency code is invalid'). On the other hand if the json is 
        
        '{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}'

    then this function returns False.

    The web server does NOT specify the number of spaces after the colons. The JSON
        
        '{"success":true, "src":"2 United States Dollars", "dst":"1.772814 Euros", "error":""}'
        
    is also valid (in addition to the examples above).

    Parameter json: a json string to parse
    Precondition: json a string provided by the web service (ONLY enforce the type)
    """


    length = len('"success"')
    successPOS = introcs.find_str(json, '"success"')
   
    copyJson = json[successPOS+length:]
    # print(copyJson)
    semicolonPOS = introcs.find_str(copyJson, ':')
    commaPOS = introcs.find_str(copyJson, ',', start = semicolonPOS)
    #Contains spaces and true or false
    finalizedValue = copyJson[semicolonPOS +1: commaPOS]
    finalizedValue = introcs.strip(finalizedValue)
    return finalizedValue != 'true'


def service_response(src, dst, amt):
    """
    Returns a JSON string that is a response to a currency query.

    A currency query converts amt money in currency src to the currency dst. The response 
    should be a string of the form

        '{"success": true, "src": "<src-amount>", "dst": "<dst-amount>", "error": ""}'

    where the values src-amount and dst-amount contain the value and name for the src 
    and dst currencies, respectively. If the query is invalid, both src-amount and 
    dst-amount will be empty, and the error message will not be empty.

    There may or may not be spaces after the colon.  To test this function, you should
    choose specific examples from your web browser.

    Parameter src: the currency on hand
    Precondition: src is a nonempty string with only letters

    Parameter dst: the currency to convert to
    Precondition: dst is a nonempty string with only letters

    Parameter amt: amount of currency to convert
    Precondition: amt is a float or int
    """
    #Enforce the Type
    assert type(src) == str
    assert type(dst) == str
    assert type(amt) == float or type(amt) == int
    # Enforce no numbers
    assert introcs.isnumeric(src) == False
    assert introcs.isnumeric(dst) == False
    # Enforce no spaces in text
    assert introcs.find_str(src, ' ') == -1
    assert introcs.find_str(dst, ' ') == -1
    # Enforce length at least 1 characters
    assert len(src) > 0
    assert len(dst) > 0

    response = ''
    amt = str(amt) # Convert to String
    #Put together the URL
    url = 'https://ecpyfac.ecornell.com/python/currency/fixed?src=' + src +\
             '&dst=' + dst + '&amt=' + amt + '&key=' + APIKEY
    #CALLAPI and receive response
    response = introcs.urlread(url)
    return response


def iscurrency(currency):
    """
    Returns True if currency is a valid (3 letter code for a) currency.

    It returns False otherwise.

    Parameter currency: the currency code to verify
    Precondition: currency is a nonempty string with only letters
    """
    # Enforce that it is a text
    assert type(currency) == str
    # Enforce that there is no empty spaces
    assert introcs.find_str(currency, ' ') == -1
    # Enforce that it is not empty 
    assert len(currency) > 0
    # Enforce no numbers in the string
    assert introcs.isnumeric(currency) == False

    testDST = 'EUR'
    testAmount = 2
    response = service_response(currency,testDST,testAmount)
    
    return not has_error(response)


def exchange(src, dst, amt):
    """
    Returns the amount of currency received in the given exchange.

    In this exchange, the user is changing amt money in currency src to the currency 
    dst. The value returned represents the amount in currency currency_to.

    The value returned has type float.

    Parameter src: the currency on hand
    Precondition: src is a string for a valid currency code

    Parameter dst: the currency to convert to
    Precondition: dst is a string for a valid currency code

    Parameter amt: amount of currency to convert
    Precondition: amt is a float or int
    """

    #Enforcing Assertions
    assert iscurrency(src) == True
    assert iscurrency(dst) == True
    assert type(amt) == float or type(amt) == int

    response = ''
    # Get the response from API call
    response = service_response(src, dst, amt)
    # print("Returned Response: ", response)
    dst = get_dst(response)
    # print("Extracted DST: ", dst)
    stringAmount = before_space(dst)
    # print("After Space Function: ", stringAmount)
    floatAmount = float(stringAmount)

    return floatAmount