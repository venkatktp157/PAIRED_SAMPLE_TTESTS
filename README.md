# 📊 Interactive T-Test Statistical Calculator

An intuitive, production-ready Streamlit web application designed to perform **Independent Samples T-Tests** and **Paired Samples T-Tests**. Upload your datasets in CSV or Excel format, dynamically adjust your parameters, and receive instant, publication-ready statistical breakdowns and interpretations.

---

## 🚀 Features

* **Flexible T-Test Modes:** Easily toggle between Independent (Two-Sample) and Paired (Dependent) T-Tests.
* **Smart Variance Detection:** For Independent T-Tests, the app runs a *Levene's Test* under the hood to evaluate equal variances. It automatically falls back to **Welch's T-Test** if variances are unequal.
* **Custom Hypotheses:** Supports both Two-Tailed and One-Tailed (Greater/Less) directional tests.
* **Dynamic Significance:** Adjust your alpha level ($\alpha$) on the fly between `0.01` and `0.10`.
* **Robust Statistics:** Outputs sample sizes, sample means, standard deviations, standard errors, exact degrees of freedom ($df$), $t$-statistics, critical values, and precise $p$-values.
* **Automated Data Cleaning:** Automatically detects and isolates missing values (NaNs) to ensure mathematical accuracy.

---

## 🛠️ Project Architecture & Requirements

To keep this project clean and deployable, three structural components work together:
1. `app.py`: The core python file containing the Streamlit layout and SciPy execution logic.
2. `requirements.txt`: Specifies the external Python packages required to run the environment.
3. `.gitignore`: Protects your repository by instructing Git to ignore local virtual environments and temporary system logs.

---

## 📦 Installation & Local Setup

Follow these steps to get the application running on your local machine.

### 1. Clone or Download the Project
Ensure you have `app.py`, `requirements.txt`, and `.gitignore` inside your root directory.

### 2. Create and Activate a Virtual Environment
It is highly recommended to isolate your dependencies using a virtual environment:

```bash
# Create the environment
python -m venv .venv

# Activate it (Mac/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate