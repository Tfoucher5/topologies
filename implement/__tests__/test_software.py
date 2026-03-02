import pytest
from implement.software import Software

@pytest.fixture
def create_software():
    return Software()

class TestSoftware:
    @pytest.mark.parametrize("input_data, expected_output", [
        ("bonjour", "message => bonjour"),
        ("au revoir", "message => au revoir")
    ])
    def test_display_message(self, input_data, expected_output, create_software):
        result = create_software.display_message(input_data)
        assert result == expected_output