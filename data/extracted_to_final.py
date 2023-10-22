from fillpdf import fillpdfs
import pandas as pd
import json

json_file = "extracted_data.json"
empty_pdf = "CPL160.59SealingApplication.pdf"
output_pdf = "FilledApplication.pdf"
fields = fillpdfs.get_form_fields(empty_pdf, sort=False)

# returns a dictionary of fields
# Set the returned dictionary values a save to a variable
# For radio boxes ('Off' = not filled, 'Yes' = filled)

pdf_map_extract = {
    "Filing Court Name": "Court",
    'Filing Court County': '',
    'Applicant Name': "Defendant",
    'AKAs': '', 
    'NYSID': '',
    'Date of Birth': 'Defendant DOB',
    'Case Number 1': "Docket/Case Number",
    'Court Name 1': "Court", 
    'Case Number 2': None, 
    'Court Name 2': None, 
    'Street Address': None, 
    'City State Zip': None, 
    'Phone': None, 
    'Email': None, 
    '59 sealing': None, 
    'Case Number 3': '', 
    'Court Name 3': '', 
    'Document 3': '', 
    'Document 4': '', 
    'Document 5': '', 
    'Document 6': '', 
    'Document 7': '', 
    'Document 8': '', 
    'Document 9': '', 
    'Document 10': '', 
    'Reasons for sealing': '',
    'Notary day - Application': ' ', 
    'Notary month - Application': ' ', 
    'Notary year - Application': ' ', 
    'Server Name': '', 
    'Server Address': '', 
    'Service Date': '', 
    'Prosecutor County': ' ', 
    'Prosecutor Address': '', 
    'Type of Service': None, 
    'Notary day - Affidavit of service': ' ', 
    'Notary month - Affidavit of service': ' ', 
    'Notary year - Affidavit of service': ' '
}

data_dict = {
'Date of Birth': 'RANDOM SHIT ',
'Phone': 'TESTEST',
'Court Name 3': 'BANNAA',
}

def map_single_row(key, value):
    pdf_key = pdf_map_extract[key]

    return {pdf_key, value}

def main():
    file = open(json_file)
    data = json.load(file)
    print(data)

    # here you would manage the logic for mapping all the rows from the dictionary
    data_dict = map_single_row('Applicant Name', "john doe") # this is a test

    # save the data dict
    fillpdfs.write_fillable_pdf(empty_pdf, output_pdf, data_dict)

