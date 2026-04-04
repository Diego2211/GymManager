

def es_admin(membership):
    return membership.rol in ["admin", "owner"]

def es_profesor(membership):
    return membership.rol in ["profesor"]