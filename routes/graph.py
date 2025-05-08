from flask import Blueprint, render_template, request
from services.graph_service import generate_paginated_graphs
import pandas as pd

graph_bp = Blueprint('graph_bp', __name__, url_prefix='/graph')

@graph_bp.route('/create_graph', methods=['GET'])
def create_graph():
    query = request.args.get('q', '')
    print('creating graph')
    

    page = int(request.args.get('page', 1))
    df = construct_dataframe(query)
    total_pages = (len(df) + 23) // 24
    graph_html = generate_paginated_graphs(df, page, 24)

    # Save to file for debugging
    # debug_dir = 'debug_graphs'
    # os.makedirs(debug_dir, exist_ok=True)
    # filepath = os.path.join(debug_dir, f'graph_page_{page}.html')
    # with open(filepath, 'w', encoding='utf-8') as f:
    #     f.write(graph_html)
    
    return render_template('graph_module.html',
                           query=query,
                           page=page,
                           total_pages=total_pages,
                           graph_html=graph_html)

def construct_dataframe(query):
    # Mock example
    import numpy as np
    return pd.DataFrame({
        'x': list(range(96)),
        'y': np.random.rand(96)
    })