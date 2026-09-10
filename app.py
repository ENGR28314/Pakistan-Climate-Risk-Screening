import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from workflow import (
    run_screening,
    generate_simulation_data,
    build_ai_summary,
    calculate_ghg,
    calculate_shadow_carbon_price,
    calculate_climate_cobenefit,
)
from environmental_rules import SECTORS, HAZARDS, RISK_BANDS, SCREENING_DISCLAIMER

st.set_page_config(
    page_title="EcoScreen Pakistan | Climate Risk Decision Support",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 EcoScreen Pakistan")
st.subheader("AI-Powered Climate Risk Screening for Development Planning & Decision-Support")
st.caption("Early-stage analytical screening tool — not a regulatory approval, EIA/IEE, engineering design, or site-specific climate forecast.")

with st.sidebar:
    st.header("Project profile")
    project_name = st.text_input("Project name", "Demo Development Project")
    sector = st.selectbox("Sector", SECTORS)
    province = st.selectbox(
        "Province / territory",
        ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan",
         "Islamabad Capital Territory", "Gilgit-Baltistan", "Azad Jammu & Kashmir"]
    )
    project_life = st.slider("Project life (years)", 5, 50, 25)
    capital_cost = st.number_input("Capital cost (USD)", min_value=0.0, value=10_000_000.0, step=500_000.0)
    st.divider()
    st.info("For real projects, replace the simulation inputs with verified project, hazard, climate, and emissions data.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Screening", "🌧 Climate Indicators", "🩺 CHRI",
    "🌱 GHG & Carbon", "🤝 Co-benefits", "🏗 In-depth Tools", "📄 Report"
])

with tab1:
    st.header("Climate & Disaster Risk Screening")
    col1, col2 = st.columns(2)
    with col1:
        exposure = st.slider("Project exposure", 0, 100, 60)
        vulnerability = st.slider("Project vulnerability", 0, 100, 55)
        adaptive_capacity = st.slider("Adaptive capacity", 0, 100, 50)
    with col2:
        hazard = st.selectbox("Primary hazard", HAZARDS)
        sensitivity = st.slider("Sensitivity", 0, 100, 55)
        criticality = st.slider("Asset / service criticality", 0, 100, 60)

    if st.button("Run climate risk screening", type="primary"):
        result = run_screening(
            sector=sector,
            hazard=hazard,
            exposure=exposure,
            vulnerability=vulnerability,
            adaptive_capacity=adaptive_capacity,
            sensitivity=sensitivity,
            criticality=criticality,
        )
        st.session_state["screening"] = result

    if "screening" in st.session_state:
        r = st.session_state["screening"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Risk score", f"{r['risk_score']:.1f}/100")
        c2.metric("Risk band", r["risk_band"])
        c3.metric("Exposure", f"{exposure}/100")
        c4.metric("Adaptive capacity", f"{adaptive_capacity}/100")

        st.progress(min(r["risk_score"] / 100, 1.0))
        st.write("**Priority actions**")
        for item in r["actions"]:
            st.write(f"- {item}")

        with st.expander("ℹ️ Screening scope & limitations", expanded=False):
            st.info(SCREENING_DISCLAIMER)

with tab2:
    st.header("Climate Indicators & Simulation")
    st.write("The charts below are scenario simulations for demonstration and decision-support prototyping. They are not official forecasts.")
    years = st.slider("Projection horizon", 5, 30, 20)
    baseline_rain = st.number_input("Baseline annual precipitation (mm)", 100.0, 3000.0, 500.0)
    baseline_temp = st.number_input("Baseline mean temperature (°C)", 5.0, 40.0, 24.0)
    scenario = st.selectbox("Illustrative scenario", ["Low change", "Moderate change", "High change"])
    df = generate_simulation_data(years, baseline_rain, baseline_temp, scenario)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(df, x="Year", y="Temperature_C", title="Simulated mean temperature")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.line(df, x="Year", y="Precipitation_mm", title="Simulated annual precipitation")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)

with tab3:
    st.header("Climate & Health Risk Index (CHRI) — project screening proxy")
    st.caption("The official World Bank CHRI is a country/subnational analytical index. This application uses a transparent project-level proxy for demonstration and does not reproduce the official CHRI methodology.")
    heat = st.slider("Climate hazard pressure", 0, 100, 60)
    vuln = st.slider("Population vulnerability", 0, 100, 55)
    readiness = st.slider("Health-system readiness", 0, 100, 50)
    chri = 0.40 * heat + 0.35 * vuln + 0.25 * (100 - readiness)
    st.metric("Illustrative project CHRI proxy", f"{chri:.1f}/100")
    chri_df = pd.DataFrame({
        "Component": ["Climate hazard", "Population vulnerability", "Health-system readiness gap"],
        "Score": [heat, vuln, 100 - readiness],
    })
    st.plotly_chart(px.bar(chri_df, x="Component", y="Score", title="CHRI proxy components"), use_container_width=True)

