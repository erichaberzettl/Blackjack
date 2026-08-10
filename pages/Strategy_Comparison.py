import streamlit as st
import backend.strategies as strats
from backend.strategy_comparison import run_comparison

st.set_page_config("Strategy Comparison", "🂡", layout="wide")
st.title("Blackjack Simulator")
st.header("Strategy Comparison")

st.markdown("Playing Blackjack is all about winning and making money. There are many strategies to use, but how do they perform side by side?" \
" Here you can compare two strategies to find out if there is a significant difference in performance (average return).")

with st.form(key="comparison_input", border=True, enter_to_submit=True):
    
    st.markdown("#### Configuration options")
    col1, col2 = st.columns(2)
    strategies = strats.STRATEGY_NAMES_LIST
    with col1:
        st.selectbox("Select first strategy", options=strategies, key="strat_1")
        st.checkbox("Insurance", help="Player pays insurance (50% of the bet) when the dealer has an ace and gets payed 1:1 on it if the dealer gets a Blackjack.", key="pay_insurance_1")

    with col2:
        st.selectbox("Select second strategy", options=strategies, key="strat_2")
        st.checkbox("Insurance", help="Player pays insurance (50% of the bet) when the dealer has an ace and gets payed 1:1 on it if the dealer gets a Blackjack.", key="pay_insurance_2")

    submitted = st.form_submit_button("Compare")

    if submitted:

        results = run_comparison(strategy_1=st.session_state.strat_1, 
                                strategy_2=st.session_state.strat_2,
                                pay_insurance_1=st.session_state.pay_insurance_1,
                                pay_insurance_2=st.session_state.pay_insurance_2)

        strat_1_string = st.session_state.strat_1 + (" (Insurance)" if st.session_state.pay_insurance_1 else "")
        strat_2_string = st.session_state.strat_2 + (" (Insurance)" if st.session_state.pay_insurance_2 else "")
        st.markdown("### Hypotheses")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Null hypothesis")
            st.latex(r"H_0: \mu_1 = \mu_2")

        with col2:
            st.markdown("##### Alternative hypothesis")
            st.latex(r"H_1: \mu_1 \neq \mu_2")

        st.markdown(r"Where $\mu_1$ and $\mu_2$ are the average returns of strategy 1 and 2.")        

        
        st.markdown("### Parameters")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"##### {strat_1_string}")
            st.write(f"- Sample mean: ${results["mean_1"]:.4f}$")
            st.write(f"- Sample variance: ${results["var_1"]:.4f}$")
        

        with col2:
            st.markdown(f"##### {strat_2_string}")
            st.write(f"- Sample mean: ${results["mean_2"]:.4f}$")
            st.write(f"- Sample variance: ${results["var_2"]:.4f}$")

        st.metric("Sample size", results["n"])
        st.metric("Estimated effect size (Cohen's d)", f"{results["estimated_d"]:.4f}")

        if results["mean_1"] > results["mean_2"]:
            winner_strat = strat_1_string
            loser_strat = strat_2_string
        else:
            winner_strat = strat_2_string
            loser_strat = strat_1_string

        st.markdown("### Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("P-value", f"{results["p_value"]:.4f}")
            st.metric("T-statistic", f"{results["t_stat"]:.4f}")

        with col2:
            st.metric("95%-Confidence Interval", f"[{results['conf_interval'][0]:.4f};{results['conf_interval'][1]:.4f}]")
            st.metric("Effect size (Cohen's d)", f"{results["d"]:.4f}")
        
        pvalue_percent = round(results['p_value'], 4) * 100
        if results["p_value"] <= 0.05:
            st.markdown(f"At a significance level of $α = 0.05$ the null hypothesis can be rejected."  \
                        f"The p-value tells us that only {pvalue_percent}% of samples would " \
                        f" have this or a more extreme result if we believe the null hypothesis (equal performance of the strategies)." \
                        f" {winner_strat} is a better performing strategy than {loser_strat}."  \
                        f" The test results show that the higher return of {winner_strat} is significant and unlikely to be explained by chance.")
        else:
            st.markdown("At a significance level of $α = 0.05$ the null hypothesis can't be rejected." \
            f" Neither strategy is performing better than the other.")

        st.markdown(f"*Control values: The test was also run using the scipy library. Values under 'Results' should match the following: " \
                    f"p-value: {results['scipy_pvalue']:.4f}, t-statistic: {results['scipy_tstat']:.4f}*")

st.markdown("#### About the test")
st.markdown("The comparison of strategies works based on a [Welch t-test](https://en.wikipedia.org/wiki/Welch%27s_t-test), manually implemented without a library. " \
" The advantage of this specific test is that it does not require equal variances of the Blackjack strategies." \
" Additionally, a Power test is performed beforehand together with an estimated effect size for the selected strategies " \
"to calculate a meaningful sample size. The maximum sample size is capped at 101010 Blackjack rounds for performance reasons. In case this happens, the power of the test would decrease to under 80%. ")

st.markdown("##### Test assumptions")
st.markdown("**1. Normality of population means:**")
st.markdown("- the average return of a strategy must approximitely follow a normal distribution")
st.markdown("- the test is run on thousands of hands. We can assume a normal distribution following the Central Limit Theorem")
st.markdown("- with 30 or less hands per strategy the assumption might not be fulfilled")
st.markdown("**2. Independence of observations:**")
st.markdown("- each Blackjack hand must be independent from the others") 
st.markdown("- independence is given between strategies since strategy is simulated separately") 
st.markdown("- within a strategy's simulation, the shoe is played until 80% penetration before reshuffling")
st.markdown("- consecutive hands drawn from the same shoe are therefore not strictly independent")
st.markdown("- this violates the independence assumption of the t-test in a strict sense")
st.markdown("- in practice, the effect is expected to be small: autocorrelation between individual hands is weak, " \
            "and with thousands of hands per strategy the sample mean is still well-approximated by the CLT")

st.markdown("##### Test procedure")

st.markdown("""
0. Pilot simulation run of 30k hands for each strategy with and without insurance to capture a first mean and variance estimate (one-time calculation).
1. For the selected strategies, calculate a first estimate of the effect size (Cohen's d) using the pilot metrics.
2. With the estimate from 1, a Power test is performed to know the minimum required number of samples n (Blackjack hands) 
to correctly identify a significant performance difference 80% of the times.
3. Both strategies are simulated in  independent games of n rounds.
4. The resulting data is then used for the Welch test that calculates the p-value and other statistical metrics
""")

