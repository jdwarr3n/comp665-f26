import numpy as np
import plotly.graph_objects as go
import pywavefront

with open('XYZ_Blocks.obj', 'r') as file:
    obj_data = file.read()

scene = pywavefront.Wavefront('XYZ_Blocks.obj', collect_faces=True)

vertices = np.array(scene.vertices)
x, y, z = vertices.T
i, j, k, fc = [], [], [], []

color_mapping = {
    'cubex':'red', 'cubey':'green', 'cubez':'blue',
    'textx':'grey','texty':'grey', 'textz':'grey',
    'cube_center':'grey'
}

for name, blend_mesh in scene.meshes.items():
    faces = np.array(blend_mesh.faces)
    i1, j1, k1 = faces.T
    i += list(i1)
    j += list(j1)
    k += list(k1)
    fc += [color_mapping[name] for _ in range(faces.shape[0])]

mesh = go.Mesh3d(x=x, y=y, z=z,
                 i=i, j=j, k=k,
                 facecolor=fc,
                 showscale=False)
# Source: https://community.plotly.com/t/visualize-3d-models-saved-as-wavefront-obj-files/18514/2
mesh.update(lighting=dict(ambient= 0.18,
                          diffuse= 1,
                          fresnel=  .1,
                          specular= 1,
                          roughness= .1),

            lightposition=dict(x=100,
                               y=200,
                               z=150))

layout = go.Layout(scene=dict(aspectratio=dict(x=1,y=1,z=1),
                              camera=dict(eye=dict(x=1., y=1., z=0.5)),
                              xaxis_title='data x',
                              yaxis_title='data y',
                              zaxis_title='data z'),
                   title='First-person view (data coordinates)')

fig = go.Figure(data=[mesh], layout=layout)
print(fig.to_json())