with tab4:
    st.header("GHG Accounting & Shadow Price of Carbon")
    st.write("Use activity data and emission factors appropriate to the project and reporting standard.")
    electricity_mwh = st.number_input("Electricity use (MWh/year)", 0.0, value=5000.0)
    fuel_l = st.number_input("Liquid fuel (litres/year)", 0.0, value=100000.0)
    travel_km = st.number_input("Vehicle travel (km/year)", 0.0, value=500000.0)
    ef_elec = st.number_input("Electricity EF (tCO₂e/MWh)", 0.0, value=0.45)
    ef_fuel = st.number_input("Fuel EF (kgCO₂e/litre)", 0.0, value=2.68)
    ef_travel = st.number_input("Travel EF (kgCO₂e/km)", 0.0, value=0.18)

    ghg = calculate_ghg(electricity_mwh, fuel_l, travel_km, ef_elec, ef_fuel, ef_travel)
    st.metric("Estimated annual GHG emissions", f"{ghg['total_tco2e']:,.1f} tCO₂e/year")
    st.dataframe(pd.DataFrame(ghg["breakdown"]), use_container_width=True)

    carbon_price = st.number_input("Illustrative shadow carbon price (USD/tCO₂e)", 0.0, value=50.0)
    carbon = calculate_shadow_carbon_price(ghg["total_tco2e"], project_life, carbon_price)
    st.metric("Undiscounted lifetime carbon cost", f"${carbon:,.0f}")

with tab5:
    st.header("Climate Co-benefits")
    mitigation = st.slider("Mitigation contribution", 0, 100, 50)
    adaptation = st.slider("Adaptation contribution", 0, 100, 60)
    social = st.slider("Social / development co-benefits", 0, 100, 55)
    score = calculate_climate_cobenefit(mitigation, adaptation, social)
    st.metric("Illustrative co-benefit score", f"{score:.1f}/100")
    cb = pd.DataFrame({
        "Dimension": ["Mitigation", "Adaptation", "Social / development"],
        "Score": [mitigation, adaptation, social],
    })
    st.plotly_chart(px.bar(cb, x="Dimension", y="Score", title="Climate co-benefit profile"), use_container_width=True)

with tab6:
    st.header("Sector In-depth Screening Assessments")
    selected = st.selectbox("Select assessment", [
        "Agriculture In-depth Screening Assessment",
        "Energy In-depth Screening Assessment",
        "Health In-depth Screening Assessment",
        "Transportation In-depth Screening Assessment",
        "Water In-depth Screening Assessment",
    ])
    intensity = st.slider("Climate stress intensity", 0, 100, 60)
    resilience = st.slider("Existing resilience", 0, 100, 45)
    sim = generate_simulation_data(20, 500, 24, "Moderate change")
    sim["Risk_Index"] = np.clip(
        intensity + np.linspace(0, 20, len(sim)) - resilience * 0.4, 0, 100
    )
    st.plotly_chart(
        px.line(sim, x="Year", y="Risk_Index", title=f"{selected}: simulated climate stress trajectory"),
        use_container_width=True,
    )
    st.write("**Assessment focus**")
    focus = {
        "Agriculture In-depth Screening Assessment": ["Heat stress", "Rainfall variability", "Drought", "Flooding", "Water availability", "Crop/livestock resilience"],
        "Energy In-depth Screening Assessment": ["Heat impacts", "Hydropower/water availability", "Flooding", "Grid resilience", "Cooling demand"],
        "Health In-depth Screening Assessment": ["Heat-health", "Vector-borne disease", "Water-borne disease", "Air quality", "Health-system readiness"],
        "Transportation In-depth Screening Assessment": ["Flooding", "Extreme heat", "Landslides", "Road/bridge resilience", "Supply-chain disruption"],
        "Water In-depth Screening Assessment": ["Drought", "Flooding", "Water quality", "Demand pressure", "Catchment resilience"],
    }[selected]
    for x in focus:
        st.write(f"- {x}")

with tab7:
    st.header("AI Decision-Support Summary")
    if st.button("Generate screening summary"):
        context = st.session_state.get("screening", {})
        summary = build_ai_summary(project_name, sector, province, context)
        st.markdown(summary)
    st.divider()
    st.download_button(
        "Download screening inputs as CSV",
        data=pd.DataFrame([{
            "project_name": project_name,
            "sector": sector,
            "province": province,
            "project_life_years": project_life,
            "capital_cost_usd": capital_cost,
        }]).to_csv(index=False),
        file_name="project_screening_inputs.csv",
        mime="text/csv",
    )

st.divider()
st.caption("EcoScreen Pakistan is a prototype decision-support application. Validate all findings with qualified climate, environmental, engineering, health, and regulatory specialists before using them for real investment or compliance decisions.")
