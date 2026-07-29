/**
 * Modified by Zion, Spring 2021
 *
 * learn_webgl_events_01.js, By Wayne Brown, Fall 2015
 *
 * These event handlers can modify the characteristics of a scene.
 * These will be specific to a scene's models and the models' attributes.
 */

/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 C. Wayne Brown
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

"use strict";

// model for the 1st person plot's camera position
let init_model = {
    eye: {x: 1.327, y: 1.306, z: 1.104},
    center: {x: 0, y: 0, z: 0},
    up: {x: 0, y: 0, z: 1}
}

let model = {...JSON.parse(JSON.stringify(init_model))}

function bindEvents(plot_1st_person_div, plot_3rd_person_div) {
    let plot3d_scene = plot_1st_person_div._fullLayout.scene._scene;


    const text_eye = document.querySelector('#eye_text')
    const text_center = document.querySelector('#center_text')
    const text_up = document.querySelector('#up_text')

    const slider_eyeX = document.querySelector('#W1_eyeX');
    const slider_eyeY = document.querySelector('#W1_eyeY');
    const slider_eyeZ = document.querySelector('#W1_eyeZ');

    const slider_centerX = document.querySelector('#W1_cX');
    const slider_centerY = document.querySelector('#W1_cY');
    const slider_centerZ = document.querySelector('#W1_cZ');

    const slider_upX = document.querySelector('#W1_upX');
    const slider_upY = document.querySelector('#W1_upY');
    const slider_upZ = document.querySelector('#W1_upZ');

    const reset_btn = document.querySelector('#W1_reset');


    function update_text() {
        text_eye.innerHTML = '<strong>eye ('
            + model.eye.x.toFixed(1) + ', '
            + model.eye.y.toFixed(1) + ', '
            + model.eye.z.toFixed(1) + ')</strong>';
        text_center.innerHTML = '<strong>center ('
            + model.center.x.toFixed(1) + ', '
            + model.center.y.toFixed(1) + ', '
            + model.center.z.toFixed(1) + ')</strong>';
        text_up.innerHTML = '<strong>up &lt;'
            + model.up.x.toFixed(1) + ', '
            + model.up.y.toFixed(1) + ', '
            + model.up.z.toFixed(1) + '&gt;</strong>';
    }

    function saveSliderValues() {
        model.eye.x = Number(slider_eyeX.value);
        model.eye.y = Number(slider_eyeY.value);
        model.eye.z = Number(slider_eyeZ.value);

        model.center.x = Number(slider_centerX.value);
        model.center.y = Number(slider_centerY.value);
        model.center.z = Number(slider_centerZ.value);

        model.up.x = Number(slider_upX.value);
        model.up.y = Number(slider_upY.value);
        model.up.z = Number(slider_upZ.value);
    }

    function update_plot2() {
        const update_eye = {
            x: [[model.eye.x]],
            y: [[model.eye.y]],
            z: [[model.eye.z]]
        }

        const update_eyesight = {
            x: [[model.eye.x, model.center.x]],
            y: [[model.eye.y, model.center.y]],
            z: [[model.eye.z, model.center.z]]
        }

        const update_up = {
            x: [[model.eye.x, model.eye.x + model.up.x]],
            y: [[model.eye.y, model.eye.y + model.up.y]],
            z: [[model.eye.z, model.eye.z + model.up.z]]
        }

        Plotly.restyle(plot_3rd_person_div, update_eye, 0);
        Plotly.restyle(plot_3rd_person_div, update_eyesight, 1);
        Plotly.restyle(plot_3rd_person_div, update_up, 2);
    }

    function update_plot1() {
        plot3d_scene.camera.lookAt([model.eye.x, model.eye.y, model.eye.z], [model.center.x, model.center.y, model.center.z], [model.up.x, model.up.y, model.up.z]);
    }

    //------------------------------------------------------------------------------
    function onSlided() {
        saveSliderValues();
        update_text();
        update_plot1();
        update_plot2();
    }

    function update_sliders() {
        slider_eyeX.value = model.eye.x;
        slider_eyeY.value = model.eye.y;
        slider_eyeZ.value = model.eye.z;
        slider_centerX.value = model.center.x;
        slider_centerY.value = model.center.y;
        slider_centerZ.value = model.center.z;
        slider_upX.value = model.up.x;
        slider_upY.value = model.up.y;
        slider_upZ.value = model.up.z;
    }

    function onResetCameraPressed() {
        model = {...JSON.parse(JSON.stringify(init_model))};

        update_sliders();
        update_text();
        update_plot1();
        update_plot2();
    }

    function onPlot1Interaction() {
        const cam = plot3d_scene.getCamera();
        model.eye.x = cam.eye.x;
        model.eye.y = cam.eye.y;
        model.eye.z = cam.eye.z;
        model.center.x = cam.center.x;
        model.center.y = cam.center.y;
        model.center.z = cam.center.z;
        model.up.x = cam.up.x;
        model.up.y = cam.up.y;
        model.up.z = cam.up.z;

        update_sliders();
        update_text();
        update_plot2();
    }

    let dragging = false;

    function onMouseUp() {
        dragging = false;
    }

    function onMouseDown() {
        dragging = true;
    }

    function onMouseMove() {
        if (dragging) {
            onPlot1Interaction();
        }
    }

    function onWheel() {
        onPlot1Interaction();
    }

    //------------------------------------------------------------------------------
    // Constructor code for the class.

    plot_1st_person_div.addEventListener('mousedown', onMouseDown);
    plot_1st_person_div.addEventListener('mouseup', onMouseUp);
    plot_1st_person_div.addEventListener('mousemove', onMouseMove);
    plot_1st_person_div.addEventListener('wheel', onWheel);

    document.addEventListener('input', onSlided)
    reset_btn.addEventListener('click', onResetCameraPressed);
    reset_btn.dispatchEvent(new Event('click'));
}