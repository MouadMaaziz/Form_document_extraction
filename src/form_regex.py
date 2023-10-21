import re

# to add:  ZIP code


"""failing patterns: 

no \n or \t between fname and lname
all patterns ends with \n



""" 




patterns = {
    "full_name": r'^[A-Za-z]{2,25}( [A-Z]+[a-z]*)?( [A-Z]+[a-z]*)$',
    "sex": re.compile(r'\b(F|M|male|female|woman|man|girl|boy|transgender|(non-)?binary|genderqueer|cisgender|genderfluid)\b', re.IGNORECASE),
    "dates": r'(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}',
    "date_of_birth": r'(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}',
    "phone": r'((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))',
    "email": r'([a-zA-Z0-9!#$%&\'*+\/=?^_`{|.}~-]+@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)',
    "street_address": re.compile('\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE),
    "address": r'(\d{1,4}[ ,]?\w{1,10}[ ,].*[ ,]\w{1,10}[ ,]\d{5})',
    "ssn": r'(?!000|666|333)0*(?:[0-6][0-9][0-9]|[0-7][0-6][0-9]|[0-7][0-7][0-2])[- ](?!00)[0-9]{2}[- ](?!0000)[0-9]{4}',
    "driver_license": r'(Driver|License|Number|DL)\s[:\s]?([A-Z]{1,2}\d{1,8}[A-Z]?)',
    "marital_status": re.compile(r'\b(single|married|divorced|widowed|separated|engaged|in a relationship)\b', re.IGNORECASE),
    "price": r'(?:USD|US\$|CAD|C\$|€|EUR|[$€])(?:\s?[+-]?[0-9]{1,3}(?:(?:,?[0-9]{3}))*(?:\.[0-9]{1,2})?)?'
}















# results = {'full_name': ['Mouad Maaziz', 'Mustafa B FAKAK',  'Daytime Phone Number'],
#             'date_of_birth': ['12/01/1975', '31/12/1999'], 
#             'dates': ['12/01/1975', '31/12/1999', '03/01/1997', '19/10/2023'], 
#             'phone': ['21290-3003', '555.123.4567', '21290-3003'], 
#             'address': ['132, Hay Mohammadi,Taroudant 30000', '12, Hay Mohammadi,Taroudant 30000', '789 Elm St, Othertown, Province 98765.'],
#             'street_address': ['789 Elm St, Othertown, Province 98765.'],
#             'ssn': ['555-66-7777'],
#             'price': ['$15.00', '$15.00', '$15.01', '$100', '$ 16.50', '$5,000', '$15.01', '$100', '$ 16.50', '$5,000', '$15.01',
#                        '$100', '$ 16.50', '$5,000', '$15.01', '$100', '$ 16.50', '$5,000', '$15.00', '$15.00', '$15.00', '$15.01',
#                         '$100', '$ 16.50', '$5,000'
#                     ]
#             }














patterns2 = {

    "full_name_a": r'([A-Z]+[a-z]*){1,3}(?!\W+)',

    "full_name_b": r'(?:Name|name)+(?:.*)?(?:[:\s])+([A-Z]+[A-Za-z]*[ ][A-Z]+[A-Za-z]*[ ][A-Z]+[A-Za-z]*)(?=$|\n)',
    
    "last_name": r'(?:Last\s*Name|Surname|Family\s*Name)[:\s]?([A-Za-z\s-]+)(?=$|\n)',
    "first_name": r'(?:First\s*Name|Given\s*Name|Forename)[:\s]?([A-Za-z\s-]+)(?=$|\n)',
    "date_MMDDYYYY": r'^([1][12]|[0]?[1-9])[\/-]([3][01]|[12]\d|[0]?[1-9])[\/-](\d{4}|\d{2})(?=$|\n)',
    "date_of_birth": r'(?:birth|DOB)+\n+(\d{2}/\d{2}/\d{4})(?=$|\n)',
    "phone": r'(?:[:\s])+(\d{3}[-. ]\d{3}[-. ]\d{4})(?=$|\n)',
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b(?=$|\n)',
    "address": r'(?:Address|address)+(?:\s)?(?:.*[:\s\n]+){1,4}(?:\s)?(\d{1,4}[ ,]?\w{1,10}[ ,].*[ ,]\w{1,10}[ ,]\d{5})(?=$|\n)',
    "social_security_number": r'(?:Social|security|number|SSN)?(?:[:\s])+(\d{3}[-\s]?\d{2}[-\s]?\d{4})(?=$|\n)',
    "driver_license": r'(Driver|License|Number|DL)\s[:\s]?([A-Z]{1,2}\d{1,8}[A-Z]?)(?=$|\n)',
    "marital_status": r'(?:Marital\s+Status|Status)[:\s]?(\w+)(?=$|\n)',
}


