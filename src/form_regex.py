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



"""


{'fieldName': 'Detailed Earnings information\n(If you check this block, tell us below\nwhy you need this information.)', 'fieldValue': '☑'}
{'fieldName': 'Yes', 'fieldValue': '☐'}
{'fieldName': 'No', 'fieldValue': '☑'}
{'fieldName': 'Date of Birth\n(Mo/Day/Yr)', 'fieldValue': '03/01/1997'}
{'fieldName': 'Date', 'fieldValue': '19/10/2023'}
{'fieldName': 'For the period(s)/year(s):', 'fieldValue': '2020-2022'}
{'fieldName': 'Name', 'fieldValue': 'Mouad Maaziz'}
{'fieldName': 'Number', 'fieldValue': '555-66-7777'}
{'fieldName': 'Address', 'fieldValue': '789 Elm St, Othertown, Province 98765.'}
{'fieldName': 'Name', 'fieldValue': 'Mustafa B FAKAK'}
{'fieldName': 'Certified Total Earnings For Each Year.\n(Check this box only if you want the information\ncertified. Otherwise, call 1-800-772-1213 to\nrequest Form SSA-7004, Request for Earnings\nand Benefit Estimate Statement)', 'fieldValue': ''}
{'fieldName': 'If yes, enter $15.00', 'fieldValue': 'B. $\n$300,500'}
{'fieldName': 'Area Code) (Telephone Number)', 'fieldValue': '555.123.4567\n('}
{'fieldName': 'City, State & Zip Code', 'fieldValue': 'Burlington, Ontario L7R 2G6'}
{'fieldName': '(Do not print)', 'fieldValue': 'your name here\n>\nmouad.maziz@gmail.com'}
{'fieldName': 'Mail Completed Form(s) To:', 'fieldValue': '6. Social Security Administration\nDivision of Earnings Record Operations\nP.O. Box 33003\nBaltimore Maryland 21290-3003'}
{'fieldName': 'Ontario', 'fieldValue': ', L7R 2G6'}
{'fieldName': 'P.O. Box', 'fieldValue': '33003'}
{'fieldName': '300 N.', 'fieldValue': 'Greene St.'}
{'fieldName': 'Mustafa B FAKAK', 'fieldValue': 'Name'}




Entity Type: id
Mention Text: 2020-2022
Confidence: 0.6736993

Entity Type: phone  / fixed / id-token
Mention Text: 1-800-772-1213
Confidence: 0.99956685

Entity Type: page_number /public / id-token
Mention Text: 3
Confidence: 0.58820766

Entity Type: price
Mention Text: $ 500,000
Confidence: 0.9680597

Entity Type: price
Mention Text: $15.00
Confidence: 0.98402756

Entity Type: price
Mention Text: $
$300,500
Confidence: 0.6153776






BETWEEN ---> Mouad Maaziz
(name
 --------------------------------------------------
(name) ---> Robert Last
 --------------------------------------------------
(Court seal) ---> (and
 --------------------------------------------------
IF YOU DO NOT PAY THE TOTAL AMOUNT OF ---> 300
$
LESS
 --------------------------------------------------
Garnishment no ---> 154847
 --------------------------------------------------
Date ---> 27/10/2023
 --------------------------------------------------
File no ---> 45
 --------------------------------------------------
Court ---> BSH
 --------------------------------------------------
Office at ---> 10:30 am
 --------------------------------------------------
Debtor ---> Robert Last
 --------------------------------------------------
Amount enclosed $ ---> 200
 --------------------------------------------------
Date of payment ---> 28/102023
 --------------------------------------------------
Garnishee ---> Yassine Walid
 --------------------------------------------------
Local registrar ---> Mohamed B Fakkak
 --------------------------------------------------
Creditor ---> Mouad Maaziz
 --------------------------------------------------
telephone no. ---> (555) 123-4567
 --------------------------------------------------
Address of court office ---> 567 Willow Lane, Apt 302, Vancouver, BC V6B 2S2
 --------------------------------------------------
Creditor's address ---> 789 Country Road 42, Red Deer County, AB T4E0P7
 --------------------------------------------------



 














































Entity Type: date_time
Mention Text: 10/20/23, 7:24 PM
Confidence: 0.9894482

Entity Type: url
Mention Text: https://www.abcsubmit.com/free-form-templates/free-dog-adoption-form-template-id_1ceoqrdg6_1tfu
Confidence: 1.0

Entity Type: page_number
Mention Text: 1/6
Confidence: 0.966953

Entity Type: date_time
Mention Text: 10/20/23, 7:24 PM
Confidence: 0.98944575

Entity Type: url
Mention Text: https://www.abcsubmit.com/free-form-templates/free-dog-adoption-form-template-id_1ceoqrdg6_1tfu
Confidence: 1.0

Entity Type: page_number
Mention Text: 2/6
Confidence: 0.97476566

Entity Type: date_time
Mention Text: 10/20/23, 7:24 PM
Confidence: 0.9897822

Entity Type: organization
Mention Text: Mouad
Confidence: 0.2262319

Entity Type: address
Mention Text: 101 Redwood Ave, Seattle, WA, 98101
Confidence: 0.9946188

Entity Type: address
Mention Text: 789 Maplewood Rd, Calgary, AB, T2P 3H4
Confidence: 0.82987577

Entity Type: organization
Mention Text: Seattle
Confidence: 0.8672856

Entity Type: phone
Mention Text: 0608-811030
Confidence: 0.89902914

Entity Type: phone
Mention Text: (201) 254-7854
Confidence: 0.99577653

Entity Type: email
Mention Text: mouad.maaziz@gmail.com
Confidence: 0.8807771

Entity Type: url
Mention Text: https://www.abcsubmit.com/free-form-templates/free-dog-adoption-form-template-id_1ceoqrdg6_1tfu
Confidence: 1.0

Entity Type: page_number
Mention Text: 3/6
Confidence: 0.97354597

Entity Type: date_time
Mention Text: 10/20/23, 7:24 PM
Confidence: 0.9893838

Entity Type: person
Mention Text: Rachid
Confidence: 0.7669241

Entity Type: person
Mention Text: Bassidi
Confidence: 0.11165256

Entity Type: quantity
Mention Text: 12 months
Confidence: 0.94807404

Entity Type: url
Mention Text: https://www.abcsubmit.com/free-form-templates/free-dog-adoption-form-template-id_1ceoqrdg6_1tfu
Confidence: 1.0

Entity Type: page_number
Mention Text: 4/6
Confidence: 0.9672056

Entity Type: date_time
Mention Text: 10/20/23, 7:24 PM
Confidence: 0.9887284

Entity Type: organization
Mention Text: Maaziz
Confidence: 0.2606593

Entity Type: quantity
Mention Text: 10 years
Confidence: 0.96588695

Entity Type: quantity
Mention Text: 10 years
Confidence: 0.9671062

Entity Type: url
Mention Text: https://www.abcsubmit.com/free-form-templates/free-dog-adoption-form-template-id_1ceoqrdg6_1tfu
Confidence: 1.0

Entity Type: page_number
Mention Text: 5/6
Confidence: 0.97007895

Entity Type: date_time
Mention Text: 10/20/23, 7:24 PM
Confidence: 0.9881022

Entity Type: organization
Mention Text: Google
Confidence: 0.60175204

Entity Type: url
Mention Text: Abcsubmit.com
Confidence: 1.0

Entity Type: organization
Mention Text: SC ABCSUBMIT SRL
Confidence: 0.38188207

Entity Type: address
Mention Text: Săcălaz, Main Street 464D, Timiş, Romania, ZipCode 307370
Confidence: 0.90061456

Entity Type: url
Mention Text: https://www.abcsubmit.com/free-form-templates/free-dog-adoption-form-template-id_1ceoqrdg6_1tfu
Confidence: 1.0

Entity Type: page_number
Mention Text: 6/6
Confidence: 0.9683196


























"""

