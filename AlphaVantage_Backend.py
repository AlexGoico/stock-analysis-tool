from functools import lru_cache
from datetime import datetime

from time import sleep
import requests

API_ENDPOINT = 'https://www.alphavantage.co/query?'

def make_api_call_url(key, ticker, func):
  return f"{API_ENDPOINT}function={func}&symbol={ticker}&apikey={key}"

def get_statement(key, ticker, func, err_msg):
  res = requests.get(make_api_call_url(key, ticker, func))
  sleep(1)

  if res.status_code > 299 or res.status_code < 200:
    raise Exception(err_msg)

  return res.json()

def get_prices(key, ticker):
  url = f"{API_ENDPOINT}function=TIME_SERIES_DAILY&outputsize=full&symbol={ticker}&apikey={key}"
  res = requests.get(url)
  sleep(1)

  if res.status_code > 299 or res.status_code < 200:
    raise Exception(f"Unable to get full list of prices for {ticker}")

  return res.json()

def get_company_overview(key, ticker):
  return get_statement(key, ticker, "OVERVIEW", f"Unable to retrieve {ticker} overview")

def get_income_statement(key, ticker):
  return get_statement(key, ticker, "INCOME_STATEMENT", f"Unable to retrieve {ticker} income statement")

def get_balance_sheet(key, ticker):
  return get_statement(key, ticker, "BALANCE_SHEET", f"Unable to retrieve {ticker} balance sheet")

def get_cash_flow_statement(key, ticker):
  return get_statement(key, ticker, "CASH_FLOW", f"Unable to retrieve {ticker} cashflow statement")

def parse_yymmdd(date_str):
  return datetime.strptime(date_str, '%Y-%m-%d')

def format_yymmdd(date_str):
  return datetime.strftime(date_str, '%Y-%m-%d')

class AlphaVantage_Backend:
  def __init__(self, key):
    self.key = key

  @lru_cache
  def _get_prices(self, ticker):
    return get_prices(self.key, ticker)

  @lru_cache
  def _get_company_overview(self, ticker):
    return get_company_overview(self.key, ticker)

  @lru_cache
  def _get_income_statement(self, ticker):
    return get_income_statement(self.key, ticker)

  @lru_cache
  def _get_balance_sheet(self, ticker):
    return get_balance_sheet(self.key, ticker)

  @lru_cache
  def _get_cashflow_statement(self, ticker):
    return get_cash_flow_statement(self.key, ticker)

  @lru_cache
  def _get_dilluted_eps(key, ticker):
    pass

  def prices(self, ticker):
    return self._get_prices(ticker)

  def market_cap(self, ticker):
    overview = self._get_company_overview(ticker)

    return int(overview['MarketCapitalization'])

  def revenues(self, ticker, tp = 'All'):
    income = self._get_income_statement(ticker)

    revenues = { report['fiscalDateEnding']: int(report['totalRevenue'])
                 for report in income['annualReports'] }

    ttm_reports = sorted(income['quarterlyReports'],
                         key=lambda report: parse_yymmdd(report['fiscalDateEnding']),
                         reverse=True)[:4]
    revenues['ttm'] = sum(int(report['totalRevenue']) for report in ttm_reports)

    return revenues

  def profits(self, ticker, tp = 'All'):
    income = self._get_income_statement(ticker)

    profits = { report['fiscalDateEnding']: int(report['netIncome'])
                for report in income['annualReports'] }

    ttm_reports = sorted(income['quarterlyReports'],
                         key=lambda report: parse_yymmdd(report['fiscalDateEnding']),
                         reverse=True)[:4]

    profits['ttm'] = sum(int(report['netIncome']) for report in ttm_reports)

    return profits

  def fcfs(self, ticker, tp = 'All'):
    cashflows = self._get_cashflow_statement(ticker)

    free_cashflows = {cashflow['fiscalDateEnding']: int(cashflow['operatingCashflow']) + int(cashflow['cashflowFromInvestment'])
                      for cashflow in cashflows['annualReports']}

    ttm_cashflows = ttm_reports = sorted(cashflows['quarterlyReports'],
                                         key=lambda report: parse_yymmdd(report['fiscalDateEnding']),
                                         reverse=True)[:4]

    free_cashflows['ttm'] = sum(int(cashflow['operatingCashflow']) + int(cashflow['cashflowFromInvestment'])
                                for cashflow in ttm_cashflows)

    return free_cashflows

  def cur_pe(self, ticker):
    overview = self._get_company_overview(ticker)

    return float(overview['PERatio'])

  def cur_pfcf(self, ticker):
    market_cap = self.market_cap(ticker)
    fcf = self.fcfs(ticker)['ttm']

    return market_cap / fcf

  def current_assets(self, ticker, tp = 'All'):
    balance_sheet = self._get_balance_sheet(ticker)

    assets = {report['fiscalDateEnding']: int(report['totalCurrentAssets'])
              for report in balance_sheet['annualReports']}

    ttm_assets = ttm_reports = sorted(balance_sheet['quarterlyReports'],
                                      key=lambda report: parse_yymmdd(report['fiscalDateEnding']),
                                      reverse=True)[:4]

    assets['ttm'] = sum(int(report['totalCurrentAssets']) for report in ttm_assets)

    return assets

  def current_liabilities(self, ticker, tp='All'):
    balance_sheet = self._get_balance_sheet(ticker)

    liabilities = {report['fiscalDateEnding']: int(report['totalCurrentLiabilities'])
                   for report in balance_sheet['annualReports']}

    ttm_liabilities = ttm_reports = sorted(balance_sheet['quarterlyReports'],
                                      key=lambda report: parse_yymmdd(report['fiscalDateEnding']),
                                      reverse=True)[:4]

    liabilities['ttm'] = sum(int(report['totalCurrentLiabilities']) for report in ttm_liabilities)

    return liabilities

  def net_profit_margins(self, ticker, tp = 'All'):
    revenues = self.revenues(ticker)
    profits = self.profits(ticker)

    npms = { dt: profits[dt] / rev for dt, rev in revenues.items() }

    return npms

  def dilluted_total_shares(self, ticker):
    pass