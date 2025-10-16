"""
Visualizer Module
Generate charts and visualizations untuk Quadrant Matrix
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class QuadrantVisualizer:
    """Visualizer untuk Quadrant Matrix dan score breakdowns"""
    
    def __init__(self):
        self.colors = {
            'STAR': '#28a745',
            'GROWTH': '#ffc107',
            'VALUE': '#17a2b8',
            'DOG': '#dc3545'
        }
    
    def create_quadrant_matrix(self, stocks_data, threshold=3.0):
        """
        Create Quadrant Matrix scatter plot
        
        Args:
            stocks_data: list of dicts with keys [ticker, cs, ss, quadrant]
            threshold: threshold line (default 3.0)
        
        Returns:
            plotly figure
        """
        fig = go.Figure()
        
        # Add quadrant background rectangles
        quadrants = [
            {'name': 'DOG', 'x': [1, threshold], 'y': [1, threshold], 'color': 'rgba(220, 53, 69, 0.1)'},
            {'name': 'VALUE', 'x': [threshold, 4], 'y': [1, threshold], 'color': 'rgba(23, 162, 184, 0.1)'},
            {'name': 'GROWTH', 'x': [1, threshold], 'y': [threshold, 4], 'color': 'rgba(255, 193, 7, 0.1)'},
            {'name': 'STAR', 'x': [threshold, 4], 'y': [threshold, 4], 'color': 'rgba(40, 167, 69, 0.1)'}
        ]
        
        for quad in quadrants:
            fig.add_shape(
                type="rect",
                x0=quad['x'][0], x1=quad['x'][1],
                y0=quad['y'][0], y1=quad['y'][1],
                fillcolor=quad['color'],
                line=dict(width=0),
                layer='below'
            )
            
            # Add quadrant labels
            mid_x = (quad['x'][0] + quad['x'][1]) / 2
            mid_y = (quad['y'][0] + quad['y'][1]) / 2
            fig.add_annotation(
                x=mid_x, y=mid_y,
                text=f"<b>{quad['name']}</b>",
                showarrow=False,
                font=dict(size=16, color='gray'),
                opacity=0.3
            )
        
        # Add threshold lines
        fig.add_hline(y=threshold, line_dash="dash", line_color="gray", 
                     annotation_text="Threshold", annotation_position="right")
        fig.add_vline(x=threshold, line_dash="dash", line_color="gray",
                     annotation_text="Threshold", annotation_position="top")
        
        # Add stocks as scatter points
        for stock in stocks_data:
            fig.add_trace(go.Scatter(
                x=[stock['cs']],
                y=[stock['ss']],
                mode='markers+text',
                name=stock['ticker'],
                text=[stock['ticker']],
                textposition='top center',
                marker=dict(
                    size=15,
                    color=self.colors.get(stock['quadrant'], 'gray'),
                    line=dict(width=2, color='white')
                ),
                hovertemplate=(
                    f"<b>{stock['ticker']}</b><br>" +
                    f"Company Score: {stock['cs']:.2f}<br>" +
                    f"Stock Score: {stock['ss']:.2f}<br>" +
                    f"Quadrant: {stock['quadrant']}<br>" +
                    "<extra></extra>"
                )
            ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': '<b>Quadrant Matrix Classification</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis=dict(
                title='<b>Company Score (CS)</b>',
                range=[1, 4],
                dtick=0.5,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='<b>Stock Score (SS)</b>',
                range=[1, 4],
                dtick=0.5,
                gridcolor='lightgray'
            ),
            plot_bgcolor='white',
            showlegend=False,
            height=600,
            width=800
        )
        
        return fig
    
    def create_score_breakdown(self, cs_result, ss_result):
        """
        Create score breakdown bar chart
        
        Args:
            cs_result: dict from calculator.calculate_company_score()
            ss_result: dict from calculator.calculate_stock_score()
        
        Returns:
            plotly figure
        """
        # Prepare data
        categories = ['VCS', 'VC', 'FP', 'Valuation', 'Growth']
        scores = [
            cs_result['vcs_score'],
            cs_result['vc_score'],
            cs_result['fp_score'],
            ss_result['valuation_score'],
            ss_result['growth_score']
        ]
        weights = [0.50, 0.35, 0.15, 0.65, 0.35]
        weighted_scores = [
            cs_result['vcs_weighted'],
            cs_result['vc_weighted'],
            cs_result['fp_weighted'],
            ss_result['valuation_weighted'],
            ss_result['growth_weighted']
        ]
        
        colors_list = ['#4472C4', '#4472C4', '#4472C4', '#70AD47', '#70AD47']
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Raw Scores', 'Weighted Contribution'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Raw scores
        fig.add_trace(
            go.Bar(
                x=categories,
                y=scores,
                name='Raw Score',
                marker_color=colors_list,
                text=[f'{s:.2f}' for s in scores],
                textposition='outside',
                hovertemplate='%{x}<br>Score: %{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Weighted scores
        fig.add_trace(
            go.Bar(
                x=categories,
                y=weighted_scores,
                name='Weighted',
                marker_color=colors_list,
                text=[f'{w:.2f}' for w in weighted_scores],
                textposition='outside',
                hovertemplate='%{x}<br>Weighted: %{y:.2f}<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text='<b>Score Breakdown Analysis</b>',
            showlegend=False,
            height=400
        )
        
        fig.update_yaxes(title_text='Score', range=[0, 4.5], row=1, col=1)
        fig.update_yaxes(title_text='Weighted Score', range=[0, 3], row=1, col=2)
        
        return fig
    
    def create_component_radar(self, vcs_data, vc_data, fp_data):
        """
        Create radar chart for component scores
        
        Args:
            vcs_data: dict with VCS components
            vc_data: dict with VC components
            fp_data: dict with FP components
        
        Returns:
            plotly figure
        """
        # VCS components
        vcs_categories = ['Lifecycle', 'Porter', 'Management', 'ESG']
        vcs_values = [
            vcs_data['lifecycle'],
            vcs_data['porter'],
            vcs_data['management'],
            vcs_data['esg']
        ]
        
        # VC components
        vc_categories = ['ROA', 'EBIT Margin', 'Sales Growth', 'Profit Growth']
        vc_values = [
            vc_data['roa'],
            vc_data['ebit_margin'],
            vc_data['sales_growth'],
            vc_data['profit_growth']
        ]
        
        # FP components
        fp_categories = ['OCF/EBIT', 'Equity/Asset', 'Cash/Asset']
        fp_values = [
            fp_data['ocf_ebit'],
            fp_data['equity_asset'],
            fp_data['cash_asset']
        ]
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('VCS Components', 'VC Components', 'FP Components'),
            specs=[[{'type': 'scatterpolar'}, {'type': 'scatterpolar'}, {'type': 'scatterpolar'}]]
        )
        
        # VCS radar
        fig.add_trace(
            go.Scatterpolar(
                r=vcs_values + [vcs_values[0]],
                theta=vcs_categories + [vcs_categories[0]],
                fill='toself',
                name='VCS',
                marker_color='#4472C4'
            ),
            row=1, col=1
        )
        
        # VC radar
        fig.add_trace(
            go.Scatterpolar(
                r=vc_values + [vc_values[0]],
                theta=vc_categories + [vc_categories[0]],
                fill='toself',
                name='VC',
                marker_color='#70AD47'
            ),
            row=1, col=2
        )
        
        # FP radar
        fig.add_trace(
            go.Scatterpolar(
                r=fp_values + [fp_values[0]],
                theta=fp_categories + [fp_categories[0]],
                fill='toself',
                name='FP',
                marker_color='#FFC000'
            ),
            row=1, col=3
        )
        
        # Update layout
        fig.update_layout(
            title_text='<b>Component Analysis</b>',
            showlegend=False,
            height=400,
            polar=dict(radialaxis=dict(range=[0, 4]))
        )
        
        return fig
    
    def create_comparison_chart(self, stocks_comparison):
        """
        Create comparison chart for multiple stocks
        
        Args:
            stocks_comparison: list of dicts from classifier.compare_stocks()
        
        Returns:
            plotly figure
        """
        tickers = [s['ticker'] for s in stocks_comparison]
        cs_scores = [s['company_score'] for s in stocks_comparison]
        ss_scores = [s['stock_score'] for s in stocks_comparison]
        upsides = [s['upside'] for s in stocks_comparison]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Company Score', 'Stock Score', 'Upside Potential', 'Quadrant Distribution'),
            specs=[
                [{'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'pie'}]
            ]
        )
        
        # Company Score
        fig.add_trace(
            go.Bar(x=tickers, y=cs_scores, name='CS', marker_color='#4472C4',
                   text=[f'{s:.2f}' for s in cs_scores], textposition='outside'),
            row=1, col=1
        )
        
        # Stock Score
        fig.add_trace(
            go.Bar(x=tickers, y=ss_scores, name='SS', marker_color='#70AD47',
                   text=[f'{s:.2f}' for s in ss_scores], textposition='outside'),
            row=1, col=2
        )
        
        # Upside
        colors_upside = ['green' if u > 0 else 'red' for u in upsides]
        fig.add_trace(
            go.Bar(x=tickers, y=upsides, name='Upside', marker_color=colors_upside,
                   text=[f'{u:.1f}%' for u in upsides], textposition='outside'),
            row=2, col=1
        )
        
        # Quadrant distribution
        quadrant_counts = {}
        for s in stocks_comparison:
            q = s['quadrant']
            quadrant_counts[q] = quadrant_counts.get(q, 0) + 1
        
        fig.add_trace(
            go.Pie(
                labels=list(quadrant_counts.keys()),
                values=list(quadrant_counts.values()),
                marker=dict(colors=[self.colors[q] for q in quadrant_counts.keys()])
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text='<b>Multi-Stock Comparison</b>',
            showlegend=False,
            height=700
        )
        
        fig.update_yaxes(title_text='Score', range=[0, 4.5], row=1, col=1)
        fig.update_yaxes(title_text='Score', range=[0, 4.5], row=1, col=2)
        fig.update_yaxes(title_text='Upside (%)', row=2, col=1)
        
        return fig

