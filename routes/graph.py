from flask import Blueprint, render_template, request
from services.graph_service import generate_paginated_graphs, save_dataframe_cache, load_cached_dataframe
from services.weather_service import construct_weather_dataframe
from services.graph_metadata import WeatherGraphMetadata
import pandas as pd

graph_bp = Blueprint('graph_bp', __name__, url_prefix='/graph')

def get_cached_df_and_metadata_or_generate(key, construct_method, metadata_cls):
    df, metadata = load_cached_dataframe(key, metadata_cls)
    if df is None:
        df, metadata = construct_method(key)
        save_dataframe_cache(key, df, metadata)
    return df, metadata 

@graph_bp.route('/weather', methods=['GET'])
def create_weather_graph():
    query = request.args.get('q', '')
    city = str.lower(' '.join(query.split(' ')[1:]))

    page = int(request.args.get('page', 1))
    metric = request.args.get('metric', 'temperature_2m')

    print('creating weather graph')

    # df, metadata = construct_weather_dataframe(city)
    df, metadata = get_cached_df_and_metadata_or_generate(city, construct_weather_dataframe, WeatherGraphMetadata)
    metadata.y_axis = metric
    total_pages = (len(df) + metadata.num_points - 1) // metadata.num_points
    graph_html = generate_paginated_graphs(df, metadata, page)

    return render_template('weather_module.html',
                           query=query,
                           page=page,
                           total_pages=total_pages,
                           metric=metric,
                           graph_html=graph_html)

def construct_dataframe(query):
    # Mock example
    import numpy as np
    return pd.DataFrame({
        'Hour': list(range(96)),
        'Temperatrue (°F)': np.random.rand(96)
    })