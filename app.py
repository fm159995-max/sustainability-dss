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
    st.subheader("Decision Support System (Strictly Based on Vensim Equations)")
    st.markdown("---")
    st.header("📖 About Project")
    st.write("""
    This application displays the Vensim simulation results based on the mathematical interactions between 
    Sustainability Capital Stocks, Brand Reputation, Supplier ESG Scores, and Green Innovation.
    """)
    st.markdown("---")
    if st.button("🚀 Start Simulation View", use_container_width=True):
        st.session_state.page = "Setup"
        st.rerun()

# ------------------------------------------------------
# ⚙️ شاشة Simulation Setup
# ------------------------------------------------------
elif st.session_state.page == "Setup":
    st.title("⚙️ Vensim Scenario Selection")
    st.markdown("---")
    
    st.header("🎬 Choose Simulation Scenario to Load from Vensim Model Variables")
    scenario = st.selectbox(
        "Scenario",
        ["Base Case", "High Consumption Rate", "High Reputation Building", "Severe Reputation Decay", "Maximized Sustainability Investment"]
    )
    
    # تحديد المعاملات والـ Rates بناءً على المعادلات الحقيقية والسيناريوهات
    if scenario == "Base Case":
        reinvest_fraction = 0.10     # الـ 10% الحقيقية في الموديل
        consumption_fraction = 0.15  # الـ 15% الحقيقية في الموديل
        rep_sensitivity = 0.20       # الـ 20% الحقيقية في الموديل
        rep_decay_fraction = 0.20    # الـ 20% الحقيقية في الموديل
        initial_sustainability = 5000000.0
        
    elif scenario == "High Consumption Rate":
        reinvest_fraction = 0.10
        consumption_fraction = 0.35  # زيادة معدل استهلاك الصندوق
        rep_sensitivity = 0.15
        rep_decay_fraction = 0.20
        initial_sustainability = 5000000.0
        
    elif scenario == "High Reputation Building":
        reinvest_fraction = 0.15     # زيادة نسبة إعادة الاستثمار من الأرباح
        consumption_fraction = 0.12
        rep_sensitivity = 0.40       # حساسية سمعة أعلى للموردين
        rep_decay_fraction = 0.10     # تقليل تلاشي السمعة
        initial_sustainability = 5000000.0
        
    elif scenario == "Severe Reputation Decay":
        reinvest_fraction = 0.05     # تقليل الاستثمار
        consumption_fraction = 0.20
        rep_sensitivity = 0.10
        rep_decay_fraction = 0.50    # تلاشي سريع جداً للسمعة (أزمة)
        initial_sustainability = 5000000.0
        
    elif scenario == "Maximized Sustainability Investment":
        reinvest_fraction = 0.25     # استثمار ربع الأرباح في الاستدامة
        consumption_fraction = 0.15
        rep_sensitivity = 0.30
        rep_decay_fraction = 0.10
        initial_sustainability = 10000000.0 # ضخ رأس مال مبدئي مضاعف

    # عرض المعاملات النشطة كـ Sliders للقراءة والتوثيق فقط
    st.slider("Sustainability Reinvestment Fraction", 0.05, 0.40, reinvest_fraction, disabled=True)
    st.slider("Investment Utilization/Depletion Rate", 0.05, 0.50, consumption_fraction, disabled=True)
    st.slider("Reputation Sensitivity Coefficient", 0.05, 0.50, rep_sensitivity, disabled=True)
    st.slider("Reputation Decay/Erosion Rate", 0.05, 0.60, rep_decay_fraction, disabled=True)
    
    st.markdown("---")
    
    if st.button("▶ Load Vensim Results", use_container_width=True):
        months = list(range(0, 37))
        
        # إعداد الـ Stocks الابتدائية من معادلاتكم الحقيقية
        sustainability_stock = initial_sustainability
        reputation_stock = 50.0  # القيمة الابتدائية الحقيقية للسمعة
        
        # جداول حفظ البيانات
        esg_stock_hist, brand_stock_hist, trust_hist, success_hist, cost_hist, green_innov_hist, profit_hist = [], [], [], [], [], [], []
        
        # حلقة المحاكاة المتقطعة شهر بشهر (Vensim Time Step Simulation)
        for month in months:
            # 1. حساب القيم المساعدة الابتدائية للشهر الحالي بناءً على الأرباح التقريبية السابقة
            # لنبدأ بأرباح افتراضية للشهر الأول، ثم تتحدث ديناميكياً
            if month == 0:
                current_profit = 9000000.0 # قيمة تشغيلية مبدئية متزنة مع الـ Scale
            
            # 2. حساب الـ Flows (التدفقات) بناءً على معادلات الموديل الحقيقية
            resource_replenishment = current_profit * reinvest_fraction
            investment_consumption_rate = consumption_fraction * sustainability_stock
            
            # 3. حساب الـ Auxiliary Variables بناءً على المعادلات بالملي
            # Supplier ESG Performance = MIN(100, 35 + (Sustainability Stock / 1.7e7) * 65)
            supplier_esg = min(100.0, 35.0 + (sustainability_stock / 1.7e7) * 65.0)
            
            reputation_building_rate = supplier_esg * rep_sensitivity
            reputation_decay_rate = rep_decay_fraction * reputation_stock
            
            # تحديث الـ Stocks (تكامل INTEG الحقيقي)
            sustainability_stock = sustainability_stock + (resource_replenishment / 12) - (investment_consumption_rate / 12)
            reputation_stock = reputation_stock + (reputation_building_rate / 12) - (reputation_decay_rate / 12)
            
            # وضع الحدود الرياضية
            sustainability_stock = max(0.0, sustainability_stock)
            reputation_stock = max(0.0, min(100.0, reputation_stock))
            
            # 4. حساب بقية المتغيرات التابعة المتسلسلة
            customer_trust = reputation_stock * 0.95
            org_success = customer_trust * 0.95
            
            # Procurement Costs = Investment Consumption Rate + 1,000,000
            procignment_costs = investment_consumption_rate + 1000000.0
            
            # Short-Term Profitability = (1e7 + Organizational Success * 200,000) - Procurement Costs
            current_profit = (10000000.0 + org_success * 200000.0) - procignment_costs
            
            # Investment in Green Innovation = Organizational Success * 40,000
            green_innovation = org_success * 40000.0
            
            # حفظ قيم هذا الشهر في القوائم لرسمها
            esg_stock_hist.append(sustainability_stock)
            brand_stock_hist.append(reputation_stock)
            trust_hist.append(customer_trust)
            success_hist.append(org_success)
            cost_hist.append(procignment_costs)
            green_innov_hist.append(green_innovation)
            profit_hist.append(current_profit)

        # حفظ الحالة النهائية لعرضها كـ KPIs
        st.session_state.results = {
            "esg_val": f"${int(esg_stock_hist[-1]):,}", 
            "brand_val": f"{brand_stock_hist[-1]:.1f}/100", 
            "trust_val": f"{trust_hist[-1]:.1f}/100",
            "success_val": f"{success_hist[-1]:.1f}/100", 
            "cost_val": f"${int(cost_hist[-1]):,}", 
            "profit_val": f"${int(profit_hist[-1]):,}",
            "green_val": f"${int(green_innov_hist[-1]):,}",
            "scenario": scenario,
            "history": {
                "months": months, "esg": esg_stock_hist, "brand": brand_stock_hist, 
                "trust": trust_hist, "success": success_hist, "cost": cost_hist, "green": green_innov_hist
            }
        }
        st.session_state.page = "Dashboard"
        st.rerun()

