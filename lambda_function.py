[16:29] Kumar, Manish
#import aws_cdk.aws_ssm as ssm
import json
import boto3
import ast
# import aws
# These two variables need to be treated as a pair #
# this variable has the list of groups to add to the account, the groups need to be created before hand #
def lambda_handler(event, context):
#Calling group list and permission set list from perameter store
client = boto3.client('ssm')
resp = client.get_parameter( Name = 'group_list', WithDecryption=True )
var_group_names= resp['Parameter']['Value']
var_group_names = var_group_names.split(",")
print(var_group_names)
#test = ssm.StringParameter.value_for_string_parameter(
#self, "group_list")
#print(test)
response = client.get_parameter( Name = 'permission_list', WithDecryption=True )
var_permission_set= response['Parameter']['Value']
var_permission_set = var_permission_set.split(",")
print(var_permission_set)
#var_group_names = ['SSO','test-mk']
#var_permission_set = ['DataEngineer', 'AWSAdministratorAccess']
dict_group_names={​​}​​
dict_permission_set={​​}​​
print("loading function")
## Instance arn & Identity store ##
client = boto3.client('sso-admin')
instance = client.list_instances()
print(instance)
#instance_arn = instance(int(['Instances']['InstanceArn']))
#identitystore_id = instance['Instances']['IdentityStoreId']
for d in instance["Instances"]:
instance_arn = (d['InstanceArn'])
identitystore_id = (d['IdentityStoreId'])
## Instance arn & Identity store ## ## Target id ##
target_id=(event['serviceEventDetails']['createAccountStatus']['accountId'])
## Target id ## ## GroupId ##
client = boto3.client('identitystore')
index=0
for gn in var_group_names:
#print(gn)
groups = client.list_groups(
IdentityStoreId = identitystore_id,
Filters=[
{​​
'AttributePath': 'DisplayName',
'AttributeValue': gn
}​​,
]
)
for g in groups['Groups']:
groupid = (g["GroupId"])
dict_group_names.update({​​index:groupid}​​)
index+=1
## GroupId ##
## Permission set arn ##
client = boto3.client('sso-admin')
permissions = client.list_permission_sets(
InstanceArn= instance_arn
)
#print(permissions)
index=0
for p in permissions['PermissionSets']:
for pn in var_permission_set:
print(pn)
response = client.describe_permission_set(
InstanceArn=instance_arn,
PermissionSetArn=p
)
if (response['PermissionSet']['Name']==pn):
#dict_permission_set.update({​​response['PermissionSet']['Name']: p}​​)
dict_permission_set.update({​​index: p}​​),
index+=1
## Permission set arn ## ## Assigning permissions sets and groups to the account created ##
for i in range(len(var_group_names)):
response = client.create_account_assignment(
InstanceArn= instance_arn,
TargetId=target_id,
TargetType='AWS_ACCOUNT',
PermissionSetArn=dict_permission_set[i],
PrincipalType='GROUP',
PrincipalId=dict_group_names[i]
)
print('event:', json.dumps(event))
## Assigning permissions sets and groups to the account created ##

