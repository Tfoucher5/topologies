class Workstation:
    def __init__(self, hostname, ipAddress, os):
        self.hostname = hostname
        self.ipAddress = ipAddress
        self.os = os

class User:
    def __init__(self, user_id, name, role, department, workstation=None):
        self.id = user_id
        self.name = name
        self.role = role
        self.department = department
        self.workstation = workstation

    def get_assignment_label(self):
        """Retourne une chaîne formatée pour valider l'affectation réseau"""
        # Si workstation existe, on prend son hostname, sinon on met "Aucun"
        ws_name = self.workstation.hostname if self.workstation else "Aucun"
        return f"{self.name} est affecté à {ws_name}"