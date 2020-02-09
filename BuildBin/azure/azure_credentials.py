from azure.common.credentials import ServicePrincipalCredentials

# Tenant ID for your Azure subscription
TENANT_ID = ''

# Your service principal App ID
CLIENT = ''

# Your service principal password
KEY = ''

credentials = ServicePrincipalCredentials(
    client_id = CLIENT,
    secret = KEY,
    tenant = TENANT_ID
)

subscription_id = ''

def get_credentials():
    return credentials

def get_subscription():
    return subscription_id