# Omnipage utilise un format des coordonnées independant du DPI de l'image
# donc voici la formule à utiliser pour bien avoir les coordonnées sur l'image

def omni_coords_to_normal(omni_coord_value, image_dpi=300):
    res = int((omni_coord_value * image_dpi) / 1440)
    return res
