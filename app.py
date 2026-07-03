import streamlit as st
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة لتكون بعرض الشاشة بالكامل (Wide Mode)
st.set_page_config(page_title="Supply Chain Sustainability DSS", page_icon="🌱", layout="wide")

# دالة محاكاة البيانات بناءً على الاستثمار والسيناريو
def run_simulation(investment, scenario):
    months = list(range(37)) # من 0 لـ 36 شهر
    
    # تحديد المعاملات بناءً على السيناريو المختار
    if scenario == "Optimistic (High Impact)":
        esg_growth = 1.8
        brand_growth = 1.5
        trust_growth = 1.6
        cost_multiplier = 0.85
    elif scenario == "Pessimistic (Low Impact)":
        esg_growth = 0.6
        brand_growth = 0.5
        trust_growth = 0.4
        cost_multiplier = 1.15
    else: # Base Case
        esg_growth = 1.2
        brand_growth = 1.0
        trust_growth = 1.1
        cost_multiplier = 1.0
        
    # معادلات محاكاة بسيطة تشبه ديناميكيات النظام (System Dynamics)
    esg_hist = [50 + (i * esg_growth * (investment / 50000)) for i in months]
    brand_hist = [40 + (i * brand_growth * (investment / 50000)) for i in months]
    trust_hist = [45 + (i * trust_growth * (investment / 50000)) for i in months]
    
    # حساب تكاليف الشراء Procurement Cost وتأثرها بالاستثمار والسيناريو
    base_cost = 100000
    cost_reduction = (investment * 0.2)
    cost_hist = [(base_cost - cost_reduction) * (1 + (i * 0.005)) * cost_multiplier for i in months]
    
    # حساب النجاح المؤسسي كمحصلة للمؤشرات
    success_hist = [(esg + br + tr) / 3 for esg, br, tr in zip(esg_hist, brand_hist, trust_hist)]
    
    # التأكد من عدم تخطي المؤشرات لنسبة 100%
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

# شاشة التطبيق الرئيسية
st.title("🌱 Supply Chain Sustainability Decision Support System")
st.subheader("System Dynamics & Scenario Planning Model (36-Month)")

st.markdown("---")

# تقسيم المدخلات في الجانب الأيسر (Sidebar)
st.sidebar.header("📊 Simulation Controls")
investment_val = st.sidebar.slider("Green Procurement Investment ($)", 0, 100000, 50000, step=5000)
scenario_val = st.sidebar.selectbox("Select Scenario", ["Base Case", "Optimistic (High Impact)", "Pessimistic (Low Impact)"])

# تشغيل النموذج وحساب النتائج
hist = run_simulation(investment_val, scenario_val)

# عرض النتائج الحالية بشكل رقمي سريع (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Final Supplier ESG Score", f"{hist['esg'][-1]:.1f}%")
col2.metric("Final Brand Reputation", f"{hist['brand'][-1]:.1f}%")
col3.metric("Final Customer Trust", f"{hist['trust'][-1]:.1f}%")
col4.metric("Final Procurement Cost", f"${hist['cost'][-1]:,.0f}")

st.markdown("---")

# 2. رسم الجرافات مصغرة ومقسمة على أعمدة (جنب بعض)
st.header("📈 Vensim Dynamic Trends")

# دالة الرسم بحجم أصغر ومناسب للأعمدة (figsize=(4, 2.2))
def plot_vensim_graph(title, y_data, color):
    fig, ax = plt.subplots(figsize=(4, 2.2)) # حجم ملموم جداً ومناسب للعرض
    ax.plot(hist["months"], y_data, color=color, linewidth=2)
    ax.set_title(title, fontsize=9, fontweight='bold')
    ax.set_xlabel("Months", fontsize=8)
    ax.tick_params(axis='both', labelsize=8)
    ax.grid(True, linestyle='--', alpha=0.5)
    return fig

# السطر الأول: يحتوي على 3 جرافات جنب بعض
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.pyplot(plot_vensim_graph("Supplier ESG Performance", hist["esg"], "green"))
with row1_col2:
    st.pyplot(plot_vensim_graph("Brand Reputation", hist["brand"], "blue"))
with row1_col3:
    st.pyplot(plot_vensim_graph("Customer Trust", hist["trust"], "purple"))

st.markdown("---") # خط فاصل بين السطرين

# السطر الثاني: يحتوي على الـ 3 جرافات المتبقية جنب بعض
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.pyplot(plot_vensim_graph("Organizational Success Index", hist["success"], "orange"))
with row2_col2:
    # جراف ثابت لقيمة الاستثمار المدخلة
    st.pyplot(plot_vensim_graph("Procurement Investment Level", [investment_val]*37, "gold"))
with row2_col3:
    st.pyplot(plot_vensim_graph("Procurement Cost Trends ($)", hist["cost"], "red"))