import pytest
from tests.factories import BranchFactory

@pytest.mark.django_db
class TestBranchModel:
    def test_create_branch(self):
        branch = BranchFactory()
        assert branch.name is not None
        assert branch.slug is not None
        assert branch.address is not None
    
    def test_branch_str_representation(self):
        branch = BranchFactory(name='Main Branch')
        assert str(branch) == 'Main Branch'