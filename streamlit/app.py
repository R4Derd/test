import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
import folium
from streamlit_folium import st_folium
from datetime import datetime, timezone
import pandas as pd
from io import StringIO


def refresh_map():
    """Refreshes all app data"""

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Create API client for gcs bucket
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = storage.Client(credentials=credentials)

    m = folium.Map(location=[53.799, -1.549], tiles="Stamen Terrain", zoom_start=11.5)

    def read_file(bucket_name, file_path):
        """Get bucket content"""

        bucket = client.bucket(bucket_name)
        content = bucket.blob(file_path).download_as_string().decode("utf-8")
        return content

    def get_df_from_bucket():
        """csv to dataframe"""

        bucket_name = "bus-tracking-376121-bus_data"
        file_path = "late_buses.csv"

        data = read_file(bucket_name, file_path)
        df = pd.read_csv(StringIO(data))

        return df

    def create_marker(
        lat, long, route, stop_name, vehicle, scheduled_time, actual_time
    ):
        """Add a circle marker to the map"""

        marker = folium.Circle(
            location=[lat, long],
            tooltip=f"<b>Route: {route} </b><br>Stop: {stop_name} <br>Vehicle: {vehicle} <br>Scheduled : {scheduled_time} <br>Actual : {actual_time}",
            radius=100,
            color="crimson",
            fill=True,
        ).add_to(m)

        return marker