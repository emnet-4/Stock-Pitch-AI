"""
Free AI Alternative using Hugging Face models
This provides a cost-free option for basic stock analysis
"""

import os
from typing import Dict, Any
import requests
import sys
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger

class FreeStockAnalyzer:
    """Free stock analyzer using Hugging Face models."""
    
    def __init__(self):
        self.logger = setup_logger()
        self.hf_api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        # Note: You can use Hugging Face models for free with their API
        
    def analyze_stock_free(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive free stock analysis with full data structure.
        Uses rule-based analysis + financial calculations.
        """
        try:
            self.logger.info(f"Starting free analysis for {stock_data.get('symbol', 'UNKNOWN')}")
            
            # Rule-based analysis (completely free) - this now includes valuation analysis
            analysis = self._rule_based_analysis(stock_data)
            
            # Get the valuation analysis that was already performed in _rule_based_analysis
            valuation_analysis = analysis.get('valuation_analysis', {})
            
            # Add comprehensive structure expected by presentation generator
            analysis.update({
                'analysis_date': datetime.now().isoformat(),
                'ai_analysis': self._generate_detailed_analysis_text(stock_data, analysis),
                'financial_ratios': self._calculate_basic_ratios(stock_data),
                'valuation': valuation_analysis,  # This includes DCF and WACC
                'investment_thesis': analysis.get('investment_thesis', ''),
                'metrics': {
                    'current_price': stock_data.get('current_price'),
                    'market_cap': stock_data.get('market_cap'),
                    'pe_ratio': stock_data.get('pe_ratio'),
                    'eps': stock_data.get('eps'),
                    '52w_high': stock_data.get('52w_high'),
                    '52w_low': stock_data.get('52w_low'),
                    'dividend_yield': stock_data.get('dividend_yield'),
                    'beta': stock_data.get('beta')
                },
                'key_highlights': self._generate_key_highlights(stock_data, analysis),
                'risks': self._identify_financial_risks(stock_data),
                'recommendation': analysis.get('recommendation', 'HOLD'),
                # Add DCF and WACC values to top level for easy access
                'dcf_value': valuation_analysis.get('dcf_analysis', {}).get('fair_value', 0),
                'wacc': valuation_analysis.get('wacc_analysis', {}).get('wacc_percentage', 0)
            })
            
            self.logger.info(f"Free analysis completed for {stock_data.get('symbol', 'UNKNOWN')}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in free analysis: {str(e)}")
            return self._fallback_analysis(stock_data)
    
    def _rule_based_analysis(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analysis using financial rules (no AI needed)."""
        
        current_price = stock_data.get('current_price', 0)
        pe_ratio = stock_data.get('pe_ratio', 0)
        market_cap = stock_data.get('market_cap', 0)
        beta = stock_data.get('beta', 0)
        dividend_yield = stock_data.get('dividend_yield', 0)
        eps = stock_data.get('eps', 0)
        
        # Enhanced valuation rules with DCF integration
        basic_recommendation = "HOLD"
        basic_valuation = "Fair value"
        
        # Basic P/E analysis
        if pe_ratio and pe_ratio < 12:
            basic_valuation = "Significantly undervalued"
            basic_recommendation = "STRONG BUY"
            price_target = current_price * 1.25  # 25% upside
        elif pe_ratio and pe_ratio < 18:
            basic_valuation = "Moderately undervalued"
            basic_recommendation = "BUY"
            price_target = current_price * 1.15  # 15% upside
        elif pe_ratio and pe_ratio > 35:
            basic_valuation = "Significantly overvalued"
            basic_recommendation = "SELL"
            price_target = current_price * 0.85  # 15% downside
        elif pe_ratio and pe_ratio > 25:
            basic_valuation = "Moderately overvalued"
            basic_recommendation = "HOLD"
            price_target = current_price * 0.95  # 5% downside
        else:
            basic_valuation = "Fair value"
            basic_recommendation = "HOLD"
            price_target = current_price * 1.05  # 5% upside
        
        # Perform valuation analysis first to get DCF insights
        valuation_analysis = self._perform_basic_valuation(stock_data)
        
        # Integrate DCF analysis into recommendation
        final_recommendation = basic_recommendation
        final_valuation = basic_valuation
        
        dcf_analysis = valuation_analysis.get('dcf_analysis', {})
        if dcf_analysis.get('status') == 'Completed':
            dcf_assessment = dcf_analysis.get('assessment', '')
            dcf_fair_value = dcf_analysis.get('fair_value', current_price)
            
            # Adjust recommendation based on DCF
            if dcf_assessment == "Significantly Undervalued":
                if basic_recommendation in ["HOLD", "BUY"]:
                    final_recommendation = "STRONG BUY"
                elif basic_recommendation == "SELL":
                    final_recommendation = "HOLD"  # DCF suggests undervaluation
                price_target = max(price_target, dcf_fair_value * 0.9)  # Use 90% of DCF value as target
            elif dcf_assessment == "Undervalued":
                if basic_recommendation == "HOLD":
                    final_recommendation = "BUY"
                elif basic_recommendation == "SELL":
                    final_recommendation = "HOLD"
                price_target = max(price_target, dcf_fair_value * 0.95)
            elif dcf_assessment == "Significantly Overvalued":
                if basic_recommendation in ["STRONG BUY", "BUY"]:
                    final_recommendation = "HOLD"
                elif basic_recommendation == "HOLD":
                    final_recommendation = "SELL"
                price_target = min(price_target, dcf_fair_value * 1.1)
            elif dcf_assessment == "Overvalued":
                if basic_recommendation == "STRONG BUY":
                    final_recommendation = "BUY"
                elif basic_recommendation == "BUY":
                    final_recommendation = "HOLD"
                price_target = min(price_target, dcf_fair_value * 1.05)
        
        # Generate comprehensive analysis structure
        return {
            'symbol': stock_data.get('symbol', ''),
            'company_name': stock_data.get('company_name', ''),
            'current_price': current_price,
            'target_price': round(price_target, 2) if price_target else current_price,
            'price_target_12m': round(price_target, 2) if price_target else current_price,
            'valuation_assessment': final_valuation,
            'recommendation': final_recommendation,
            'investment_thesis': self._generate_investment_thesis(stock_data, final_valuation, final_recommendation),
            'key_metrics': {
                'pe_ratio': pe_ratio,
                'market_cap': market_cap,
                'beta': beta,
                'dividend_yield': dividend_yield,
                'eps': eps,
                'current_price': current_price,
                'price_performance': self._calculate_price_performance(stock_data)
            },
            'analysis_type': 'Rule-based Fundamental Analysis (Free)',
            'analyst_rating': final_recommendation,
            'upside_potential': f"{((price_target - current_price) / current_price * 100):.1f}%" if price_target and current_price else "N/A",
            'investment_horizon': "12 months",
            'risk_level': self._assess_risk_level(stock_data),
            'sector_outlook': self._generate_sector_outlook(stock_data),
            'key_catalysts': self._identify_catalysts(stock_data),
            'competitive_position': self._assess_competitive_position(stock_data),
            'financial_strength': self._assess_financial_strength(stock_data),
            'growth_prospects': self._assess_growth_prospects(stock_data),
            'valuation_analysis': valuation_analysis  # Include the detailed valuation analysis
        }
    
    def _generate_basic_summary(self, stock_data: Dict[str, Any]) -> str:
        """Generate a basic summary without premium AI."""
        company = stock_data.get('company_name', 'Company')
        sector = stock_data.get('sector', 'Unknown')
        
        return f"""
        {company} operates in the {sector} sector. 
        Based on current financial metrics, the stock shows standard market characteristics.
        This analysis is based on quantitative rules and publicly available financial data.
        For more detailed AI-powered insights, consider upgrading to the premium OpenAI-powered analysis.
        """
    
    def _fallback_analysis(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis if everything else fails."""
        return {
            'symbol': stock_data.get('symbol', ''),
            'company_name': stock_data.get('company_name', ''),
            'analysis_type': 'Basic (Free)',
            'recommendation': 'HOLD',
            'note': 'Limited analysis available. Consider premium features for detailed insights.'
        }

    def _generate_detailed_analysis_text(self, stock_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate detailed analysis text for the presentation."""
        symbol = stock_data.get('symbol', '')
        company_name = stock_data.get('company_name', '')
        current_price = stock_data.get('current_price', 0)
        pe_ratio = stock_data.get('pe_ratio', 0)
        market_cap = stock_data.get('market_cap', 0)
        target_price = analysis.get('target_price', current_price)
        
        return f"""
        # {company_name} ({symbol}) - Investment Analysis
        
        ## Executive Summary
        {company_name} presents a {analysis.get('recommendation', 'HOLD').lower()} opportunity with our 12-month price target of ${target_price:.2f}, representing {analysis.get('upside_potential', 'N/A')} potential upside from current levels.
        
        ## Current Market Position
        - **Current Price**: ${current_price:.2f}
        - **Market Capitalization**: ${market_cap:,.0f} ({self._format_market_cap(market_cap)})
        - **P/E Ratio**: {pe_ratio:.2f}x
        - **Risk Level**: {analysis.get('risk_level', 'MODERATE')}
        
        ## Valuation Assessment
        Our analysis indicates the stock is **{analysis.get('valuation_assessment', 'fairly valued')}** based on:
        - Price-to-earnings ratio of {pe_ratio:.2f}x vs sector average
        - {analysis.get('financial_strength', 'Moderate financial strength')}
        - {analysis.get('competitive_position', 'Established market position')}
        
        ## Investment Thesis
        {analysis.get('investment_thesis', 'Standard investment profile with balanced risk-return characteristics.')}
        
        ## Key Investment Highlights
        - **Recommendation**: {analysis.get('recommendation', 'HOLD')}
        - **Price Target**: ${target_price:.2f} (12-month)
        - **Investment Horizon**: {analysis.get('investment_horizon', '12 months')}
        - **Sector Outlook**: {analysis.get('sector_outlook', 'Sector-specific dynamics apply')}
        
        ## Financial Metrics Summary
        - **Beta**: {stock_data.get('beta', 'N/A')} ({self._interpret_beta(stock_data.get('beta', 0))})
        - **Dividend Yield**: {stock_data.get('dividend_yield', 0):.2%}
        - **52-Week Range**: ${stock_data.get('52w_low', 0):.2f} - ${stock_data.get('52w_high', 0):.2f}
        
        ## Growth Prospects
        {analysis.get('growth_prospects', 'Balanced growth profile with moderate expansion expected.')}
        
        ## Risk Assessment
        - **Overall Risk Level**: {analysis.get('risk_level', 'MODERATE RISK')}
        - **Key Risk Factors**: Market volatility, sector-specific headwinds, economic sensitivity
        - **Mitigation**: Diversification recommended, position sizing appropriate to risk tolerance
        
        ## Analyst Recommendation
        **{analysis.get('recommendation', 'HOLD')}** - Based on fundamental analysis of financial metrics, valuation parameters, and market positioning.
        
        *This analysis is generated using rule-based fundamental analysis. For enhanced AI-powered insights including sentiment analysis, technical indicators, and market dynamics, consider upgrading to our premium OpenAI-powered analysis.*
        """

    def _calculate_basic_ratios(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate basic financial ratios."""
        ratios = {}
        
        # P/E Ratio
        pe_ratio = stock_data.get('pe_ratio', 0)
        if pe_ratio:
            ratios['pe_ratio'] = pe_ratio
            if pe_ratio < 15:
                ratios['pe_assessment'] = 'Low (Potentially undervalued)'
            elif pe_ratio > 30:
                ratios['pe_assessment'] = 'High (Potentially overvalued)'
            else:
                ratios['pe_assessment'] = 'Moderate (Fair value)'
        
        # Price-to-Book (if available)
        pb_ratio = stock_data.get('pb_ratio', 0)
        if pb_ratio:
            ratios['pb_ratio'] = pb_ratio
            ratios['pb_assessment'] = 'Low' if pb_ratio < 1.5 else 'High'
        
        # Dividend Yield
        dividend_yield = stock_data.get('dividend_yield', 0)
        if dividend_yield:
            ratios['dividend_yield'] = dividend_yield
            ratios['dividend_assessment'] = 'High' if dividend_yield > 0.03 else 'Low'
        
        # Beta (volatility measure)
        beta = stock_data.get('beta', 0)
        if beta:
            ratios['beta'] = beta
            if beta < 1:
                ratios['beta_assessment'] = 'Low volatility (Defensive)'
            elif beta > 1.5:
                ratios['beta_assessment'] = 'High volatility (Aggressive)'
            else:
                ratios['beta_assessment'] = 'Moderate volatility'
        
        return ratios

    def _perform_basic_valuation(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive valuation analysis using multiple methods."""
        current_price = stock_data.get('current_price', 0)
        
        # Run all valuation methods
        dcf_valuation = self._calculate_dcf_valuation(stock_data)
        wacc_analysis = self._calculate_wacc(stock_data)
        financial_statement_analysis = self._analyze_financial_statements(stock_data)
        comparative_valuation = self._calculate_comparative_valuation(stock_data)
        
        # Combine all valuation methods
        valuation = {
            'current_price': current_price,
            'methods': ['DCF', 'WACC', 'Financial Statement Analysis', 'Comparative Valuation'],
            'dcf_analysis': dcf_valuation,
            'wacc_analysis': wacc_analysis,
            'financial_statement_analysis': financial_statement_analysis,
            'comparative_valuation': comparative_valuation,
            'weighted_fair_value': self._calculate_weighted_fair_value(dcf_valuation, comparative_valuation, current_price),
            'assessment': self._determine_overall_valuation_assessment(dcf_valuation, comparative_valuation, current_price)
        }
        
        return valuation

    def _generate_key_highlights(self, stock_data: Dict[str, Any], analysis: Dict[str, Any]) -> list:
        """Generate key highlights for the presentation."""
        highlights = []
        
        # Price-based highlights
        current_price = stock_data.get('current_price', 0)
        high_52w = stock_data.get('52w_high', 0)
        low_52w = stock_data.get('52w_low', 0)
        
        if current_price and high_52w and low_52w:
            position_in_range = (current_price - low_52w) / (high_52w - low_52w)
            if position_in_range < 0.3:
                highlights.append(f"Trading near 52-week low (${low_52w:.2f})")
            elif position_in_range > 0.7:
                highlights.append(f"Trading near 52-week high (${high_52w:.2f})")
        
        # P/E ratio highlights
        pe_ratio = stock_data.get('pe_ratio', 0)
        if pe_ratio:
            if pe_ratio < 15:
                highlights.append(f"Low P/E ratio of {pe_ratio:.1f} suggests potential value")
            elif pe_ratio > 30:
                highlights.append(f"High P/E ratio of {pe_ratio:.1f} indicates growth premium")
        
        # Market cap highlights
        market_cap = stock_data.get('market_cap', 0)
        if market_cap:
            if market_cap > 10e9:  # $10B+
                highlights.append("Large-cap stock with established market presence")
            elif market_cap > 2e9:  # $2B+
                highlights.append("Mid-cap stock with growth potential")
            else:
                highlights.append("Small-cap stock with higher growth/risk profile")
        
        # Dividend highlights
        dividend_yield = stock_data.get('dividend_yield', 0)
        if dividend_yield and dividend_yield > 0.02:
            highlights.append(f"Dividend yield of {dividend_yield:.1%} provides income")
        
        # Volatility highlights
        beta = stock_data.get('beta', 0)
        if beta:
            if beta < 0.8:
                highlights.append("Low beta suggests defensive characteristics")
            elif beta > 1.5:
                highlights.append("High beta indicates growth/cyclical nature")
        
        # Default highlights if none generated
        if not highlights:
            highlights = [
                "Rule-based analysis completed",
                "Consider upgrading for AI-powered insights",
                "Diversification recommended"
            ]
        
        return highlights

    def _identify_financial_risks(self, stock_data: Dict[str, Any]) -> list:
        """Identify potential financial risks."""
        risks = []
        
        # High P/E ratio risk
        pe_ratio = stock_data.get('pe_ratio', 0)
        if pe_ratio and pe_ratio > 40:
            risks.append("High P/E ratio suggests elevated valuation risk")
        
        # High volatility risk
        beta = stock_data.get('beta', 0)
        if beta and beta > 1.5:
            risks.append("High beta indicates above-average market sensitivity")
        
        # Low dividend risk (for income investors)
        dividend_yield = stock_data.get('dividend_yield', 0)
        if not dividend_yield or dividend_yield < 0.01:
            risks.append("Low/no dividend yield - not suitable for income-focused portfolios")
        
        # Market cap risks
        market_cap = stock_data.get('market_cap', 0)
        if market_cap and market_cap < 2e9:  # Less than $2B
            risks.append("Small market cap increases liquidity and volatility risks")
        
        # Price position risks
        current_price = stock_data.get('current_price', 0)
        high_52w = stock_data.get('52w_high', 0)
        if current_price and high_52w and (current_price / high_52w) > 0.95:
            risks.append("Trading near 52-week high - limited upside potential")
        
        # Default risks if none identified
        if not risks:
            risks = [
                "General market volatility",
                "Sector-specific risks",
                "Economic cycle sensitivity"
            ]
        
        return risks

    def _assess_financial_health(self, stock_data: Dict[str, Any]) -> str:
        """Assess overall financial health."""
        health_factors = []
        
        # P/E ratio health
        pe_ratio = stock_data.get('pe_ratio', 0)
        if pe_ratio and 10 <= pe_ratio <= 25:
            health_factors.append("reasonable")
        elif pe_ratio and pe_ratio < 10:
            health_factors.append("strong value")
        elif pe_ratio and pe_ratio > 30:
            health_factors.append("growth-oriented")
        
        # Market cap stability
        market_cap = stock_data.get('market_cap', 0)
        if market_cap and market_cap > 10e9:
            health_factors.append("stable")
        
        # Dividend health
        dividend_yield = stock_data.get('dividend_yield', 0)
        if dividend_yield and dividend_yield > 0.02:
            health_factors.append("income-generating")
        
        if health_factors:
            return f"{' and '.join(health_factors)} characteristics"
        else:
            return "mixed financial characteristics"

    def _generate_investment_thesis(self, stock_data: Dict[str, Any], valuation: str, recommendation: str) -> str:
        """Generate a compelling investment thesis."""
        company_name = stock_data.get('company_name', 'Company')
        symbol = stock_data.get('symbol', '')
        current_price = stock_data.get('current_price', 0)
        pe_ratio = stock_data.get('pe_ratio', 0)
        market_cap = stock_data.get('market_cap', 0)
        
        # Create a compelling thesis based on the data
        thesis_parts = []
        
        # Add market position
        if market_cap:
            if market_cap > 10e9:
                thesis_parts.append(f"{company_name} is a large-cap stock with established market presence")
            elif market_cap > 2e9:
                thesis_parts.append(f"{company_name} is a mid-cap stock with significant growth potential")
            else:
                thesis_parts.append(f"{company_name} is a small-cap stock with high growth prospects")
        
        # Add valuation perspective
        if valuation == "Potentially undervalued":
            thesis_parts.append("trading at attractive valuation levels")
        elif valuation == "Potentially overvalued":
            thesis_parts.append("reflecting premium growth expectations")
        else:
            thesis_parts.append("trading at fair market value")
        
        # Add recommendation rationale
        if recommendation == "BUY":
            thesis_parts.append("presenting a compelling investment opportunity with upside potential")
        elif recommendation == "SELL":
            thesis_parts.append("facing headwinds that warrant caution")
        else:
            thesis_parts.append("suitable for portfolio diversification with balanced risk-return profile")
        
        return f"{', '.join(thesis_parts)}. Our analysis suggests a {recommendation} rating based on fundamental metrics."
    
    def _calculate_price_performance(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate price performance metrics."""
        current_price = stock_data.get('current_price', 0)
        high_52w = stock_data.get('52w_high', 0)
        low_52w = stock_data.get('52w_low', 0)
        
        performance = {}
        
        if current_price and high_52w and low_52w:
            performance['52w_performance'] = f"{((current_price - low_52w) / low_52w * 100):.1f}%"
            performance['distance_from_high'] = f"{((high_52w - current_price) / high_52w * 100):.1f}%"
            performance['position_in_range'] = f"{((current_price - low_52w) / (high_52w - low_52w) * 100):.1f}%"
        
        return performance

    def _assess_risk_level(self, stock_data: Dict[str, Any]) -> str:
        """Assess overall risk level."""
        risk_factors = 0
        
        # Beta risk
        beta = stock_data.get('beta', 0)
        if beta > 1.5:
            risk_factors += 2
        elif beta > 1.2:
            risk_factors += 1
        
        # P/E ratio risk
        pe_ratio = stock_data.get('pe_ratio', 0)
        if pe_ratio > 40:
            risk_factors += 2
        elif pe_ratio > 25:
            risk_factors += 1
        
        # Market cap risk
        market_cap = stock_data.get('market_cap', 0)
        if market_cap < 2e9:  # < $2B
            risk_factors += 2
        elif market_cap < 10e9:  # < $10B
            risk_factors += 1
        
        if risk_factors >= 4:
            return "HIGH RISK"
        elif risk_factors >= 2:
            return "MODERATE RISK"
        else:
            return "LOW RISK"

    def _generate_sector_outlook(self, stock_data: Dict[str, Any]) -> str:
        """Generate sector outlook."""
        sector = stock_data.get('sector', 'Unknown')
        
        sector_outlooks = {
            'Technology': 'Positive long-term growth driven by digital transformation',
            'Healthcare': 'Stable growth supported by aging demographics',
            'Financial Services': 'Cyclical performance tied to interest rates',
            'Consumer Discretionary': 'Sensitive to economic cycles and consumer spending',
            'Consumer Staples': 'Defensive characteristics with steady demand',
            'Energy': 'Volatile sector dependent on commodity prices',
            'Industrials': 'Cyclical growth tied to economic expansion',
            'Materials': 'Commodity-dependent with cyclical patterns',
            'Real Estate': 'Interest rate sensitive with income generation',
            'Utilities': 'Defensive sector with stable dividend yields',
            'Communication Services': 'Mixed growth driven by media and telecom trends'
        }
        
        return sector_outlooks.get(sector, 'Sector-specific dynamics require careful analysis')

    def _identify_catalysts(self, stock_data: Dict[str, Any]) -> list:
        """Identify potential catalysts."""
        catalysts = []
        
        # P/E-based catalysts
        pe_ratio = stock_data.get('pe_ratio', 0)
        if pe_ratio and pe_ratio < 15:
            catalysts.append("Potential re-rating as market recognizes value")
        elif pe_ratio > 30:
            catalysts.append("Earnings growth needed to justify valuation")
        
        # Dividend catalysts
        dividend_yield = stock_data.get('dividend_yield', 0)
        if dividend_yield and dividend_yield > 0.04:
            catalysts.append("Attractive dividend yield in low-rate environment")
        
        # Market cap catalysts
        market_cap = stock_data.get('market_cap', 0)
        if market_cap and market_cap < 2e9:
            catalysts.append("Potential acquisition target")
        elif market_cap > 50e9:
            catalysts.append("Index inclusion and institutional buying")
        
        # Beta catalysts
        beta = stock_data.get('beta', 0)
        if beta and beta < 0.8:
            catalysts.append("Defensive characteristics in volatile markets")
        
        # Default catalysts
        if not catalysts:
            catalysts = [
                "Earnings growth acceleration",
                "Market sentiment improvement",
                "Sector rotation benefits"
            ]
        
        return catalysts

    def _assess_competitive_position(self, stock_data: Dict[str, Any]) -> str:
        """Assess competitive position."""
        market_cap = stock_data.get('market_cap', 0)
        
        if market_cap > 100e9:
            return "Market leader with significant competitive advantages"
        elif market_cap > 10e9:
            return "Established player with solid market position"
        elif market_cap > 2e9:
            return "Growing company with emerging market presence"
        else:
            return "Smaller player with niche opportunities"

    def _assess_financial_strength(self, stock_data: Dict[str, Any]) -> str:
        """Assess financial strength."""
        strength_score = 0
        
        # P/E ratio strength
        pe_ratio = stock_data.get('pe_ratio', 0)
        if pe_ratio and 10 <= pe_ratio <= 20:
            strength_score += 1
        
        # Dividend strength
        dividend_yield = stock_data.get('dividend_yield', 0)
        if dividend_yield and dividend_yield > 0.02:
            strength_score += 1
        
        # Market cap strength
        market_cap = stock_data.get('market_cap', 0)
        if market_cap and market_cap > 10e9:
            strength_score += 1
        
        if strength_score >= 3:
            return "Strong financial foundation"
        elif strength_score >= 2:
            return "Solid financial position"
        else:
            return "Moderate financial strength"

    def _assess_growth_prospects(self, stock_data: Dict[str, Any]) -> str:
        """Assess growth prospects."""
        pe_ratio = stock_data.get('pe_ratio', 0)
        beta = stock_data.get('beta', 0)
        
        if pe_ratio and pe_ratio > 25:
            if beta and beta > 1.2:
                return "High growth expectations with elevated risk"
            else:
                return "Growth premium reflected in valuation"
        elif pe_ratio and pe_ratio < 15:
            return "Value opportunity with potential upside"
        else:
            return "Balanced growth and value characteristics"
    
    def _format_market_cap(self, market_cap: float) -> str:
        """Format market cap for display."""
        if market_cap > 1e12:
            return f"${market_cap/1e12:.1f}T"
        elif market_cap > 1e9:
            return f"${market_cap/1e9:.1f}B"
        elif market_cap > 1e6:
            return f"${market_cap/1e6:.1f}M"
        else:
            return f"${market_cap:,.0f}"

    def _interpret_beta(self, beta: float) -> str:
        """Interpret beta value."""
        if beta < 0.8:
            return "Low volatility"
        elif beta > 1.5:
            return "High volatility"
        else:
            return "Moderate volatility"
    
    def _calculate_dcf_valuation(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Discounted Cash Flow (DCF) valuation."""
        try:
            eps = stock_data.get('eps', 0)
            current_price = stock_data.get('current_price', 0)
            
            if not eps:
                return {
                    'method': 'DCF Analysis',
                    'status': 'Insufficient data',
                    'fair_value': current_price,
                    'assessment': 'Unable to calculate'
                }
            
            # DCF assumptions - adjust based on company characteristics
            market_cap = stock_data.get('market_cap', 0)
            pe_ratio = stock_data.get('pe_ratio', 0)
            
            # Dynamic growth assumptions based on company size and valuation
            if market_cap > 1e12:  # Mega-cap (>$1T)
                growth_rate_5y = 0.06  # 6% growth for mega-cap
                terminal_growth_rate = 0.025  # 2.5% terminal growth
                discount_rate = 0.08  # 8% discount rate for stable mega-cap
            elif market_cap > 200e9:  # Large-cap ($200B+)
                growth_rate_5y = 0.08  # 8% growth for large-cap
                terminal_growth_rate = 0.03  # 3% terminal growth
                discount_rate = 0.09  # 9% discount rate
            elif market_cap > 10e9:  # Mid-cap ($10B+)
                growth_rate_5y = 0.10  # 10% growth for mid-cap
                terminal_growth_rate = 0.035  # 3.5% terminal growth
                discount_rate = 0.10  # 10% discount rate
            else:  # Small-cap
                growth_rate_5y = 0.12  # 12% growth for small-cap
                terminal_growth_rate = 0.04  # 4% terminal growth
                discount_rate = 0.12  # 12% discount rate for higher risk
            
            # Calculate projected cash flows
            projected_cashflows = []
            current_cf = eps
            
            for year in range(1, 6):
                future_cf = current_cf * (1 + growth_rate_5y) ** year
                present_value = future_cf / (1 + discount_rate) ** year
                projected_cashflows.append({
                    'year': year,
                    'projected_cf': future_cf,
                    'present_value': present_value
                })
            
            # Terminal value calculation
            terminal_cf = projected_cashflows[-1]['projected_cf'] * (1 + terminal_growth_rate)
            terminal_value = terminal_cf / (discount_rate - terminal_growth_rate)
            terminal_pv = terminal_value / (1 + discount_rate) ** 5
            
            # Sum all present values
            sum_pv_cashflows = sum([cf['present_value'] for cf in projected_cashflows])
            dcf_fair_value = sum_pv_cashflows + terminal_pv
            
            # Calculate upside/downside
            upside_potential = ((dcf_fair_value - current_price) / current_price) * 100 if current_price > 0 else 0
            
            # Assessment
            if dcf_fair_value > current_price * 1.15:
                assessment = 'Significantly Undervalued'
            elif dcf_fair_value > current_price * 1.05:
                assessment = 'Undervalued'
            elif dcf_fair_value < current_price * 0.85:
                assessment = 'Significantly Overvalued'
            elif dcf_fair_value < current_price * 0.95:
                assessment = 'Overvalued'
            else:
                assessment = 'Fair Value'
            
            return {
                'method': 'DCF Analysis',
                'assumptions': {
                    'growth_rate_5y': f"{growth_rate_5y:.1%}",
                    'terminal_growth_rate': f"{terminal_growth_rate:.1%}",
                    'discount_rate': f"{discount_rate:.1%}"
                },
                'projected_cashflows': projected_cashflows,
                'terminal_value': terminal_value,
                'terminal_pv': terminal_pv,
                'sum_pv_cashflows': sum_pv_cashflows,
                'fair_value': dcf_fair_value,
                'current_price': current_price,
                'upside_potential': f"{upside_potential:.1f}%",
                'assessment': assessment,
                'status': 'Completed'
            }
            
        except Exception as e:
            return {
                'method': 'DCF Analysis',
                'status': f'Error: {str(e)}',
                'fair_value': current_price,
                'assessment': 'Unable to calculate'
            }

    def _calculate_wacc(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Weighted Average Cost of Capital (WACC)."""
        try:
            market_cap = stock_data.get('market_cap', 0)
            beta = stock_data.get('beta', 1.0)
            
            # WACC calculation assumptions
            risk_free_rate = 0.045  # 4.5% (10-year treasury)
            market_risk_premium = 0.065  # 6.5% market risk premium
            tax_rate = 0.25  # 25% corporate tax rate
            
            # Cost of equity using CAPM
            cost_of_equity = risk_free_rate + (beta * market_risk_premium)
            
            # Estimate debt-to-equity ratio based on company size
            if market_cap > 50e9:
                debt_to_equity = 0.3
            elif market_cap > 10e9:
                debt_to_equity = 0.25
            else:
                debt_to_equity = 0.2
            
            # Cost of debt
            if market_cap > 50e9:
                credit_spread = 0.02
            elif market_cap > 10e9:
                credit_spread = 0.03
            else:
                credit_spread = 0.05
            
            cost_of_debt = risk_free_rate + credit_spread
            after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)
            
            # Calculate weights
            equity_weight = 1 / (1 + debt_to_equity)
            debt_weight = debt_to_equity / (1 + debt_to_equity)
            
            # Calculate WACC
            wacc = (equity_weight * cost_of_equity) + (debt_weight * after_tax_cost_of_debt)
            
            return {
                'method': 'WACC Analysis',
                'assumptions': {
                    'risk_free_rate': f"{risk_free_rate:.1%}",
                    'market_risk_premium': f"{market_risk_premium:.1%}",
                    'beta': beta,
                    'tax_rate': f"{tax_rate:.1%}",
                    'debt_to_equity': f"{debt_to_equity:.1%}"
                },
                'calculations': {
                    'cost_of_equity': f"{cost_of_equity:.1%}",
                    'cost_of_debt': f"{cost_of_debt:.1%}",
                    'after_tax_cost_of_debt': f"{after_tax_cost_of_debt:.1%}",
                    'equity_weight': f"{equity_weight:.1%}",
                    'debt_weight': f"{debt_weight:.1%}"
                },
                'wacc': f"{wacc:.1%}",
                'wacc_decimal': wacc,
                'interpretation': self._interpret_wacc(wacc),
                'status': 'Completed'
            }
            
        except Exception as e:
            return {
                'method': 'WACC Analysis',
                'status': f'Error: {str(e)}',
                'wacc': 'Unable to calculate'
            }

    def _analyze_financial_statements(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial statements and ratios."""
        try:
            analysis = {
                'method': 'Financial Statement Analysis',
                'profitability_analysis': self._analyze_profitability(stock_data),
                'liquidity_analysis': self._analyze_liquidity(stock_data),
                'leverage_analysis': self._analyze_leverage(stock_data),
                'efficiency_analysis': self._analyze_efficiency(stock_data),
                'valuation_ratios': self._analyze_valuation_ratios(stock_data),
                'growth_analysis': self._analyze_growth_metrics(stock_data),
                'status': 'Completed'
            }
            
            # Calculate overall financial health score
            score = self._calculate_financial_health_score(analysis)
            analysis['overall_score'] = score
            analysis['grade'] = self._assign_financial_grade(score)
            analysis['summary'] = self._generate_financial_summary(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'method': 'Financial Statement Analysis',
                'status': f'Error: {str(e)}',
                'summary': 'Unable to complete analysis'
            }

    def _calculate_comparative_valuation(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comparative valuation using multiple methods."""
        try:
            current_price = stock_data.get('current_price', 0)
            pe_ratio = stock_data.get('pe_ratio', 0)
            pb_ratio = stock_data.get('pb_ratio', 0)
            eps = stock_data.get('eps', 0)
            dividend_yield = stock_data.get('dividend_yield', 0)
            
            # Industry average assumptions
            industry_averages = {
                'pe_ratio': 20.0,
                'pb_ratio': 2.5,
                'dividend_yield': 0.025
            }
            
            valuation_methods = {}
            
            # P/E Multiple Valuation
            if pe_ratio and eps:
                pe_fair_value = eps * industry_averages['pe_ratio']
                valuation_methods['pe_multiple'] = {
                    'method': 'P/E Multiple',
                    'current_pe': pe_ratio,
                    'industry_avg_pe': industry_averages['pe_ratio'],
                    'fair_value': pe_fair_value,
                    'premium_discount': f"{((pe_ratio - industry_averages['pe_ratio']) / industry_averages['pe_ratio'] * 100):.1f}%"
                }
            
            # P/B Multiple Valuation
            if pb_ratio and current_price:
                book_value_per_share = current_price / pb_ratio if pb_ratio > 0 else 0
                pb_fair_value = book_value_per_share * industry_averages['pb_ratio']
                valuation_methods['pb_multiple'] = {
                    'method': 'P/B Multiple',
                    'current_pb': pb_ratio,
                    'industry_avg_pb': industry_averages['pb_ratio'],
                    'fair_value': pb_fair_value,
                    'premium_discount': f"{((pb_ratio - industry_averages['pb_ratio']) / industry_averages['pb_ratio'] * 100):.1f}%" if pb_ratio > 0 else "N/A"
                }
            
            # Dividend Yield Comparison
            if dividend_yield:
                dividend_comparison = {
                    'method': 'Dividend Yield Comparison',
                    'current_yield': f"{dividend_yield:.1%}",
                    'industry_avg_yield': f"{industry_averages['dividend_yield']:.1%}",
                    'yield_premium': f"{((dividend_yield - industry_averages['dividend_yield']) / industry_averages['dividend_yield'] * 100):.1f}%"
                }
                valuation_methods['dividend_yield'] = dividend_comparison
            
            # Calculate weighted average fair value
            fair_values = []
            if 'pe_multiple' in valuation_methods:
                fair_values.append(valuation_methods['pe_multiple']['fair_value'])
            if 'pb_multiple' in valuation_methods:
                fair_values.append(valuation_methods['pb_multiple']['fair_value'])
            
            if fair_values:
                avg_fair_value = sum(fair_values) / len(fair_values)
                upside_potential = ((avg_fair_value - current_price) / current_price * 100) if current_price > 0 else 0
                
                if avg_fair_value > current_price * 1.15:
                    assessment = 'Significantly Undervalued'
                elif avg_fair_value > current_price * 1.05:
                    assessment = 'Undervalued'
                elif avg_fair_value < current_price * 0.85:
                    assessment = 'Significantly Overvalued'
                elif avg_fair_value < current_price * 0.95:
                    assessment = 'Overvalued'
                else:
                    assessment = 'Fair Value'
            else:
                avg_fair_value = current_price
                upside_potential = 0
                assessment = 'Unable to determine'
            
            return {
                'method': 'Comparative Valuation',
                'valuation_methods': valuation_methods,
                'average_fair_value': avg_fair_value,
                'current_price': current_price,
                'upside_potential': f"{upside_potential:.1f}%",
                'assessment': assessment,
                'status': 'Completed'
            }
            
        except Exception as e:
            return {
                'method': 'Comparative Valuation',
                'status': f'Error: {str(e)}',
                'assessment': 'Unable to calculate'
            }

    def _calculate_weighted_fair_value(self, dcf_valuation: Dict, comparative_valuation: Dict, current_price: float) -> Dict[str, Any]:
        """Calculate weighted average fair value from different methods."""
        try:
            fair_values = []
            weights = []
            
            # DCF valuation (40% weight)
            if dcf_valuation.get('status') == 'Completed' and dcf_valuation.get('fair_value', 0) > 0:
                fair_values.append(dcf_valuation['fair_value'])
                weights.append(0.4)
            
            # Comparative valuation (60% weight)
            if comparative_valuation.get('status') == 'Completed' and comparative_valuation.get('average_fair_value', 0) > 0:
                fair_values.append(comparative_valuation['average_fair_value'])
                weights.append(0.6)
            
            if fair_values and weights:
                total_weight = sum(weights)
                normalized_weights = [w / total_weight for w in weights]
                weighted_fair_value = sum(fv * w for fv, w in zip(fair_values, normalized_weights))
                confidence = min(len(fair_values) * 25, 100)
                
                return {
                    'weighted_fair_value': weighted_fair_value,
                    'confidence_level': f"{confidence}%",
                    'methods_used': len(fair_values),
                    'current_price': current_price,
                    'implied_return': f"{((weighted_fair_value - current_price) / current_price * 100):.1f}%" if current_price > 0 else "N/A"
                }
            else:
                return {
                    'weighted_fair_value': current_price,
                    'confidence_level': '0%',
                    'methods_used': 0,
                    'current_price': current_price,
                    'implied_return': '0.0%'
                }
                
        except Exception as e:
            return {
                'weighted_fair_value': current_price,
                'confidence_level': '0%',
                'methods_used': 0,
                'error': str(e)
            }

    def _determine_overall_valuation_assessment(self, dcf_valuation: Dict, comparative_valuation: Dict, current_price: float) -> str:
        """Determine overall valuation assessment."""
        try:
            assessments = []
            
            if dcf_valuation.get('status') == 'Completed':
                assessments.append(dcf_valuation.get('assessment', ''))
            
            if comparative_valuation.get('status') == 'Completed':
                assessments.append(comparative_valuation.get('assessment', ''))
            
            if not assessments:
                return 'Unable to determine valuation'
            
            # Count assessment types
            undervalued_count = sum(1 for a in assessments if 'undervalued' in a.lower())
            overvalued_count = sum(1 for a in assessments if 'overvalued' in a.lower())
            fair_value_count = sum(1 for a in assessments if 'fair' in a.lower())
            
            # Determine consensus
            if undervalued_count > overvalued_count and undervalued_count > fair_value_count:
                return 'Strong Undervaluation Signal' if undervalued_count == len(assessments) else 'Likely Undervalued'
            elif overvalued_count > undervalued_count and overvalued_count > fair_value_count:
                return 'Strong Overvaluation Signal' if overvalued_count == len(assessments) else 'Likely Overvalued'
            else:
                return 'Mixed Signals - Fair Value Range'
                
        except Exception as e:
            return 'Unable to determine valuation'

    # Helper methods for financial statement analysis
    def _analyze_profitability(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze profitability metrics."""
        eps = stock_data.get('eps', 0)
        pe_ratio = stock_data.get('pe_ratio', 0)
        
        profitability_score = 0
        if eps > 0:
            profitability_score += 3
            if eps > 2:
                profitability_score += 2
        
        if pe_ratio > 0 and pe_ratio < 25:
            profitability_score += 2
        
        return {
            'eps': eps,
            'pe_ratio': pe_ratio,
            'profitability_score': profitability_score,
            'assessment': self._score_to_assessment(profitability_score, 5)
        }

    def _analyze_liquidity(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze liquidity metrics."""
        market_cap = stock_data.get('market_cap', 0)
        
        liquidity_score = 0
        if market_cap > 10e9:
            liquidity_score += 5
        elif market_cap > 2e9:
            liquidity_score += 3
        else:
            liquidity_score += 1
        
        return {
            'market_cap': market_cap,
            'liquidity_score': liquidity_score,
            'assessment': self._score_to_assessment(liquidity_score, 5)
        }

    def _analyze_leverage(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze leverage metrics."""
        dividend_yield = stock_data.get('dividend_yield', 0)
        market_cap = stock_data.get('market_cap', 0)
        
        leverage_score = 0
        if dividend_yield > 0.03:
            leverage_score += 3
        elif dividend_yield > 0.01:
            leverage_score += 2
        else:
            leverage_score += 1
        
        if market_cap > 10e9:
            leverage_score += 2
        
        return {
            'dividend_yield': dividend_yield,
            'leverage_score': leverage_score,
            'assessment': self._score_to_assessment(leverage_score, 5)
        }

    def _analyze_efficiency(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze efficiency metrics."""
        pe_ratio = stock_data.get('pe_ratio', 0)
        beta = stock_data.get('beta', 1.0)
        
        efficiency_score = 0
        if pe_ratio > 0 and pe_ratio < 20:
            efficiency_score += 3
        elif pe_ratio > 0 and pe_ratio < 30:
            efficiency_score += 2
        
        if 0.8 <= beta <= 1.2:
            efficiency_score += 2
        
        return {
            'pe_ratio': pe_ratio,
            'beta': beta,
            'efficiency_score': efficiency_score,
            'assessment': self._score_to_assessment(efficiency_score, 5)
        }

    def _analyze_valuation_ratios(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze valuation ratios."""
        pe_ratio = stock_data.get('pe_ratio', 0)
        pb_ratio = stock_data.get('pb_ratio', 0)
        
        valuation_score = 0
        if pe_ratio > 0:
            if pe_ratio < 15:
                valuation_score += 3
            elif pe_ratio < 25:
                valuation_score += 2
            else:
                valuation_score += 1
        
        if pb_ratio > 0:
            if pb_ratio < 2:
                valuation_score += 2
            elif pb_ratio < 3:
                valuation_score += 1
        
        return {
            'pe_ratio': pe_ratio,
            'pb_ratio': pb_ratio,
            'valuation_score': valuation_score,
            'assessment': self._score_to_assessment(valuation_score, 5)
        }

    def _analyze_growth_metrics(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze growth metrics."""
        pe_ratio = stock_data.get('pe_ratio', 0)
        market_cap = stock_data.get('market_cap', 0)
        
        growth_score = 0
        if pe_ratio > 20:
            growth_score += 2
        elif pe_ratio > 15:
            growth_score += 1
        
        if market_cap < 10e9:
            growth_score += 2
        elif market_cap < 50e9:
            growth_score += 1
        
        return {
            'pe_ratio': pe_ratio,
            'market_cap': market_cap,
            'growth_score': growth_score,
            'assessment': self._score_to_assessment(growth_score, 4)
        }

    def _calculate_financial_health_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall financial health score."""
        total_score = 0
        total_score += analysis['profitability_analysis'].get('profitability_score', 0)
        total_score += analysis['liquidity_analysis'].get('liquidity_score', 0)
        total_score += analysis['leverage_analysis'].get('leverage_score', 0)
        total_score += analysis['efficiency_analysis'].get('efficiency_score', 0)
        total_score += analysis['valuation_ratios'].get('valuation_score', 0)
        total_score += analysis['growth_analysis'].get('growth_score', 0)
        return total_score

    def _assign_financial_grade(self, score: int) -> str:
        """Assign letter grade based on financial health score."""
        if score >= 20:
            return 'A+ (Excellent)'
        elif score >= 17:
            return 'A (Very Good)'
        elif score >= 14:
            return 'B+ (Good)'
        elif score >= 11:
            return 'B (Above Average)'
        elif score >= 8:
            return 'C+ (Average)'
        elif score >= 5:
            return 'C (Below Average)'
        else:
            return 'D (Poor)'

    def _generate_financial_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate financial summary."""
        grade = analysis['grade']
        score = analysis['overall_score']
        return f"Financial Health Grade: {grade} (Score: {score}/24). Assessment based on profitability, liquidity, leverage, efficiency, valuation, and growth metrics."

    def _score_to_assessment(self, score: int, max_score: int) -> str:
        """Convert numerical score to assessment."""
        ratio = score / max_score
        if ratio >= 0.8:
            return 'Excellent'
        elif ratio >= 0.6:
            return 'Good'
        elif ratio >= 0.4:
            return 'Average'
        elif ratio >= 0.2:
            return 'Below Average'
        else:
            return 'Poor'

    def _interpret_wacc(self, wacc: float) -> str:
        """Interpret WACC value."""
        if wacc < 0.08:
            return 'Low cost of capital - favorable for investment'
        elif wacc < 0.12:
            return 'Moderate cost of capital - typical for most companies'
        else:
            return 'High cost of capital - higher risk profile'
