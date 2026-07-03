import streamlit as st
import pandas as pd

# إعدادات الصفحة العامة
st.set_page_config(page_title="Sustainable Supply Chain DSS", page_icon="🌱", layout="wide")

# استخدام الـ Session State عشان نتحكم في تنقل الصفحات
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ------------------------------------------------------
# 🏠 شاشة الـ Home
# ------------------------------------------------------
if st.session_state.page == "Home":
    st.title("🌱 Sustainable Supply Chain")
    st.subheader("Decision Support System (Based on System Dynamics)")
    st.markdown("---")
    
    st.header("📖 About Project")
    st.write("""
    This application simulates the impact of sustainability investment on supplier performance 
    and organizational success using a System Dynamics model.
    """)
    st.markdown("---")
    
    # لما يدوس هنا ينقله لصفحة الـ Setup
    if st.button("🚀 Start Simulation", use_container_width=True):
        st.session_state.page = "Setup"
        st.rerun()

# ------------------------------------------------------
# ⚙️ شاشة Simulation Setup
# ------------------------------------------------------
elif st.session_state.page == "Setup":
    st.title("⚙️ Simulation Setup")
    st.subheader("تجهيز متغيرات المحاكاة والسيناريوهات")
    st.markdown("---")
    
    # 🌟 ميزة السيناريوهات الجاهزة
    st.header("🎬 Choose Scenario")
    scenario = st.selectbox(
        "Scenario",
        ["Base Case", "High Investment", "High Collaboration", "Cost Reduction"]
    )
    
    # تحديد القيم الافتراضية للـ Sliders بناءً على السيناريو المختار
    if scenario == "Base Case":
        init_invest = 12.0
        init_collab = 50
        init_green = 50
        init_budget = 12.0
    elif scenario == "High Investment":
        init_invest = 20.0
        init_collab = 80
        init_green = 90
        init_budget = 18.0
    elif scenario == "High Collaboration":
        init_invest = 10.0
        init_collab = 100
        init_green = 40
        init_budget = 10.0
    elif scenario == "Cost Reduction":
        init_invest = 5.0
        init_collab = 20
        init_green = 10
        init_budget = 5.0

    st.markdown("---")
    st.header("⚙️ Simulation Parameters")
    
    # الـ Sliders وبياخدوا قيمتهم تلقائياً من السيناريو
    invest = st.slider("Investment in Sustainability (M)", min_value=5.0, max_value=20.0, value=init_invest, step=0.1)
    collab = st.slider("Supplier Collaboration (0-100)", min_value=0, max_value=100, value=init_collab)
    green = st.slider("Green Innovation Investment (0-100)", min_value=0, max_value=100, value=init_green)
    budget = st.slider("Procurement Budget (M)", min_value=5.0, max_value=20.0, value=init_budget, step=0.1)
    
    st.markdown("---")
    
    # زرار تشغيل المحاكاة
    if st.button("▶ Run Simulation", use_container_width=True):
        # هنا بنعمل معادلات رياضية بسيطة (System Dynamics Logic) عشان نحسب النتايج لحظياً
        # الـ ESG Score بيزيد بزيادة الاستثمار والابتكار الأخضر والتعاون
        esg_score = min(100, int(50 + (invest * 1.5) + (collab * 0.2) + (green * 0.15)))
        brand_rep = min(100, int(45 + (esg_score * 0.4) + (collab * 0.1)))
        cust_trust = min(100, int(40 + (brand_rep * 0.5)))
        org_success = min(100, int((esg_score + brand_rep + cust_trust) / 3 + 5))
        
        # التكاليف
        proc_cost = round((budget * 0.5) + (invest * 0.2), 1)
        
        # حفظ النتائج في الـ Session عشان الـ Dashboard يشوفها
        st.session_state.results = {
            "esg": esg_score,
            "brand": brand_rep,
            "trust": cust_trust,
            "success": org_success,
            "invest": invest,
            "cost": proc_cost
        }
        
        # نقل المستخدم لصفحة الـ Dashboard
        st.session_state.page = "Dashboard"
        st.rerun()
        
    # زرار للرجوع للرئيسية لو حب
    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# ------------------------------------------------------
# 📊 شاشة الـ Dashboard (هنكملها في المرحلة الرابعة)
# ------------------------------------------------------
elif st.session_state.page == "Dashboard":
    st.title("📊 Dashboard & Results")
    st.write("هنا هنعرض الـ KPI Cards والجرافات الشيك اللي اتفقنا عليها!")
    
    # عرض سريع للتأكد أن الحسابات شغالة
    st.json(st.session_state.results)
    
    if st.button("⬅ Back to Setup"):
        st.session_state.page = "Setup"
        st.rerun()