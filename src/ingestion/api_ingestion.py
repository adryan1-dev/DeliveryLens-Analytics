import requests
import src.config.settings as cs


def run_ingestion():
   response = requests.get(
       cs.API_URL,
       timeout=cs.API_TIMEOUT
   )
   
   response.raise_for_status()
   
   return response.json()