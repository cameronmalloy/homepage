import pandas as pd
from dataclasses import dataclass, asdict

@dataclass
class GraphMetadata:
    title: str 
    x_axis: str 
    y_axis: str 
    num_points: int 

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
    
    def format_title(self, df):
        return self.title

    def format_x_labels(self, df):
        return None

    def format_y_labels(self, df):
        return None
    

class WeatherGraphMetadata(GraphMetadata):

    weather_code_map = {
        0: "Clear", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
        45: "Fog", 48: "Freezing Fog", 51: "Drizzle (Light)", 53: "Drizzle (Moderate)",
        55: "Drizzle (Dense)", 61: "Rain (Light)", 63: "Rain (Moderate)",
        65: "Rain (Heavy)", 80: "Rain Showers", 95: "Thunderstorm"
    }

    def format_title(self, df):
        date_time = pd.to_datetime(df['time'].iloc[0]).strftime('%A, %B %d')
        title = f'{date_time} | {self.title}'
        return title

    def format_x_labels(self, df, interval=3):
        df = df.copy()
        df['time'] = pd.to_datetime(df['time'])
        df['weather_condition'] = df['weathercode'].map(WeatherGraphMetadata.weather_code_map)
        return [
            f"{row['time'].strftime('%H:%M')}<br>{row['weather_condition']}" if i % interval == 0 else ""
            for i, row in df.iterrows()
        ]
