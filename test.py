
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('aws-inventory-contacts')

with open("aws-inventory-contacts.json") as json_file:
    contacts = json.load(json_file, parse_float = decimal.Decimal)
    for contact in contacts:
        ExecutiveSponsorEmail = contact['ExecutiveSponsorEmail']
        TechnicalContact = contact['TechnicalContact']
        TechnicalContactEmail = contact['TechnicalContactEmail']
        ExecutiveSponsor = contact['ExecutiveSponsor']
        account_name = contact['account_name']
        account_id = contact['account_id']

        table.put_item(
           Item={
               'ExecutiveSponsorEmail': ExecutiveSponsorEmail,
               'TechnicalContact': TechnicalContact,
               'TechnicalContactEmail': TechnicalContactEmail,
               'ExecutiveSponsor': ExecutiveSponsor,
               'account_name': account_name,
               'account_id': account_id
            }
        )
