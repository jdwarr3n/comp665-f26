function plot_3rd_person(new_div, old_div, init_camera) {
    let old_plotly_scene = old_div._fullLayout.scene;
    let old_plot3d_scene = old_plotly_scene._scene;

    // 0: eye; 1: center
    let scatter_eye = {type: 'scatter3d', mode: 'markers', ...model.eye, marker: {size: 5}, name: 'eye'};

    let line_eyesight = {
        type: 'scatter3d', mode: 'lines',
        x: [model.eye.x, model.center.x], y: [model.eye.y, model.center.y], z: [model.eye.z, model.center.z],
        line: {dash: 'dot', width: 6, color: 'orange'},
        name: 'eyesight'
    }

    let line_up = {
        type: 'scatter3d', mode: 'lines',
        x: [model.eye.x, model.eye.x+model.up.x], y: [model.eye.y, model.eye.y+model.up.y], z: [model.eye.z, model.eye.z+model.up.z],
        line: {dash: 'dash', width: 6, color: 'green'},
        name: 'up vector'
    }

    let data2 = [scatter_eye, line_eyesight, line_up];
    const display_objs = old_plot3d_scene.glplot.objects;
    for (obj of display_objs) {
        const data = obj._trace.data._input;
        switch (data.type) {
            case 'mesh3d':
                let mesh2 = {
                    ...data,
                    x: Array.from(obj.positions).map(p => p[0]),
                    y: Array.from(obj.positions).map(p => p[1]),
                    z: Array.from(obj.positions).map(p => p[2]),
                    i: Array.from(obj.cells).map(p => p[0]),
                    j: Array.from(obj.cells).map(p => p[1]),
                    k: Array.from(obj.cells).map(p => p[2]),
                    opacity: 0.4
                }
                data2.push(mesh2);
                break;

            default:
                // Not yet supported
                console.log(`Trace type ${type} is not supported`);
                console.assert(false)
        }
    }

    let [x1, y1, z1] = old_plot3d_scene.glplot.bounds[0];
    let [x2, y2, z2] = old_plot3d_scene.glplot.bounds[1];

    console.log('figure_x_range', x1, x2);
    console.log('figure_y_range', y1, y2);
    console.log('figure_z_range', z1, z2);

    let layout2 = {...plot_1st_person_div.layout, title: 'Third-person view (figure coordinates)', showlegend: true,};
    layout2.scene = {
        ...layout2.scene,
        xaxis: {title: 'figure x', range: [x1 - 2, x2 + 2], autorange: false, fixedrange: true},
        yaxis: {title: 'figure y', range: [y1 - 2, y2 + 2], autorange: false, fixedrange: true},
        zaxis: {title: 'figure z', range: [z1 - 2, z2 + 2], autorange: false, fixedrange: true},
        camera: init_camera,
    };



    Plotly.newPlot(new_div, data2, layout2, {displayModeBar: false});

    const minus = String.fromCharCode(8722); // −
    const hypen_minus = String.fromCharCode(45); // -

    layout2.scene.xaxis.tickmode = 'array'
    layout2.scene.xaxis.tickvals = new_div._fullLayout.scene._scene.axesOptions.ticks[0].map(tick=>parseInt(tick.text.replace(minus, hypen_minus)))
    layout2.scene.yaxis.tickmode = 'array'
    layout2.scene.yaxis.tickvals = new_div._fullLayout.scene._scene.axesOptions.ticks[1].map(tick=>parseInt(tick.text.replace(minus, hypen_minus)))
    layout2.scene.zaxis.tickmode = 'array'
    layout2.scene.zaxis.tickvals = new_div._fullLayout.scene._scene.axesOptions.ticks[2].map(tick=>parseInt(tick.text.replace(minus, hypen_minus)))

    return new_div;
}

let plot_3rd_person_div = document.querySelector('#js-plotly-plot2')
plot_3rd_person(plot_3rd_person_div, plot_1st_person_div, {
    eye: {
        "x": 1.5078432950522334,
        "y": 0.6290198835110671,
        "z": 0.7488817797123491
    },
    center: {x: 0, y: 0, z: 0},
    up: {x: 0, y: 0, z: 1}
})

// plot_3rd_person_div._fullLayout.scene._scene.getCamera()