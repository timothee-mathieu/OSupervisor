# OSupervisor

Outil graphique de supervision d'une installation OpenStack. 

Identité (Keystone) : Authentification via login ou fichier keystonerc_admin. Listage des projets, des utilisateurs et des keypairs.

Gestion des images (Glance) : Listage des images.

Compute (Nova) : Listage des instances et de leur état. 

Réseau (Neutron) : Listage des routeurs, réseaux et leurs sous-réseaux, des IPs floattantes, des agents réseau, des ports, des groupes et règles de sécurité.

Orchestration (Heat) : Listage des stacks.

Fonctionnalité d'ajout/suppresion de projets, utilisateurs, instances, routeurs, réseaux, sous-réseaux, IP flottantes, groupes et règles de sécurité.




### Prérequis

1. Python 3.8 ou supérieur https://www.python.org/doc/versions/ 

2. OpenStackSDK (version 0.47.0.dev44 ou supérieure) via PyPi.   
```
pip install openstacksdk
```


### Lancement

```
python app.py
```
S'authentifier auprès de Keystone en tant qu'administrateur.

## Guide d'utilisation 

* [OpenStackSDK Doc](https://docs.openstack.org/openstacksdk/latest/user/index.html) 


## Auteurs

* **Timothée MATHIEU** 
* **Guillaume PIOLEE** 


## License

Ce projet est soumis à une licence GNU General Public License v3.0 -  [LICENSE](LICENSE) 

