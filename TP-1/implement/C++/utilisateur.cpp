#include <iostream>
#include <string>

class Workstation {
public:
    std::string hostname, ipAddress, os;
    
    Workstation(std::string h, std::string ip, std::string o) 
        : hostname(h), ipAddress(ip), os(o) {}
};

class User {
private:
    int id;
    std::string name, role, department;
    Workstation* workstation; // Association via un pointeur

public:
    User(int i, std::string n, std::string r, std::string d, Workstation* ws = nullptr)
        : id(i), name(n), role(r), department(d), workstation(ws) {}

    void afficherInfos() {
        std::cout << "Utilisateur: " << name;
        if (workstation) {
            std::cout << " | Poste: " << workstation->hostname << std::endl;
        } else {
            std::cout << " | Aucun poste affecte." << std::endl;
        }
    }
};

int main() {
    Workstation pcRachel("PC-SEC-01", "192.168.30.11", "Windows 10");
    User rachel(2, "Rachel", "Secretaire", "Direction", &pcRachel);

    rachel.afficherInfos();
    return 0;
}