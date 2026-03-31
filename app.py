import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from segmentation import generate_sample_data, run_segmentation, get_segment_summary
from ai_insights import get_segment_insight, generate_campaign_email

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Customer Segmentation",
    page_icon="📊",
    layout="wide",
)

st.title("🧠 AI-Powered Customer Segmentation & Marketing Insights Dashboard")
st.caption("End-to-end ML pipeline: data → clustering → visualization → AI insights → exportable report")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    n_clusters = st.slider("Number of segments", min_value=2, max_value=8, value=5)
    n_customers = st.slider("Sample customers", min_value=100, max_value=1000, value=300, step=50)
    st.divider()
    st.markdown("**Pipeline**")
    st.markdown(
        "1. Generate sample customer data\n"
        "2. Feature engineering\n"
        "3. K-Means clustering (ML)\n"
        "4. LLM-powered marketing insights\n"
        "5. Export results as CSV"
    )

# ── Run segmentation ──────────────────────────────────────────────────────────
if st.button("🚀 Run Segmentation", type="primary", use_container_width=True):
    with st.spinner("Running ML segmentation..."):
        df = generate_sample_data(n_customers)
        df = run_segmentation(df, n_clusters)
        st.session_state["df"] = df
        st.session_state["summary"] = get_segment_summary(df)
        st.session_state["n_clusters"] = n_clusters
    st.success(f"✅ Segmented {n_customers} customers into {n_clusters} groups!")

if "df" not in st.session_state:
    st.info("👆 Click **Run Segmentation** to get started.")
    st.stop()

df       = st.session_state["df"]
summary  = st.session_state["summary"]
chosen_k = st.session_state.get("n_clusters", 5)
colors   = ["#7F77DD", "#1D9E75", "#D85A30", "#378ADD", "#BA7517", "#D4537E", "#639922", "#888780"]

