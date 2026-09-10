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
    "Screening is an early-stage decision-support exercise. It is not a substitute "
    "for an Environmental Impact Assessment, Initial Environmental Examination, "
    "engineering design, hydrological study, health assessment, or regulatory review."
)

# These are application-level rules, not Pakistani legal thresholds.
SECTOR_PRIORITIES = {
    "Agriculture": ["drought", "heat", "flood", "water availability", "crop resilience"],
    "Energy": ["heat", "water availability", "flood", "grid resilience", "cooling demand"],
    "Health": ["heat", "vector disease", "water-borne disease", "air quality", "health readiness"],
    "Transportation": ["flood", "extreme heat", "landslide", "asset resilience", "disruption"],
    "Water": ["drought", "flood", "water quality", "demand", "catchment resilience"],
}
