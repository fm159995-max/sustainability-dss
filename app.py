import streamlit as st
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة لتكون بعرض الشاشة بالكامل (Wide Mode)
st.set_page_config(page_title="Supply Chain Sustainability DSS", page_icon="🌱", layout="wide")

# شاشة التطبيق الرئيسية
st.title("🌱 Supply Chain Sustainability Decision Support System")
st.subheader("System Dynamics & Scenario Planning Model (36-Month)")

st.markdown("---")

# تقسيم المدخلات في الجانب الأيسر (Sidebar)
st.sidebar.header("📊 Simulation Controls")
investment_val = st.sidebar.slider("Green Procurement Investment ($)", 0, 100000, 50000, step=5000)
scenario_val = st.sidebar.selectbox("Select Scenario", ["Base Case", "Optimistic (High Impact)", "Pessimistic (Low Impact)"])

# دالة محاكاة تعتمد على الـ Stock and Flow ونظام الديناميكيات
def run_simulation(investment, scenario):
    months = list(range(37))
    
    # الـ Rates والتأثيرات بناءً على السيناريو المختار (تؤثر جوة الـ Flows)
    if scenario == "Optimistic (High Impact)":
        esg_flow_rate = 1.8
        brand_flow_rate = 1.5
        trust_flow_rate = 1.6
        cost_drain_rate = 0.85
    elif scenario == "Pessimistic (Low Impact)":
        esg_flow_rate = 0.6
        brand_flow_rate = 0.5
        trust_flow_rate = 0.4
        cost_drain_rate = 1.15
    else: # Base Case
        esg_flow_rate = 1.2
        brand_flow_rate = 1.0
        trust_flow_rate = 1.1
        cost_drain_rate = 1.0
        
    # محاكاة الـ Stocks عبر الزمن (تأثير الـ Investment والـ Rates)
    esg_hist = [50 + (i * esg_flow_rate * (investment / 50000)) for i in months]
    brand_hist = [40 + (i * brand_flow_rate * (investment / 50000)) for i in months]
    trust_hist = [45 + (i * trust_flow_rate * (investment / 50000)) for i in months]
    
    base_cost = 100000
    cost_reduction = (investment * 0.2)
    cost_hist = [(base_cost - cost_reduction) * (1 + (i * 0.005)) * cost_drain_rate for i in months]
    
    success_hist = [(esg + br + tr) / 3 for esg, br, tr in zip(esg_hist, brand_hist, trust_hist)]
    
    # حدود الـ Stocks (Max 100%)
    esg_hist = [min(100, x) for x in esg_hist]
    brand_hist = [min(100, x) for x in brand_hist]
    trust_hist = [min(100, x) for x in trust_hist]
    success_hist = [min(100, x) for x in success_hist]
    
    return {
        "months": months,
        "esg": esg_hist,
        "brand": brand_hist,
        "trust": trust_hist,
        "cost": cost_hist,
        "success": success_hist
    }

# تشغيل النموذج وحساب النتائج
hist = run_simulation(investment_val, scenario_val)

# عرض النتائج الرقمية السريعة (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Final Supplier ESG Score", f"{hist['esg'][-1]:.1f}%")
col2.metric("Final Brand Reputation", f"{hist['brand'][-1]:.1f}%")
col3.metric("Final Customer Trust", f"{hist['trust'][-1]:.1f}%")
col4.metric("Final Procurement Cost", f"${hist['cost'][-1]:,.0f}")

st.markdown("---")

# 2. رسم الجرافات بحجم أصغر جداً (Mini-graphs) لضمان أخذ لقطة شاشة واحدة
st.header("📈 Vensim Dynamic Trends")

def plot_vensim_graph(title, y_data, color):
    fig, ax = plt.subplots(figsize=(3.5, 1.6)) # تصغير إضافي ومكثف جداً ليناسب شاشة واحدة
    ax.plot(hist["months"], y_data, color=color, linewidth=2)
    ax.set_title(title, fontsize=8, fontweight='bold')
    ax.set_xlabel("Months", fontsize=7)
    ax.tick_params(axis='both', labelsize=7)
    ax.grid(True, linestyle='--', alpha=0.4)
    return fig

# السطر الأول للجرافات (3 جرافات جنب بعض) مع نصوص الحالة التوضيحية
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.pyplot(plot_vensim_graph("Supplier ESG Performance", hist["esg"], "green"))
    esg_status = "High Growth" if hist["esg"][-1] > 75 else "Stable Growth" if hist["esg"][-1] > 55 else "Low/Stable"
    st.caption(f"Status: **{esg_status}** ({hist['esg'][-1]:.1f}%)")

with row1_col2:
    st.pyplot(plot_vensim_graph("Brand Reputation", hist["brand"], "blue"))
    brand_status = "Reputable/High" if hist["brand"][-1] > 70 else "Stable" if hist["brand"][-1] > 50 else "Critical/Low"
    st.caption(f"Status: **{brand_status}** ({hist['brand'][-1]:.1f}%)")

with row1_col3:
    st.pyplot(plot_vensim_graph("Customer Trust", hist["trust"], "purple"))
    trust_status = "High Trust" if hist["trust"][-1] > 70 else "Stable"
    st.caption(f"Status: **{trust_status}** ({hist['trust'][-1]:.1f}%)")

st.markdown("---")

# السطر الثاني للجرافات (3 جرافات المتبقية جنب بعض) مع نصوص الحالة التوضيحية
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.pyplot(plot_vensim_graph("Organizational Success Index", hist["success"], "orange"))
    success_status = "High Performance" if hist["success"][-1] > 70 else "Stable/Moderate"
    st.caption(f"Status: **{success_status}** ({hist['success'][-1]:.1f}%)")

with row2_col2:
    st.pyplot(plot_vensim_graph("Procurement Investment Level", [investment_val]*37, "gold"))
    st.caption(f"Status: **Fixed Input** (${investment_val:,})")

with row2_col3:
    st.pyplot(plot_vensim_graph("Procurement Cost Trends ($)", hist["cost"], "red"))
    cost_status = "Controlled/Low" if scenario_val == "Optimistic (High Impact)" else "High Drain" if scenario_val == "Pessimistic (Low Impact)" else "Stable"
    st.caption(f"Status: **{cost_status}** (${hist['cost'][-1]:,.0f})")