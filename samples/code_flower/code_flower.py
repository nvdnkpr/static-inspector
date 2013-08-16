# -*- coding: utf-8 -*-
import json
import os
import sys

from inspector.analyzer.project_analyzer import LocCounter
from inspector.models.base import Project


if __name__ == '__main__':
    if len(sys.argv) < 2:
        project_dir = str(raw_input('Please enter project path: '))
    else:
        project_dir = sys.argv[1]

    hnd = LocCounter()
    p = Project(project_dir)
    p.ignored_dirs = ['.git', 'bin', '.settings', '.idea']
    p.rescan_files(hnd)

    params = {
        'width': 750,
        'height': 500,
        'data': json.dumps(hnd.get_data()),
    }
    html = """<html>
    <head>
        <script type="text/javascript" src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
        <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/d3/3.2.2/d3.min.js"></script>
        <script type="text/javascript" src="http://redotheweb.com/CodeFlower/javascripts/CodeFlower.js"></script>
        <style>
            circle.node {
                cursor: pointer;
                stroke: #000000;
                stroke-width: 0.5px;
            }
            circle.node.directory {
                stroke: #9ECAE1;
                stroke-width: 2px;
            }
            circle.node.collapsed {
                stroke: #555555;
            }
            .nodetext {
                fill: #252929;
                font-weight: bold;
                text-shadow: 0 0 0.2em white;
            }
            line.link {
                fill: none;
                stroke: #9ECAE1;
                stroke-width: 1.5px;
            }
            #graph svg > rect {
                fill: #EEE !important;
            }
        </style>
    </head>
    <body>
        <div style="margin: 5%% auto 0; width:%(width)dpx" id="graph"></div>
        <script type="text/javascript">
            var codeChart;
            $(function() {
                codeChart = new CodeFlower('#graph', %(width)d, %(height)d);
                codeChart.update(%(data)s);
            });
        </script>
    </body>
</html>
    """ % params

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'report.html'), 'w') as f:
        f.write(html)
