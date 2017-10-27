
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, NumberAttribute
# Create your models here.

class Contacts(Model):

    class Meta:
        table_name = "aws-inventory-contacts"
        region = 'us-west-1'
    account_id = UnicodeAttribute(hash_key=True)
    account_name = UnicodeAttribute()
    ExecutiveSponsor = UnicodeAttribute()
    ExecutiveSponsorEmail = UnicodeAttribute()
    TechnicalContact = UnicodeAttribute()
    TechnicalContactEmail = UnicodeAttribute()

class Payerlist(Model):
    class Meta:
        table_name = "aws-inventory-payerlist"
        region = 'us-west-1'
    account_id = UnicodeAttribute(hash_key=True)
    account_name = UnicodeAttribute()
    account_status = UnicodeAttribute()
    payer_id = UnicodeAttribute()
    payer_record = JSONAttribute()
    root_email = UnicodeAttribute()

class Roles(Model):
    class Meta:
        table_name = "aws-inventory-roles"
        region = 'us-west-1'
    account_id = UnicodeAttribute(hash_key=True)
    iso_role_arn = UnicodeAttribute()
    iso_role_template_version = UnicodeAttribute()
    AlertLogicConsolidatedTemplateName = UnicodeAttribute()
    AlertLogicConsolidatedTemplateVersion = UnicodeAttribute()
