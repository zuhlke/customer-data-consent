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
    json_data = {
    "consentData" : {
        "consentGiver" : "Steer, Steven",
        "retentionPeriod": "90",
        "consentedOrganistions": ["NGESO","EON","EDF"],
        "dataControllerName": "Steer, Steven",
        "processKey": 12345,
        "consentMethod": "Online",
        "lawfulBasis": "Consent",
        "processingPermitted": ["Analytics",
            "Reporting",
            "Marketing",
            "Performance",
            "Regulatory"
            ],
        "consentStatus": "Updated",
        "businessKey": 2849453,
        "dateConsented": "23-03-2023",
        "consentVersionRef": 2,
        "typeProcessingPermitted": ["Marketing","Analytics"],
        "consentReviewDate": ["20-03-1923","21=03-2023"]
    },
    "businessProcessing": {
        "processType": "Matching",
        "processingPurpose": "Aggregation",
        "participatingOrganisation": ["Octopus",
            "EON",
            "EDF",
            "SPEN",
            "UKPN",
            "ENWL"],
        "dataProcessingConducted": "Matching with another dataset",
        "consentKey": 1243902,
        "retentionReviewDate": "30-03-2023",
        "precedentProcess": "data ingestion",
        "dependentProcesses": "visualisation and export",
        "outputProcessList": ["process 1","process 2"],
        "businessKey": 318943
    },
    "businessData":  {
        "dataClassification": "RED",
        "retentionReviewDate": "30-03-2023",
        "datasetOwner": "Steer, Steven",
        "consentKey":1243902,
        "processKey":12345
    }
}





    consent_compatibility_check(json_data, EXISTING_CONSENT_FILE)