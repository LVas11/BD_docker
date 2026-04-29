import requests
import json
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

console = Console()


def load_weather_codes():
    """ Load weather code descriptions from a local JSON file. """
    try:
        with open("weather_codes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_weather_data(city):
    """ Fetch geocoding and weather data for a given city. """

    # Getting the geocoding data to find latitude and longitude
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_res = requests.get(geo_url).json()
    if not geo_res.get("results"): return None
    
    loc = geo_res["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]

    # Getting the hourly data for the 24 hour forecast chart
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m"
    data = requests.get(weather_url).json()
    
    return loc, data


def generate_chart(hourly_data, city_name):

    """ Generate a line chart for the 24-hour temperature forecast. """

    # Getting raw data
    raw_times = hourly_data["time"][:24]
    temps = hourly_data["temperature_2m"][:24]
    
    # Formatting time ISO strings into hours for graph
    formatted_times = [datetime.fromisoformat(t).strftime("%H:%M") for t in raw_times]
    
    plt.figure(figsize=(10, 5))
    plt.plot(formatted_times, temps, color='tab:blue', marker='o', markersize=4)
    
    plt.xticks(formatted_times[::3], rotation=45) # Show every 3rd hour on x-axis
    
    plt.title(f"24-Hour Temperature Forecast: {city_name}")
    plt.xlabel("Time of Day")
    plt.ylabel("Temperature (°C)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    # Creating unique name for the chart file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"forecast_{city_name}_{timestamp}.png"


    plt.savefig(filename)
    console.print(f"[green]Forecasting chart saved as {filename}[/green]")
    plt.close()    


def main():
    codes = load_weather_codes()
    
    while True:
        console.print(Panel("[bold blue]Global Weather Tool[/bold blue]\nType 'exit' to quit", expand=False))
        city = console.input("[bold green]Enter City: [/bold green]").strip()

        if city.lower() == 'exit': break

        result = get_weather_data(city)
        if result:
            loc, data = result
            current = data["current_weather"]
            
            table = Table(title=f"Current Weather: {loc['name']}")
            table.add_column("Attribute")
            table.add_column("Value")
            table.add_row("Condition", codes.get(str(current["weathercode"]), "Unknown"))
            table.add_row("Temperature", f"{current['temperature']}°C")
            table.add_row("Wind Speed", f"{current['windspeed']} km/h")
            console.print(table)

            generate_chart(data["hourly"], loc["name"])
        else:
            console.print("[red]City not found.[/red]")

if __name__ == "__main__":
    main()