import json
import datetime
import boto3

from lambdapool.version import __version__

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

class LambdaFunction:
    def __init__(self, function_name):
        self.function_name = function_name

    def exists(self):
        try:
            lambda_client.get_function(FunctionName=self.function_name)
        except lambda_client.exceptions.ResourceNotFoundException:
            return False

        return True

    def create(self, archive):
        if self.exists():
            raise ValueError(f'Function {self.function_name} already exists')

        role_name = f'lambdapool-role-{self.function_name}'
        role = Role(role_name)
        role.create()

        # XXX-Nabarun: Hack to solve the issue of propagation of roles
        # AWS IAM Roles do not instantly propagate through the AWS infrastructure
        # Also, there is no defined way to know if the propagation is complete
        # https://stackoverflow.com/questions/37503075/invalidparametervalueexception-the-role-defined-for-the-function-cannot-be-assu
        created = False
        while not created:
            try:
                self._create_function(role, archive)
                created = True
            except lambda_client.exceptions.InvalidParameterValueException:
                created = False

    def _create_function(self, role, archive):
        lambda_client.create_function(
            FunctionName=self.function_name,
            Runtime='python3.6',
            Role=role.get_arn(),
            Handler='lambdapool.lambda_handler',
            Code={
                'ZipFile': archive,
            },
            Tags={
                'creator': 'lambdapool',
                'function_name': self.function_name
            },
            Environment={
                'Variables': {
                    'CREATOR': 'lambdapool',
                    'FUNCTION_NAME': self.function_name,
                    'LAMBDAPOOL_VERSION': __version__
                }
            }
        )

    def update(self, archive):
        if not self.exists():
            raise ValueError(f'Function {self.function_name} does not exist')

        lambda_client.update_function_code(
            FunctionName=self.function_name,
            ZipFile=archive
            )

    def delete(self):
        if not self.exists():
            raise ValueError(f'Function {self.function_name} does not exist')

        lambda_client.delete_function(FunctionName=self.function_name)

        role_name = f'lambdapool-role-{self.function_name}'
        role = Role(role_name)
        role.delete()

def list_functions():
    return [function for function in _list_functions() if is_lambdapool_function(function['environment'])]

def _list_functions():
    kwargs = {}
    while True:
        response = lambda_client.list_functions(**kwargs)
        yield from [
            {
                'function_arn': function['FunctionArn'],
                'function_name': function['FunctionName'],
                'size': function['CodeSize'],
                'last_updated': datetime.datetime.strptime(function['LastModified'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                'environment': function.get('Environment', {}).get('Variables', {})
            }
            for function in response.get('Functions', [])
        ]

        next_marker = response.get('NextMarker')
        if next_marker:
            kwargs['Marker'] = next_marker
        else:
            break

def is_lambdapool_function(environment):
    return environment.get('CREATOR') == 'lambdapool'
