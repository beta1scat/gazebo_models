import os
import shutil
import trimesh
import random
import xml.etree.ElementTree as ET
import xml.dom.minidom

def get_random_gazebo_material():
    materials = [
        # 'Gazebo/Blue', 'Gazebo/Green', 'Gazebo/Red',
        # 'Gazebo/Orange', 'Gazebo/Yellow', 'Gazebo/Purple',
        # 'Gazebo/White', 'Gazebo/Black', 'Gazebo/Gray',
        # "Gazebo/Turquoise",
        # "Gazebo/Orange",
        # "Gazebo/Indigo",
        # "Gazebo/WhiteGlow",
        # "Gazebo/RedGlow",
        # "Gazebo/GreenGlow",
        # "Gazebo/BlueGlow",
        # "Gazebo/YellowGlow",
        # "Gazebo/PurpleGlow",
        # "Gazebo/RedTransparentOverlay",
        # "Gazebo/BlueTransparentOverlay",
        # "Gazebo/GreenTransparentOverlay",
        # "Gazebo/OrangeTransparentOverlay",
        # "Gazebo/DarkOrangeTransparentOverlay",
        "Gazebo/WoodFloor",
        "Gazebo/CeilingTiled",
        "Gazebo/PaintedWall",
        "Gazebo/PioneerBody",
        "Gazebo/Pioneer2Body",
        "Gazebo/Gold",
        "Gazebo/GreyGradientSky",
        "Gazebo/CloudySky",
        "Gazebo/WoodPallet",
        "Gazebo/Wood",
        "Gazebo/Bricks",
        "Gazebo/Road",
        "Gazebo/Residential",
        "Gazebo/Tertiary",
        "Gazebo/Pedestrian",
        "Gazebo/Footway",
        "Gazebo/Motorway",
    ]
    return random.choice(materials)

def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_model_config(name, author_name, author_email, description, output_dir):
    model_config = ET.Element('model')
    # Add name element
    model_name = ET.SubElement(model_config, 'name')
    model_name.text = name
    # Add version element
    version = ET.SubElement(model_config, 'version')
    version.text = '1.0'
    # Add sdf element
    sdf = ET.SubElement(model_config, 'sdf', {'version': '1.6'})
    sdf.text = 'model.sdf'
    # Add author element
    author = ET.SubElement(model_config, 'author')
    author_name_elem = ET.SubElement(author, 'name')
    author_name_elem.text = author_name
    author_email_elem = ET.SubElement(author, 'email')
    author_email_elem.text = author_email
    # Add description element
    desc = ET.SubElement(model_config, 'description')
    desc.text = description

    # Write to file with pretty print
    with open(os.path.join(output_dir, 'model.config'), 'w') as f:
        f.write(prettify(model_config))

def create_model_sdf(name, mass, inertia, mesh_uri, output_dir):
    sdf = ET.Element('sdf', {'version': '1.6'})
    model = ET.SubElement(sdf, 'model', {'name': name})
    static = ET.SubElement(model, 'static')
    static.text = 'false'
    link = ET.SubElement(model, 'link', {'name': 'link'})

    # Add inertial element
    inertial = ET.SubElement(link, 'inertial')
    mass_elem = ET.SubElement(inertial, 'mass')
    mass_elem.text = str(mass)

    inertia_elem = ET.SubElement(inertial, 'inertia')
    ix = ET.SubElement(inertia_elem, 'ixx')
    ix.text = str(inertia[0])
    iy = ET.SubElement(inertia_elem, 'iyy')
    iy.text = str(inertia[1])
    iz = ET.SubElement(inertia_elem, 'izz')
    iz.text = str(inertia[2])
    ixy = ET.SubElement(inertia_elem, 'ixy')
    ixy.text = '0.0'
    ixz = ET.SubElement(inertia_elem, 'ixz')
    ixz.text = '0.0'
    iyz = ET.SubElement(inertia_elem, 'iyz')
    iyz.text = '0.0'

    # Add visual element
    visual = ET.SubElement(link, 'visual', {'name': 'visual'})
    geo = ET.SubElement(visual, 'geometry')
    mesh = ET.SubElement(geo, 'mesh')
    uri = ET.SubElement(mesh, 'uri')
    uri.text = mesh_uri

    # Add material element
    material = ET.SubElement(visual, 'material')
    script = ET.SubElement(material, 'script')
    uri = ET.SubElement(script, 'uri')
    uri.text = 'file://media/materials/scripts/gazebo.material'
    name_elem = ET.SubElement(script, 'name')
    name_elem.text = get_random_gazebo_material()

    # Add collision element
    collision = ET.SubElement(link, 'collision', {'name': 'collision'})
    col_geo = ET.SubElement(collision, 'geometry')
    col_mesh = ET.SubElement(col_geo, 'mesh')
    col_uri = ET.SubElement(col_mesh, 'uri')
    col_uri.text = mesh_uri

    # Write to file with pretty print
    with open(os.path.join(output_dir, 'model.sdf'), 'w') as f:
        f.write(prettify(sdf))
input_dir = "/home/niu/Downloads/3560735"
output_dir = "./YCB_gazebo"
files = os.listdir(input_dir)
for file in files:
    name = "YCB_" + file[:-4]
    dest_dir = os.path.join(output_dir, name + "/meshes")
    os.makedirs(dest_dir, exist_ok=True)
    mesh = trimesh.load(os.path.join(input_dir, file))
    mesh.export(os.path.join(dest_dir, "model.stl"))
    author_name = 'beta1scat'
    author_email = 'https://github.com/beta1scat/'
    description = f'Model of {name}.'
    mass = 2.0  # mass in kg
    inertia = (0.001, 0.001, 0.001)  # inertia tensor components ixx, iyy, izz
    mesh_uri = f'model://{name}/meshes/model.stl'
    xmlDir = os.path.join(output_dir, name)
    create_model_config(name, author_name, author_email, description, xmlDir)
    create_model_sdf(name, mass, inertia, mesh_uri, xmlDir)
