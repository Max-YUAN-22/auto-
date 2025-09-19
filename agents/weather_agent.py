# agents/weather_agent.py
from core.base_agent import BaseAgent

class WeatherAgent(BaseAgent):
    def __init__(self, dsl_instance):
        super().__init__(dsl_instance, 'weather', ['trigger_weather_alert', 'activate_drainage_system', 'respond_to_autonomous_driving'])

    def trigger_weather_alert(self, alert):
        """
        Triggers actions based on a weather alert.
        """
        alert_type = alert.get('alert_type', 'unknown')
        area = alert.get('area', 'unknown area')
        severity = alert.get('severity', 5)
        
        result = f"Weather Monitor: Weather alert triggered - {alert_type} in {area} with severity {severity}. Monitoring conditions and activating response systems."
        print(result)
        return result

    def activate_drainage_system(self, area):
        """
        Activates the drainage system.
        """
        print(f"Activating drainage system in {area}.")

    def respond_to_autonomous_driving(self, data):
        """
        Responds to autonomous driving requests by providing weather conditions.
        """
        start_location = data.get('start_location', 'Unknown')
        end_location = data.get('end_location', 'Unknown')
        
        result = f"Weather Monitor: Providing weather conditions for autonomous driving route from {start_location} to {end_location}. Current conditions are favorable for autonomous operation."
        print(result)
        return result
