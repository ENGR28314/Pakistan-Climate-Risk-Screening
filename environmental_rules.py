SECTORS = [
    "Agriculture",
    "Energy",
    "Health",
    "Transportation",
    "Water",
    "Urban Development",
    "Industry",
    "Buildings",
    "Other",
]

HAZARDS = [
    "Flood",
    "Extreme heat",
    "Drought",
    "Extreme precipitation",
    "Landslide",
    "Storm",
    "Wildfire",
    "Sea-level rise",
]

RISK_BANDS = ["Low", "Moderate", "High", "Critical"]

SCREENING_DISCLAIMER = (
    "This screening is an early-stage decision-support exercise. Use the results "
    "to identify issues that may need further investigation. It does not replace "
    "an Environmental Impact Assessment (EIA), Initial Environmental Examination "
    "(IEE), engineering design, hydrological study, health assessment, disaster-risk "
    "assessment, or regulatory review."
)

# These are application-level rules, not Pakistani legal thresholds.
SECTOR_PRIORITIES = {
    "Agriculture": ["drought", "heat", "flood", "water availability", "crop resilience"],
    "Energy": ["heat", "water availability", "flood", "grid resilience", "cooling demand"],
    "Health": ["heat", "vector disease", "water-borne disease", "air quality", "health readiness"],
    "Transportation": ["flood", "extreme heat", "landslide", "asset resilience", "disruption"],
    "Water": ["drought", "flood", "water quality", "demand", "catchment resilience"],
}
