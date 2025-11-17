# 🧬 MeditronAlchemia  
### *Personalized Chemotherapy Optimization using ML + Tumor Growth Modeling*

This repository contains the full pipeline for **predicting tumor response**, **simulating tumor growth dynamics under different regimens**, and **generating optimized chemotherapy recommendations** using machine learning and based on I-SPY 2 clinical trial [[1](https://www.cancerimagingarchive.net/collection/ispy2/)].

# MisisAlchemia — Tumor Response Modeling & Treatment Optimization  
### Data preparation
- Tumor dynamics modeling 
- pCR prediction
- Regimen ranking

This notebook implements a full pipeline for **preprocessing I-SPY2 clinical data**,  **modelling tumor size dynamics**, and **predicting treatment effectiveness** using ML.

---

## Dataset

We use the public clinical trial dataset from  
**I-SPY2: “Investigation of Serial studies to Predict Your Therapeutic Response with Imaging And moLecular analysis 2”**.

Although the raw trial dataset contains **719 patients**,  
only **384 patients** had **recorded tumor size measurements**,  
so they were used in modeling.

We did **not extract tumor size directly from MRI images** due to time constraints —  
this step requires additional radiomics processing and is left for future work.

All preprocessing (SDTM merge, time intervals, weekly tumor dynamics, subtype construction)  
was performed separately.  
This notebook loads the cleaned dataset: `data/clean_data.csv` and uses columns:

- `tumor_size_week_0`  
- `tumor_size_week_4`  
- `tumor_size_week_12`  
- `tumor_size_week_24`  
- clinical factors (`ER`, `PR`, `HER2`, `menopausal status`, `age`, `race`)  
- `treatment arm  `
- pathological complete response (`pCR`)

---

## Goals of the Notebook

### 1. Compute tumor dynamics (0 $\rightarrow$ 24 weeks)  
Using the weekly trends present in the cleaned dataset, we calculate:

- relative reduction at weeks 4 / 12 / 24  
- slopes between MRI scans  
- area under the curve (AUC)

### 2. Analyze pCR rates across subtypes and treatment arms  
We compute:

```text
mean pCR
patient counts
ranking of arms by pCR
```


### 3. Visualize residual tumor size (week 24)

A heatmap is generated:

rows $\rightarrow$ breast cancer subtype

columns $\rightarrow$ treatment regimens

cell value $\rightarrow$ tumor size at week 24


### 4. Train two models:
#### (A) Logistic regression for pCR

Features:

- subtype
- treatment arm
- menopausal status
- race
- age
- HR / HER2 / MP status

Performance:
`ROC-AUC ≈ 0.756`

#### (B) Gradient Boosting Regressor – tumor size prediction

Three separate regressors predict tumor size at:

- week 4
- week 12
- week 24

> MAE and $R^2$ are printed for each model.


### 5. Treatment Recommendation System

Given a patient profile:
```python
patient = {
    "subtype": "TNBC",
    "age": 19,
    "menopausal_status": "premenopausal",
    "race": "white",
    "hr": 0,
    "her2": 0,
    "mp": 0,
}
```

we evaluate all arms available for that subtype and compute predicted probability of pCR:

```recommend_regimens(patient, df, clf)```


Output example:

arm	| p_pcr
--:|:--
paclitaxel_pembrolizumab | 0.68
paclitaxel_abt_888_carboplatin	| 0.63
paclitaxel_mk2206	| 0.50

A visualization of top regimens is provided (horizontal bar ranking).


### 6. Tumor Trajectory Simulation

We combine regression models + baseline tumor size
to produce predicted tumor volume curves:

```python
traj_df = predict_tumor_trajectory_for_patient(...)
plot_tumor_trajectories(traj_df)
```

The output is a smooth trajectory for each regimen:

- week 0

- week 3 (pred)

- week 6 (pred)

- week 18 (pred ≈ pre-surgical)

Visualization uses a modern pastel color scheme with shading.


### Contents of This Notebook
#### Data loading and inspection
```python
df = pd.read_csv("../data/clean_data.csv")
```

__pCR__
- pivot table
- ranking
- count statistics

__Mean tumor shrinkage curves__
- subtype × arm
- 0, 4, 12, 24 weeks

__Heatmap visualization__

- Custom colormap
- Styled axes, colorbar, layout

__Machine Learning__
- Logistic Regression (classification)
- HistGradientBoostingClassifier (hyperparameter search)
- GradientBoostingRegressor (tumor size prediction)

__Personalized Treatment Recommendation__

- ranked regimens
- probability of complete response
- interactive plotting

__Tumor Trajectory Forecast__
- ML-driven predicted tumor size
- visualization for top-K regimens



### Future Work

- Integrate MRI-derived radiomics for direct tumor quantification
- Build a full PK/PD-based tumor regression model
- Add Bayesian optimization to choose ideal regimens
- Deploy interactive version via Streamlit or FastAPI
- Include confidence intervals for trajectory predictions

## References

[1] Li, W., Newitt, D. C., Gibbs, J., Wilmes, L. J., Jones, E. F., Arasu, V. A., Strand, F., Onishi, N., Nguyen, A. A.-T., Kornak, J., Joe, B. N., Price, E. R., Ojeda-Fournier, H., Eghtedari, M., Zamora, K. W., Woodard, S. A., Umphrey, H., Bernreuter, W., Nelson, M., … Hylton, N. M. (2022). I-SPY 2 Breast Dynamic Contrast Enhanced MRI Trial (ISPY2)  (Version 1) [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/TCIA.D8Z0-9T85

[2] National Cancer Institute. Pathologic complete response. NCI Dictionary of Cancer Terms.
Available at: https://www.cancer.gov/publications/dictionaries/cancer-terms/def/pathologic-complete-response 
Accessed: 17 November 2025.