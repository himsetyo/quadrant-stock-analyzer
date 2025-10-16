"""
Quadrant Classifier Module
Mengklasifikasikan saham ke dalam 4 quadrant berdasarkan CS dan SS
"""

class QuadrantClassifier:
    """Classifier untuk menentukan quadrant berdasarkan Company Score dan Stock Score"""
    
    def __init__(self, threshold=3.0):
        """
        Initialize classifier
        
        Args:
            threshold: threshold untuk membedakan High vs Low score (default 3.0)
        """
        self.threshold = threshold
        
        self.quadrants = {
            'STAR': {
                'name': 'STAR',
                'emoji': '⭐',
                'color': '#28a745',  # Green
                'description': 'Strong fundamentals + Attractive valuation',
                'strategy': 'STRONG BUY',
                'characteristics': [
                    'High quality business with proven track record',
                    'Attractive valuation with significant upside',
                    'Positive growth momentum',
                    'Best risk-reward profile'
                ],
                'action': 'Accumulate aggressively',
                'risk_level': 'Low'
            },
            'GROWTH': {
                'name': 'GROWTH',
                'emoji': '📈',
                'color': '#ffc107',  # Yellow/Orange
                'description': 'Weak fundamentals + Attractive valuation',
                'strategy': 'BUY',
                'characteristics': [
                    'Fundamentals still developing or recovering',
                    'Attractive valuation with high upside potential',
                    'Strong growth momentum',
                    'Speculative/turnaround play'
                ],
                'action': 'Buy with caution, monitor fundamentals',
                'risk_level': 'Medium-High'
            },
            'VALUE': {
                'name': 'VALUE',
                'emoji': '💎',
                'color': '#17a2b8',  # Blue
                'description': 'Strong fundamentals + Expensive valuation',
                'strategy': 'HOLD',
                'characteristics': [
                    'High quality business with strong fundamentals',
                    'Limited upside or overvalued',
                    'Weak momentum',
                    'Wait for better entry point'
                ],
                'action': 'Hold existing position, wait for pullback',
                'risk_level': 'Low-Medium'
            },
            'DOG': {
                'name': 'DOG',
                'emoji': '🐕',
                'color': '#dc3545',  # Red
                'description': 'Weak fundamentals + Expensive valuation',
                'strategy': 'SELL/AVOID',
                'characteristics': [
                    'Weak fundamentals and deteriorating business',
                    'Overvalued or no upside',
                    'Negative momentum',
                    'Value trap or declining business'
                ],
                'action': 'Sell or avoid completely',
                'risk_level': 'High'
            }
        }
    
    def classify(self, company_score, stock_score):
        """
        Classify stock into quadrant
        
        Args:
            company_score: Company Score (CS)
            stock_score: Stock Score (SS)
        
        Returns:
            dict with quadrant info
        """
        # Determine quadrant based on threshold
        if company_score >= self.threshold and stock_score >= self.threshold:
            quadrant = 'STAR'
        elif company_score < self.threshold and stock_score >= self.threshold:
            quadrant = 'GROWTH'
        elif company_score >= self.threshold and stock_score < self.threshold:
            quadrant = 'VALUE'
        else:
            quadrant = 'DOG'
        
        # Get quadrant details
        quadrant_info = self.quadrants[quadrant].copy()
        quadrant_info['company_score'] = company_score
        quadrant_info['stock_score'] = stock_score
        quadrant_info['threshold'] = self.threshold
        
        # Add position details
        quadrant_info['position'] = self._get_position_details(
            company_score, stock_score
        )
        
        return quadrant_info
    
    def _get_position_details(self, cs, ss):
        """Get detailed position information"""
        # Distance from threshold
        cs_distance = cs - self.threshold
        ss_distance = ss - self.threshold
        
        # Position strength
        if abs(cs_distance) < 0.3 or abs(ss_distance) < 0.3:
            strength = 'Borderline'
        elif abs(cs_distance) > 0.7 and abs(ss_distance) > 0.7:
            strength = 'Strong'
        else:
            strength = 'Moderate'
        
        return {
            'cs_distance': round(cs_distance, 2),
            'ss_distance': round(ss_distance, 2),
            'strength': strength,
            'cs_category': 'High' if cs >= self.threshold else 'Low',
            'ss_category': 'High' if ss >= self.threshold else 'Low'
        }
    
    def get_investment_recommendation(self, quadrant_info, target_price, 
                                     current_price):
        """
        Generate detailed investment recommendation
        
        Args:
            quadrant_info: dict from classify()
            target_price: target price
            current_price: current price
        
        Returns:
            dict with recommendation details
        """
        quadrant = quadrant_info['name']
        upside = ((target_price - current_price) / current_price) * 100
        
        # Base recommendation from quadrant
        base_rating = {
            'STAR': 'STRONG BUY',
            'GROWTH': 'BUY',
            'VALUE': 'HOLD',
            'DOG': 'SELL'
        }[quadrant]
        
        # Adjust based on position strength
        strength = quadrant_info['position']['strength']
        
        if strength == 'Borderline':
            if quadrant == 'STAR':
                rating = 'BUY'
            elif quadrant == 'GROWTH':
                rating = 'HOLD'
            elif quadrant == 'VALUE':
                rating = 'HOLD'
            else:  # DOG
                rating = 'AVOID'
        else:
            rating = base_rating
        
        # Priority ranking
        priority_map = {
            'STAR': 1,
            'GROWTH': 2,
            'VALUE': 3,
            'DOG': 4
        }
        
        # Risk assessment
        risk_factors = self._assess_risk_factors(quadrant_info)
        
        return {
            'rating': rating,
            'quadrant': quadrant,
            'priority': priority_map[quadrant],
            'target_price': target_price,
            'current_price': current_price,
            'upside': round(upside, 2),
            'risk_level': quadrant_info['risk_level'],
            'action': quadrant_info['action'],
            'risk_factors': risk_factors,
            'time_horizon': self._get_time_horizon(quadrant),
            'position_sizing': self._get_position_sizing(quadrant, strength)
        }
    
    def _assess_risk_factors(self, quadrant_info):
        """Assess risk factors based on scores"""
        cs = quadrant_info['company_score']
        ss = quadrant_info['stock_score']
        
        risks = []
        
        if cs < 2.5:
            risks.append('Weak fundamental quality')
        if ss < 2.5:
            risks.append('Limited upside potential')
        if cs < self.threshold and ss < self.threshold:
            risks.append('Both fundamentals and valuation are weak')
        
        if quadrant_info['position']['strength'] == 'Borderline':
            risks.append('Near threshold - could shift quadrant')
        
        return risks if risks else ['Minimal risk factors']
    
    def _get_time_horizon(self, quadrant):
        """Get recommended time horizon"""
        return {
            'STAR': '12-18 months',
            'GROWTH': '6-12 months (monitor closely)',
            'VALUE': '18-24 months (wait for catalyst)',
            'DOG': 'Exit ASAP'
        }[quadrant]
    
    def _get_position_sizing(self, quadrant, strength):
        """Get recommended position sizing"""
        base_size = {
            'STAR': '5-8%',
            'GROWTH': '3-5%',
            'VALUE': '2-3%',
            'DOG': '0%'
        }[quadrant]
        
        if strength == 'Strong':
            return base_size
        elif strength == 'Borderline':
            return {
                'STAR': '3-5%',
                'GROWTH': '2-3%',
                'VALUE': '1-2%',
                'DOG': '0%'
            }[quadrant]
        else:
            return base_size
    
    def compare_stocks(self, stocks_data):
        """
        Compare multiple stocks and rank them
        
        Args:
            stocks_data: list of dicts with keys [ticker, cs, ss, target_price, current_price]
        
        Returns:
            list of dicts with ranking and recommendations
        """
        results = []
        
        for stock in stocks_data:
            quadrant_info = self.classify(stock['cs'], stock['ss'])
            recommendation = self.get_investment_recommendation(
                quadrant_info,
                stock['target_price'],
                stock['current_price']
            )
            
            results.append({
                'ticker': stock['ticker'],
                'company_score': stock['cs'],
                'stock_score': stock['ss'],
                'quadrant': quadrant_info['name'],
                'rating': recommendation['rating'],
                'priority': recommendation['priority'],
                'upside': recommendation['upside'],
                'risk_level': recommendation['risk_level']
            })
        
        # Sort by priority (STAR > GROWTH > VALUE > DOG)
        results.sort(key=lambda x: (x['priority'], -x['upside']))
        
        return results
    
    def get_quadrant_matrix_data(self):
        """Get quadrant matrix layout data for visualization"""
        return {
            'quadrants': [
                {
                    'name': 'GROWTH',
                    'position': {'x': [0, 3], 'y': [3, 4]},
                    'color': self.quadrants['GROWTH']['color'],
                    'label_pos': {'x': 1.5, 'y': 3.5}
                },
                {
                    'name': 'STAR',
                    'position': {'x': [3, 4], 'y': [3, 4]},
                    'color': self.quadrants['STAR']['color'],
                    'label_pos': {'x': 3.5, 'y': 3.5}
                },
                {
                    'name': 'DOG',
                    'position': {'x': [0, 3], 'y': [0, 3]},
                    'color': self.quadrants['DOG']['color'],
                    'label_pos': {'x': 1.5, 'y': 1.5}
                },
                {
                    'name': 'VALUE',
                    'position': {'x': [3, 4], 'y': [0, 3]},
                    'color': self.quadrants['VALUE']['color'],
                    'label_pos': {'x': 3.5, 'y': 1.5}
                }
            ],
            'threshold': self.threshold,
            'axes': {
                'x': {'label': 'Company Score (CS)', 'range': [1, 4]},
                'y': {'label': 'Stock Score (SS)', 'range': [1, 4]}
            }
        }

