import json
import boto3

iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')
iam_resource = boto3.resource('iam')

class Role:
    def __init__(self, role_name):
        self.role_name = role_name
        self.role = self.get_role()

    def get_role(self):
        try:
            role = iam_resource.Role(self.role_name)
            role.description
            return role
        except iam_client.exceptions.NoSuchEntityException as e:
            return

    def exists(self):
        return self.role is not None

    def create(self):
        try:
            iam_client.create_role(
                RoleName=self.role_name,
                Path='/lambdapool/',
                AssumeRolePolicyDocument=json.dumps({
                    'Version': '2012-10-17',
                    'Statement': [{
                        'Effect': 'Allow',
                        'Principal': {'Service': 'lambda.amazonaws.com'},
                        'Action': 'sts:AssumeRole'
                    }]
                }),
                Tags=[
                    {
                        'Key': 'creator',
                        'Value': 'lambdapool'
                    }
                ]
            )
        except iam_client.exceptions.EntityAlreadyExistsException as e:
            pass

        self.role = self.get_role()
        self.attach_policies()

    def attach_policies(self):
        self.role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')

    def detach_policies(self):
        self.role.detach_policy(PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')

    def delete(self):
        self.detach_policies()
        self.role.delete()
        self.role = None

    def get_arn(self):
        return self.role.arn

    def __repr__(self):
        return f'Role {self.role_name}'

def create_function(function_name, encoded_archive, role_arn):
    lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.6',
        Role=role_arn,
        Handler='lambdapool.lambda_handler',
        Code={
            'ZipFile': encoded_archive,
        },
        Tags={
            'creator': 'lambdapool',
            'function_name': function_name
        }
    )
