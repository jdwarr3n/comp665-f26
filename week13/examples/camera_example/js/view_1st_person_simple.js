function plot_1st_person_simple(div) {
    let mesh1 = {
        x: Array(50).fill().map(_ => Math.random() * 1),
        y: Array(50).fill().map(_ => Math.random() * 20),
        z: Array(50).fill().map(_ => Math.random() * 400),
        opacity: 0.8,
        color: 'rgb(300,100,200)',
        type: 'mesh3d',
    };

    let data1 = [mesh1];

    let layout1 = {
        title: 'First-person view',
        margin: {l: 0, r: -10, b: 0, t: 30, pad: 0},
        scene: {
            aspectmode: 'manual',
            aspectratio: {x: 1, y: 1, z: 1},
        }
    }
    layout1.scene = {
        ...layout1.scene,
        xaxis: {title: 'data x', range: [-1, 1], autorange: false, fixedrange: true},
        yaxis: {title: 'data y', range: [-20, 20], autorange: false, fixedrange: true},
        zaxis: {title: 'data z', range: [-400, 400], autorange: false, fixedrange: true},
    }

    Plotly.newPlot(plot_1st_person_div, data1, layout1, {displayModeBar: false});
    const plot3d_scene = plot_1st_person_div._fullLayout.scene._scene;
    plot3d_scene.camera.lookAt([model.eye.x, model.eye.y, model.eye.z], [model.center.x, model.center.y, model.center.z], [model.up.x, model.up.y, model.up.z]);

    return div;
}

let plot_1st_person_div = document.querySelector("#js-plotly-plot")
plot_1st_person_simple(plot_1st_person_div);