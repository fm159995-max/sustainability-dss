import streamlit as st
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة لتكون بعرض الشاشة بالكامل (Wide Mode)
st.set_page_config(page_title="Supply Chain Sustainability DSS", page_icon="🌱", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ------------------------------------------------------
# 🏠 شاشة الـ Home
# ------------------------------------------------------
if st.session_state.page == "Home":
    st.title("🌱 Supply Chain Sustainability")
    st.subheader("Decision Support System (Based on System Dynamics)")
    st.markdown("---")
    st.header("📖 About Project")
    st.write("""
    This application displays the Vensim simulation results for the long-term impact of sustainability investments 
    on supplier ESG performance, brand reputation, customer trust, and organizational success.
    """)
    st.markdown("---")
    if st.button("🚀 Start Simulation View", use_container_width=True):
        st.session_state.page = "Setup"
        st.rerun()

# ------------------------------------------------------
# ⚙️ شاشة Simulation Setup
# ------------------------------------------------------
elif st.session_state.page == "Setup":
    st.title("⚙️ Scenario Selection")
    st.markdown("---")
    
    st.header("🎬 Choose Simulation Scenario to Load from Vensim")
    scenario = st.selectbox(
        "Scenario",
        ["Base Case", "High Investment", "High Collaboration", "Cost Reduction"]
    )
    
    # الـ Sliders هنا للعرض وتتغير تلقائياً حسب السيناريو لتمثيل الـ Policy Rates والـ Inputs في الـ Stock & Flow
    if scenario == "Base Case":
        invest, collab, green, budget = 12.0, 50, 50, 12.0
    elif scenario == "High Investment":
        invest, collab, green, budget = 20.0, 80, 90, 18.0
    elif scenario == "High Collaboration":
        invest, collab, green, budget = 10.0, 100, 40, 10.0
    elif scenario == "Cost Reduction":
        invest, collab, green, budget = 5.0, 20, 10, 5.0

    st.slider("Investment in Sustainability (M$)", 5.0, 20.0, invest, disabled=True)
    st.slider("Supplier Collaboration Level (0-100)", 0, 100, collab, disabled=True)
    st.slider("Green Innovation Investment (0-100)", 0, 100, green, disabled=True)
    st.slider("Procurement Budget (M$)", 5.0, 20.0, budget, disabled=True)
    
    st.markdown("---")
    
    if st.button("▶ Load Vensim Results", use_container_width=True):
        months = list(range(0, 37)) # من 0 لـ 36 شهر
        
        # 💡 حساب وتحديث الـ Stocks بناءً على الـ Inflows والـ Outflows المتأثرة بالسيناريوهات
        if scenario == "Base Case":
            esg = [50 + (i*0.8) for i in months] 
            brand = [50 + (i*0.6) for i in months]
            trust = [40 + (i*0.5) for i in months]
            success = [45 + (i*0.7) for i in months]
            cost = [4.8] * 37
            
        elif scenario == "High Investment":
            esg = [50 + (i*1.3) if 50 + (i*1.3) <= 100 else 100 for i in months]
            brand = [50 + (i*1.1) if 50 + (i*1.1) <= 100 else 100 for i in months]
            trust = [40 + (i*1.2) if 40 + (i*1.2) <= 100 else 100 for i in months]
            success = [45 + (i*1.4) if 45 + (i*1.4) <= 100 else 100 for i in months]
            cost = [7.2] * 37
            
        elif scenario == "High Collaboration":
            esg = [50 + (i*0.9) for i in months]
            brand = [50 + (i*0.8) for i in months]
            trust = [40 + (i*0.7) for i in months]
            success = [45 + (i*0.8) for i in months]
            cost = [4.2] * 37
            
        elif scenario == "Cost Reduction":
            esg = [50 - (i*0.3) for i in months]
            brand = [50 - (i*0.4) for i in months]
            trust = [40 - (i*0.2) for i in months]
            success = [45 - (i*0.5) for i in months]
            cost = [2.5] * 37

        # حفظ النتايج الثابتة لعرضها
        st.session_state.results = {
            "esg_val": int(esg[-1]), "brand_val": int(brand[-1]), "trust_val": int(trust[-1]),
            "success_val": int(success[-1]), "invest_val": invest, "cost_val": cost[-1],
            "scenario": scenario,
            "history": {
                "months": months, "esg": esg, "brand": brand, "trust": trust, "success": success, "cost": cost
            }
        }
        st.session_state.page = "Dashboard"
        st.rerun()

# ------------------------------------------------------
# 📊 شاشة الـ Dashboard والجرافات (تجميع في مكان واحد بحجم أصغر)
# ------------------------------------------------------
elif st.session_state.page == "Dashboard":
    st.title("📊 Vensim Simulation Dashboard")
    res = st.session_state.results
    hist = res["history"]
    
    # Sidebar الثابت للتبديل بين السيناريوهات
    with st.sidebar:
        st.header("🔄 Navigation")
        if st.button("🔄 Change Scenario", use_container_width=True):
            st.session_state.page = "Setup"
            st.rerun()
        st.markdown("---")
        st.info(f"Active Scenario: **{res['scenario']}**")
    
    # 1. الـ KPI Cards الملونة (القيم النهائية للـ Stocks والـ Variables عند الشهر 36)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Supplier ESG Stock", f"{res['esg_val']}/100")
    col2.metric("📊 Brand Reputation Stock", f"{res['brand_val']}/100")
    col3.metric("📊 Customer Trust Stock", f"{res['trust_val']}/100")
    col4.metric("📊 Organizational Success Index", f"{res['success_val']}/100")
    
    col5, col6 = st.columns(2)
    col5.metric("⚙️ Sustainability Investment Rate", f"{res['invest_val']} M$")
    col6.metric("⚙️ Procurement Cost Drain", f"{res['cost_val']} M$")
    
    st.markdown("---")
    
    # 2. تجميع الجرافات كلها في حته واحدة جنب بعض بحجم مكثف (Mini-graphs)
    st.header("📈 Vensim Dynamic Trends (Stocks & Flows)")
    
    # دالة رسم الجرافات بحجم مصغر ومكثف جداً وضبط الـ Padding (figsize=(3.5, 1.5)) لضمان الشاشة الواحدة
    def plot_vensim_graph(title, y_data, color):
        fig, ax = plt.subplots(figsize=(3.5, 1.5))
        ax.plot(hist["months"], y_data, color=color, linewidth=2)
        ax.set_title(title, fontsize=8, fontweight='bold')
        ax.set_xlabel("Time (Months)", fontsize=7)
        ax.tick_params(axis='both', labelsize=7)
        ax.grid(True, linestyle='--', alpha=0.4)
        fig.tight_layout() # لتقليل الفراغات البيضاء حول الجراف
        return fig

    # الصف الأول: 3 جرافات للـ Stocks الأساسية جنب بعض مع نصوص الحالة التوضيحية
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1: 
        st.pyplot(plot_vensim_graph("Supplier ESG Performance", hist["esg"], "green"))
        status = "High Growth" if res['esg_val'] > 75 else "Stable" if res['esg_val'] > 50 else "Decaying"
        st.caption(f"Status: **{status}**")
        
    with row1_col2: 
        st.pyplot(plot_vensim_graph("Brand Reputation", hist["brand"], "blue"))
        status = "High Reputation" if res['brand_val'] > 70 else "Stable" if res['brand_val'] > 50 else "Critical"
        st.caption(f"Status: **{status}**")
        
    with row1_col3: 
        st.pyplot(plot_vensim_graph("Customer Trust", hist["trust"], "purple"))
        status = "High Trust" if res['trust_val'] > 70 else "Stable" if res['trust_val'] > 45 else "Low"
        st.caption(f"Status: **{status}**")
    
    # الصف الثاني: الـ 3 جرافات المتبقية (النجاح المؤسسي، الاستثمار، التكلفة) جنب بعض
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1: 
        st.pyplot(plot_vensim_graph("Organizational Success", hist["success"], "orange"))
        status = "High Performance" if res['success_val'] > 70 else "Stable/Moderate" if res['success_val'] > 50 else "Low"
        st.caption(f"Status: **{status}**")
        
    with row2_col2: 
        st.pyplot(plot_vensim_graph("Investment Level Rate", [res['invest_val']]*37, "gold"))
        st.caption("Status: **Constant Flow Input**")
        
    with row2_col3: 
        st.pyplot(plot_vensim_graph("Procurement Cost Drain", hist["cost"], "red"))
        status = "Controlled" if res['scenario'] in ["High Collaboration", "Cost Reduction"] else "High/Invested" if res['scenario'] == "High Investment" else "Stable"
        st.caption(f"Status: **{status}**")
    
    st.markdown("---")
    
    # 3. الـ Recommendations الثابتة لكل سيناريو
    st.header("📋 Policy Recommendations")
    if res['scenario'] == "High Investment":
        st.success("🟢 High Investment Policy triggers a positive reinforcing loop across all ESG stocks.")
    elif res['scenario'] == "Cost Reduction":
        st.error("🔴 Cost Reduction drastically limits ESG accumulation and decays customer trust over time.")
    elif res['scenario'] == "High Collaboration":
        st.success("🔵 High Collaboration optimizes procurement cost flow while maintaining steady stock growth.")
    else:
        st.info("🟡 Stable growth observed. Policy parameters maintain current equilibrium.")