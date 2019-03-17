import pytest

from lambdapool.aws import Role, iam_resource
from lambdapool.exceptions import AWSError

def get_role_arn(role_name):
    role = iam_resource.Role(role_name)
    return role.arn

def get_role_policies(role_name):
    role = iam_resource.Role(role_name)
    return list(role.attached_policies.all())

@pytest.mark.s3
class TestRoleGeneric:
    @pytest.fixture(autouse=True)
    def setup_role(self):
        self.role = Role('test-role')
        self.role.create()

    def teardown_method(self):
        self.role.delete()

    def test_role_policy_attachment(self):
        policies = get_role_policies('test-role')

        assert len(policies) == 1
        assert policies[0].arn == 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'

    def test_role_policy_detachment(self):
        self.role.detach_policies()

        policies = get_role_policies('test-role')

        assert len(policies) == 0

        self.role.attach_policies()

    def test_repr(self):
        assert repr(self.role) == 'Role test-role'

@pytest.mark.s3
class TestRoleWhileDoesNotExist:
    def teardown_method(self):
        role = Role('test-role')
        if role.exists():
            role.delete()

    def test_role_exists(self):
        role = Role('test-role')
        assert role.exists() == False

    def test_role_create(self):
        role = Role('test-role')
        role.create()
        assert role.get_role().name == 'test-role'

    def test_role_delete(self):
        role = Role('test-role')
        with pytest.raises(AWSError):
            role.delete()

    def test_role_get_arn(self):
        role = Role('test-role')

        with pytest.raises(AWSError):
            role.get_arn()

@pytest.mark.s3
class TestRoleExists:
    @pytest.fixture(autouse=True)
    def setup_role(self):
        role = Role('test-role')
        role.create()

    def teardown_method(self):
        role = Role('test-role')
        if role.exists():
            role.delete()

    def test_role_exists(self):
        role = Role('test-role')
        assert role.exists() == True

    def test_role_create(self):
        role = Role('test-role')
        with pytest.raises(AWSError):
            role.create()

    def test_role_delete(self):
        role = Role('test-role')
        role.delete()

        assert role.exists() == False

    def test_role_get_arn(self):
        role = Role('test-role')

        assert role.get_arn() == get_role_arn('test-role')
