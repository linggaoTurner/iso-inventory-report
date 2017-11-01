from django.shortcuts import render
from django.template import loader,RequestContext
from django.http import HttpResponse,JsonResponse
from boto3.dynamodb.conditions import Key, Attr
import boto3
import pandas as pd
import numpy  as np
import json

db = boto3.resource('dynamodb', region_name='us-east-1')
def cross_account_report(request):
    data = data_consolidate(get_contacts(),get_payer(),get_roles())

    context = {'dataset':data,'totalData':len(data),'jsondata':json.dumps(data)}
    return render(request, 'cross_account_report.html', context)

def update_info(request):
    if request.is_ajax():
        lists = request.POST.get('list')
        #recieve json file from ajax
        jd = json.dumps(lists)
        jsonlist = eval(json.loads(jd))

        for i in range(0,len(jsonlist)):
            if jsonlist[i]['ExecutiveSponsor']!="":
                ExecutiveSponsor = jsonlist[i]['ExecutiveSponsor']
            else:
                ExecutiveSponsor = ""
            if jsonlist[i]['ExecutiveSponsorEmail']!="":
                ExecutiveSponsorEmail = jsonlist[i]['ExecutiveSponsorEmail']
            else:
                ExecutiveSponsorEmail = ""
            if jsonlist[i]['TechnicalContact']!="":
                TechnicalContact = jsonlist[i]['TechnicalContact']
            else:
                TechnicalContact = ""
            if jsonlist[i]['TechnicalContactEmail']!="":
                TechnicalContactEmail = jsonlist[i]['TechnicalContactEmail']
            else:
                TechnicalContactEmail = ""


            db = boto3.resource('dynamodb', region_name='us-east-1')
            table = db.Table('aws-inventory-contacts')

            if ExecutiveSponsor!= "":
                response = table.update_item(
                    Key={
                        'account_id': jsonlist[i]['account_id']
                    },
                    UpdateExpression="SET ExecutiveSponsor = :e",
                    ExpressionAttributeValues={
                        ':e': ExecutiveSponsor,
                    },
                    ReturnValues="UPDATED_NEW"
                )

            if ExecutiveSponsorEmail!= "":
                response = table.update_item(
                    Key={
                        'account_id': jsonlist[i]['account_id']
                    },
                    UpdateExpression="SET ExecutiveSponsorEmail = :ee",
                    ExpressionAttributeValues={
                        ':ee': ExecutiveSponsorEmail,
                    },
                    ReturnValues="UPDATED_NEW"
                )

            if TechnicalContact!= "":
                response = table.update_item(
                    Key={
                        'account_id': jsonlist[i]['account_id']
                    },
                    UpdateExpression="SET TechnicalContact = :t",
                    ExpressionAttributeValues={
                        ':t': TechnicalContact,
                    },
                    ReturnValues="UPDATED_NEW"
                )

            if TechnicalContactEmail!= "":
                response = table.update_item(
                    Key={
                        'account_id': jsonlist[i]['account_id']
                    },
                    UpdateExpression="SET TechnicalContactEmail = :te",
                    ExpressionAttributeValues={
                        ':te': TechnicalContactEmail,
                    },
                    ReturnValues="UPDATED_NEW"
                )

        return JsonResponse({"success": True, "message":jsonlist})
    else:
        return JsonResponse({"success": False})


def get_contacts():
    return scan_all_items(db,'aws-inventory-contacts')

def get_payer():
    return scan_all_items(db,'aws-inventory-payerlist')

def get_roles():
    return scan_all_items(db,'aws-inventory-roles')

def data_consolidate(contacts,payers,roles):
    contactDF = pd.DataFrame(contacts)
    payerDF = pd.DataFrame(payers)
    roleDF = pd.DataFrame(roles)
    df0 = contactDF.join(payerDF.set_index('account_id'), on='account_id',lsuffix='account_id')

    df1 = df0.join(roleDF.set_index('account_id'), on='account_id')

    filterdf = df1[['account_name','account_id','payer_id','ExecutiveSponsor','ExecutiveSponsorEmail','TechnicalContact','TechnicalContactEmail','iso_role_arn','iso_role_template_version']]

    newdf = pd.concat([filterdf,pd.DataFrame(columns=["iso_arn_link"])])

    for index, row in newdf.iterrows():
        if row['payer_id'] == '830840543013':
            row['payer_id'] = 'TurnerApps'
        if row['payer_id'] == '625885815701':
            row['payer_id'] = 'Dan Penn'
        if row['payer_id'] == '867690557112':
            row['payer_id'] = 'Bleacher Report'
        if type(row['ExecutiveSponsor']) is float or row['ExecutiveSponsor'] == 'XXXX' :
            row['ExecutiveSponsor'] = ""
        if type(row['ExecutiveSponsorEmail']) is float or row['ExecutiveSponsorEmail'] == 'XXXX':
            row['ExecutiveSponsorEmail'] = ""

        if type(row['TechnicalContact']) is float or row['TechnicalContact'] == 'XXXX':
            row['TechnicalContact'] = ""
        if type(row['TechnicalContactEmail']) is float or row['TechnicalContactEmail'] == 'XXXX':
            row['TechnicalContactEmail'] = ""
        if type(row['iso_role_template_version']) is float or row['iso_role_template_version'] == 'XXXX':
            row['iso_role_template_version'] = ""
        if type(row['iso_role_template_version']) is not str:
            row['iso_role_template_version'] = str(row['iso_role_template_version'])
        if type(row['iso_role_arn']) is not float:
            row['iso_arn_link']  = 'https://signin.aws.amazon.com/switchrole?account=' + row['account_id'] +  '&roleName=' + str(row['iso_role_arn']).split('/')[-1] + '&displayName=' + row['account_name']
            row['iso_role_arn'] = row['iso_role_arn'].split('/')[-1]
        else:
            row['iso_arn_link'] = ""
            row['iso_role_arn'] = 'No Cross-Account Role'
        row['payer_id'] = str(row['payer_id'])


    return newdf.to_dict('records')

'''
do full scan to get all items from table
'''
def scan_all_items(db,table_name):

    table = db.Table(table_name)
    response = table.scan()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items
