import pandas as pd
import re

# Load your data
# Replace 'your_file.csv' with the path to your actual file
df = pd.read_csv('erdwärmesonden_potential.csv')

# Define a function to extract the first set of coordinates for POINTs or POLYGONs
def extract_coordinates(shape_str):
    # Find all numbers (including decimals) in the string
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", shape_str)
    # Convert numbers to floats and pair them (assuming longitude comes first, then latitude)
    coordinates = list(map(float, numbers))
    # For POINT, just return the first pair. For POLYGON, return the first pair found (assuming it's representative)
    return coordinates[:2] if coordinates else [None, None]

# Apply the function to each row in the 'SHAPE' column and create new columns for latitude and longitude
df[['Longitude', 'Latitude']] = df['SHAPE'].apply(lambda x: pd.Series(extract_coordinates(x)))

# Display the modified DataFrame
print(df.head())