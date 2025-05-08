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