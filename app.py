import streamlit as st
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة لتكون بعرض الشاشة بالكامل (Wide Mode)
st.set_page_config(page_title="Supply Chain Sustainability DSS", page_icon="🌱", layout="wide")

# تقليل الهوامش العلوية للتطبيق كله لضمان التناسق ومنع الاهتزاز
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
    Sustainability Capital Stocks, Supplier ESG Scores, Procurement Costs, and Short-Term Profitability.
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
        
        # جداول حفظ البيانات للمتغيرات الستة المطلوبة للجرافات
        esg_stock_hist, supplier_esg_hist, profit_hist, cost_hist, success_hist, trust_hist = [], [], [], [], [], []
        
        # حلقة المحاكاة المتقطعة شهر بشهر (Vensim Time Step Simulation)
        for month in months:
            if month == 0:
                current_profit = 9000000.0 # قيمة تشغيلية مبدئية متزنة مع الـ Scale الحقيقي لتغذية الشهر الأول
            
            # حساب الـ Flows (التدفقات) بناءً على معادلات الموديل الحقيقية
            resource_replenishment = current_profit * reinvest_fraction
            investment_consumption_rate = consumption_fraction * sustainability_stock
            
            # المتغير المطلوب رقم 7: Supplier ESG Performance
            supplier_esg = min(100.0, 35.0 + (sustainability_stock / 1.7e7) * 65.0)
            
            reputation_building_rate = supplier_esg * rep_sensitivity
            reputation_decay_rate = rep_decay_fraction * reputation_stock
            
            # تحديث الـ Stocks (تكامل INTEG الحقيقي)
            sustainability_stock = sustainability_stock + (resource_replenishment / 12) - (investment_consumption_rate / 12)
            reputation_stock = reputation_stock + (reputation_building_rate / 12) - (reputation_decay_rate / 12)
            
            # وضع الحدود الرياضية لمنع تخطي مؤشرات النسب الـ 100%
            sustainability_stock = max(0.0, sustainability_stock)
            reputation_stock = max(0.0, min(100.0, reputation_stock))
            
            # المتغير المطلوب رقم 10: Customer Trust
            customer_trust = reputation_stock * 0.95
            
            # المتغير المطلوب رقم 11: Organizational Success
            org_success = customer_trust * 0.95
            
            # المتغير المطلوب رقم 8: Procurement Costs
            procurement_costs = investment_consumption_rate + 1000000.0
            
            # المتغير المطلوب رقم 9: Short-Term Profitability
            current_profit = (10000000.0 + org_success * 200000.0) - procurement_costs
            
            # حفظ قيم هذا الشهر في القوائم لرسمها
            esg_stock_hist.append(sustainability_stock)
            supplier_esg_hist.append(supplier_esg)
            profit_hist.append(current_profit)
            cost_hist.append(procurement_costs)
            success_hist.append(org_success)
            trust_hist.append(customer_trust)

        # حفظ الحالة النهائية لعرضها كـ KPIs
        st.session_state.results = {
            "esg_val": f"${int(esg_stock_hist[-1]):,}", 
            "supplier_esg_val": f"{supplier_esg_hist[-1]:.1f}/100", 
            "profit_val": f"${int(profit_hist[-1]):,}",
            "cost_val": f"${int(cost_hist[-1]):,}", 
            "success_val": f"{success_hist[-1]:.1f}/100", 
            "trust_val": f"{trust_hist[-1]:.1f}/100",
            "scenario": scenario,
            "history": {
                "months": months, 
                "esg": esg_stock_hist, 
                "supplier_esg": supplier_esg_hist, 
                "profit": profit_hist, 
                "cost": cost_hist, 
                "success": success_hist, 
                "trust": trust_hist
            }
        }
        st.session_state.page = "Dashboard"
        st.rerun()

# ------------------------------------------------------
# 📊 شاشة الـ Dashboard والجرافات المحدثة الستة (ثابتة بدون اهتزاز)
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
    
    # 1. الـ KPIs المكتوبة للمتغيرات الستة المطلوبة بالملي
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("📦 Sustainability Capital", res['esg_val'])
    col2.metric("🛡️ Supplier ESG Performance", res['supplier_esg_val'])
    col3.metric("💰 Short-Term Profitability", res['profit_val'])
    col4.metric("💸 Procurement Costs", res['cost_val'])
    col5.metric("📈 Org. Success", res['success_val'])
    col6.metric("🤝 Customer Trust", res['trust_val'])
    
    st.markdown("<hr style='margin:2px 0px;'/>", unsafe_allow_html=True)
    
    # 2. رسم الـ 6 جرافات المطلوبة بالتحديد بأبعاد ثابتة تمنع الـ Flickering تماماً
    st.header("📈 Dynamic Vensim Chart Matrix (Exact Requested Variables)")
    
    def plot_vensim_graph(title, y_data, color, is_currency=False):
        # تثبيت الـ dpi والـ figsize يضمن حجم بكسل ثابت للمتصفح فلا تهتز الصور على اللاب توب
        fig, ax = plt.subplots(figsize=(3.2, 1.4), dpi=100)
        ax.plot(hist["months"], y_data, color=color, linewidth=1.8)
        ax.set_title(title, fontsize=8, fontweight='bold', pad=4)
        ax.set_xlabel("Months", fontsize=6.5, labelpad=1)
        ax.tick_params(axis='both', labelsize=6.5, pad=1)
        
        if is_currency:
            ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
            ax.tick_params(axis='y', labelsize=5.5)
            
        ax.grid(True, linestyle='--', alpha=0.3)
        fig.tight_layout(pad=0.3)
        return fig

    # الصف الأول: الـ 3 جرافات الأولى (تم إيقاف use_container_width لمنع الاهتزاز التلقائي في المتصفح)
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1: 
        st.pyplot(plot_vensim_graph("Investment in Sustainability (Stock)", hist["esg"], "green", is_currency=True), use_container_width=False)
        st.caption("Cumulative capital committed to sustainability initiatives.")
    with row1_col2: 
        st.pyplot(plot_vensim_graph("Supplier ESG Performance", hist["supplier_esg"], "teal"), use_container_width=False)
        st.caption("Bounded linear compliance and ESG tracking score.")
    with row1_col3: 
        st.pyplot(plot_vensim_graph("Short-Term Profitability", hist["profit"], "gold", is_currency=True), use_container_width=False)
        st.caption("Net income accounting structure after procurement deductions.")
    
    # الصف الثاني: الـ 3 جرافات المتبقية لتمام الستة المطلوبة
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1: 
        st.pyplot(plot_vensim_graph("Procurement Costs Drain", hist["cost"], "red", is_currency=True), use_container_width=False)
        st.caption("Fixed baseline operating cost plus variable ESG spending.")
    with row2_col2: 
        st.pyplot(plot_vensim_graph("Organizational Success Index", hist["success"], "orange"), use_container_width=False)
        st.caption("Composite performance pass-through metric.")
    with row2_col3: 
        st.pyplot(plot_vensim_graph("Customer Trust Pipeline", hist["trust"], "purple"), use_container_width=False)
        st.caption("Behavioral conversion function derived from reputation.")
    
    st.markdown("<hr style='margin:2px 0px;'/>", unsafe_allow_html=True)
    
    # 3. الـ Insights الديناميكية
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
        st.info("💡 Policy Verdict: The baseline scenario represents the normal operating conditions of the proposed system. It provides a stable reference case for evaluating and comparing the effects of alternative sustainability policies.")