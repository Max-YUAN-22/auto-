from core.base_agent import BaseAgent

class TrafficMonitorAgent(BaseAgent):
    def __init__(self, dsl_instance):
        super().__init__(
            dsl_instance=dsl_instance,
            role="Traffic Coordinator",
            capabilities=["monitor_traffic", "adjust_signal", "analyze_autonomous_driving_request", "respond_to_weather_alert", "respond_to_parking_update", "respond_to_safety_inspection"]
        )

    def monitor_traffic(self, data):
        """
        Monitors traffic flow and adjusts signals during congestion.
        """
        print(f"Monitoring traffic at {data['location']} with speed {data['speed']} km/h")
        if data['speed'] < 20:  # Assuming speed < 20 km/h is congestion
            self.adjust_signal(data['location'])

    def adjust_signal(self, location):
        """
        Adjusts the traffic signal.
        """
        print(f"Adjusting traffic signal at {location} to handle congestion.")

    def analyze_autonomous_driving_request(self, data):
        """
        Analyzes autonomous driving requests and optimizes routes.
        """
        start_location = data.get('start_location', 'Unknown')
        end_location = data.get('end_location', 'Unknown')
        passengers = data.get('passengers', 1)
        
        result = f"Traffic Manager: Analyzing route from {start_location} to {end_location} for {passengers} passengers. Route optimization complete."
        print(result)
        return result

    def respond_to_weather_alert(self, data):
        """
        Responds to weather alerts by adjusting traffic management.
        """
        alert_type = data.get('alert_type', 'unknown')
        location = data.get('location', 'unknown area')
        
        result = f"Traffic Manager: Responding to {alert_type} weather alert in {location}. Adjusting traffic signals and route recommendations."
        print(result)
        return result

    def respond_to_parking_update(self, data):
        """
        Responds to parking updates by adjusting traffic flow.
        """
        location = data.get('location', 'unknown location')
        available_spots = data.get('available_spots', 0)
        
        result = f"Traffic Manager: Parking update received for {location} with {available_spots} available spots. Adjusting traffic flow accordingly."
        print(result)
        return result

    def respond_to_safety_inspection(self, data):
        """
        Responds to safety inspection results by adjusting traffic management.
        """
        location = data.get('location', 'unknown location')
        safety_status = data.get('safety_status', 'unknown')
        
        result = f"Traffic Manager: Safety inspection result for {location} shows {safety_status} status. Adjusting traffic management protocols."
        print(result)
        return result
