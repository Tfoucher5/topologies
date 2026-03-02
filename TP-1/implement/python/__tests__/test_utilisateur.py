import pytest
from python.utilisateur import User, Workstation

@pytest.fixture
def create_env():
    """Fixture pour créer un environnement de base"""
    ws = Workstation("PC-PROD-01", "192.168.1.10", "Windows 10")
    user = User(1, "Robert", "CEO", "Direction", ws)
    return user, ws

class TestUserSystem:
    # On teste ici si l'affichage de l'affectation est correct selon les données
    @pytest.mark.parametrize("name, role, hostname, expected_output", [
        ("Rachel", "Secrétaire", "PC-SEC-01", "Rachel est affecté à PC-SEC-01"),
        ("Guillaume", "IT Guy", "PC-IT-01", "Guillaume est affecté à PC-IT-01"),
        ("Nathan", "Dev", "PC-DEV-01", "Nathan est affecté à PC-DEV-01")
    ])
    def test_assignment_display(self, name, role, hostname, expected_output):
        # Arrange
        ws = Workstation(hostname, "10.0.0.1", "Linux")
        user = User(99, name, role, "Service", ws)
        
        # Act
        result = user.get_assignment_label()
        
        # Assert
        assert result == expected_output

    def test_no_workstation(self):
        """Test spécifique pour un utilisateur sans poste"""
        user = User(2, "Celia", "Marketeuse", "Marketing")
        assert user.get_assignment_label() == "Celia est affecté à Aucun"