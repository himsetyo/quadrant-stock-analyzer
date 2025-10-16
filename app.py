"""
Quadrant Stock Analyzer - Streamlit App
Aplikasi untuk menganalisis saham Indonesia berdasarkan metodologi Quadrant
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.calculator import QuadrantCalculator
from src.classifier import QuadrantClassifier
from src.visualizer import QuadrantVisualizer

# Page configuration
st.set_page_config(
    page_title="Quadrant Stock Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e78;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4472C4;
    }
    .quadrant-star {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .quadrant-growth {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .quadrant-value {
        background: linear-gradient(135deg, #17a2b8 0%, #0056b3 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .quadrant-dog {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculator' not in st.session_state:
    st.session_state.calculator = QuadrantCalculator()
if 'classifier' not in st.session_state:
    st.session_state.classifier = QuadrantClassifier()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = QuadrantVisualizer()
if 'results' not in st.session_state:
    st.session_state.results = None

# Header
st.markdown('<div class="main-header">📊 Quadrant Stock Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analisis Saham Indonesia berdasarkan Metodologi Quadrant</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/combo-chart.png", width=80)
    st.title("Navigation")
    
    page = st.radio(
        "Pilih Halaman:",
        ["🏠 Home", "📝 Input Data", "📊 Analysis", "📈 Results", "ℹ️ About"]
    )
    
    st.markdown("---")
    st.markdown("### Quick Guide")
    st.markdown("""
    **4 Quadrants:**
    - ⭐ **STAR**: Strong Buy
    - 📈 **GROWTH**: Buy
    - 💎 **VALUE**: Hold
    - 🐕 **DOG**: Sell
    """)

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    st.header("Welcome to Quadrant Stock Analyzer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Metodologi Quadrant")
        st.markdown("""
        Quadrant Matrix mengklasifikasikan saham berdasarkan **2 dimensi**:
        
        **1. Company Score (CS) - X-axis**
        - Value Creation Sustainability (50%)
        - Value Creation (35%)
        - Financial Power (15%)
        
        **2. Stock Score (SS) - Y-axis**
        - Valuation (65%)
        - Growth Score (35%)
        """)
        
        st.info("**Threshold: 3.0** - Membedakan High vs Low score")
    
    with col2:
        st.subheader("🎯 The 4 Quadrants")
        
        st.markdown('<div class="quadrant-star">⭐ STAR<br>High CS + High SS<br><b>STRONG BUY</b></div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown('<div class="quadrant-growth">📈 GROWTH<br>Low CS + High SS<br><b>BUY</b></div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown('<div class="quadrant-value">💎 VALUE<br>High CS + Low SS<br><b>HOLD</b></div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown('<div class="quadrant-dog">🐕 DOG<br>Low CS + Low SS<br><b>SELL</b></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🚀 Getting Started")
    st.markdown("""
    1. Klik **📝 Input Data** untuk memasukkan data saham
    2. Isi semua field yang diperlukan (Company Info, VCS, Financial Data, Valuation)
    3. Klik **Calculate Scores** di halaman **📊 Analysis**
    4. Lihat hasil di halaman **📈 Results**
    """)

# ==================== INPUT DATA PAGE ====================
elif page == "📝 Input Data":
    st.header("Input Data Saham")
    
    # Tabs for different input sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Company Info", "🏢 VCS (Qualitative)", "💰 Financial Data", "💹 Valuation & Growth"])
    
    with tab1:
        st.subheader("Company Information")
        
        col1, col2 = st.columns(2)
        with col1:
            ticker = st.text_input("Ticker Symbol", value="AMRT", help="e.g., AMRT, BBCA, TLKM")
            company_name = st.text_input("Company Name", value="PT Sumber Alfaria Trijaya Tbk")
            sector = st.text_input("Sector", value="Consumer Defensive")
        
        with col2:
            current_price = st.number_input("Current Price (IDR)", value=2210, min_value=0)
            shares_outstanding = st.number_input("Shares Outstanding (Million)", value=41524.5, min_value=0.0)
            market_cap = st.number_input("Market Cap (IDR Trillion)", value=91.77, min_value=0.0)
        
        st.session_state.company_info = {
            'ticker': ticker,
            'company_name': company_name,
            'sector': sector,
            'current_price': current_price,
            'shares_outstanding': shares_outstanding,
            'market_cap': market_cap
        }
    
    with tab2:
        st.subheader("Value Creation Sustainability (VCS)")
        
        st.markdown("#### 1. Company Lifecycle")
        lifecycle = st.slider("Score (1=Start-up, 4=Growth)", 1.0, 4.0, 3.5, 0.5)
        
        st.markdown("#### 2. Porter's Five Forces")
        col1, col2 = st.columns(2)
        with col1:
            suppliers = st.slider("Suppliers Power", 1.0, 4.0, 3.5, 0.5)
            entry_barrier = st.slider("Entry Barrier", 1.0, 4.0, 3.5, 0.5)
            rivalry = st.slider("Rivalry", 1.0, 4.0, 2.5, 0.5)
        with col2:
            substitution = st.slider("Product Substitution", 1.0, 4.0, 2.5, 0.5)
            buyers = st.slider("Buyers Power", 1.0, 4.0, 3.0, 0.5)
        
        porter = st.session_state.calculator.calculate_porter_score(
            suppliers, entry_barrier, rivalry, substitution, buyers
        )
        st.info(f"Porter's Five Forces Score: **{porter:.2f}**")
        
        st.markdown("#### 3. Management Quality")
        management = st.slider("Score (1=Poor, 4=Excellent)", 1.0, 4.0, 3.0, 0.5)
        
        st.markdown("#### 4. ESG Score")
        col1, col2, col3 = st.columns(3)
        with col1:
            environment = st.slider("Environment", 1.0, 4.0, 2.0, 0.5)
        with col2:
            social = st.slider("Social", 1.0, 4.0, 4.0, 0.5)
        with col3:
            governance = st.slider("Governance", 1.0, 4.0, 4.0, 0.5)
        
        esg = st.session_state.calculator.calculate_esg_score(environment, social, governance)
        st.info(f"ESG Score: **{esg:.2f}**")
        
        st.session_state.vcs_data = {
            'lifecycle': lifecycle,
            'porter': porter,
            'management': management,
            'esg': esg
        }
    
    with tab3:
        st.subheader("Financial Data (Historical & Projected)")
        
        st.markdown("#### Macroeconomic Assumptions")
        col1, col2 = st.columns(2)
        with col1:
            nominal_gdp = st.number_input("Nominal GDP Growth (%)", value=8.0, min_value=0.0) / 100
        with col2:
            real_gdp = st.number_input("Real GDP Growth (%)", value=5.0, min_value=0.0) / 100
        
        st.markdown("#### Historical Data (2 years)")
        st.markdown("**Year 1 (e.g., 2023)**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            h1_revenue = st.number_input("Revenue (B)", value=106944.7, key="h1_rev")
            h1_ebit = st.number_input("EBIT (B)", value=4444.9, key="h1_ebit")
        with col2:
            h1_net_income = st.number_input("Net Income (B)", value=3403.7, key="h1_ni")
            h1_ocf = st.number_input("OCF (B)", value=6817.0, key="h1_ocf")
        with col3:
            h1_assets = st.number_input("Total Assets (B)", value=34246.2, key="h1_assets")
            h1_equity = st.number_input("Equity (B)", value=15705.2, key="h1_equity")
        with col4:
            h1_cash = st.number_input("Cash (B)", value=4074.5, key="h1_cash")
        
        st.markdown("**Year 2 (e.g., 2024)**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            h2_revenue = st.number_input("Revenue (B)", value=118227.0, key="h2_rev")
            h2_ebit = st.number_input("EBIT (B)", value=4140.1, key="h2_ebit")
        with col2:
            h2_net_income = st.number_input("Net Income (B)", value=3148.1, key="h2_ni")
            h2_ocf = st.number_input("OCF (B)", value=8063.1, key="h2_ocf")
        with col3:
            h2_assets = st.number_input("Total Assets (B)", value=38798.4, key="h2_assets")
            h2_equity = st.number_input("Equity (B)", value=17695.9, key="h2_equity")
        with col4:
            h2_cash = st.number_input("Cash (B)", value=4845.2, key="h2_cash")
        
        st.markdown("#### Projected Data (3 years)")
        st.markdown("**Year 1 Projection (e.g., 2025E)**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            p1_revenue = st.number_input("Revenue (B)", value=127685.2, key="p1_rev")
            p1_ebit = st.number_input("EBIT (B)", value=4469.0, key="p1_ebit")
        with col2:
            p1_net_income = st.number_input("Net Income (B)", value=3424.4, key="p1_ni")
            p1_ocf = st.number_input("OCF (B)", value=8700.0, key="p1_ocf")
        with col3:
            p1_assets = st.number_input("Total Assets (B)", value=42678.2, key="p1_assets")
            p1_equity = st.number_input("Equity (B)", value=19891.8, key="p1_equity")
        with col4:
            p1_cash = st.number_input("Cash (B)", value=5650.0, key="p1_cash")
        
        st.markdown("**Year 2 Projection (e.g., 2026E)**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            p2_revenue = st.number_input("Revenue (B)", value=136623.1, key="p2_rev")
            p2_ebit = st.number_input("EBIT (B)", value=4781.8, key="p2_ebit")
        with col2:
            p2_net_income = st.number_input("Net Income (B)", value=3673.1, key="p2_ni")
            p2_ocf = st.number_input("OCF (B)", value=9300.0, key="p2_ocf")
        with col3:
            p2_assets = st.number_input("Total Assets (B)", value=46946.1, key="p2_assets")
            p2_equity = st.number_input("Equity (B)", value=22264.9, key="p2_equity")
        with col4:
            p2_cash = st.number_input("Cash (B)", value=6550.0, key="p2_cash")
        
        st.markdown("**Year 3 Projection (e.g., 2027E)**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            p3_revenue = st.number_input("Revenue (B)", value=143054.3, key="p3_rev")
            p3_ebit = st.number_input("EBIT (B)", value=5003.5, key="p3_ebit")
        with col2:
            p3_net_income = st.number_input("Net Income (B)", value=3851.4, key="p3_ni")
            p3_ocf = st.number_input("OCF (B)", value=9750.0, key="p3_ocf")
        with col3:
            p3_assets = st.number_input("Total Assets (B)", value=50240.1, key="p3_assets")
            p3_equity = st.number_input("Equity (B)", value=24516.3, key="p3_equity")
        with col4:
            p3_cash = st.number_input("Cash (B)", value=7500.0, key="p3_cash")
        
        # Store financial data
        st.session_state.historical_data = [
            {'revenue': h1_revenue, 'ebit': h1_ebit, 'net_income': h1_net_income, 
             'ocf': h1_ocf, 'total_assets': h1_assets, 'equity': h1_equity, 'cash': h1_cash},
            {'revenue': h2_revenue, 'ebit': h2_ebit, 'net_income': h2_net_income,
             'ocf': h2_ocf, 'total_assets': h2_assets, 'equity': h2_equity, 'cash': h2_cash}
        ]
        
        st.session_state.projected_data = [
            {'revenue': p1_revenue, 'ebit': p1_ebit, 'net_income': p1_net_income,
             'ocf': p1_ocf, 'total_assets': p1_assets, 'equity': p1_equity, 'cash': p1_cash},
            {'revenue': p2_revenue, 'ebit': p2_ebit, 'net_income': p2_net_income,
             'ocf': p2_ocf, 'total_assets': p2_assets, 'equity': p2_equity, 'cash': p2_cash},
            {'revenue': p3_revenue, 'ebit': p3_ebit, 'net_income': p3_net_income,
             'ocf': p3_ocf, 'total_assets': p3_assets, 'equity': p3_equity, 'cash': p3_cash}
        ]
        
        st.session_state.macro_data = {
            'nominal_gdp': nominal_gdp,
            'real_gdp': real_gdp
        }
    
    with tab4:
        st.subheader("Valuation & Growth")
        
        st.markdown("#### Valuation")
        col1, col2, col3 = st.columns(3)
        with col1:
            model_tp = st.number_input("Model Target Price (IDR)", value=3050, min_value=0)
        with col2:
            relative_val = st.number_input("Relative Valuation (IDR)", value=2882, min_value=0)
        with col3:
            current_price_val = st.number_input("Current Price (IDR)", value=2210, min_value=0, key="val_price")
        
        blended_tp = (model_tp + relative_val) / 2
        upside = ((blended_tp - current_price_val) / current_price_val) * 100
        st.info(f"Blended Target Price: **IDR {blended_tp:,.0f}** | Upside: **{upside:.1f}%**")
        
        st.markdown("#### Blended-Forward Growth")
        col1, col2, col3 = st.columns(3)
        with col1:
            revenue_growth = st.number_input("Revenue Growth (%)", value=14.4, min_value=0.0) / 100
        with col2:
            ebit_growth = st.number_input("EBIT Growth (%)", value=16.6, min_value=0.0) / 100
        with col3:
            np_growth = st.number_input("Net Profit Growth (%)", value=16.6, min_value=0.0) / 100
        
        st.session_state.valuation_data = {
            'model_tp': model_tp,
            'relative_val': relative_val,
            'current_price': current_price_val
        }
        
        st.session_state.growth_data = {
            'revenue_growth': revenue_growth,
            'ebit_growth': ebit_growth,
            'np_growth': np_growth
        }
    
    st.success("✅ Data input completed! Go to **📊 Analysis** to calculate scores.")

# ==================== ANALYSIS PAGE ====================
elif page == "📊 Analysis":
    st.header("Score Calculation & Analysis")
    
    if st.button("🔄 Calculate Scores", type="primary"):
        with st.spinner("Calculating scores..."):
            try:
                # Calculate VC scores
                calc = st.session_state.calculator
                
                roa_score = calc.calculate_roa_score(
                    st.session_state.historical_data,
                    st.session_state.projected_data
                )
                
                ebit_margin_score = calc.calculate_ebit_margin_score(
                    st.session_state.historical_data,
                    st.session_state.projected_data
                )
                
                sales_growth_score = calc.calculate_sales_growth_score(
                    st.session_state.historical_data,
                    st.session_state.projected_data,
                    st.session_state.macro_data['nominal_gdp']
                )
                
                profit_growth_score = calc.calculate_profit_growth_score(
                    st.session_state.historical_data,
                    st.session_state.projected_data,
                    st.session_state.macro_data['real_gdp']
                )
                
                vc_data = {
                    'roa': roa_score,
                    'ebit_margin': ebit_margin_score,
                    'sales_growth': sales_growth_score,
                    'profit_growth': profit_growth_score
                }
                
                # Calculate FP scores
                ocf_ebit_score = calc.calculate_ocf_ebit_score(
                    st.session_state.historical_data,
                    st.session_state.projected_data
                )
                
                equity_asset_score = calc.calculate_equity_asset_score(
                    st.session_state.historical_data,
                    st.session_state.projected_data
                )
                
                cash_asset_score = calc.calculate_cash_asset_score(
                    st.session_state.historical_data,
                    st.session_state.projected_data
                )
                
                fp_data = {
                    'ocf_ebit': ocf_ebit_score,
                    'equity_asset': equity_asset_score,
                    'cash_asset': cash_asset_score
                }
                
                # Calculate Company Score
                cs_result = calc.calculate_company_score(
                    st.session_state.vcs_data,
                    vc_data,
                    fp_data
                )
                
                # Calculate Stock Score
                ss_result = calc.calculate_stock_score(
                    st.session_state.valuation_data,
                    st.session_state.growth_data
                )
                
                # Classify
                classifier = st.session_state.classifier
                quadrant_info = classifier.classify(
                    cs_result['company_score'],
                    ss_result['stock_score']
                )
                
                recommendation = classifier.get_investment_recommendation(
                    quadrant_info,
                    ss_result['blended_tp'],
                    st.session_state.company_info['current_price']
                )
                
                # Store results
                st.session_state.results = {
                    'cs_result': cs_result,
                    'ss_result': ss_result,
                    'quadrant_info': quadrant_info,
                    'recommendation': recommendation
                }
                
                st.success("✅ Calculation completed! Go to **📈 Results** to view.")
                
            except Exception as e:
                st.error(f"Error during calculation: {str(e)}")
                st.error("Please make sure all data is filled in **📝 Input Data** page.")
    
    st.markdown("---")
    
    if st.session_state.results:
        st.subheader("Preview Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Company Score", f"{st.session_state.results['cs_result']['company_score']:.2f}")
        with col2:
            st.metric("Stock Score", f"{st.session_state.results['ss_result']['stock_score']:.2f}")
        with col3:
            quadrant = st.session_state.results['quadrant_info']['name']
            st.metric("Quadrant", f"{st.session_state.results['quadrant_info']['emoji']} {quadrant}")
        with col4:
            rating = st.session_state.results['recommendation']['rating']
            st.metric("Rating", rating)

# ==================== RESULTS PAGE ====================
elif page == "📈 Results":
    st.header("Analysis Results")
    
    if not st.session_state.results:
        st.warning("⚠️ No results available. Please calculate scores in **📊 Analysis** page first.")
    else:
        results = st.session_state.results
        company_info = st.session_state.company_info
        
        # Summary Cards
        st.subheader(f"📊 {company_info['ticker']} - {company_info['company_name']}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Company Score", f"{results['cs_result']['company_score']:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Stock Score", f"{results['ss_result']['stock_score']:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            quadrant = results['quadrant_info']['name']
            emoji = results['quadrant_info']['emoji']
            st.markdown(f'<div class="quadrant-{quadrant.lower()}">', unsafe_allow_html=True)
            st.markdown(f"<h3>{emoji} {quadrant}</h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Rating", results['recommendation']['rating'])
            st.metric("Upside", f"{results['recommendation']['upside']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quadrant Matrix Visualization
        st.subheader("🎯 Quadrant Matrix")
        
        stocks_data = [{
            'ticker': company_info['ticker'],
            'cs': results['cs_result']['company_score'],
            'ss': results['ss_result']['stock_score'],
            'quadrant': quadrant
        }]
        
        fig_matrix = st.session_state.visualizer.create_quadrant_matrix(stocks_data)
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        # Score Breakdown
        st.subheader("📊 Score Breakdown")
        
        fig_breakdown = st.session_state.visualizer.create_score_breakdown(
            results['cs_result'],
            results['ss_result']
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)
        
        # Component Radar
        st.subheader("🔍 Component Analysis")
        
        fig_radar = st.session_state.visualizer.create_component_radar(
            results['cs_result']['breakdown']['vcs'],
            results['cs_result']['breakdown']['vc'],
            results['cs_result']['breakdown']['fp']
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Detailed Breakdown Tables
        st.subheader("📋 Detailed Breakdown")
        
        tab1, tab2 = st.tabs(["Company Score", "Stock Score"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**VCS Components**")
                vcs_df = pd.DataFrame({
                    'Component': ['Lifecycle', 'Porter', 'Management', 'ESG'],
                    'Score': [
                        results['cs_result']['breakdown']['vcs']['lifecycle'],
                        results['cs_result']['breakdown']['vcs']['porter'],
                        results['cs_result']['breakdown']['vcs']['management'],
                        results['cs_result']['breakdown']['vcs']['esg']
                    ]
                })
                st.dataframe(vcs_df, hide_index=True)
                st.metric("VCS Score", f"{results['cs_result']['vcs_score']:.2f}")
            
            with col2:
                st.markdown("**VC Components**")
                vc_df = pd.DataFrame({
                    'Component': ['ROA', 'EBIT Margin', 'Sales Growth', 'Profit Growth'],
                    'Score': [
                        results['cs_result']['breakdown']['vc']['roa'],
                        results['cs_result']['breakdown']['vc']['ebit_margin'],
                        results['cs_result']['breakdown']['vc']['sales_growth'],
                        results['cs_result']['breakdown']['vc']['profit_growth']
                    ]
                })
                st.dataframe(vc_df, hide_index=True)
                st.metric("VC Score", f"{results['cs_result']['vc_score']:.2f}")
            
            with col3:
                st.markdown("**FP Components**")
                fp_df = pd.DataFrame({
                    'Component': ['OCF/EBIT', 'Equity/Asset', 'Cash/Asset'],
                    'Score': [
                        results['cs_result']['breakdown']['fp']['ocf_ebit'],
                        results['cs_result']['breakdown']['fp']['equity_asset'],
                        results['cs_result']['breakdown']['fp']['cash_asset']
                    ]
                })
                st.dataframe(fp_df, hide_index=True)
                st.metric("FP Score", f"{results['cs_result']['fp_score']:.2f}")
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Valuation**")
                val_data = results['ss_result']['breakdown']['valuation']
                val_df = pd.DataFrame({
                    'Metric': ['Model TP', 'Relative Val', 'Blended TP', 'Current Price', 'Upside'],
                    'Value': [
                        f"IDR {val_data['model_tp']:,.0f}",
                        f"IDR {val_data['relative_val']:,.0f}",
                        f"IDR {val_data['blended_tp']:,.0f}",
                        f"IDR {val_data['current_price']:,.0f}",
                        f"{val_data['upside']:.1f}%"
                    ]
                })
                st.dataframe(val_df, hide_index=True)
                st.metric("Valuation Score", f"{results['ss_result']['valuation_score']:.2f}")
            
            with col2:
                st.markdown("**Growth**")
                growth_data = results['ss_result']['breakdown']['growth']
                growth_df = pd.DataFrame({
                    'Metric': ['Revenue Growth', 'EBIT Growth', 'Net Profit Growth'],
                    'Value': [
                        f"{growth_data['revenue_growth']:.1f}%",
                        f"{growth_data['ebit_growth']:.1f}%",
                        f"{growth_data['np_growth']:.1f}%"
                    ],
                    'Score': [
                        growth_data['revenue_score'],
                        growth_data['ebit_score'],
                        growth_data['np_score']
                    ]
                })
                st.dataframe(growth_df, hide_index=True)
                st.metric("Growth Score", f"{results['ss_result']['growth_score']:.2f}")
        
        # Investment Recommendation
        st.markdown("---")
        st.subheader("💡 Investment Recommendation")
        
        rec = results['recommendation']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Rating:** {rec['rating']}")
            st.markdown(f"**Quadrant:** {emoji} {quadrant}")
            st.markdown(f"**Action:** {results['quadrant_info']['action']}")
            st.markdown(f"**Risk Level:** {rec['risk_level']}")
            st.markdown(f"**Time Horizon:** {rec['time_horizon']}")
            st.markdown(f"**Position Sizing:** {rec['position_sizing']}")
        
        with col2:
            st.markdown(f"**Target Price:** IDR {rec['target_price']:,.0f}")
            st.markdown(f"**Current Price:** IDR {rec['current_price']:,.0f}")
            st.markdown(f"**Upside:** {rec['upside']:.1f}%")
            
            st.markdown("**Risk Factors:**")
            for risk in rec['risk_factors']:
                st.markdown(f"- {risk}")

# ==================== ABOUT PAGE ====================
elif page == "ℹ️ About":
    st.header("About Quadrant Stock Analyzer")
    
    st.markdown("""
    ### 📚 Metodologi
    
    Aplikasi ini menggunakan **Quadrant Methodology** yang dikembangkan oleh Mandiri Investasi untuk menganalisis dan mengklasifikasikan saham berdasarkan:
    
    1. **Company Score (CS)** - Fundamental quality analysis
    2. **Stock Score (SS)** - Valuation and growth momentum
    
    ### 🎯 Tujuan
    
    Membantu investor untuk:
    - Melakukan analisis fundamental yang terstruktur
    - Mengidentifikasi opportunity investasi terbaik
    - Membuat keputusan investasi yang data-driven
    - Memahami risk-reward profile dari setiap saham
    
    ### 🛠️ Tech Stack
    
    - **Frontend**: Streamlit
    - **Backend**: Python 3.11
    - **Visualization**: Plotly
    - **Data Processing**: Pandas, NumPy
    
    ### 📝 Disclaimer
    
    Aplikasi ini dibuat untuk tujuan **edukasi dan riset**. Bukan merupakan rekomendasi investasi. 
    Pengguna harus melakukan due diligence sendiri dan berkonsultasi dengan financial advisor sebelum membuat keputusan investasi.
    
    ### 📧 Contact
    
    For questions or feedback, please contact:
    - Email: your.email@example.com
    - GitHub: github.com/yourusername
    
    ---
    
    **Made with ❤️ for Indonesian Stock Market Investors**
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Quadrant Stock Analyzer v1.0 | © 2025 | Based on Mandiri Investasi Methodology</p>
</div>
""", unsafe_allow_html=True)