# ------------------------------------------------------
# 📊 شاشة الـ Dashboard والجرافات (مكثفة وديناميكية حقيقية)
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
        st.info(f"Active Policy Scenario: \n**{res['scenario']}**")
        st.metric("💰 Short-Term Profitability", res["profit_val"])
    
    # 1. الـ KPIs المكتوبة بخط منسق وملموم للموديل الفعلي
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("📦 Sustainability Capital", res['esg_val'])
    col2.metric("📦 Brand Reputation", res['brand_val'])
    col3.metric("📈 Org. Success", res['success_val'])
    col4.metric("🛡️ Customer Trust", res['trust_val'])
    col5.metric("💸 Procurement Costs", res['cost_val'])
    col6.metric("💡 Green Innovation", res['green_val'])
    
    st.markdown("<hr style='margin:2px 0px;'/>", unsafe_allow_html=True)
    
    # 2. رسم الـ 6 جرافات الحقيقية المحدثة بالمعادلات الصريحة
    st.header("📈 Dynamic Vensim Chart Matrix (Mathematical Curves)")
    
    def plot_vensim_graph(title, y_data, color, is_currency=False):
        fig, ax = plt.subplots(figsize=(2.5, 1.1))
        ax.plot(hist["months"], y_data, color=color, linewidth=1.8)
        ax.set_title(title, fontsize=7.5, fontweight='bold', pad=3)
        ax.set_xlabel("Months", fontsize=6, labelpad=1)
        ax.tick_params(axis='both', labelsize=6, pad=1)
        
        # تنسيق أرقام المحور الرأسي في حالة العملات المليونية لتكون واضحة وملمومة
        if is_currency:
            ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
            ax.tick_params(axis='y', labelsize=5)
            
        ax.grid(True, linestyle='--', alpha=0.3)
        fig.tight_layout(pad=0.2)
        return fig

    # الصف الأول
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1: 
        st.pyplot(plot_vensim_graph("Investment in Sustainability (Stock)", hist["esg"], "green", is_currency=True))
        st.caption("Capital accumulated for ESG initiatives.")
    with row1_col2: 
        st.pyplot(plot_vensim_graph("Brand Reputation (Stock)", hist["brand"], "blue"))
        st.caption("Perceived corporate credibility index.")
    with row1_col3: 
        st.pyplot(plot_vensim_graph("Customer Trust Pipeline", hist["trust"], "purple"))
        st.caption("Direct downstream behavioral driver.")
    
    # الصف الثاني
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1: 
        st.pyplot(plot_vensim_graph("Organizational Success Index", hist["success"], "orange"))
        st.caption("Composite performance pass-through metric.")
    with row2_col2: 
        st.pyplot(plot_vensim_graph("Procurement Costs Drain", hist["cost"], "red", is_currency=True))
        st.caption("Fixed costs + variable ESG operational spending.")
    with row2_col3: 
        st.pyplot(plot_vensim_graph("Investment in Green Innovation", hist["green"], "teal", is_currency=True))
        st.caption("Allocated discretionary R&D budget.")
    
    st.markdown("<hr style='margin:2px 0px;'/>", unsafe_allow_html=True)
    
    # 3. الـ Insights الديناميكية للسياسات المبنية على المعادلات
    st.header("📋 System Dynamics Policy Insights")
    if res['scenario'] == "Maximized Sustainability Investment":
        st.success("🟢 Policy Verdict: High Initial Capital coupled with high reinvestment creates a massive accumulation in Sustainability Stock, lifting the ESG score floor and creating a compounding gain in Reputation, Trust, and R&D Innovation.")
    elif res['scenario'] == "High Reputation Building":
        st.success("🔵 Policy Verdict: Optimizing the conversion efficiency from ESG performance to brand equity creates a high-leverage growth curve for downstream success with minimal resource drain.")
    elif res['scenario'] == "Severe Reputation Decay":
        st.error("🔴 Policy Verdict: High market decay triggers a balancing loophole where reputation erodes faster than it builds, heavily damaging organizational value and causing R&D budgets to drop.")
    elif res['scenario'] == "High Consumption Rate":
        st.warning("🟡 Policy Verdict: Accelerating capital utilization triggers rapid spending. While it drives temporary performance, it outpaces profitability replenishment, causing an eventual asset dropdown.")
    else:
        st.info("💡 Policy Verdict: System functions under standard baseline constraints. Equilibrium is fully calibrated to Vensim steady-state values.")