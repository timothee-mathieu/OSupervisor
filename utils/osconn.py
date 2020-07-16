
import sys
import openstack


#Fonction de creation de la connexion 
def createConnection(auth_url, region, project_name, username, password,
                      user_domain, project_domain):
    openstack.enable_logging(True, stream=sys.stdout)                  
    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region,
        user_domain_name=user_domain,
        project_domain_name=project_domain,
    )


