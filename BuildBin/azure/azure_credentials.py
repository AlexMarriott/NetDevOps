from azure.common.credentials import ServicePrincipalCredentials

# Tenant ID for your Azure subscription
TENANT_ID = 'ede29655-d097-42e4-bbb5-f38d427fbfb8'

# Your service principal App ID
CLIENT = 'eb5ebc59-4284-4195-8ff1-aac0e02f086e'

# Your service principal password
KEY = '47a7b544-d96d-4a27-b19c-64cf8db71fd6'

credentials = ServicePrincipalCredentials(
    client_id = CLIENT,
    secret = KEY,
    tenant = TENANT_ID
)

subscription_id = '8da87477-14ec-488c-a181-1dbdcc25525e'

def get_credentials():
    return credentials

def get_subscription():
    return subscription_id