"""
Score Calculator Module
Menghitung Company Score dan Stock Score berdasarkan metodologi Quadrant
"""

import pandas as pd
import numpy as np

class QuadrantCalculator:
    """Calculator untuk Company Score dan Stock Score"""
    
    def __init__(self):
        self.cs_weights = {
            'vcs': 0.50,  # Value Creation Sustainability
            'vc': 0.35,   # Value Creation
            'fp': 0.15    # Financial Power
        }
        
        self.ss_weights = {
            'valuation': 0.65,
            'growth': 0.35
        }
    
    # ==================== COMPANY SCORE CALCULATION ====================
    
    def calculate_company_score(self, vcs_data, vc_data, fp_data):
        """
        Calculate Company Score (CS)
        
        Args:
            vcs_data: dict with keys [lifecycle, porter, management, esg]
            vc_data: dict with keys [roa, ebit_margin, sales_growth, profit_growth]
            fp_data: dict with keys [ocf_ebit, equity_asset, cash_asset]
        
        Returns:
            dict with CS and breakdown
        """
        # Calculate VCS (average of 4 components)
        vcs_score = np.mean([
            vcs_data['lifecycle'],
            vcs_data['porter'],
            vcs_data['management'],
            vcs_data['esg']
        ])
        
        # Calculate VC (average of 4 components)
        vc_score = np.mean([
            vc_data['roa'],
            vc_data['ebit_margin'],
            vc_data['sales_growth'],
            vc_data['profit_growth']
        ])
        
        # Calculate FP (average of 3 components)
        fp_score = np.mean([
            fp_data['ocf_ebit'],
            fp_data['equity_asset'],
            fp_data['cash_asset']
        ])
        
        # Weighted Company Score
        company_score = (
            vcs_score * self.cs_weights['vcs'] +
            vc_score * self.cs_weights['vc'] +
            fp_score * self.cs_weights['fp']
        )
        
        return {
            'company_score': round(company_score, 2),
            'vcs_score': round(vcs_score, 2),
            'vc_score': round(vc_score, 2),
            'fp_score': round(fp_score, 2),
            'vcs_weighted': round(vcs_score * self.cs_weights['vcs'], 2),
            'vc_weighted': round(vc_score * self.cs_weights['vc'], 2),
            'fp_weighted': round(fp_score * self.cs_weights['fp'], 2),
            'breakdown': {
                'vcs': vcs_data,
                'vc': vc_data,
                'fp': fp_data
            }
        }
    
    # ==================== VCS SCORING ====================
    
    def calculate_esg_score(self, environment, social, governance):
        """Calculate ESG score (average of E, S, G)"""
        return np.mean([environment, social, governance])
    
    def calculate_porter_score(self, suppliers, entry_barrier, rivalry, 
                               substitution, buyers):
        """Calculate Porter's Five Forces score (average of 5 forces)"""
        return np.mean([suppliers, entry_barrier, rivalry, substitution, buyers])
    
    # ==================== VC SCORING ====================
    
    def score_discrepancy(self, future_avg, historical_avg, metric_type='ratio'):
        """
        Score based on discrepancy between future and historical average
        
        Args:
            future_avg: 3-year future average
            historical_avg: 2-year historical average
            metric_type: 'ratio' or 'growth'
        
        Returns:
            score (1-4)
        """
        if metric_type == 'ratio':
            # For ratios (ROA, EBIT Margin, OCF/EBIT, etc.)
            # Calculate in basis points (bps)
            disc_bps = (future_avg - historical_avg) * 100
            
            if disc_bps > 20:
                return 4
            elif disc_bps > 15:
                return 3
            elif disc_bps > 10:
                return 2
            else:
                return 1
        
        elif metric_type == 'growth':
            # For growth rates
            disc_bps = (future_avg - historical_avg) * 100
            
            if disc_bps > 10:
                return 4
            elif disc_bps > 5:
                return 3
            elif disc_bps > 0:
                return 2
            else:
                return 1
    
    def score_vs_gdp(self, company_growth, gdp_growth):
        """
        Score growth vs GDP
        
        Returns:
            score (1-4)
        """
        diff_bps = (company_growth - gdp_growth) * 100
        
        if diff_bps > 4:
            return 4
        elif diff_bps > 0:
            return 3
        elif diff_bps > -2:
            return 2
        else:
            return 1
    
    def calculate_roa_score(self, historical_data, projected_data):
        """Calculate ROA score"""
        # Calculate ROA for each year
        hist_roa = [
            (data['net_income'] / data['total_assets']) 
            for data in historical_data
        ]
        proj_roa = [
            (data['net_income'] / data['total_assets']) 
            for data in projected_data
        ]
        
        hist_avg = np.mean(hist_roa)
        proj_avg = np.mean(proj_roa)
        
        return self.score_discrepancy(proj_avg, hist_avg, 'ratio')
    
    def calculate_ebit_margin_score(self, historical_data, projected_data):
        """Calculate EBIT Margin score"""
        hist_margin = [
            (data['ebit'] / data['revenue']) 
            for data in historical_data
        ]
        proj_margin = [
            (data['ebit'] / data['revenue']) 
            for data in projected_data
        ]
        
        hist_avg = np.mean(hist_margin)
        proj_avg = np.mean(proj_margin)
        
        return self.score_discrepancy(proj_avg, hist_avg, 'growth')
    
    def calculate_sales_growth_score(self, historical_data, projected_data, 
                                     nominal_gdp):
        """Calculate Sales Growth score (2 components)"""
        # Component 1: vs GDP
        proj_revenue_growth = [
            (projected_data[i]['revenue'] / projected_data[i-1]['revenue'] - 1)
            for i in range(1, len(projected_data))
        ]
        avg_revenue_growth = np.mean(proj_revenue_growth)
        score_gdp = self.score_vs_gdp(avg_revenue_growth, nominal_gdp)
        
        # Component 2: Historical acceleration
        hist_revenue_growth = [
            (historical_data[i]['revenue'] / historical_data[i-1]['revenue'] - 1)
            for i in range(1, len(historical_data))
        ]
        hist_avg = np.mean(hist_revenue_growth)
        proj_avg = avg_revenue_growth
        score_accel = self.score_discrepancy(proj_avg, hist_avg, 'growth')
        
        # Average of 2 components
        return np.mean([score_gdp, score_accel])
    
    def calculate_profit_growth_score(self, historical_data, projected_data, 
                                      real_gdp):
        """Calculate Profit Growth score (2 components)"""
        # Component 1: vs GDP
        proj_profit_growth = [
            (projected_data[i]['net_income'] / projected_data[i-1]['net_income'] - 1)
            for i in range(1, len(projected_data))
        ]
        avg_profit_growth = np.mean(proj_profit_growth)
        score_gdp = self.score_vs_gdp(avg_profit_growth, real_gdp)
        
        # Component 2: Historical acceleration
        hist_profit_growth = [
            (historical_data[i]['net_income'] / historical_data[i-1]['net_income'] - 1)
            for i in range(1, len(historical_data))
        ]
        hist_avg = np.mean(hist_profit_growth)
        proj_avg = avg_profit_growth
        score_accel = self.score_discrepancy(proj_avg, hist_avg, 'growth')
        
        # Average of 2 components
        return np.mean([score_gdp, score_accel])
    
    # ==================== FP SCORING ====================
    
    def calculate_ocf_ebit_score(self, historical_data, projected_data):
        """Calculate OCF/EBIT score"""
        hist_ratio = [
            (data['ocf'] / data['ebit']) 
            for data in historical_data
        ]
        proj_ratio = [
            (data['ocf'] / data['ebit']) 
            for data in projected_data
        ]
        
        hist_avg = np.mean(hist_ratio)
        proj_avg = np.mean(proj_ratio)
        
        return self.score_discrepancy(proj_avg, hist_avg, 'ratio')
    
    def calculate_equity_asset_score(self, historical_data, projected_data):
        """Calculate Equity/Asset score"""
        hist_ratio = [
            (data['equity'] / data['total_assets']) 
            for data in historical_data
        ]
        proj_ratio = [
            (data['equity'] / data['total_assets']) 
            for data in projected_data
        ]
        
        hist_avg = np.mean(hist_ratio)
        proj_avg = np.mean(proj_ratio)
        
        return self.score_discrepancy(proj_avg, hist_avg, 'ratio')
    
    def calculate_cash_asset_score(self, historical_data, projected_data):
        """Calculate Cash/Total Asset score"""
        hist_ratio = [
            (data['cash'] / data['total_assets']) 
            for data in historical_data
        ]
        proj_ratio = [
            (data['cash'] / data['total_assets']) 
            for data in projected_data
        ]
        
        hist_avg = np.mean(hist_ratio)
        proj_avg = np.mean(proj_ratio)
        
        return self.score_discrepancy(proj_avg, hist_avg, 'ratio')
    
    # ==================== STOCK SCORE CALCULATION ====================
    
    def calculate_stock_score(self, valuation_data, growth_data):
        """
        Calculate Stock Score (SS)
        
        Args:
            valuation_data: dict with keys [model_tp, relative_val, current_price]
            growth_data: dict with keys [revenue_growth, ebit_growth, np_growth]
        
        Returns:
            dict with SS and breakdown
        """
        # Calculate Valuation Score
        valuation_score = self.calculate_valuation_score(
            valuation_data['model_tp'],
            valuation_data['relative_val'],
            valuation_data['current_price']
        )
        
        # Calculate Growth Score
        growth_score = self.calculate_growth_score(
            growth_data['revenue_growth'],
            growth_data['ebit_growth'],
            growth_data['np_growth']
        )
        
        # Weighted Stock Score
        stock_score = (
            valuation_score['score'] * self.ss_weights['valuation'] +
            growth_score['score'] * self.ss_weights['growth']
        )
        
        return {
            'stock_score': round(stock_score, 2),
            'valuation_score': valuation_score['score'],
            'growth_score': growth_score['score'],
            'valuation_weighted': round(valuation_score['score'] * self.ss_weights['valuation'], 2),
            'growth_weighted': round(growth_score['score'] * self.ss_weights['growth'], 2),
            'blended_tp': valuation_score['blended_tp'],
            'upside': valuation_score['upside'],
            'breakdown': {
                'valuation': valuation_score,
                'growth': growth_score
            }
        }
    
    def calculate_valuation_score(self, model_tp, relative_val, current_price):
        """Calculate Valuation Score"""
        # Blended Target Price (50% model, 50% relative)
        blended_tp = (model_tp + relative_val) / 2
        
        # Upside calculation
        upside = (blended_tp - current_price) / current_price
        
        # Score based on upside
        if upside > 0.30:
            score = 4
        elif upside > 0.15:
            score = 3
        elif upside > 0:
            score = 2
        else:
            score = 1
        
        return {
            'score': score,
            'blended_tp': round(blended_tp, 2),
            'upside': round(upside * 100, 2),
            'model_tp': model_tp,
            'relative_val': relative_val,
            'current_price': current_price
        }
    
    def calculate_growth_score(self, revenue_growth, ebit_growth, np_growth):
        """Calculate Growth Score"""
        # Score each growth component
        def score_growth(growth_rate):
            if growth_rate > 0.50:
                return 4
            elif growth_rate > 0.25:
                return 3
            elif growth_rate > 0.05:
                return 2
            else:
                return 1
        
        revenue_score = score_growth(revenue_growth)
        ebit_score = score_growth(ebit_growth)
        np_score = score_growth(np_growth)
        
        # Average score
        avg_score = np.mean([revenue_score, ebit_score, np_score])
        
        return {
            'score': round(avg_score, 2),
            'revenue_score': revenue_score,
            'ebit_score': ebit_score,
            'np_score': np_score,
            'revenue_growth': round(revenue_growth * 100, 2),
            'ebit_growth': round(ebit_growth * 100, 2),
            'np_growth': round(np_growth * 100, 2)
        }
    
    # ==================== HELPER FUNCTIONS ====================
    
    def get_scoring_rules(self):
        """Return scoring rules reference"""
        return {
            'vc_metrics': {
                'ROA Discrepancy': {4: '>20 bps', 3: '15-20 bps', 2: '10-15 bps', 1: '<10 bps'},
                'EBIT Margin Disc': {4: '>10 bps', 3: '5-10 bps', 2: '0-5 bps', 1: '<0 bps'},
                'Sales vs GDP': {4: '>4 bps', 3: '4-0 bps', 2: '-2 to 0', 1: '<-2 bps'},
                'Profit vs GDP': {4: '>4 bps', 3: '4-0 bps', 2: '-2 to 0', 1: '<-2 bps'}
            },
            'fp_metrics': {
                'OCF/EBIT Disc': {4: '>10 bps', 3: '5-10 bps', 2: '0-5 bps', 1: '<0 bps'},
                'Equity/Asset Disc': {4: '>10 bps', 3: '5-10 bps', 2: '0-5 bps', 1: '<0 bps'},
                'Cash/Asset Disc': {4: '>10 bps', 3: '5-10 bps', 2: '0-5 bps', 1: '<0 bps'}
            },
            'ss_metrics': {
                'Valuation Upside': {4: '>30%', 3: '15-30%', 2: '0-15%', 1: '<0%'},
                'Growth Rate': {4: '>50%', 3: '25-50%', 2: '5-25%', 1: '<5%'}
            }
        }

