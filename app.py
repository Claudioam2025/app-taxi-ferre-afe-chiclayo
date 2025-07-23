
import streamlit as st
import pandas as pd
from datetime import datetime
from geopy.distance import geodesic

st.set_page_config(page_title="Taxi Ferreñafe - Chiclayo", layout="centered")

st.title("🚖 Servicio de Taxi Compartido: Ferreñafe - Chiclayo")

st.sidebar.header("📋 Registro de Usuario")
name = st.sidebar.text_input("Nombre completo")
origin = st.sidebar.selectbox("Punto de recojo", ["Ferreñafe", "Chiclayo", "Reque", "Picsi", "Lambayeque"])
destination = st.sidebar.selectbox("Destino", ["Ferreñafe", "Chiclayo", "Reque", "Picsi", "Lambayeque"])
register = st.sidebar.button("Solicitar Taxi")

# Simulador de ubicación (coordenadas ficticias)
locations = {
    "Ferreñafe": (-6.636, -79.793),
    "Chiclayo": (-6.763, -79.836),
    "Reque": (-6.875, -79.839),
    "Picsi": (-6.698, -79.855),
    "Lambayeque": (-6.704, -79.906)
}

# Registro de pasajeros
if "passengers" not in st.session_state:
    st.session_state.passengers = []

if register and name:
    passenger = {
        "Nombre": name,
        "Origen": origin,
        "Destino": destination,
        "Hora": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.passengers.append(passenger)
    st.success(f"✅ Solicitud registrada para {name}")

# Mostrar usuarios registrados
st.subheader("🧑‍🤝‍🧑 Pasajeros Solicitando Viaje")
if st.session_state.passengers:
    df = pd.DataFrame(st.session_state.passengers)
    st.dataframe(df)

    # Agrupar en vehículos de 4
    st.subheader("🚗 Agrupación por Vehículo")
    vehicle_groups = [st.session_state.passengers[i:i + 4] for i in range(0, len(st.session_state.passengers), 4)]
    for i, group in enumerate(vehicle_groups):
        st.markdown(f"**Vehículo {i + 1}**")
        for p in group:
            st.markdown(f"- {p['Nombre']} desde {p['Origen']} hacia {p['Destino']}")

        # Calcular distancia total estimada
        total_distance = 0
        points = [locations[p['Origen']] for p in group] + [locations[group[0]['Destino']]]
        for i in range(len(points) - 1):
            total_distance += geodesic(points[i], points[i+1]).km
        st.markdown(f"📏 Distancia estimada: `{total_distance:.2f} km`")
else:
    st.info("No hay pasajeros registrados todavía.")
