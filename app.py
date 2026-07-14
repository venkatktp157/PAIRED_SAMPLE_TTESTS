import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats

# Set page configuration (Must be the very first Streamlit command)
st.set_page_config(page_title="T-Test Calculator", layout="wide")

st.title("📊 Interactive T-Test Statistical Calculator")
st.markdown("""
Upload your dataset (CSV or Excel) to perform either an **Independent Samples T-Test** or a **Paired Samples T-Test**. Configure your parameters in the sidebar.
""")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("1. Configure Test Parameters")

# Test Type Toggle
test_type = st.sidebar.radio(
    "Select T-Test Type:",
    ("Independent Samples T-Test", "Paired Samples T-Test"),
    help="Independent: Compares means of two unique groups.\nPaired: Compares means from the same group at different times."
)

# Error Rate (Alpha)
alpha = st.sidebar.slider(
    "Significance Level (α):",
    min_value=0.01, max_value=0.10, value=0.05, step=0.01,
    help="Probability of rejecting the null hypothesis when it is true."
)

# Alternative Hypothesis (Tails)
tail_type = st.sidebar.selectbox(
    "Alternative Hypothesis (Tail Type):",
    options=["Two-Tailed", "Greater (One-Tailed)", "Less (One-Tailed)"],
    index=0
)

# --- FILE UPLOADER ---
st.sidebar.header("2. Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read file safely based on extension
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.subheader("📋 Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)
        
        # --- COLUMN SELECTION ---
        st.sidebar.header("3. Select Variables")
        columns = df.columns.tolist()
        
        col1_name = st.sidebar.selectbox("Select Sample 1 / Variable 1:", columns, index=0)
        col2_name = st.sidebar.selectbox("Select Sample 2 / Variable 2:", columns, index=min(1, len(columns)-1))
        
        sample1 = df[col1_name].dropna().astype(float)
        sample2 = df[col2_name].dropna().astype(float)
        
        n1 = len(sample1)
        n2 = len(sample2)
        
        # --- VALIDATION & COMPUTATION ---
        proceed = True
        if test_type == "Paired Samples T-Test" and n1 != n2:
            st.error(f"❌ **Error:** Paired t-test requires both samples to have the same size. Currently, Sample 1 has {n1} rows and Sample 2 has {n2} rows after dropping missing values.")
            proceed = False
            
        if proceed:
            st.divider()
            st.header(f"📈 Results: {test_type}")
            
            # Descriptive Statistics Table
            stats_data = {
                "Metric": ["Sample Size (N)", "Mean (μ)", "Std Deviation (σ)", "Std Error of Mean"],
                col1_name: [n1, np.mean(sample1), np.std(sample1, ddof=1), stats.sem(sample1)],
                col2_name: [n2, np.mean(sample2), np.std(sample2, ddof=1), stats.sem(sample2)]
            }
            desc_df = pd.DataFrame(stats_data).set_index("Metric")
            
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                st.subheader("Descriptive Statistics")
                st.table(desc_df)
            
            # --- T-TEST CALCULATIONS ---
            alt_mapping = {
                "Two-Tailed": "two-sided",
                "Greater (One-Tailed)": "greater",
                "Less (One-Tailed)": "less"
            }
            scipy_alt = alt_mapping[tail_type]
            
            if test_type == "Independent Samples T-Test":
                levene_stat, levene_p = stats.levene(sample1, sample2)
                equal_var = True if levene_p > 0.05 else False
                
                t_stat, p_val = stats.ttest_ind(sample1, sample2, alternative=scipy_alt, equal_var=equal_var)
                
                if equal_var:
                    df_val = n1 + n2 - 2
                else:
                    v1 = np.var(sample1, ddof=1) / n1
                    v2 = np.var(sample2, ddof=1) / n2
                    df_val = ((v1 + v2) ** 2) / ((v1 ** 2) / (n1 - 1) + (v2 ** 2) / (n2 - 1))
                
                test_info = f"Equal Variances Assumed: {equal_var} (Levene's p = {levene_p:.4f})"
                
            else:  # Paired T-Test
                t_stat, p_val = stats.ttest_rel(sample1, sample2, alternative=scipy_alt)
                df_val = n1 - 1
                test_info = "Paired Observations Model"

            # --- CRITICAL VALUE CALCULATION ---
            if tail_type == "Two-Tailed":
                crit_val = stats.t.ppf(1 - alpha/2, df_val)
                crit_string = f"± {crit_val:.4f}"
                is_significant = p_val < alpha
            elif tail_type == "Greater (One-Tailed)":
                crit_val = stats.t.ppf(1 - alpha, df_val)
                crit_string = f"> {crit_val:.4f}"
                is_significant = (p_val < alpha) and (t_stat > 0)
            else:  # Less
                crit_val = stats.t.ppf(alpha, df_val)
                crit_string = f"< {crit_val:.4f}"
                is_significant = (p_val < alpha) and (t_stat < 0)

            # --- INFERENCE BLOCK ---
            inference = "🚨 **REJECT the Null Hypothesis (H₀)**. There is a statistically significant difference between the means." if is_significant else "✅ **FAIL TO REJECT the Null Hypothesis (H₀)**. There is no statistically significant difference between the means."
            
            with col_right:
                st.subheader("Test Metrics")
                metrics_df = pd.DataFrame({
                    "Statistical Measure": ["Test Statistic (t)", "Degrees of Freedom (df)", "P-Value", f"Critical Value (at α={alpha})"],
                    "Value": [f"{t_stat:.4f}", f"{df_val:.2f}", f"{p_val:.5f}", crit_string]
                }).set_index("Statistical Measure")
                st.table(metrics_df)
            
            # Final Summary Output Box
            st.subheader("💡 Statistical Inference")
            if is_significant:
                st.success(inference)
            else:
                st.info(inference)
                
            # --- FIXED DYNAMIC CONTEXT BLOCK ---
            # Using clean Markdown strings to completely sidestep frontend text formatting crashes
            if tail_type == "Two-Tailed":
                h0_str = "**Null Hypothesis ($H_0$):** $\mu_1 = \mu_2$ (The true means are equal)"
                ha_str = r"**Alternative Hypothesis ($H_a$):** $\mu_1 \neq \mu_2$ (The true means are not equal)"
            elif tail_type == "Greater (One-Tailed)":
                h0_str = "**Null Hypothesis ($H_0$):** $\mu_1 \le \mu_2$ (Mean of Sample 1 is $\le$ Sample 2)"
                ha_str = "**Alternative Hypothesis ($H_a$):** $\mu_1 > \mu_2$ (Mean of Sample 1 is strictly greater)"
            else:
                h0_str = "**Null Hypothesis ($H_0$):** $\mu_1 \ge \mu_2$ (Mean of Sample 1 is $\ge$ Sample 2)"
                ha_str = "**Alternative Hypothesis ($H_a$):** $\mu_1 < \mu_2$ (Mean of Sample 1 is strictly less)"
            
            with st.expander("🔬 View Context & Assumptions applied"):
                st.markdown(f"- **Test Context:** {test_info}")
                st.markdown(f"- {h0_str}")
                st.markdown(f"- {ha_str}")
                st.markdown(f"- **Decision Rule:** Reject $H_0$ if P-Value < {alpha}")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("👋 Welcome! Please upload a `.csv` or `.xlsx` file using the sidebar to begin your analysis.")