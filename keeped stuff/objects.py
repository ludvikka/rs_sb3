from robosuite.models.objects import BoxObject, LemonObject, BreadObject
from robosuite.utils.mjcf_utils import CustomMaterial

from robosuite.models.objects import MujocoXMLObject
from robosuite.utils.mjcf_utils import array_to_string, find_elements, xml_path_completion

tex_attrib = {
            "type": "cube",
        }
mat_attrib = {
    "texrepeat": "1 1",
    "specular": "0.4",
    "shininess": "1.1",
}
redwood = CustomMaterial(
    texture=[1,1,0,0.5],
    tex_name="redwood",
    mat_name="redwood_mat",
    tex_attrib=tex_attrib,
    mat_attrib=mat_attrib,
)
CubeA = BoxObject(
    name="cube",
    size_min=[0.020, 0.020, 0.020],  # [0.015, 0.015, 0.015],
    size_max=[0.022, 0.022, 0.022],  # [0.018, 0.018, 0.018])
    #rgba=[1, 0, 0, 1],
    material=redwood
)

class RandomObject(MujocoXMLObject):
    """
    Bottle object
    """

    def __init__(self, name):
        super().__init__(
            xml_path_completion("objects/bottle.xml"),
            name=name,
            joints=[dict(type="free", damping="0.0005")],
            obj_type="all",
            duplicate_collision_geoms=True,
        )


#objects.append(LemonObject(name = "Lemon"))
#objects.append(BreadObject(name = "Bread"))