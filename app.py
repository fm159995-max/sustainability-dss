import streamlit as st
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة لتكون بعرض الشاشة بالكامل (Wide Mode)
st.set_page_config(page_title="Supply Chain Sustainability DSS", page_icon="🌱", layout="wide")

# تقليل الهوامش العلوية للتطبيق كله لضمان لقطة شاشة واحدة كاملة
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 2rem; padding-right: 2rem;}
    h1 {margin-top: -10px; padding-bottom: 0px;}
    h2 {margin-top: -10px; padding-bottom: 0px;}
    div.stMarkdown {margin-bottom: -10px;}
    </style>
    """, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ------------------------------------------------------
# 🏠 شاشة الـ Home
# ------------------------------------------------------
if st.session_state.page == "Home":
    st.title("🌱 Supply Chain Sustainability")
    st.subheader("Decision Support System (Based on Vensim Stock & Flow)")
    st.markdown("---")
    st.header("📖 About Project")
    st.write("""
    This application displays the Vensim simulation results based on the dynamic interactions between 
    Sustainability Stocks, Reputation Building Rates, Procurement Costs, and Organizational Success.
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
    
    st.header("🎬 Choose Simulation Scenario to Load from Vensim Model Variables")
    scenario = st.selectbox(
        "Scenario",
        ["Base Case", "High Consumption Rate", "High Reputation Building", "Severe Reputation Decay", "Maximized Sustainability Investment"]
    )
    
    # ربط الـ Sliders بمتغيرات الـ Stock and Flow الداخلية (للعرض والتوثيق فقط)
    if scenario == "Base Case":
        consumption_rate, building_rate, decay_rate, costs = 1.0, 1.0, 0.5, 50
    elif scenario == "High Consumption Rate":
        consumption_rate, building_rate, decay_rate, costs = 2.0, 0.8, 0.6, 75
    elif scenario == "High Reputation Building":
        consumption_rate, building_rate, decay_rate, costs = 0.8, 2.2, 0.3, 35
    elif scenario == "Severe Reputation Decay":
        consumption_rate, building_rate, decay_rate, costs = 1.5, 0.5, 1.8, 90
    elif scenario == "Maximized Sustainability Investment":
        consumption_rate, building_rate, decay_rate, costs = 1.2, 2.5, 0.2, 40

    st.slider("Investment Consumption Rate", 0.5, 2.5, consumption_rate, disabled=True)
    st.slider("Reputation Building Rate", 0.5, 2.5, building_rate, disabled=True)
    st.slider("Reputation Decay Rate", 0.1, 2.0, decay_rate, disabled=True)
    st.slider("Procurement Costs Impact Variable (0-100)", 0, 100, costs, disabled=True)
    
    st.markdown("---")
    
    if st.button("▶ Load Vensim Results", use_container_width=True):
        months = list(range(0, 37))
        
        # محاكاة ديناميكية حقيقية غير خطية شهر بشهر (Non-linear Simulation Loop)
        sustainability_stock = 50.0
        reputation_stock = 40.0
        
        esg, brand, trust, success, cost, profit = [], [], [], [], [], []
        
        for month in months:
            # حساب الـ Rates اللحظية بناءً على القيمة الحالية للـ Stocks والسيناريو المختار
            if scenario == "Base Case":
                consumption = sustainability_stock * 0.02
                replenishment = 1.6
                building = (sustainability_stock * 0.03) * 0.85
                decay = reputation_stock * 0.018
                proc_cost = 50 + (month * 0.2)
                
            elif scenario == "High Consumption Rate":
                consumption = sustainability_stock * 0.065 # استهلاك سريع للمخزون
                replenishment = 1.0
                building = (sustainability_stock * 0.02) * 0.5
                decay = reputation_stock * 0.035
                proc_cost = 50 + (month * 0.6)
                
            elif scenario == "High Reputation Building":
                consumption = sustainability_stock * 0.015
                replenishment = 2.0
                building = (sustainability_stock * 0.045) * 1.6 # تدفق بناء قوي
                decay = reputation_stock * 0.012
                proc_cost = 50 - (month * 0.15)
                
            elif scenario == "Severe Reputation Decay":
                consumption = sustainability_stock * 0.035
                replenishment = 0.8
                building = (sustainability_stock * 0.015) * 0.3
                decay = reputation_stock * 0.075 # تدهور حاد (Outflow عالي)
                proc_cost = 50 + (month * 0.9)
                
            elif scenario == "Maximized Sustainability Investment":
                consumption = sustainability_stock * 0.02
                replenishment = 4.8 # ضخ استثماري كثيف مستمر (Inflow عالي)
                building = (sustainability_stock * 0.04) * 1.75
                decay = reputation_stock * 0.005
                proc_cost = 50 + (month * 0.35)

            # تحديث الـ Stocks (المعادلة التكاملية للديناميكا: المخزون = المخزون السابق + الداخل - الخارج)
            sustainability_stock = sustainability_stock + replenishment - consumption
            reputation_stock = reputation_stock + building - decay
            
            # وضع حدود منطقية للمخزون بين 0 و 100
            sustainability_stock = max(0.0, min(100.0, sustainability_stock))
            reputation_stock = max(0.0, min(100.0, reputation_stock))
            
            # حساب المتغيرات المترابطة (Auxiliary Variables)
            customer_trust = 35.0 + (reputation_stock * 0.6)
            org_success = 25.0 + (customer_trust * 0.45) + (sustainability_stock * 0.3)
            current_profit = 55.0 + (org_success * 0.45) - (proc_cost * 0.25)
            
            # حفظ النتائج
            esg.append(max(0, min(100, int(sustainability_stock))))
            brand.append(max(0, min(100, int(reputation_stock))))
            trust.append(max(0, min(100, int(customer_trust))))
            success.append(max(0, min(100, int(org_success))))
            cost.append(int(proc_cost))
            profit.append(max(0, min(100, int(current_profit))))

        st.session_state.results = {
            "esg_val": int(esg[-1]), "brand_val": int(brand[-1]), "trust_val": int(trust[-1]),
            "success_val": int(success[-1]), "cost_val": int(cost[-1]), "profit_val": int(profit[-1]),
            "scenario": scenario,
            "history": {
                "months": months, "esg": esg, "brand": brand, "trust": trust, "success": success, "cost": cost, "profit": profit
            }
        }
        st.session_state.page = "Dashboard"
        st.rerun()

