import csv
import os


def set_defaults(params: 'PTRenderParams') -> 'PTRenderParams':
    params.time_limit = 60
    params.store_lum = True
    params.store_illum = False
    params.vs_accumulation = PTVSAccumulation.VS_OUTSIDE
    params.is_lum = True
    params.show_lights = True
    params.show_indirect = True
    params.is_direct = True
    params.quasi_specular = False
    return params


fields = ['path', 'image_quality', 'killed_path_num', 'overlength_path_num', 'backward_path_num', 'backward_hit_num', 'forward_path_num', 'forward_hit_num', 'phase', 'accuracy', 'time']
scene_names = ['c-box', 'c-box2', 'room2', 'light_guides', 'car_interior', 'interior1']
kernel = GetKernel()
with open('stats.csv', 'w', newline='') as f:
    wr = csv.writer(f, delimiter=' ')
    wr.writerow(fields)
    for sn in scene_names:
        scene = OpenScene(os.path.join('additional scenes', sn, sn + '.IOF'))
        LoadScene(scene)
        qualities = [PTImageQuality.ADAPTIVE, PTImageQuality.MULTIPLE] + ([] if sn != 'room2' else [PTImageQuality.HIGH_FREQUENCY_NOISE, PTImageQuality.LOW_FREQUENCY_NOISE, PTImageQuality.TRUE_EDGE_EFFECTS])
        for q in qualities: 
            params = set_defaults(scene.PTRenderParams())
            params.path = scene.name + '_' + str(q).replace('PTImageQuality.', '')
            params.image_quality = q
            kernel.PTRender()
            wr.writerow([(getattr(params, f) if f != 'accuracy' else getattr(params, f) * 100)  for f in fields])
        kernel.UnloadScene(True)
