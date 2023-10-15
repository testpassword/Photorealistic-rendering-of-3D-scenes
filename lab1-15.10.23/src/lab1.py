def render(scene_in_path, with_imaps = True, with_pt = False):
    def decorator(fn):
        scene_out_path = fn.__name__
        scene = OpenScene(scene_in_path)
        fn(scene)
        LoadScene(scene)
        kernel = GetKernel()
        if with_imaps:
            imaps = scene.IMapsParams()
            imaps.req_acc = 0.01
            imaps.time_limit = 60
            kernel.CalculateIMaps()
        params = scene.RenderParams()
        params.time_limit = 60
        params.store_lum = True
        params.path = scene_out_path
        kernel.Render()
        if with_pt:
            pt_params = scene.PTRenderParams()
            pt_params.time_limit = 60
            pt_params.store_lum = True
            pt_params.path = scene_out_path + '_pt'
            kernel.PTRender()
        scene.Save(scene_out_path, OverwriteMode.OVERWRITE)
    return decorator


@render('./CornelBox')
def light_up(scene):
    light_node = scene.GetNode('F000001')
    light_node.light.kind = LightKind.LIGHT_POINT
    light_node.tr = Transform(azim = 90, tilt = 180, rot = 180)
    light_node.Translate(278000, -279500, 548700)

@render('./light_up')
def light_down(scene):
    light_node = scene.GetNode('F000001')
    light = light_node.light
    light.kind = LightKind.LIGHT_POINT
    light.gonio = IesGonio('./NewGonio.ies')
    light_node.tr = Transform(azim = 90, tilt = 0, rot = 0)
    light_node.targ_dist = 548700
    light_node.Translate(278000, -279500, 548700)

@render('./light_down')
def spherical(scene):
    SphereClass = GetClass(Shape, 'Sphere')
    sphere = SphereClass(radius = 70)
    part = sphere.parts[0]
    surface_front = part.surf_attrs.front_side
    surface_front.kd = 0
    surface_front.ktd = 1
    surface_front.kd_color = BWSurfColor(1)
    env = scene.GetMedium('env')
    part.front_medium = env
    part.back_medium = env
    scene.AddNode(MeshNode(
        sphere, 
        name = 'Sphere', 
        tr = XYZTransform(pos = (278000, -279500, 548700))
    ))

@render('./spherical')
def subdivided(scene):
    scene.SetSubdivision(use_subd = True, rel_step = 0.01)

@render('./subdivided', with_pt=True)
def gaussian(scene):
    for i in range(4):
        surface_front = scene.GetNode('brs_' + str(i)).shape.parts[0].surf_attrs.front_side
        surface_front.kd = 0
        surface_front.gr_val = 1
        surface_front.gr_ang = 5
    scene.GetNode('Sphere').SimHide()
