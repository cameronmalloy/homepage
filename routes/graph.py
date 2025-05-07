from flask import Blueprint, request, jsonify, Response
import os
import json

# Import services
from services.graph_service import create_graph, get_graph_data, create_example_graph

# Create blueprint
graph_bp = Blueprint('graph', __name__, url_prefix='/graph')

@graph_bp.route('/example')
def example():
    """Create an example graph and return its ID"""
    graph_id = create_example_graph()
    if not graph_id:
        return jsonify({"success": False, "error": "Failed to create example graph"}), 500
    
    # Just return the graph_id so the frontend can use it
    return Response(f'<div data-graph_id="{graph_id}"></div>', mimetype='text/html')

# API endpoints
@graph_bp.route('/api/create', methods=['POST'])
def api_create_graph():
    """
    API endpoint to create a graph from a dataframe
    
    Expected JSON payload:
    {
        "dataframe": [{"col1": val1, "col2": val2, ...}, {...}],
        "num_points": 24,
        "height": 400,
        "x_axis_label": "Time",
        "y_axis_label": "Temperature (°C)",
        "x_column": "timestamp",
        "y_column": "temperature",
        "titles": ["Day 1", "Day 2", "Day 3", "Day 4"],
        "line_color": "#3366cc",
        "line_width": 2,
        "point_color": "#ff9900",
        "point_size": 5
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'dataframe' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing dataframe in request'
            }), 400
            
        result = create_graph(data['dataframe'], data)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@graph_bp.route('/api/data/<graph_id>/<int:page>')
def api_get_graph_data(graph_id, page):
    """Get data for a specific page of a graph"""
    result = get_graph_data(graph_id, page)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 404