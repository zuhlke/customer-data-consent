from flask import jsonify
from jsonschema import validate
import json


JSON_SCHEMA_FILE = r'consent_data_mods/consent_json_schema.json'
JSON_TAXONOMY_FILE = r'consent_data_mods/json_taxonomy.json'
EXISTING_CONSENT_FILE = r'consent_data_mods/existing_consent.json'

def consent_quality_checks(json_data):

    try:
        schema_validation(json_data)
    except Exception as e:
        return jsonify({'message': f'JSON Schema is Invalid {e}'}), 400

    try:
        taxonomy_validation(json_data,JSON_TAXONOMY_FILE)
    except Exception as e:
        return jsonify({'message': f'JSON taxonomy is Invalid - {e}'}), 400

    try:
        consent_compatibility_check(json_data,EXISTING_CONSENT_FILE)
    except:
        return jsonify({'message': 'Consent of new and existing data are incompatible'}), 400

    
    return jsonify({'message': 'JSON is valid'}), 200



def schema_validation(json_data):
    '''
    This function takes a JSON data as input and validates it against a pre-defined JSON schema.

    Parameters
    ----------
    json_data : dict
        A JSON object to be validated against a pre-defined schema.

    Raises
    ------
    ValueError
        If the received JSON object is not compliant with the pre-defined JSON schema.

    Returns
    -------
    None
    '''

    with open(JSON_SCHEMA_FILE,'r') as file:
        json_schema = json.load(file)

    # Validate the JSON against the schema
    validate(instance=json_data, schema=json_schema)


def find_key(dictionary, key):
    for k, v in dictionary.items():
        if k == key:
            return v
        elif isinstance(v, dict):
            result = find_key(v, key)
            if result is not None:
                return result
    return None


def is_subset(list1, list2):
    return set(list1).issubset(set(list2))

def is_superset(list1, list2):
    return set(list1).issuperset(set(list2))



def taxonomy_validation(consent_json,JSON_TAXONOMY_FILE):

    # get taxonomy file
    with open(JSON_TAXONOMY_FILE, 'r') as file:
        json_taxonomy_data = json.load(file)



        for key in json_taxonomy_data:
            taxonomy_key = key
            taxonomy_values = json_taxonomy_data[key]

            # get the same key from the consent json dict
            consent_json_values = find_key(consent_json, key)

            # verify that the consent json has values which are compliant with the taxonomy

            if is_subset(consent_json_values, taxonomy_values):
                return None
            else:
                raise ValueError('There are terms in the recieved consent data which do not comply with the taxonomy')
            

def consent_compatibility_check(consent_json, EXISTING_CONSENT_FILE):

    # get taxonomy file
    with open(JSON_TAXONOMY_FILE, 'r') as file:
        existing_consent_data = json.load(file)



        for key in existing_consent_data:
            existing_consent_key = key
            existing_consent_values = existing_consent_data[key]
            # get the same key from the consent json dict
            consent_json_values = find_key(consent_json, key)

            # verify that the consent json has values which are compliant with the taxonomy

            if is_superset(consent_json_values, existing_consent_values):
                return None
            else:
                print(key)
                print(consent_json_values)
                print(existing_consent_values)
                raise ValueError('The recieved consent is not compatible with the existing consent. Data cannot be combined without additional measures')




        
if __name__ == "__main__":
    test_json = {
    "consentGiver": "Steer, Steven",
    "retentionPeriodDays": 90,
    "dataCreationDate":"23-03-2020",
    "retentionDates": "23-03-2024",
    "consentedOrganisations": ["UKPN", "NGESO","Octopus"],
    "dataController": "Steer, Steven",
    "foreignKeyProcess": 4328934,
    "consentMethod": "Online",
    "lawfulBasis": "Consent",
    "permittedProcessing": ["Analytics",
        "Reporting",
        "Marketing",
        "Performance",
        "Regulatory",
        "Sale to 3rd Parties"
        ],
    "dataConsentStatus": "Withdrawn",
    "consentDate": "23-03-2023",
    "consentVersionRef": "2",
    "processingPermitted": ["Analytics",
        "Reporting",
        "Marketing",
        "Performance",
        "Regulatory",
        "Sale to 3rd Parties"
        ],
    "consentReviewDate":"23-03-2023",
    "dataZoneClassification": "Unclassified",
    "datasetOwner": "Steer, Steven",
    "processType": "Analytics",
    "processPurpose": "Analytics",
    "participatingOrganisations": ["Octopus",
        "EON",
        "EDF",
        "SPEN",
        "Scottish Power",
        "UKPN",
        "ENWL"],
    "dataProcessingConducted": ["type1","type2"],
    "foreignKeyConsent":1234324,
    "precedentProcesses": [],
    "dependentProcesses": [],
    "outputDataList": []


}

   
    print(consent_compatibility_check(test_json, EXISTING_CONSENT_FILE))
    print('DONE')