// COMP 665 dashboard — week-page viewer (no external dependencies).
// Tabs carry data-kind (report | image | video | interactive | file) and
// data-src; the report panel is prerendered in the page.

(function () {
    'use strict';

    var reportPanel = document.getElementById('report-panel');
    var mediaPanel = document.getElementById('media-panel');
    var viewerLabel = document.getElementById('viewer-label');

    function show(btn) {
        document.querySelectorAll('.tab-item').forEach(function (b) {
            b.classList.toggle('active', b === btn);
        });

        if (btn.dataset.kind === 'report') {
            reportPanel.style.display = 'block';
            mediaPanel.style.display = 'none';
            viewerLabel.textContent = '';
            return;
        }

        reportPanel.style.display = 'none';
        mediaPanel.style.display = 'flex';
        mediaPanel.textContent = '';

        var el;
        if (btn.dataset.kind === 'image') {
            el = document.createElement('img');
            el.className = 'viewer-media';
            el.src = btn.dataset.src;
            el.alt = btn.textContent;
        } else if (btn.dataset.kind === 'video') {
            el = document.createElement('video');
            el.className = 'viewer-media';
            el.src = btn.dataset.src;
            el.controls = true;
        } else if (btn.dataset.kind === 'interactive') {
            el = document.createElement('iframe');
            el.className = 'viewer-media viewer-iframe';
            el.src = btn.dataset.src;
        } else {
            el = document.createElement('a');
            el.className = 'viewer-link';
            el.href = btn.dataset.src;
            el.textContent = 'Download ' + btn.textContent;
        }
        mediaPanel.appendChild(el);
        viewerLabel.textContent = btn.textContent;
    }

    document.querySelectorAll('.tab-item').forEach(function (btn) {
        btn.addEventListener('click', function () { show(btn); });
    });

    var first = document.querySelector('.tab-item');
    if (first) { show(first); }
}());
