import os
import json
import uuid
import math
from datetime import datetime, timedelta
import random

# Path to store graph data
GRAPH_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'graphs')

def ensure_data_directory():
    """Ensure the graph data directory exists"""
    os.makedirs(GRAPH_DATA_DIR, exist_ok=True)

def create_graph(dataframe, config):
    """
    Create a new graph from dataframe data
    
    Args:
        dataframe: List of dictionaries with data points
        config: Dictionary with graph configuration
        
    Returns:
        Dictionary with success status and graph_id
    """
    try:
        ensure_data_directory()
        
        # Generate unique ID for the graph
        graph_id = str(uuid.uuid4())
        
        # Extract parameters from config
        num_points = config.get('num_points', 24)
        x_column = config.get('x_column', 'x')
        y_column = config.get('y_column', 'y')
        titles = config.get('titles', ['Data'])
        
        # Validate required fields
        if x_column not in dataframe[0] or y_column not in dataframe[0]:
            return {
                'success': False,
                'error': f'Missing required columns: {x_column} or {y_column}'
            }
            
        # Prepare data for paging
        total_points = len(dataframe)
        total_pages = (total_points + num_points - 1) // num_points  # Ceiling division
        
        # Create pages
        pages = []
        for i in range(total_pages):
            start = i * num_points
            end = min(start + num_points, total_points)
            page_data = []
            
            for j in range(start, end):
                point = dataframe[j]
                page_data.append({
                    'x': point[x_column],
                    'y': point[y_column],
                    'label': f"{point[x_column]}: {point[y_column]}"
                })
                
            # Determine title for this page
            if i < len(titles):
                title = titles[i]
            else:
                title = f"Page {i+1}"
                
            pages.append({
                'title': title,
                'data': page_data
            })
        
        # Save graph data
        graph_data = {
            'created_at': datetime.now().isoformat(),
            'total_pages': total_pages,
            'pages': pages,
            'config': {
                'height': config.get('height', 400),
                'x_axis_label': config.get('x_axis_label', 'X Axis'),
                'y_axis_label': config.get('y_axis_label', 'Y Axis'),
                'line_color': config.get('line_color', '#3366cc'),
                'line_width': config.get('line_width', 2),
                'point_color': config.get('point_color', '#ff9900'),
                'point_size': config.get('point_size', 5)
            }
        }
        
        # Save to file
        graph_file = os.path.join(GRAPH_DATA_DIR, f'{graph_id}.json')
        with open(graph_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
            
        return {
            'success': True,
            'graph_id': graph_id,
            'total_pages': total_pages
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_graph_data(graph_id, page):
    """
    Get data for a specific page of a graph
    
    Args:
        graph_id: ID of the graph
        page: Page number (1-based)
        
    Returns:
        Dictionary with graph data for the specified page
    """
    try:
        ensure_data_directory()
        
        # Validate page number
        if page < 1:
            return {
                'success': False,
                'error': 'Page number must be greater than 0'
            }
            
        # Load graph data
        graph_file = os.path.join(GRAPH_DATA_DIR, f'{graph_id}.json')
        if not os.path.exists(graph_file):
            return {
                'success': False,
                'error': 'Graph not found'
            }
            
        with open(graph_file, 'r') as f:
            graph_data = json.load(f)
            
        # Check if page is valid
        if page > graph_data['total_pages']:
            return {
                'success': False,
                'error': f'Page number {page} exceeds total pages {graph_data["total_pages"]}'
            }
            
        # Get page data (adjust for 0-based index)
        page_data = graph_data['pages'][page - 1]
        
        return {
            'success': True,
            'total_pages': graph_data['total_pages'],
            'title': page_data['title'],
            'data': page_data['data'],
            'x_axis_label': graph_data['config']['x_axis_label'],
            'y_axis_label': graph_data['config']['y_axis_label'],
            'config': graph_data['config']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def create_example_graph():
    """
    Create an example graph with sample data
    
    Returns:
        Graph ID or None on failure
    """
    try:
        # Generate sample temperature data for 4 days
        dataframe = []
        start_date = datetime.now() - timedelta(days=4)
        
        for day in range(4):
            for hour in range(24):
                current_time = start_date + timedelta(days=day, hours=hour)
                timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Generate temperature with some randomness and daily cycle
                base_temp = 20 + 5 * math.sin(hour / 24 * 2 * math.pi)
                temperature = round(base_temp + random.uniform(-2, 2), 1)
                
                dataframe.append({
                    'timestamp': timestamp,
                    'temperature': temperature,
                    'day': day + 1
                })
        
        # Create graph configuration
        config = {
            'dataframe': dataframe,
            'num_points': 24,  # One day per page
            'height': 400,
            'x_axis_label': 'Time',
            'y_axis_label': 'Temperature (°C)',
            'x_column': 'timestamp',
            'y_column': 'temperature',
            'titles': ['Day 1', 'Day 2', 'Day 3', 'Day 4'],
            'line_color': '#3366cc',
            'line_width': 2,
            'point_color': '#ff9900',
            'point_size': 5
        }
        
        # Create the graph
        result = create_graph(dataframe, config)
        
        if result['success']:
            return result['graph_id']
        else:
            print(f"Error creating example graph: {result['error']}")
            return None
            
    except Exception as e:
        print(f"Exception creating example graph: {str(e)}")
        return None