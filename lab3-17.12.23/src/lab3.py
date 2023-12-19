GONIO_LIB = GetLibrary(Gonio).GetFolder('Standard')
SphereClass = GetClass(Shape, 'Sphere')
RectangleClass = GetClass(Shape, 'Rectangle')
RectangleHoleClass = GetClass(Shape, 'RectangleHole')
KERNEL = GetKernel()


def get_front(node: Node):
    return node.shape.parts[0].surf_attrs.front_side


def apply_def_PT_params(scene: 'Scene', path: str):
    params = scene.PTRenderParams()
    params.time_limit = 60
    params.store_lum = True
    params.store_illum = False
    params.vs_accumulation = PTVSAccumulation.VS_OUTSIDE 
    params.image_quality = PTImageQuality.TRUE_EDGE_EFFECTS
    params.path = path
    params.is_lum = True
    params.show_lights = True
    params.show_indirect = True
    params.is_direct = True
    params.quasi_specular = True
    return params


def make_mirror_sphere_node(idx: int, pos: tuple) -> 'Node':
    return MeshNode(
        SphereClass(radius = 70000), 
        name = 'sphere_' + str(idx),
        tr = XYZTransform(pos = pos)
    )


def hide_node(node):
    node.SimHide()
    node.VisHide()


def unhide_node(node):
    node.SimUnhide()
    node.VisUnhide()



# NO BOUNDING_SPHERE
scene = OpenScene("./cornel_box0")
light_node = scene.GetNode("F000001")
light_node.light.name = "point_1"
light_node.light.kind = LightKind.LIGHT_POINT
sphs = [
    make_mirror_sphere_node(i, it) for i, it in 
    enumerate(
        [
            (190000, -164000, 235000), 
            (368000, -325000, 400000)
        ],
        start = 1
    )
]
for it in sphs:
    front = get_front(it)
    front.kd = 0
    front.ks = 0.99
    front.kd_color = BWSurfColor(1)
    scene.AddNode(it)
LoadScene(scene)
no_bounding_sphere_scene_name = 'no_bounding_sphere'
params = apply_def_PT_params(scene, no_bounding_sphere_scene_name)
KERNEL.PTRender()
scene.Save(no_bounding_sphere_scene_name, OverwriteMode.OVERWRITE)
KERNEL.UnloadScene(True)


# BOUNDING SPHERE
sphere_node_3 = MeshNode(
    SphereClass(
        name = "sphere_3", 
        radius = 70
    ), 
    name = "sphere_3",
    tr = XYZTransform(
        pos = (278000, -279500, 548700)
    )
)
sph3_front = get_front(sphere_node_3)
sph3_front.kd = 0
sph3_front.ktd = 0.95
sph3_front.kd_color = BWSurfColor(1)
scene.AddNode(sphere_node_3)
LoadScene(scene)
for r in [0.07, 7, 70, 700, 7000]:
    r_s = str(r).replace('.', '_')
    scene_name = 'bounding_sphere_r' + r_s
    params.path = scene_name
    sphere_node_3.shape.radius = r * 1000
    KERNEL.PTRender()
    scene.Save(scene_name, OverwriteMode.OVERWRITE)

KERNEL.UnloadScene(True)


# RECTANGLE ORIGINAL
scene = OpenScene('bounding_sphere_r7000')
light_node = scene.GetNode("F000001")
light_node.light.name = "rectangle_1"
light_node.light.kind = LightKind.LIGHT_RECTANGLE
hide_node(scene.GetNode("sphere_3"))
LoadScene(scene)
rectangle_original_scene_name = 'rectangle_original'
params = apply_def_PT_params(scene, rectangle_original_scene_name)
KERNEL.PTRender()
scene.Save(rectangle_original_scene_name, OverwriteMode.OVERWRITE)
KERNEL.UnloadScene(True)


# RECTANGE LAMBERT
light_node = scene.GetNode("F000001")
light_node.targ_dist = 548700
light_node.light.gonio = GONIO_LIB.GetItem('lambertian')
light_node.tr = Transform(azim = 90, tilt = 0, rot = 0)
light_node.Translate(278000, -279500, 548700)
LoadScene(scene)
rectangle_lambert_scene_name = 'rectangle_lambert'
params.path = rectangle_lambert_scene_name
KERNEL.PTRender()
scene.Save(rectangle_lambert_scene_name, OverwriteMode.OVERWRITE)
KERNEL.UnloadScene(True)


