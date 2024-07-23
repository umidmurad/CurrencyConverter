"""
Unit tests for module currency

When run as a script, this module invokes several procedures that test
the various functions in the module currency.

Author: Umid Muradli
Date:   7/7/2024
"""

import introcs
import currency


def test_before_space():
    """Test procedure for before_space"""
    print("Testing before_space")
    # Test case 1: A string with 1 space in the middle
    result = currency.before_space("Text ishere")
    introcs.assert_equals("Text",result)

    # Test case 2: A string with multiple spaces
    result = currency.before_space("Multiple spaces here")
    introcs.assert_equals("Multiple", result)

    # Test case 3: A string with Two spaces in the middle
    result = currency.before_space("Two  space")
    introcs.assert_equals("Two", result)

    # Test case 4: A string with just space
    result = currency.before_space(" ")
    introcs.assert_equals("", result)


def test_after_space():
    """Test procedure for after_space"""
    print("Testing after_space")

    # Test case 1: A string with 1 space in the middle
    result = currency.after_space("Text ishere")
    introcs.assert_equals("ishere",result)

    # Test case 2: A string with multiple spaces
    result = currency.after_space("Multiple spaces here")
    introcs.assert_equals("spaces here", result)

    # Test case 3: A string with Two spaces in the middle
    result = currency.after_space("Two  space")
    introcs.assert_equals(" space", result)

    # Test case 4: A string with just space
    result = currency.after_space(" ")
    introcs.assert_equals("", result)


def test_first_inside_quotes():
    """Test procedure for first_inside_quotes"""
    print("Testing first_inside_quotes")

    # Test case 1: A string with a single pair of quotes with text inside
    result = currency.first_inside_quotes('A "B C" D')
    introcs.assert_equals("B C", result)

    # Test case 2: A string with multiple pairs of quotes
    result = currency.first_inside_quotes('A "B C" D "E F" G')
    introcs.assert_equals("B C", result)

    # Test case 3: A string with adjacent quotes (no space between quotes)
    result = currency.first_inside_quotes('A """C" D')
    introcs.assert_equals("", result)

    # Test case 4: A string with nothing inside the double quotes
    result = currency.first_inside_quotes('"\'"')
    introcs.assert_equals("'", result)


def test_get_src():
    """Test procedure for get_src"""
    print("Testing get_src")
    # Test case 1: a test with a nonempty value for "src" and no spaces after the colon
    result = currency.get_src('{"success": true, "src": "2 United States Dollars", \
                                "dst": "1.772814 Euros", "error": ""}')
    introcs.assert_equals("2 United States Dollars", result)
    
    # Test Case 2:  a test with a nonempty value for "src" and spaces after the colon
    result = currency.get_src('{"success": true, "src" : " ", "dst": \
                                "1.772814 Euros", "error": ""}')
    introcs.assert_equals(" ", result)
    # Test Case 3:  a test with an empty value for "src" and no spaces after the colon
    result = currency.get_src('{"success":false,"src":"","dst":"","error":\
                                "Source currency code is invalid."}')
    introcs.assert_equals("", result)  
    # Test Case 4:  a test with an empty value for "src" and spaces after the colon
    result = currency.get_src('{"success":false,"src": "","dst":"","error":\
                                "Source currency code is invalid."}')
    introcs.assert_equals("", result)  
    

def test_get_dst():
    """Test procedure for get_dst"""
    print("Testing get_dst")
    # Test case 1:  a test with a nonempty value for "dst" and no spaces after the colon
    result = currency.get_dst('{"success": true, "src": "2 United States Dollars", \
                                "dst":"1.772814 Euros", "error": ""}')
    introcs.assert_equals("1.772814 Euros", result)

    # Test Case 2:  * a test with a nonempty value for "dst" and spaces after the colon
    result = currency.get_dst('{"success": true, "src" : "something", "dst": \
                                "1.772814 Euros", "error": ""}')
    introcs.assert_equals("1.772814 Euros", result)

    # Test Case 3:  a test with an empty value for "dst" and no spaces after the colon
    result = currency.get_dst('{"success":false,"src":"","dst":"","error":"Source \
                                currency code is invalid."}')
    introcs.assert_equals("", result)  

    # Test Case 4:  a test with an empty value for "dst" and spaces after the colon
    result = currency.get_dst('{"success":false,"src":"","dst": "","error":\
                                "Source currency code is invalid."}')
    introcs.assert_equals("", result)  


def test_has_error():
    """Test procedure for has_error"""
    print("Testing has_error")
    result = currency.has_error('{"success":false,"src":"","dst":"",\
                                "error":"Source currency code is invalid."}')
    introcs.assert_equals(True, result)  

    result = currency.has_error('{"success": false        ,"src":"","dst":"",\
                                "error":  "Source currency code is invalid."}')
    introcs.assert_equals(True, result)  

    result = currency.has_error('{"success":true, "src":"2 United States Dollars", \
                                "dst":"1.772814 Euros", "error":""}')
    introcs.assert_equals(False, result)  
    result = currency.has_error('{"success": true, "src":"2 United States Dollars", \
                                "dst":"1.772814 Euros", "error": ""}')
    introcs.assert_equals(False, result)  


def test_service_response():
    """Test procedure for service_response"""
    print("Testing service_response")
    #Test 2 : a test with an invalid src currency
    result = currency.service_response('ASD', 'EUR', 2.5)
    expectedResult = ('{"success": false, "src": "", "dst": "", '+
                    '"error": "The rate for currency ASD is not present."}')
    introcs.assert_equals(expectedResult, result)

    # Test 1: a test with valid currencies and non-negative amount
    result = currency.service_response('USD','EUR',2.5)
    expectedResult= ('{"success": true, "src": "2.5 United States Dollars", '+
                    '"dst": "2.2160175 Euros", "error": ""}')
    introcs.assert_equals(expectedResult, result)  
    
    # Test 3: a test with an invalid src currency
    result = currency.service_response('USD', 'TST', 2.5)
    expectedResult =('{"success": false, "src": "", "dst": "", '+
                    '"error": "The rate for currency TST is not present."}')
    introcs.assert_equals(expectedResult, result)

    # Test 4:
    result = currency.service_response('USD', 'EUR', -2.5)
    expectedResult = ('{"success": true, "src": "-2.5 United States Dollars", '+
                    '"dst": "-2.2160175 Euros", "error": ""}')
    introcs.assert_equals(expectedResult, result)


def test_iscurrency():
    """Test procedure for iscurrency"""
    print("Testing iscurrency")

    result = currency.iscurrency("USD")
    introcs.assert_equals(True, result)

    result = currency.iscurrency("SFD")
    introcs.assert_equals(False, result)


def test_exchange():
    """Test procedure for exchange"""
    print("Testing exchange")

    result = currency.exchange('USD','EUR', 2.5)
    introcs.assert_floats_equal(2.2160175, result)

    result = currency.exchange('USD','EUR', -2.5)
    introcs.assert_floats_equal(-2.2160175, result)


#Running the Tests
test_before_space()
test_after_space()
test_first_inside_quotes()
test_get_src()
test_get_dst()
test_has_error()
test_service_response()
test_iscurrency()
test_exchange()

print("All tests completed successfully.")