import pandas as pd
from dataclasses import dataclass, asdict

@dataclass
class GraphMetadata:
    title: str = ""
    x_axis: str = ""
    y_axis: str = ""
    num_points: int = 10
    show_x_grid: bool = True
    show_y_grid: bool = True
    name: str = ""  # legend name
    line_color: str = "orange"
    font_family: str = "Courier New, monospace"
    font_size: int = 14
    title_font_size: int = 24
    background_color: str = "white"

    def __init__(self, title="", x_axis="", y_axis="", num_points=10, show_x_grid=True, show_y_grid=True,
                 name="", line_color="orange", font_family="Courier New, monospace", font_size=14,
                 title_font_size=24, background_color="white"):   
        self.title = title 
        self.x_axis = x_axis 
        self.y_axis = y_axis 
        self.num_points = num_points 
        self.show_x_grid = show_x_grid 
        self.show_y_grid = show_y_grid 
        self.line_color = line_color 
        self.font_family = font_family
        self.font_size = font_size
        self.title_font_size = title_font_size
        self.background_color = background_color
        if name:
            self.name = name
        else:
            self.name = self.title

    def to_dict(self):
        return asdict(self) 
    
    @classmethod 
    def from_dict(cls, data):
        # Enforce required fields; raise if missing 
        return cls(
            title = data['title'],
            x_axis = data['x_axis'],
            y_axis = data['y_axis'],
            num_points = data['num_points']
        )

    def layout_config(self):
        return {
            "autosize": True,
            "height": 400,
            "margin": dict(l=40, r=40, t=60, b=40),
            "plot_bgcolor": self.background_color,
            "paper_bgcolor": self.background_color,
            "font": dict(
                family=self.font_family,
                size=self.font_size,
                color="black"
            ),
            "title": dict(
                text=self.title,
                font=dict(size=self.title_font_size),
                x=0,
                xanchor='left'
            ),
            "xaxis": dict(
                title=self.get_x_axis_title(),
                showgrid=self.show_x_grid,
                gridcolor="lightgray",
                tickfont=dict(family=self.font_family)
            ),
            "yaxis": dict(
                title=self.get_y_axis_title(),
                showgrid=self.show_y_grid,
                gridcolor="lightgray",
                tickfont=dict(family=self.font_family)
            ),
            "legend": self.get_legend(),
            "margin": self.get_margin()
        }
    
    def get_x_axis_title(self):
        return self.x_axis
    
    def get_y_axis_title(self):
        return self.y_axis
    
    def format_title(self, df):
        return self.title

    def format_x_labels(self, df):
        return None

    def format_y_labels(self, df):
        return None

    def get_legend(self):
        return dict(
            orientation='h',
            y=1.15,
            x=0,
            xanchor='left',
        )

    def get_margin(self):
        return dict(t=80, l=50, r=50, b=50)
    
    def get_name(self):
        return self.name 

    def get_line_color(self):
        return self.line_color

class WeatherGraphMetadata(GraphMetadata):

    weather_code_map = {
        0: "Clear", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
        45: "Fog", 48: "Freezing Fog", 51: "Drizzle (Light)", 53: "Drizzle (Moderate)",
        55: "Drizzle (Dense)", 61: "Rain (Light)", 63: "Rain (Moderate)",
        65: "Rain (Heavy)", 80: "Rain Showers", 95: "Thunderstorm"
    }

    title_map = {
        "temperature_2m": "Temperature (°C)",
        "apparent_temperature": "Feels Like (°C)",
        "relative_humidity_2m": "Relative Humidity (%)",
        "precipitation": "Precipitation (mm)"
    }

    color_map = {
        "temperature_2m": "orange",
        "apparent_temperature": "darkorange",
        "relative_humidity_2m": "red",
        "precipitation": "blue"
    }

    def get_y_axis_title(self):
        return None

    def format_title(self, df):
        date_time = pd.to_datetime(df['time'].iloc[0]).strftime('%A, %B %d')
        title = f'{date_time} | {self.title}'
        print(title)
        return title

    def format_x_labels(self, df, interval=3):
        df = df.copy()
        df['time'] = pd.to_datetime(df['time'])
        df['weather_condition'] = df['weathercode'].map(WeatherGraphMetadata.weather_code_map)
        return [
            f"{row['time'].strftime('%H:%M')}<br>{row['weather_condition']}" if i % interval == 0 else ""
            for i, row in df.iterrows()
        ]

    def get_name(self):
        return WeatherGraphMetadata.title_map.get(self.y_axis, 'Unknown')
    
    def get_line_color(self):
        return WeatherGraphMetadata.color_map.get(self.y_axis, 'orange')