# ── KPI Metric Cards ──────────────────────────────────────────────────────────
st.subheader("📈 Key Metrics")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Customers",   len(df))
k2.metric("Avg Spend",         f"${df['total_spend'].mean():.0f}")
k3.metric("Avg Order Value",   f"${df['avg_order_value'].mean():.0f}")
k4.metric("Avg Frequency",     f"{df['purchase_frequency'].mean():.1f}x/yr")
k5.metric("Segments",          chosen_k)

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Customer Segments",
    "📊 Visualizations",
    "🎯 Marketing Strategy",
    "🤖 AI Insights",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Customer Segments
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Customer Segmentation Results")

    # Segment metric cards
    cols = st.columns(len(summary))
    for i, (_, row) in enumerate(summary.iterrows()):
        with cols[i]:
            st.metric(
                label=row["segment_label"],
                value=f"{int(row['count'])} customers",
                delta=f"${row['avg_spend']:.0f} avg spend",
            )

    st.divider()

    # Full data table
    st.markdown("**Full customer dataset with segment labels**")
    st.dataframe(
        df.style.format({
            "total_spend":              "${:.0f}",
            "avg_order_value":          "${:.0f}",
            "purchase_frequency":       "{:.0f}",
            "days_since_last_purchase": "{:.0f} days",
        }),
        use_container_width=True,
    )

    # ── Download button ───────────────────────────────────────────────────
    st.divider()
    st.subheader("⬇️ Download Segmentation Report")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Segmentation Report (CSV)",
        data=csv,
        file_name="customer_segments.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.caption(
        "The CSV includes: customer_id, total_spend, purchase_frequency, "
        "avg_order_value, days_since_last_purchase, segment, segment_label"
    )

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Visualizations
# ════════════════════════════════════════════════════════════════════════════
with tab2:

    # Elbow method
    st.subheader("📐 Elbow Method — Choosing the Right K")
    st.caption(
        "K vs. Inertia chart justifies the number of clusters chosen. "
        "The elbow point is where adding more clusters stops giving significant benefit."
    )

    features = df[["total_spend", "purchase_frequency", "avg_order_value", "days_since_last_purchase"]]
    X = StandardScaler().fit_transform(features.fillna(0))
    inertia_values = []
    k_range = list(range(1, 10))
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X)
        inertia_values.append(km.inertia_)

    fig_elbow = go.Figure()
    fig_elbow.add_trace(go.Scatter(
        x=k_range, y=inertia_values,
        mode="lines+markers",
        marker=dict(size=8, color="#7F77DD"),
        line=dict(color="#7F77DD", width=2),
    ))
    fig_elbow.add_vline(
        x=chosen_k, line_dash="dash", line_color="#D85A30",
        annotation_text=f"  Selected K={chosen_k}",
        annotation_position="top right",
    )
    fig_elbow.update_layout(
        title="K vs. Inertia (Elbow Method)",
        xaxis_title="Number of Clusters (K)",
        yaxis_title="Inertia",
        height=350, margin=dict(t=50, b=40),
    )
    st.plotly_chart(fig_elbow, use_container_width=True)

    st.divider()

    # Segment distribution bar chart
    st.subheader("📊 Segment Distribution")
    fig_dist = px.bar(
        summary,
        x="segment_label",
        y="count",
        color="segment_label",
        title="Number of customers per segment",
        color_discrete_sequence=colors,
        labels={"count": "Customers", "segment_label": "Segment"},
        text="count",
    )
    fig_dist.update_traces(textposition="outside")
    fig_dist.update_layout(showlegend=False, margin=dict(t=50, b=0))
    st.plotly_chart(fig_dist, use_container_width=True)

    st.divider()

    # Cluster scatter plots
    st.subheader("🗺️ Cluster Visualisation")
    st.caption("Each dot is a customer. Colour = segment. Bubble size = average order value.")

    col1, col2 = st.columns(2)
    with col1:
        fig_s1 = px.scatter(
            df, x="total_spend", y="purchase_frequency",
            color="segment_label", size="avg_order_value",
            hover_data=["customer_id", "days_since_last_purchase"],
            title="Spend vs. Purchase frequency",
            color_discrete_sequence=colors,
            labels={"total_spend": "Total spend ($)",
                    "purchase_frequency": "Purchase frequency",
                    "segment_label": "Segment"},
        )
        fig_s1.update_layout(margin=dict(t=50, b=0), height=400)
        st.plotly_chart(fig_s1, use_container_width=True)

    with col2:
        fig_s2 = px.scatter(
            df, x="days_since_last_purchase", y="avg_order_value",
            color="segment_label", size="total_spend",
            hover_data=["customer_id", "purchase_frequency"],
            title="Recency vs. Order value",
            color_discrete_sequence=colors,
            labels={"days_since_last_purchase": "Days since last purchase",
                    "avg_order_value": "Avg order value ($)",
                    "segment_label": "Segment"},
        )
        fig_s2.update_layout(margin=dict(t=50, b=0), height=400)
        st.plotly_chart(fig_s2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig_pie = px.pie(
            summary, names="segment_label", values="count",
            title="Customer distribution by segment",
            color_discrete_sequence=colors, hole=0.35,
        )
        fig_pie.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col4:
        fig_bar = px.bar(
            summary, x="segment_label", y="avg_spend",
            color="segment_label",
            title="Average total spend per segment",
            color_discrete_sequence=colors,
            labels={"avg_spend": "Avg spend ($)", "segment_label": "Segment"},
        )
        fig_bar.update_layout(showlegend=False, margin=dict(t=40, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Marketing Strategy
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🎯 Marketing Strategy per Segment")
    st.caption("Actionable strategies mapped to each customer segment.")

    strategy_map = {
        "Champions": ("High spend + high frequency",  "Loyalty rewards, early access, VIP perks",         "Retention"),
        "Loyal":     ("Moderate-high spend, regular", "Personalised email offers, upsell campaigns",       "Upsell"),
        "Potential": ("Average spend, growing",        "Onboarding nudges, first-repeat-purchase offers",  "Nurture"),
        "At Risk":   ("Declining activity",            "Win-back campaigns, limited-time discounts",        "Re-engage"),
        "Lost":      ("Long inactive, low spend",      "Aggressive discounts, survey to understand churn", "Recovery"),
    }

    rows = []
    for seg_label in summary["segment_label"].tolist():
        matched = next(
            (k for k in strategy_map if k.lower() in seg_label.lower() or seg_label.lower() in k.lower()),
            None
        )
        info = strategy_map.get(matched or seg_label, ("Mixed profile", "A/B test multiple approaches", "Test"))
        r = summary[summary["segment_label"] == seg_label].iloc[0]
        rows.append({
            "Segment":       seg_label,
            "Description":   info[0],
            "Strategy":      info[1],
            "Goal":          info[2],
            "Customers":     int(r["count"]),
            "Avg Spend ($)": f"${r['avg_spend']:.0f}",
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — AI Insights
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("🤖 AI Marketing Insights")
    st.caption("Select a segment to generate a personalised marketing analysis and campaign email.")

    selected_segment = st.selectbox(
        "Choose a segment to analyse",
        options=summary["segment_label"].tolist(),
    )
    row = summary[summary["segment_label"] == selected_segment].iloc[0]

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("💡 Get Segment Insights", use_container_width=True):
            with st.spinner("Generating insights..."):
                insight = get_segment_insight(
                    segment_name=selected_segment,
                    avg_spend=row["avg_spend"],
                    avg_frequency=row["avg_frequency"],
                    count=int(row["count"]),
                    avg_recency=row["avg_recency"],
                )
            st.session_state["insight"] = insight

    with col_b:
        if st.button("✉️ Generate Campaign Email", use_container_width=True):
            with st.spinner("Writing campaign email..."):
                email = generate_campaign_email(
                    segment_name=selected_segment,
                    avg_spend=row["avg_spend"],
                    avg_frequency=row["avg_frequency"],
                )
            st.session_state["email"] = email

    if "insight" in st.session_state:
        st.info(st.session_state["insight"])

    if "email" in st.session_state:
        st.subheader("Generated Email")
        st.text_area("Email body (copy and use)", st.session_state["email"], height=220)
