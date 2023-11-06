# apply modified texture to cubes
scene = OpenScene('./initial')
for (lum_orig, lum_new) in [
    (50, 175), 
    (75, 325), 
    (100, 450)
]: 
    node = scene.GetNode(str(lum_orig) + 'nit')
    cube_name = str(lum_new) + 'nit'
    node.name = cube_name
    node.shape.name = cube_name
    surf = node.shape.parts[0].surf_attrs
    surf.self_lum = lum_new
    surf.SetTexture(
        StdTexture(
            './' + cube_name + '.png', 
            DuplicationMode.DUPL_RAGGED,
        )
    )

# build observers
scene.GetNode("floor shape node").shape.parts[0].surf_attrs.self_lum = 40  # set floor luminance by task 
for angle in [1, 10, 30, 60, 90]: 
    scene.AddNode(
        ObserverNode(
            PlaneObserver(
                res = (640, 480),
                thresh_ang = angle,
                org = (-0.5, 0.5, 0),
                x_side = (1, 0, 0),
                y_side = (0, -1, 0),
                glob_attached = True,
                occlusion = True,
                ortho = False,
                focal_dist = 3300,
                phenom = ObserverData.LUM
            ),
            name = 'plane_obs_' + str(angle),
            tr = XYZTransform(
                x_rot_ang = 67.768,
                y_rot_ang = 0,
                z_rot_ang = -17.347,
                scale = (3435.743, 2576.807, 1)
            )
        )
    )
lens_obs = ObserverNode(
    LensObserver(
        phenom = ObserverData.LUM,
        pupil_diam = 50,
        focal_length = 100,
        focusing_dist = 3300,
        view_angle = 42.65,
        res = (640, 480),
        image_dist = 103.125,
    ),
    name = 'lens_obs'
)
lens_obs.Translate(-910.77, -2915.73, 1248.6)
lens_obs.Rotate(67.768, 0, -17.347)
camera = Camera(
    view_angle = 55, 
    targ_dist = 3300, 
    name = 'cam',
    tr = XYZTransform(
        pos = (-910.77, -2915.73, 1248.6),
        x_rot_ang = 67.768,
        y_rot_ang = 3.1806e-15,
        z_rot_ang = -17.347
    )
)
camera.SetLensParams(80, 126, 220)
camera.Apply()
scene.AddNode(lens_obs)
scene.Save('lab2', OverwriteMode.OVERWRITE)
res_scene = OpenScene('./lab2')
LoadScene(res_scene)

# render
imaps = res_scene.IMapsParams()
imaps.time_limit = 60 * 60 * 3  # 3 hours
imaps.SetObserverAsAccSource(res_scene.GetNode('lens_obs'))
GetKernel().CalculateIMaps()