# RECTANGLE SPOT
light_node.light.gonio = GONIO_LIB.GetItem('spot')
LoadScene(scene)
rectangle_spot_scene_name = 'rectangle_spot'
params.path = rectangle_spot_scene_name
KERNEL.PTRender()
scene.Save(rectangle_spot_scene_name, OverwriteMode.OVERWRITE)
KERNEL.UnloadScene(True)


# BDF [ON/OFF]
scene = OpenScene(rectangle_spot_scene_name)
for it in ["brs_0", "brs_1", "brs_2", "F000001"]: hide_node(scene.GetNode(it))
for i in range(1, 3):
    front = get_front(scene.GetNode('sphere_' + str(i)))
    front.ks = 0
    front.gr_val = 0.95
    front.gr_ang = 10
dayLight = scene.DayLight()
dayLight.on = True
dayLight.SetNaturalMode()
dayLight.SetDirectMode(56.905, 340.17)
LoadScene(scene)

for it in [True, False]:
    BDF_scene_name = 'BDF_' + str(it)
    params = apply_def_PT_params(scene, BDF_scene_name)
    params.bdf_sampling = it
    KERNEL.PTRender()
    scene.Save(BDF_scene_name, OverwriteMode.OVERWRITE)
KERNEL.UnloadScene(True)


# WINDOW (scene only, need to run off/windows/automatic manually)
scene = OpenScene('BDF_False')
dayLight = scene.DayLight()
dayLight.kind = DayLightKind.SUN
for it in ["brs_0", "brs_2"]: unhide_node(scene.GetNode(it))
brs_0_right_node = scene.GetNode("brs_0").Clone()
brs_0_right_node.name = "brs_0_right"
brs_0_right_node.tr = XYZTransform(pos = (-550000, 0, 0))
for i in range(1, 3):
    front = get_front(scene.GetNode('sphere_' + str(i)))
    front.ks = 0.99
    front.gr_val = 0
    front.gr_ang = 30
camera = Camera(
    view_angle = 120, 
    targ_dist = 500,
    v_ang_type = CameraViewAngle.HORIZONTAL,
    tr = XYZTransform(
        pos = (203561, -13691, 324000),
        x_rot_ang = 82.858,
        y_rot_ang = 1.0251,
        z_rot_ang = -162.74
    )
)
scene.camera = camera
window_node = MeshNode(
    RectangleClass(
        name = "window",
        org = (-274800, 279600, 0),
        size = (274800, 279600)
    ), 
    name = "window",
    tr = XYZTransform(
        pos = (-555000, -556000, 0),
        x_rot_ang = 0,
        y_rot_ang = 90,
        z_rot_ang = 0
    )
)
window_front = get_front(window_node)
window_front.kd = 0
window_front.kts = 1
for it in [
        window_node, 
        MeshNode(
            RectangleHoleClass(
                name = "rectangle_hole",
                org = (-274800, 279600, 0),
                size = (549600, 559200),
                hsize = (274800, 279600)
            ), 
            name = "rectangle_hole",
            tr = XYZTransform(
                pos = (-555000, -556000, 0),
                x_rot_ang = 0,
                y_rot_ang = 90,
                z_rot_ang = 0,
            )
        ), 
        MeshNode(
            RectangleClass(
                name = "front_wall",
                size = (1112000, 548800),
                org = (0, 274400, 0)
            ), 
            name = "front_wall",
            tr = XYZTransform(
                x_rot_ang = 90,
                y_rot_ang = 0,
                z_rot_ang = 0
            )
        ), 
        brs_0_right_node
    ]:
    scene.AddNode(it)
scene.Notebook().AddCamera(camera)
LoadScene(scene)
sun_automatic_scene_name = 'window'
params = apply_def_PT_params(scene, sun_automatic_scene_name)
params.quasi_specular = True
params.bdf_sampling = False
params.inf_mode = PTInfinitesimalStore.INFINITESIMAL_NONE  
scene.Save(sun_automatic_scene_name, OverwriteMode.OVERWRITE)