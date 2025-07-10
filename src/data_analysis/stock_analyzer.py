"""
Stock Analyzer - AI-powered financial data analysis
Fetches stock data and performs comprehensive analysis using AI models.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import openai
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger

class StockAnalyzer:
    """AI-powered stock analysis engine."""
    
    def __init__(self, config):
        """Initialize the stock analyzer with configuration."""
        self.config = config
        self.logger = setup_logger()
        
        # Initialize OpenAI client
        if not config.openai_api_key:
            raise ValueError("OpenAI API key is required for premium analysis")
        
        openai.api_key = config.openai_api_key
        self.client = openai.OpenAI(api_key=config.openai_api_key)
        self.logger.info(f"StockAnalyzer initialized with API key: {config.openai_api_key[:8]}...")
    
    def fetch_stock_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """
        Fetch comprehensive stock data from Yahoo Finance.
        
        Args:
            symbol: Stock ticker symbol
            period: Time period for data (1y, 2y, 5y, max)
            
        Returns:
            Dictionary containing stock data and information
        """
        try:
            self.logger.info(f"Fetching stock data for {symbol}")
            
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist_data = ticker.history(period=period)
            
            # Get company info
            info = ticker.info
            
            # Get financial statements
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cashflow = ticker.cashflow
            
            # Calculate technical indicators
            technical_indicators = self._calculate_technical_indicators(hist_data)
            
            # Compile all data
            stock_data = {
                "symbol": symbol,
                "company_name": info.get("longName", symbol),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                "historical_data": hist_data,
                "company_info": info,
                "financials": financials,
                "balance_sheet": balance_sheet,
                "cashflow": cashflow,
                "technical_indicators": technical_indicators,
                "current_price": hist_data['Close'].iloc[-1] if not hist_data.empty else None,
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "eps": info.get("trailingEps"),
                "52w_high": info.get("fiftyTwoWeekHigh"),
                "52w_low": info.get("fiftyTwoWeekLow"),
                "dividend_yield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume")
            }
            
            self.logger.info(f"Successfully fetched data for {symbol}")
            return stock_data
            
        except Exception as e:
            self.logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
            raise
    
    def _calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate technical indicators from historical data."""
        try:
            indicators = {}
            
            if data.empty:
                return indicators
            
            # Moving averages
            indicators['sma_20'] = data['Close'].rolling(window=20).mean()
            indicators['sma_50'] = data['Close'].rolling(window=50).mean()
            indicators['sma_200'] = data['Close'].rolling(window=200).mean()
            
            # RSI
            indicators['rsi'] = self._calculate_rsi(data['Close'])
            
            # MACD
            macd_data = self._calculate_macd(data['Close'])
            indicators.update(macd_data)
            
            # Bollinger Bands
            bb_data = self._calculate_bollinger_bands(data['Close'])
            indicators.update(bb_data)
            
            # Volume indicators
            indicators['volume_sma'] = data['Volume'].rolling(window=20).mean()
            
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error calculating technical indicators: {str(e)}")
            return {}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series) -> Dict[str, pd.Series]:
        """Calculate MACD indicators."""
        ema_12 = prices.ewm(span=12).mean()
        ema_26 = prices.ewm(span=26).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        
        return {
            'macd': macd,
            'macd_signal': signal,
            'macd_histogram': histogram
        }
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands."""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        return {
            'bb_upper': sma + (std * 2),
            'bb_lower': sma - (std * 2),
            'bb_middle': sma
        }
    
    def analyze_stock(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive AI-powered stock analysis.
        
        Args:
            stock_data: Dictionary containing stock data
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            self.logger.info(f"Starting AI analysis for {stock_data.get('symbol', 'UNKNOWN')}")
            
            # Get comprehensive AI analysis in ONE call (now includes prompt preparation)
            ai_analysis_result = self._get_comprehensive_ai_analysis(stock_data)
            
            # Calculate financial ratios
            financial_ratios = self._calculate_financial_ratios(stock_data)
            
            # Perform valuation analysis
            valuation = self._perform_valuation_analysis(stock_data)
            
            # Compile results
            analysis_results = {
                "symbol": stock_data.get("symbol", ""),
                "company_name": stock_data.get("company_name", ""),
                "analysis_date": datetime.now().isoformat(),
                "ai_analysis": ai_analysis_result.get("analysis", "Analysis unavailable"),
                "financial_ratios": financial_ratios,
                "valuation": valuation,
                "investment_thesis": ai_analysis_result.get("investment_thesis", "Investment thesis unavailable"),
                "metrics": {
                    "current_price": stock_data.get("current_price"),
                    "market_cap": stock_data.get("market_cap"),
                    "pe_ratio": stock_data.get("pe_ratio"),
                    "eps": stock_data.get("eps"),
                    "52w_high": stock_data.get("52w_high"),
                    "52w_low": stock_data.get("52w_low"),
                    "dividend_yield": stock_data.get("dividend_yield"),
                    "beta": stock_data.get("beta")
                },
                "key_highlights": ai_analysis_result.get("highlights", []),
                "risks": ai_analysis_result.get("risks", []),
                "recommendation": ai_analysis_result.get("recommendation", "HOLD"),
                "target_price": ai_analysis_result.get("target_price", stock_data.get("current_price", 0)),
                "upside_potential": ai_analysis_result.get("upside_potential", "0%")
            }
            
            self.logger.info(f"Analysis completed for {stock_data.get('symbol', 'UNKNOWN')}")
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"Error in stock analysis: {str(e)}")
            raise
    
    def _prepare_analysis_prompt(self, stock_data: Dict[str, Any]) -> str:
        """Prepare the prompt for AI analysis."""
        # Safely format market cap
        market_cap = stock_data.get('market_cap', 0)
        market_cap_str = f"${market_cap:,}" if market_cap and market_cap > 0 else 'N/A'
        
        # Safely format other values
        current_price = stock_data.get('current_price', 0)
        pe_ratio = stock_data.get('pe_ratio', 'N/A')
        eps = stock_data.get('eps', 'N/A')
        low_52w = stock_data.get('52w_low', 'N/A')
        high_52w = stock_data.get('52w_high', 'N/A')
        beta = stock_data.get('beta', 'N/A')
        sector = stock_data.get('sector', 'N/A')
        industry = stock_data.get('industry', 'N/A')
        company_name = stock_data.get('company_name', 'Unknown Company')
        symbol = stock_data.get('symbol', 'UNKNOWN')
        
        # Get additional financial metrics for calculations
        company_info = stock_data.get('company_info', {})
        revenue = company_info.get('totalRevenue', 'N/A')
        profit_margin = company_info.get('profitMargins', 'N/A')
        debt_to_equity = company_info.get('debtToEquity', 'N/A')
        roe = company_info.get('returnOnEquity', 'N/A')
        forward_pe = company_info.get('forwardPE', 'N/A')
        price_to_book = company_info.get('priceToBook', 'N/A')
        free_cashflow = company_info.get('freeCashflow', 'N/A')
        total_debt = company_info.get('totalDebt', 'N/A')
        total_cash = company_info.get('totalCash', 'N/A')
        shares_outstanding = company_info.get('sharesOutstanding', 'N/A')
        enterprise_value = company_info.get('enterpriseValue', 'N/A')
        
        prompt = f"""
        As a CRITICAL Wall Street equity research analyst, conduct a HARSH, REALISTIC analysis of {company_name} ({symbol}).
        
        COMPANY DATA FOR CALCULATIONS:
        - Sector: {sector} | Industry: {industry}
        - Current Price: ${current_price:.2f}
        - Market Cap: {market_cap_str}
        - 52-Week Range: ${low_52w} - ${high_52w}
        
        FINANCIAL DATA FOR DCF/WACC CALCULATIONS:
        - Revenue: {revenue}
        - Free Cash Flow: {free_cashflow}
        - Total Debt: {total_debt}
        - Total Cash: {total_cash}
        - Shares Outstanding: {shares_outstanding}
        - Enterprise Value: {enterprise_value}
        - P/E Ratio: {pe_ratio} | Forward P/E: {forward_pe}
        - EPS: {eps}
        - Price-to-Book: {price_to_book}
        - Profit Margin: {profit_margin}
        - ROE: {roe}
        - Debt-to-Equity: {debt_to_equity}
        - Beta: {beta}
        
        MANDATORY ANALYSIS - USE THE ACTUAL NUMBERS ABOVE:
        
        1. DCF CALCULATION:
           - Use Free Cash Flow to calculate intrinsic value
           - Apply discount rate based on Beta and risk-free rate
           - Show your calculation steps
           - Compare to current price
        
        2. WACC CALCULATION:
           - Calculate cost of equity using CAPM
           - Factor in debt costs using Debt-to-Equity
           - Show your WACC percentage
        
        3. VALUATION ASSESSMENT:
           - Is current P/E justified vs peers?
           - Is Price-to-Book reasonable?
           - Calculate fair value range
           - Be HONEST about overvaluation
        
        4. CRITICAL ANALYSIS:
           - What's wrong with this company?
           - Why might it fail?
           - What are the red flags?
           - Is management overpaid?
        
        5. REALISTIC RECOMMENDATION:
           - Most stocks are OVERVALUED in this market
           - Only recommend BUY if truly undervalued
           - Use HOLD for fairly valued
           - Use SELL for overvalued
        
        DO REAL MATH - NO GENERIC ANALYSIS!
        """
        return prompt
    
    def _get_comprehensive_ai_analysis(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive AI analysis in ONE call for speed."""
        try:
            self.logger.info("Starting comprehensive AI analysis...")
            
            # Extract company info safely
            company_info = stock_data.get('company_info', {})
            company_name = stock_data.get('company_name', 'Unknown Company')
            symbol = stock_data.get('symbol', 'UNKNOWN')
            current_price = stock_data.get('current_price', 0)
            
            # Format financial data for calculations
            free_cashflow = company_info.get('freeCashflow', 'N/A')
            if free_cashflow != 'N/A' and free_cashflow is not None:
                free_cashflow_str = f"${free_cashflow:,.0f}"
            else:
                free_cashflow_str = 'N/A'
                
            revenue = company_info.get('totalRevenue', 'N/A')
            if revenue != 'N/A' and revenue is not None:
                revenue_str = f"${revenue:,.0f}"
            else:
                revenue_str = 'N/A'
                
            total_debt = company_info.get('totalDebt', 'N/A')
            if total_debt != 'N/A' and total_debt is not None:
                total_debt_str = f"${total_debt:,.0f}"
            else:
                total_debt_str = 'N/A'
                
            total_cash = company_info.get('totalCash', 'N/A')
            if total_cash != 'N/A' and total_cash is not None:
                total_cash_str = f"${total_cash:,.0f}"
            else:
                total_cash_str = 'N/A'
                
            market_cap = stock_data.get('market_cap', 'N/A')
            if market_cap != 'N/A' and market_cap is not None:
                market_cap_str = f"${market_cap:,.0f}"
            else:
                market_cap_str = 'N/A'
                
            shares_outstanding = company_info.get('sharesOutstanding', 'N/A')
            if shares_outstanding != 'N/A' and shares_outstanding is not None:
                shares_outstanding_str = f"{shares_outstanding:,.0f}"
            else:
                shares_outstanding_str = 'N/A'
            
            comprehensive_prompt = f"""
            PROFESSIONAL FINANCIAL ANALYSIS REQUIRED

            Company: {company_name} ({symbol})
            Current Price: ${current_price:.2f}
            
            FINANCIAL DATA (USE THESE EXACT NUMBERS FOR CALCULATIONS):
            - Free Cash Flow: {free_cashflow_str}
            - Revenue: {revenue_str}
            - Total Debt: {total_debt_str}
            - Total Cash: {total_cash_str}
            - Market Cap: {market_cap_str}
            - Shares Outstanding: {shares_outstanding_str}
            - Beta: {stock_data.get('beta', 'N/A')}
            - P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
            - Debt-to-Equity: {company_info.get('debtToEquity', 'N/A')}
            - ROE: {company_info.get('returnOnEquity', 'N/A')}
            - Profit Margin: {company_info.get('profitMargins', 'N/A')}
            - Current Ratio: {company_info.get('currentRatio', 'N/A')}
            - Revenue Growth: {company_info.get('revenueGrowth', 'N/A')}
            
            REQUIRED CALCULATIONS (SHOW YOUR WORK WITH REAL NUMBERS):
            
            1. DCF VALUATION:
               Step 1: Take Free Cash Flow = [use actual FCF number above]
               Step 2: Apply realistic growth rate (3-8% based on company/industry)
               Step 3: Calculate discount rate = Risk-free rate (4%) + Beta × Market Premium (6%)
               Step 4: Project 5-year cash flows with terminal value
               Step 5: Calculate fair value per share
               
            2. WACC CALCULATION:
               Step 1: Cost of Equity = Risk-free rate + Beta × Market Premium
               Step 2: Cost of Debt = 4-6% (estimate based on credit quality)
               Step 3: Calculate weighted average cost of capital
               
            3. FINANCIAL HEALTH ANALYSIS:
               - Assess debt levels and liquidity
               - Review profitability metrics
               - Compare to industry benchmarks
               
            4. BALANCED INVESTMENT RECOMMENDATION:
               - BUY if DCF shows >15% undervaluation AND strong fundamentals
               - HOLD if fairly valued (-15% to +15%) OR mixed signals
               - SELL if DCF shows >15% overvaluation OR weak fundamentals
               
            RESPOND WITH ONLY THIS JSON (SHOW ACTUAL CALCULATIONS):
            {{
                "analysis": "DCF Analysis: Using FCF of $X million, applying Y% growth rate for 5 years, then Z% terminal growth. Discount rate calculated at A% (Risk-free 4% + Beta B × 6% market premium). Fair value calculation: [show steps]. Current price of $C represents D% premium/discount to intrinsic value. Financial health assessment: [debt levels, profitability, liquidity]. Investment rationale: [balanced view with specific metrics and reasoning].",
                "investment_thesis": "Based on DCF analysis showing fair value of $X vs current price of $Y (Z% over/undervalued), combined with [strong/mixed/weak] fundamentals including [specific metrics]. Recommendation: [BUY/HOLD/SELL] based on valuation and risk/reward profile.",
                "highlights": ["DCF fair value $X vs current $Y", "WACC calculated at Z%", "FCF of $A million growing at B%", "Debt-to-equity ratio of C", "ROE of D% vs industry average"],
                "risks": ["Valuation risk: X% premium/discount to DCF", "Balance sheet: $Y debt vs $Z cash", "Market risk: Beta of A indicates volatility", "Execution risk on growth plans", "Industry/competitive pressures"],
                "recommendation": "HOLD",
                "target_price": 999.99,
                "upside_potential": 5.0
            }}
            
            RULES:
            - Replace ALL placeholder values with ACTUAL calculated numbers
            - Show detailed DCF and WACC calculations with real data
            - Be objective and balanced in your analysis
            - Consider both strengths and weaknesses
            - Base recommendation on valuation AND fundamentals
            - Use positive upside for undervalued, negative for overvalued
            - Provide specific reasoning for recommendation
            
            DO THE MATH WITH REAL NUMBERS!
            """
            
            self.logger.info("Making OpenAI API call...")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # FREE model that works with your account
                messages=[
                    {"role": "system", "content": "You are a professional Wall Street equity research analyst. You provide balanced, objective analysis using real financial data. You calculate DCF and WACC using actual numbers from the financial statements. Your recommendations are based on rigorous valuation analysis, considering both bullish and bearish factors. You give BUY recommendations for significantly undervalued stocks, HOLD for fairly valued stocks, and SELL for overvalued stocks. Respond ONLY with valid JSON showing your calculations."},
                    {"role": "user", "content": comprehensive_prompt}
                ],
                max_tokens=4000,  # Increased for comprehensive analysis
                temperature=0.7
            )
            
            self.logger.info(f"OpenAI API call completed. Response length: {len(response.choices[0].message.content)}")
            
            # Parse JSON response
            import json
            response_text = response.choices[0].message.content
            
            try:
                # Try to parse as JSON
                result = json.loads(response_text)
                self.logger.info("JSON parsing successful")
            except json.JSONDecodeError:
                # If JSON parsing fails, extract manually
                self.logger.warning("JSON parsing failed, extracting manually")
                # Fallback: try to extract key fields from the text
                import re
                def extract(pattern, text, default=None):
                    match = re.search(pattern, text, re.IGNORECASE)
                    return match.group(1).strip() if match else default
                result = {
                    "analysis": response_text,
                    "investment_thesis": extract(r'"investment_thesis"\s*:\s*"([^"]+)"', response_text),
                    "recommendation": extract(r'"recommendation"\s*:\s*"([^"]+)"', response_text, "N/A"),
                    "target_price": extract(r'"target_price"\s*:\s*([\d.]+)', response_text, "N/A"),
                    "upside_potential": extract(r'"upside_potential"\s*:\s*([\d.\-]+)', response_text, "N/A"),
                    "highlights": re.findall(r'"highlights"\s*:\s*\[(.*?)\]', response_text, re.DOTALL),
                    "risks": re.findall(r'"risks"\s*:\s*\[(.*?)\]', response_text, re.DOTALL)
                }
                # Try to clean up highlights/risks if found
                if result["highlights"]:
                    result["highlights"] = [h.strip(' ",') for h in result["highlights"][0].split(',') if h.strip()]
                else:
                    result["highlights"] = []
                if result["risks"]:
                    result["risks"] = [r.strip(' ",') for r in result["risks"][0].split(',') if r.strip()]
                else:
                    result["risks"] = []
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting comprehensive AI analysis: {str(e)}")
            return {
                "analysis": "AI analysis temporarily unavailable.",
                "investment_thesis": "Investment thesis temporarily unavailable.",
                "highlights": ["Analysis in progress", "Please try again"],
                "risks": ["Market volatility", "Sector-specific challenges"],
                "recommendation": "HOLD",
                "target_price": 0,
                "upside_potential": 0
            }
    
    def _get_ai_analysis(self, prompt: str) -> str:
        """Get AI analysis using OpenAI GPT."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # FREE model that works with your account
                messages=[
                    {"role": "system", "content": "You are a senior Wall Street equity research analyst with 15+ years of experience. Provide detailed, professional analysis with specific insights and actionable conclusions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,  # Increased for comprehensive analysis
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error getting AI analysis: {str(e)}")
            return "AI analysis temporarily unavailable."
    
    def _calculate_financial_ratios(self, stock_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate key financial ratios."""
        ratios = {}
        
        try:
            info = stock_data.get("company_info", {})
            
            # Profitability ratios
            ratios["profit_margin"] = info.get("profitMargins")
            ratios["operating_margin"] = info.get("operatingMargins")
            ratios["roe"] = info.get("returnOnEquity")
            ratios["roa"] = info.get("returnOnAssets")
            
            # Valuation ratios
            ratios["pe_ratio"] = info.get("trailingPE")
            ratios["peg_ratio"] = info.get("pegRatio")
            ratios["price_to_book"] = info.get("priceToBook")
            ratios["price_to_sales"] = info.get("priceToSalesTrailing12Months")
            
            # Liquidity ratios
            ratios["current_ratio"] = info.get("currentRatio")
            ratios["quick_ratio"] = info.get("quickRatio")
            
            # Leverage ratios
            ratios["debt_to_equity"] = info.get("debtToEquity")
            ratios["debt_to_assets"] = info.get("totalDebt", 0) / info.get("totalAssets", 1) if info.get("totalAssets") else None
            
        except Exception as e:
            self.logger.error(f"Error calculating financial ratios: {str(e)}")
        
        return ratios
    
    def _perform_valuation_analysis(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform valuation analysis."""
        valuation = {}
        
        try:
            info = stock_data.get("company_info", {})
            current_price = stock_data.get("current_price", 0)
            
            # DCF-based fair value estimate (simplified)
            if info.get("freeCashflow") and info.get("sharesOutstanding"):
                fcf_per_share = info["freeCashflow"] / info["sharesOutstanding"]
                # Simple DCF with 10% discount rate and 3% growth
                estimated_value = fcf_per_share * 1.03 / (0.10 - 0.03)
                valuation["dcf_estimate"] = estimated_value
                valuation["dcf_upside"] = (estimated_value - current_price) / current_price * 100
            
            # Peer comparison
            industry_pe = 20  # Default industry P/E
            if info.get("trailingEps"):
                peer_valuation = info["trailingEps"] * industry_pe
                valuation["peer_estimate"] = peer_valuation
                valuation["peer_upside"] = (peer_valuation - current_price) / current_price * 100
            
        except Exception as e:
            self.logger.error(f"Error in valuation analysis: {str(e)}")
        
        return valuation
