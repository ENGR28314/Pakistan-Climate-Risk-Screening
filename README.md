# 🌍 EcoScreen Pakistan
## AI-Powered Climate Risk Screening for Development Planning and Decision-Support

EcoScreen Pakistan is a Streamlit prototype for early-stage climate-risk screening and development decision support in Pakistan.

It brings together a single interface for:

- Climate and disaster risk screening
- Precipitation and temperature scenario simulations
- Climate and Health Risk Index (CHRI) project-level proxy
- Climate Change Knowledge Portal (CCKP)-informed workflow
- Seasonal forecast context
- GHG accounting
- Illustrative shadow price of carbon
- Climate co-benefits
- Climate indicators
- Sector-specific in-depth screening
- Agriculture, Energy, Health, Transportation and Water assessments
- Interactive simulation graphs
- AI-assisted screening summaries

## Important scope

This project is a **prototype decision-support application**. It does not reproduce official World Bank methodologies, does not provide official CCKP forecasts, does not calculate the official CHRI, and does not replace EIA/IEE, engineering, hydrological, health, disaster-risk, or regulatory assessments.

The simulation graphs use transparent illustrative formulas. Replace them with validated datasets and documented methodologies before using the application for a real project.

## Reference resources

The World Bank Climate Change Knowledge Portal (CCKP) provides historical and projected climate information and country/subnational resources. Pakistan has a dedicated CCKP country area and climate-risk profile.

- CCKP: https://climateknowledgeportal.worldbank.org/
- Pakistan CCKP resources: https://climateknowledgeportal.worldbank.org/country/pakistan/resources
- Pakistan climate trends and projections: https://climateknowledgeportal.worldbank.org/country/pakistan/trends-variability-projections
- CCKP extreme precipitation: https://climateknowledgeportal.worldbank.org/country/pakistan/extremes
- CCKP CHRI: https://climateknowledgeportal.worldbank.org/global/chri
- World Bank Climate & Disaster Risk Screening resources: https://climateknowledgeportal.worldbank.org/climate-change-development
- CCKP guidance note: https://climateknowledgeportal.worldbank.org/guidance-note

## Project structure

```text
ai-climate-risk-screening-pakistan/
│
├── app.py
├── workflow.py
├── environmental_rules.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload all project files.
3. Open Streamlit Community Cloud.
4. Create a new app.
5. Select your GitHub repository.
6. Select `app.py` as the main file.
7. Deploy.

No API key is required for the current prototype because the AI summary is deterministic/template-based.

## Future AI integration

A production version can connect `workflow.py` to an LLM provider. Keep the API key in Streamlit Secrets and never commit it to GitHub.

Example:

```toml
GROQ_API_KEY = "your-key"
```

## Recommended production upgrades

### Climate data
Replace simulation functions with validated sources such as:
- CCKP datasets/API where available
- Pakistan Meteorological Department data where authorized/available
- ERA5
- CHIRPS
- CMIP6 projections
- verified national datasets

### Seasonal forecasts
Use an authoritative forecast provider and store:
- issue date
- forecast period
- probability categories
- variable
- geographic coverage
- source/version

### GHG accounting
Implement a documented methodology and source-specific emission factors. Keep Scope 1, Scope 2 and relevant Scope 3 calculations separate.

### Shadow carbon price
Do not hard-code a universal carbon price. Allow the user to select a documented methodology/scenario and preserve the source, year, currency, unit and assumptions.

### CHRI
If official CHRI data are used, display the source and date. Do not label a project-level formula as the official CHRI.

### In-depth sector tools
Each sector should eventually have its own validated:
- hazard indicators
- exposure variables
- vulnerability variables
- adaptation measures
- economic assumptions
- uncertainty treatment
- data provenance

## Suggested production architecture

```text
User
  ↓
Streamlit UI
  ↓
Input validation
  ↓
Climate / hazard data layer
  ↓
Risk calculation engine
  ↓
Sector assessment engine
  ↓
GHG + carbon + co-benefit modules
  ↓
AI explanation layer
  ↓
Charts + dashboard + report
```

## License

Choose an appropriate open-source license before publishing. MIT is suitable for many educational prototypes, but verify that all third-party datasets and code used by a production version permit your intended use.

## Disclaimer

This software is provided for research, education and early-stage decision support. Climate risk is location-, asset-, sector- and time-specific. Results should be independently reviewed by qualified professionals before being used for investment, engineering, environmental approval, public-health planning or regulatory decisions.
