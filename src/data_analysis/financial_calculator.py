"""
Advanced Financial Calculator for Stock Analysis
Handles WACC calculations, DCF modeling, and financial statement analysis
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class FinancialCalculator:
    """Advanced financial calculations for stock valuation"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
        self._cache = {}
    
    def get_financial_statements(self) -> Dict[str, Any]:
        """Get comprehensive financial statements"""
        try:
            # Get financial statements
            financials = self.ticker.financials
            balance_sheet = self.ticker.balance_sheet
            cash_flow = self.ticker.cashflow
            
            # Get info for additional metrics
            info = self.ticker.info
            
            return {
                'income_statement': financials,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow,
                'info': info
            }
        except Exception as e:
            print(f"Error getting financial statements: {e}")
            return {}
    
    def calculate_wacc(self) -> Dict[str, Any]:
        """Calculate Weighted Average Cost of Capital"""
        try:
            info = self.ticker.info
            balance_sheet = self.ticker.balance_sheet
            
            # Market values
            market_cap = info.get('marketCap', 0)
            enterprise_value = info.get('enterpriseValue', 0)
            
            # Get debt from balance sheet
            if not balance_sheet.empty:
                latest_bs = balance_sheet.iloc[:, 0]
                total_debt = latest_bs.get('Total Debt', 0)
                if pd.isna(total_debt):
                    total_debt = latest_bs.get('Long Term Debt', 0) + latest_bs.get('Short Long Term Debt', 0)
                    if pd.isna(total_debt):
                        total_debt = 0
            else:
                total_debt = 0
            
            # Cost of equity (using CAPM)
            beta = info.get('beta', 1.0)
            if beta is None:
                beta = 1.0
            
            risk_free_rate = 0.045  # 10-year treasury rate (approximate)
            market_risk_premium = 0.065  # Historical market risk premium
            cost_of_equity = risk_free_rate + beta * market_risk_premium
            
            # Cost of debt
            interest_expense = self._get_interest_expense()
            cost_of_debt = interest_expense / total_debt if total_debt > 0 else 0.05
            
            # Handle NaN values
            if pd.isna(cost_of_debt) or cost_of_debt == 0:
                cost_of_debt = 0.05  # Default 5% cost of debt
            
            # Tax rate
            tax_rate = self._get_tax_rate()
            
            # WACC calculation
            total_value = market_cap + total_debt
            equity_weight = market_cap / total_value if total_value > 0 else 1
            debt_weight = total_debt / total_value if total_value > 0 else 0
            
            wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
            
            # Handle NaN values in final WACC
            if pd.isna(wacc):
                wacc = cost_of_equity  # Use cost of equity as fallback
            
            return {
                'wacc': wacc,
                'cost_of_equity': cost_of_equity,
                'cost_of_debt': cost_of_debt,
                'tax_rate': tax_rate,
                'beta': beta,
                'market_cap': market_cap,
                'total_debt': total_debt,
                'equity_weight': equity_weight,
                'debt_weight': debt_weight,
                'risk_free_rate': risk_free_rate,
                'market_risk_premium': market_risk_premium
            }
        except Exception as e:
            print(f"Error calculating WACC: {e}")
            return {'wacc': 0.1, 'error': str(e)}
    
    def calculate_dcf_valuation(self, years: int = 5) -> Dict[str, Any]:
        """Calculate DCF valuation with terminal value"""
        try:
            # Get cash flow data
            cash_flow = self.ticker.cashflow
            if cash_flow.empty:
                return {'error': 'No cash flow data available'}
            
            # Get latest free cash flow
            latest_cf = cash_flow.iloc[:, 0]
            free_cash_flow = latest_cf.get('Free Cash Flow', 0)
            
            if pd.isna(free_cash_flow) or free_cash_flow == 0:
                # Calculate FCF manually
                operating_cf = latest_cf.get('Total Cash From Operating Activities', 0)
                capex = latest_cf.get('Capital Expenditures', 0)
                
                # Handle NaN values
                if pd.isna(operating_cf):
                    operating_cf = 0
                if pd.isna(capex):
                    capex = 0
                    
                free_cash_flow = operating_cf + capex  # capex is negative
                
                # If still no FCF, use net income as proxy
                if pd.isna(free_cash_flow) or free_cash_flow == 0:
                    info = self.ticker.info
                    free_cash_flow = info.get('freeCashflow', 0)
                    if pd.isna(free_cash_flow) or free_cash_flow == 0:
                        # Last resort: use 10% of market cap
                        market_cap = info.get('marketCap', 0)
                        free_cash_flow = market_cap * 0.1 if market_cap > 0 else 1000000000
            
            # Growth assumptions
            revenue_growth = self._estimate_revenue_growth()
            terminal_growth = 0.025  # 2.5% long-term growth
            
            # WACC
            wacc_data = self.calculate_wacc()
            wacc = wacc_data['wacc']
            
            # Project future cash flows
            projected_fcf = []
            current_fcf = free_cash_flow
            
            for year in range(1, years + 1):
                # Declining growth rate
                growth_rate = revenue_growth * (0.9 ** (year - 1))
                current_fcf = current_fcf * (1 + growth_rate)
                projected_fcf.append(current_fcf)
            
            # Terminal value
            terminal_fcf = projected_fcf[-1] * (1 + terminal_growth)
            terminal_value = terminal_fcf / (wacc - terminal_growth)
            
            # Present value calculations
            pv_fcf = []
            for i, fcf in enumerate(projected_fcf):
                pv = fcf / ((1 + wacc) ** (i + 1))
                pv_fcf.append(pv)
            
            pv_terminal = terminal_value / ((1 + wacc) ** years)
            
            # Enterprise value
            enterprise_value = sum(pv_fcf) + pv_terminal
            
            # Equity value
            info = self.ticker.info
            cash = info.get('totalCash', 0)
            debt = wacc_data.get('total_debt', 0)
            equity_value = enterprise_value + cash - debt
            
            # Share price
            shares_outstanding = info.get('sharesOutstanding', 1)
            intrinsic_value = equity_value / shares_outstanding
            
            return {
                'enterprise_value': enterprise_value,
                'equity_value': equity_value,
                'intrinsic_value_per_share': intrinsic_value,
                'current_price': info.get('currentPrice', 0),
                'upside_downside': (intrinsic_value / info.get('currentPrice', 1) - 1) * 100,
                'projected_fcf': projected_fcf,
                'pv_fcf': pv_fcf,
                'terminal_value': terminal_value,
                'pv_terminal': pv_terminal,
                'wacc': wacc,
                'terminal_growth': terminal_growth,
                'revenue_growth': revenue_growth
            }
        except Exception as e:
            print(f"Error calculating DCF: {e}")
            return {'error': str(e)}
    
    def analyze_financial_ratios(self) -> Dict[str, Any]:
        """Calculate comprehensive financial ratios"""
        try:
            info = self.ticker.info
            financials = self.ticker.financials
            balance_sheet = self.ticker.balance_sheet
            
            if financials.empty or balance_sheet.empty:
                return {'error': 'Financial data not available'}
            
            latest_financial = financials.iloc[:, 0]
            latest_bs = balance_sheet.iloc[:, 0]
            
            # Revenue and profitability
            revenue = latest_financial.get('Total Revenue', 0)
            net_income = latest_financial.get('Net Income', 0)
            gross_profit = latest_financial.get('Gross Profit', 0)
            operating_income = latest_financial.get('Operating Income', 0)
            
            # Balance sheet items
            total_assets = latest_bs.get('Total Assets', 0)
            total_equity = latest_bs.get('Stockholders Equity', 0)
            current_assets = latest_bs.get('Current Assets', 0)
            current_liabilities = latest_bs.get('Current Liabilities', 0)
            
            # Calculate ratios
            ratios = {
                'profitability': {
                    'gross_margin': (gross_profit / revenue * 100) if revenue > 0 else 0,
                    'operating_margin': (operating_income / revenue * 100) if revenue > 0 else 0,
                    'net_margin': (net_income / revenue * 100) if revenue > 0 else 0,
                    'roe': (net_income / total_equity * 100) if total_equity > 0 else 0,
                    'roa': (net_income / total_assets * 100) if total_assets > 0 else 0
                },
                'liquidity': {
                    'current_ratio': current_assets / current_liabilities if current_liabilities > 0 else 0,
                    'quick_ratio': info.get('quickRatio', 0)
                },
                'valuation': {
                    'pe_ratio': info.get('trailingPE', 0),
                    'forward_pe': info.get('forwardPE', 0),
                    'peg_ratio': info.get('pegRatio', 0),
                    'price_to_book': info.get('priceToBook', 0),
                    'price_to_sales': info.get('priceToSalesTrailing12Months', 0),
                    'ev_to_ebitda': info.get('enterpriseToEbitda', 0)
                },
                'efficiency': {
                    'asset_turnover': revenue / total_assets if total_assets > 0 else 0,
                    'inventory_turnover': info.get('inventoryTurnover', 0),
                    'receivables_turnover': info.get('receivablesTurnover', 0)
                }
            }
            
            return ratios
        except Exception as e:
            print(f"Error analyzing financial ratios: {e}")
            return {'error': str(e)}
    
    def _get_interest_expense(self) -> float:
        """Get interest expense from income statement"""
        try:
            financials = self.ticker.financials
            if not financials.empty:
                latest = financials.iloc[:, 0]
                interest_expense = latest.get('Interest Expense', 0)
                # Handle NaN values
                if pd.isna(interest_expense):
                    # Try alternative names
                    interest_expense = latest.get('Interest Expense Non Operating', 0)
                    if pd.isna(interest_expense):
                        interest_expense = latest.get('Interest And Debt Expense', 0)
                        if pd.isna(interest_expense):
                            # Default to 3% of debt if we can't find interest expense
                            info = self.ticker.info
                            total_debt = info.get('totalDebt', 0)
                            return total_debt * 0.03 if total_debt > 0 else 0
                return abs(float(interest_expense)) if not pd.isna(interest_expense) else 0
            return 0
        except Exception as e:
            print(f"Error getting interest expense: {e}")
            return 0
    
    def _get_tax_rate(self) -> float:
        """Calculate effective tax rate"""
        try:
            financials = self.ticker.financials
            if not financials.empty:
                latest = financials.iloc[:, 0]
                pretax_income = latest.get('Pretax Income', 0)
                tax_provision = latest.get('Tax Provision', 0)
                if pretax_income > 0:
                    return tax_provision / pretax_income
            return 0.25  # Default corporate tax rate
        except:
            return 0.25
    
    def _estimate_revenue_growth(self) -> float:
        """Estimate revenue growth rate from historical data"""
        try:
            financials = self.ticker.financials
            if len(financials.columns) < 2:
                return 0.05  # Default 5% growth
            
            revenues = []
            for col in financials.columns:
                revenue = financials[col].get('Total Revenue', 0)
                if revenue > 0:
                    revenues.append(revenue)
            
            if len(revenues) < 2:
                return 0.05
            
            # Calculate compound annual growth rate
            years = len(revenues) - 1
            cagr = (revenues[0] / revenues[-1]) ** (1/years) - 1
            
            # Cap growth rate at reasonable levels
            return max(min(cagr, 0.20), -0.10)
        except:
            return 0.05
    
    def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """Get complete financial analysis"""
        try:
            return {
                'financial_statements': self.get_financial_statements(),
                'wacc_analysis': self.calculate_wacc(),
                'dcf_valuation': self.calculate_dcf_valuation(),
                'financial_ratios': self.analyze_financial_ratios(),
                'symbol': self.symbol
            }
        except Exception as e:
            return {'error': str(e), 'symbol': self.symbol}
