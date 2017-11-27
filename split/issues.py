# synapse imports
from synapse_pay_rest import Client, Node, Transaction
from synapse_pay_rest import User as SynapseUser
from synapse_pay_rest.models.nodes import AchUsNode

# Creating a user
args = {
    'email':str(user.email),
    'phone_number':str(profile.phone),
    'legal_name':str(legal_name),
    'note': str(note),
    'supp_id':str(supp_id),
    'is_business':False,
    'cip_tag':cip_tag,
}
# sent the new users request
create_user = SynapseUser.create(client, **args)

#-------------------------------------------------------------------------------

# add a base document
#submit the defualy options
options = {
    'email': 'scoobie@doo.com',
    'phone_number': '707-555-5555',
    'ip': '127.0.0.1',
    'name': 'Doctor BaseDoc',
    'alias': 'Basey',
    'entity_type': 'F',
    'entity_scope': 'Arts & Entertainment',
    'birth_day': 28,
    'birth_month': 2,
    'birth_year': 1990,
    'address_street': '42 Base Blvd',
    'address_city': 'San Francisco',
    'address_subdivision': 'CA',
    'address_postal_code': '94114',
    'address_country_code': 'US'
}
# send the request for the base document
base_document = SynapseUser.add_base_document(**options)
updated_user = base_document.SynapseUser

#-------------------------------------------------------------------------------

# add the new virual document
# submit the document valie
virtual_document = base_document.add_virtual_document(type='SSN', value='3333')
# add document values to your base document
base_document = virtual_document.base_document
