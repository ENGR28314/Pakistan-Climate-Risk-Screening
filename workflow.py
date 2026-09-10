import numpy as np
import pandas as pd

RISK_ACTIONS = {
    "Low": ["Continue routine climate screening.", "Document assumptions and monitor key indicators."],
    "Moderate": ["Add climate-resilient design measures.", "Conduct targeted site and hazard assessment."],
    "High": ["Undertake a detailed climate risk and adaptation assessment.", "Quantify critical failure modes and adaptation costs.", "Engage relevant technical specialists."],
    "Critical": ["Do not rely on screening alone.", "Commission a project-specific climate/disaster risk assessment.", "Review project design, siting, alternatives and residual risk before proceeding."],
}

def run_screening(sector, hazard, exposure, vulnerability, adaptive_capacity, sensitivity, criticality):
    hazard_pressure = {
        "Flood": 1.00, "Extreme heat": 0.95, "Drought": 0.90,
        "Extreme precipitation": 0.95, "Landslide": 0.85,
        "Storm": 0.80, "Wildfire": 0.70, "Sea-level rise": 0.90
    }.get(hazard, 0.80)
    score = (
        0.22 * exposure +
        0.20 * vulnerability +
        0.18 * sensitivity +
        0.16 * criticality +
        0.16 * (100 - adaptive_capacity) +
        0.08 * (hazard_pressure * 100)
    )
    score = float(np.clip(score, 0, 100))
    if score < 25:
        band = "Low"
    elif score < 50:
        band = "Moderate"
    elif score < 75:
        band = "High"
    else:
        band = "Critical"
    return {
        "risk_score": score,
        "risk_band": band,
        "sector": sector,
        "hazard": hazard,
        "actions": RISK_ACTIONS[band],
    }

def generate_simulation_data(years, baseline_rain, baseline_temp, scenario):
    years = int(years)
    multipliers = {"Low change": 0.35, "Moderate change": 0.70, "High change": 1.10}
    m = multipliers[scenario]
    t = np.arange(1, years + 1)
    temperature = baseline_temp + (0.025 * m) * t + 0.15 * np.sin(t / 2)
    precipitation = baseline_rain * (1 + 0.003 * m * t + 0.08 * np.sin(t / 2.8))
    return pd.DataFrame({
        "Year": t,
        "Temperature_C": np.round(temperature, 2),
        "Precipitation_mm": np.round(precipitation, 1),
    })

def calculate_ghg(electricity_mwh, fuel_l, travel_km, ef_elec, ef_fuel, ef_travel):
    electricity = electricity_mwh * ef_elec
    fuel = fuel_l * ef_fuel / 1000
    travel = travel_km * ef_travel / 1000
    return {
        "total_tco2e": electricity + fuel + travel,
        "breakdown": [
            {"Source": "Electricity", "tCO2e": electricity},
            {"Source": "Liquid fuel", "tCO2e": fuel},
            {"Source": "Vehicle travel", "tCO2e": travel},
        ],
    }

def calculate_shadow_carbon_price(annual_tco2e, years, price_usd_per_tco2e):
    return float(annual_tco2e * years * price_usd_per_tco2e)

def calculate_climate_cobenefit(mitigation, adaptation, social):
    return float(0.40 * mitigation + 0.40 * adaptation + 0.20 * social)

def build_ai_summary(project_name, sector, province, screening):
    if not screening:
        return "Run the climate risk screening first."
    return f"""
### AI Screening Summary

**Project:** {project_name}  
**Sector:** {sector}  
**Location:** {province}  
**Screening risk:** **{screening['risk_band']} ({screening['risk_score']:.1f}/100)**  
**Primary hazard:** {screening['hazard']}

#### Recommended next steps
{chr(10).join("- " + a for a in screening["actions"])}

> This is an automated screening summary based on user-provided inputs. It should be reviewed by qualified professionals and supported with verified site-specific climate, hazard, engineering, environmental and socioeconomic data.
"""
