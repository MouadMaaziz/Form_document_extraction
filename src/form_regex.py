import re



patterns = {
    "full_name": r'^[A-Za-z]{2,25}( [A-Z]+[a-z]*)?( [A-Z]+[a-z]*)?$',
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


# Define fields and their variations to look for in the text
fields = {
        'full_name': ['Name', 'name', 'First', 'Last'],
        'sex': ['sex', 'Sex', 'gender', 'Gender'],
        'date_of_birth': ['Birth','birth', 'DOB'],
        'dates': ['Date','date', 'day'],
        'phone': ['Phone', 'Telephone', 'Contact', 'Cell'],
        'email': ['Email','Electronic mail', 'e-mail','email', 'E-mail'],
        'address': ['Address', 'address','residence', 'street address', ' mail'],
        'street_address': ['Address', 'address','residence', 'street address', ' mail'],
        'ssn': ['Social','security', 'number', 'SSN', 'ssn'],
        'driver_license': [ 'Driver','License', 'DL', 'driver' ],
        'marital_status': ['Marital status','Status'],
        'price': ['price','Price', 'total','Total', '$', 'USD', 'US Dollar', 'Amount','amount', 'AMOUNT']
     }


# These are fields that have a strong matching pattern (they don't have to be close to the field name)
strong_fields = ['phone','ssn','email','address',
                 'date_of_birth', 'dates','street_address',
                'price'
                ]






















