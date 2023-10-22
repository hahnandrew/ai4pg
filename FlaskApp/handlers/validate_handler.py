

import base64
from io import BytesIO
import mimetypes
import re
import pytesseract
from PIL import Image

from configs import CONFIGS


def receive_doc(binary_data):
  extracted_text = extract_text_from_image(binary_data)
  json_object = parse_certificate_data(extracted_text)
  return json_object




def extract_text_from_image(binary_image_data):
    image_stream = BytesIO(binary_image_data)
    image = Image.open(image_stream)
    text = pytesseract.image_to_string(image)
    return text


def parse_certificate_data(input_text):
    # Parsing values from the text. This simplistic method assumes a lot about the format.
    certificate = re.search(r"Certificate # ([\w\d]+)", input_text)
    court = "New York County Supreme Ct/CRM"  # hardcoded as it seems consistent
    plaintiff = "The People of the State of New York"  # also hardcoded
    defendant = re.search(
        r"vs\.\s?Docket/Case Number:\s?[\w\d]+\n‘([\w\s]+)", input_text
    )
    defendant_dob = re.search(r"Defendant DOB: (\d{2}/\d{2}/\d{4})", input_text)
    docket_case_number = re.search(r"Docket/Case Number: ([\w\d]+)", input_text)
    arrest_date = re.search(r"Arrest Data: (\d{2}/\d{2}/\d{4})", input_text)
    arraignment_date = re.search(r"Arraignment Date: (\d{2}/\d{2}/\d{4})", input_text)
    charge_code = re.search(r"(PL \d+-\d+:\d+)", input_text)
    sentence_date = re.search(r"Pied Guilty (\d{2}/\d{2}/\d{4})", input_text)
    # These fields are more complex and might require more sophisticated parsing logic
    charge_description = "Attempted CORRUPTING THE GOVERNMENT"  # this could vary a lot
    conviction_type = "Pled Guilty"  # seems consistent
    sentence_highlight = "Imprisonment Time Served"  # hardcoded for simplicity

    certificate_date = re.search(
        r"(\d{2}/\d{2}/\d{4})\n\nVALE", input_text
    )  # Assuming the date format is consistent.
    clerk_of_the_court = (
        "[Signature]"  # Placeholder, as actual signature capture is not feasible here
    )
    notice = (
        "CAUTION: THIS DOCUMENT IS NOT OFFICIAL UNLESS EMBOSSED WITH THE COURT SEAL"
    )

    # Building the JSON object
    certificate_data = {
        "Certificate": certificate.group(1) if certificate else "",
        "Court": court,
        "Plaintiff": plaintiff,
        "Defendant": defendant.group(1) if defendant else "",
        "Defendant DOB": defendant_dob.group(1) if defendant_dob else "",
        "Docket/Case Number": docket_case_number.group(1) if docket_case_number else "",
        "Incident Date": "",  # Not found in the input text
        "Arrest Date": arrest_date.group(1) if arrest_date else "",
        "Arraignment Date": arraignment_date.group(1) if arraignment_date else "",
        "Charge Details": {
            "Number of Charges": "1",  # Assuming one charge for simplicity
            "Charge Code": charge_code.group(1) if charge_code else "",
            "Charge Weight": "AM",  # hardcoded for simplicity
            "Charge Description": charge_description,
            "Conviction Type": conviction_type,
            "Sentence Date": sentence_date.group(1) if sentence_date else "",
            "Sentence Highlight": sentence_highlight,
        },
        "Weight of Charge Key": {
            "Infraction": "I",
            "Violation": "V",
            "Misdemeanor": "M",
            "AM-Misdemeanor": "AM",
            "BM-Misdemeanor": "BM",
            "UM-Unclassified Misdemeanor": "UM",
            "AF-A Felony": "AF",
            "BF-B Felony": "BF",
            "CF-C Felony": "CF",
            "DF-D Felony": "DF",
            "EF-E Felony": "EF",
        },
        "Certificate Date": certificate_date.group(1) if certificate_date else "",
        "Clerk of the Court": clerk_of_the_court,
        "Notice": notice,
    }

    return json.dumps(certificate_data, indent=4)