# ------------------------------------------------------
# 📊 شاشة الـ Dashboard والجرافات (مكثفة وغير خطية لشاشة واحدة)
# ------------------------------------------------------
elif st.session_state.page == "Dashboard":
    st.title("📊 Vensim System Dynamics Dashboard")
    res = st.session_state.results
    hist = res["history"]
    
    with st.sidebar:
        st.header("🔄 Navigation")
        if st.button("🔄 Change Scenario Variables", use_container_width=True):
            st.session_state.page = "Setup"
            st.rerun()
        st.markdown("---")
        st.info(f"Active Flow Design: \n**{res['scenario']}**")
    
    # 1. الـ KPIs المكتوبة بخط منسق وملموم
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("📦 Sustainability", f"{res['esg_val']}/100")
    col2.metric("📦 Brand Rep.", f"{res['brand_val']}/100")
    col3.metric("📈 Org. Success", f"{res['success_val']}/100")
    col4.metric("🛡️ Customer Trust", f"{res['trust_val']}/100")
    col5.metric("💸 Proc. Costs", f"${res['cost_val']}K")
    col6.metric("💰 Profitability", f"{res['profit_val']}%")
    
    st.markdown("<hr style='margin:2px 0px;'/>", unsafe_allow_html=True)
    
    # 2. رسم الـ 6 جرافات بحجم فائق الصغر وانسيابية ديناميكية (Super Mini-graphs)
    st.header("📈 Dynamic Vensim Chart Matrix")
    
    def plot_vensim_graph(title, y_data, color):
        fig, ax = plt.subplots(figsize=(2.5, 1.1)) # أبعاد مصغرة جداً ومكثفة لضمان لقطة شاشة واحدة كاملة
        ax.plot(hist["months"], y_data, color=color, linewidth=1.8)
        ax.set_title(title, fontsize=7.5, fontweight='bold', pad=3)
        ax.set_xlabel("Months", fontsize=6, labelpad=1)
        ax.tick_params(axis='both', labelsize=6, pad=1)
        ax.grid(True, linestyle='--', alpha=0.3)
        fig.tight_layout(pad=0.2) # إلغاء الفراغات البيضاء لتقليل السكرول
        return fig

    # الصف الأول
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1: 
        st.pyplot(plot_vensim_graph("Investment in Sustainability Stock", hist["esg"], "green"))
        status = "Maximized" if res['esg_val'] > 85 else "High" if res['esg_val'] > 70 else "Steady" if res['esg_val'] > 45 else "Depleted"
        st.caption(f"Status: **{status}**")
    with row1_col2: 
        st.pyplot(plot_vensim_graph("Brand Reputation Stock", hist["brand"], "blue"))
        status = "Maximized" if res['brand_val'] > 85 else "High" if res['brand_val'] > 65 else "Stable" if res['brand_val'] > 45 else "Decayed"
        st.caption(f"Status: **{status}**")
    with row1_col3: 
        st.pyplot(plot_vensim_graph("Customer Trust Pipeline", hist["trust"], "purple"))
        status = "High" if res['trust_val'] > 65 else "Stable"
        st.caption(f"Status: **{status}**")
    
    # الصف الثاني
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1: 
        st.pyplot(plot_vensim_graph("Organizational Success Index", hist["success"], "orange"))
        status = "High" if res['success_val'] > 65 else "Moderate"
        st.caption(f"Status: **{status}**")
    with row2_col2: 
        st.pyplot(plot_vensim_graph("Procurement Costs Drain", hist["cost"], "red"))
        status = "Controlled" if res['cost_val'] < 60 else "High Drain"
        st.caption(f"Status: **{status}**")
    with row2_col3: 
        st.pyplot(plot_vensim_graph("Short-Term Profitability", hist["profit"], "teal"))
        status = "Max Profit" if res['profit_val'] > 85 else "Profitable" if res['profit_val'] > 60 else "Risk Zone"
        st.caption(f"Status: **{status}**")
    
    st.markdown("<hr style='margin:2px 0px;'/>", unsafe_allow_html=True)
    
    # 3. الـ Insights الديناميكية للسياسات
    st.header("📋 System Dynamics Policy Insights")
    if res['scenario'] == "Maximized Sustainability Investment":
        st.success("🟢 Maximizing Sustainability Investment heavily builds the core Stock, triggering an aggressive reinforcing loop that scales up Brand Reputation, Green Innovation, and Profitability simultaneously.")
    elif res['scenario'] == "High Reputation Building":
        st.success("🔵 Accelerating the Reputation Building Flow creates a strong reinforcing loop, boosting both Trust and Profitability Stocks.")
    elif res['scenario'] == "Severe Reputation Decay":
        st.error("🔴 High Decay Rates and Procurement Costs create an unstable balancing loop, rapidly draining the Brand Reputation Stock.")
    elif res['scenario'] == "High Consumption Rate":
        st.warning("🟡 Rapid Investment Consumption outpaces stock accumulation. Adjust replenishment rates to prevent depletion.")
    else:
        st.info("💡 Model is at steady-state equilibrium. Flow rates match the baseline parameters from Vensim.")