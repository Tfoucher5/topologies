# -------------------------------------------------------
# Modèles de données
# -------------------------------------------------------

class EthernetFrame:
    def __init__(self, srcMac, destMac, payload=""):
        self.srcMac = srcMac
        self.destMac = destMac
        self.payload = payload  # contient un IPPacket (encapsulation)


class IPPacket:
    def __init__(self, srcIp, destIp, ttl=64):
        self.srcIp = srcIp
        self.destIp = destIp
        self.ttl = ttl


# -------------------------------------------------------
# Classe mère Switch
# SOLID - SRP : Switch gère uniquement son nom et son
#               comportement générique de traitement
# -------------------------------------------------------

class Switch:
    def __init__(self, name):
        self.name = name

    def process(self):
        # GRASP - Polymorphisme : redéfini dans les sous-classes
        print(f"[{self.name}] Traitement générique")


# -------------------------------------------------------
# L2Switch — classe mère des switches
# SOLID - OCP : ouvert à l'extension (L3Switch), fermé
#               à la modification
# GRASP - Expert : possède et gère sa propre macTable
# -------------------------------------------------------

class L2Switch(Switch):
    def __init__(self, name):
        super().__init__(name)
        self.macTable = {}  # mac -> port

    def process(self):
        # GRASP - Polymorphisme : comportement L2 spécifique
        print(f"[{self.name}] Traitement L2 : commutation par adresse MAC")

    def forward(self, frame: EthernetFrame):
        print(f"[{self.name}] Trame reçue : {frame.srcMac} -> {frame.destMac}")
        if frame.destMac in self.macTable:
            port = self.macTable[frame.destMac]
            print(f"[{self.name}] MAC connue → envoi sur port {port}")
        else:
            print(f"[{self.name}] MAC inconnue → inondation sur tous les ports")


# -------------------------------------------------------
# L3Switch — classe enfant de L2Switch
# SOLID - LSP : L3Switch peut remplacer L2Switch partout
#               (il hérite de forward() et peut l'utiliser)
# GRASP - Polymorphisme : process() et route() ont un
#         comportement différent malgré le nom identique
# -------------------------------------------------------

class L3Switch(L2Switch):
    def __init__(self, name):
        super().__init__(name)
        self.routingTable = {}  # ip destination -> next hop

    def process(self):
        # Comportement homonyme à L2Switch.process() mais différent
        # GRASP - Polymorphisme
        print(f"[{self.name}] Traitement L3 : commutation MAC + routage IP")

    def route(self, packet: IPPacket):
        # Comportement spécifique au L3Switch uniquement
        print(f"[{self.name}] Routage : {packet.srcIp} -> {packet.destIp} (TTL={packet.ttl})")
        if packet.destIp in self.routingTable:
            next_hop = self.routingTable[packet.destIp]
            print(f"[{self.name}] Route trouvée → next hop : {next_hop}")
        else:
            print(f"[{self.name}] Aucune route pour {packet.destIp}")
        # Le L3Switch décrémente le TTL — le L2Switch ne le fait jamais
        packet.ttl -= 1
        print(f"[{self.name}] TTL décrémenté → {packet.ttl}")


# -------------------------------------------------------
# Test basé sur le schéma Packet Tracer
# -------------------------------------------------------

# SW-Marketing (L2) : Nathan, Miki, Celia
sw_marketing = L2Switch("SW-Marketing")
sw_marketing.macTable["AA:BB:CC:DD:EE:01"] = 1  # Nathan
sw_marketing.macTable["AA:BB:CC:DD:EE:02"] = 2  # Miki

sw_marketing.process()
trame = EthernetFrame("AA:BB:CC:DD:EE:01", "AA:BB:CC:DD:EE:02")
sw_marketing.forward(trame)

print()

# MainSwitch (L3) : route entre Marketing (VLAN20) et Direction (VLAN22)
main_switch = L3Switch("MainSwitch")
main_switch.routingTable["192.168.22.10"] = "192.168.22.1"

main_switch.process()
paquet = IPPacket("192.168.20.10", "192.168.22.10")  # Nathan -> DG
main_switch.route(paquet)

print()

# LSP : L3Switch utilisé là où un L2Switch est attendu
print("--- Vérification LSP ---")
trame2 = EthernetFrame("AA:BB:CC:DD:EE:03", "AA:BB:CC:DD:EE:01")
main_switch.forward(trame2)  # forward() hérité de L2Switch, fonctionne normalement
