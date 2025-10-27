import requests
import json
from datetime import datetime, timedelta, timezone

def get_weather_data(lat, lng, start_time, end_time):
    # This is a mocked response. In a real scenario, we would make an API call to Stormglass.io
    # and would need a valid API key. This function now generates data for the next 5 days dynamically.
    hours_data = []
    for i in range(5):
        current_time = start_time + timedelta(days=i)
        hour_data = {
            "time": current_time.isoformat(),
            "seaSurfaceTemperature": {"sg": 28.5 + (i * 0.5)},
            "windSpeed": {"sg": 15.0 + (i * 5.0)},
            "airPressure": {"sg": 1005.0 - (i * 3.0)},
            "humidity": {"sg": 85.0 + (i * 2.0)},
            "precipitation": {"sg": 2.5 + (i * 2.5)}
        }
        hours_data.append(hour_data)

    mock_response = {"hours": hours_data}
    return mock_response

def calculate_cyclone_risk(data):
    # This is a simplified risk calculation. A real model would be much more complex.
    score = 0

    for hour in data['hours']:
        # Sea surface temperature > 26.5 C is favorable for cyclone formation
        if hour['seaSurfaceTemperature']['sg'] > 26.5:
            score += 10

        # Wind speed > 17 m/s (34 knots) is a tropical storm
        if hour['windSpeed']['sg'] > 17:
            score += 10
        if hour['windSpeed']['sg'] > 33: # Category 1 hurricane
            score += 10

        # Low pressure is a key indicator
        if hour['airPressure']['sg'] < 1000:
            score += 10
        if hour['airPressure']['sg'] < 980:
            score += 10

        # High humidity
        if hour['humidity']['sg'] > 80:
            score += 5

        # High rainfall rate
        if hour['precipitation']['sg'] > 5:
            score += 5

    return min(100, score) # Cap the score at 100

if __name__ == '__main__':
    # Tamil Nadu coastal region
    lat_start, lat_end = 8, 13
    lon_start, lon_end = 76, 80

    # Next 5 days
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(days=5)

    # For simplicity, we'll use the center of the region
    lat = (lat_start + lat_end) / 2
    lng = (lon_start + lon_end) / 2

    weather_data = get_weather_data(lat, lng, start_time, end_time)

    if weather_data:
        risk_score = calculate_cyclone_risk(weather_data)

        # Determine risk level and other parameters based on score
        if risk_score > 75:
            risk_level = "High"
            intensity = "Severe Cyclone"
            landfall_prediction = "Yes"
            expected_landfall_location = "Nagapattinam District"
            expected_landfall_time = "36 hours"
            summary = "High rotational cloud pattern with low-pressure zone detected over Bay of Bengal; cyclone likely to hit Tamil Nadu coast."
        elif risk_score > 40:
            risk_level = "Moderate"
            intensity = "Cyclone"
            landfall_prediction = "Yes"
            expected_landfall_location = "Cuddalore District"
            expected_landfall_time = "48 hours"
            summary = "Developing cloud patterns and falling pressure indicate a potential cyclone formation."
        else:
            risk_level = "Low"
            intensity = "Tropical Depression"
            landfall_prediction = "No"
            expected_landfall_location = "N/A"
            expected_landfall_time = "N/A"
            summary = "Weather conditions are not favorable for cyclone formation at this time."

        output = {
            "region": "Tamil Nadu",
            "cyclone_probability": risk_score,
            "risk_level": risk_level,
            "intensity": intensity,
            "landfall_prediction": landfall_prediction,
            "expected_landfall_location": expected_landfall_location,
            "expected_landfall_time": expected_landfall_time,
            "summary": summary
        }

        print(json.dumps(output, indent=2))
