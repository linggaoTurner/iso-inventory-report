from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from boto3.dynamodb.conditions import Key, Attr
import boto3

dynamodb = boto3.resource('dynamodb')

def cross_account_report(request):

    return render(request, 'cross_account_report.html', context)

def get_contacts():
    return (account_id, account_name, exec_sponsor, exec_sponsor_email, tech_contacts, tech_contacts_email)

def get_payer():
    return payer_name

def get_roles():
    return (assume_role_link, template_version)
