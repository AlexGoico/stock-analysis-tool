class Metrics:
  def __init__(self, backend):
    self.backend = backend

  def market_cap(self,ticker):
    return self.backend.market_cap(ticker)

  def prices(self, ticker):
    return self.backend.prices(ticker)

  # Value Metrics
  def cur_pe(self, ticker):
    return self.backend.cur_pe(ticker)

  def cur_pfcf(self, ticker):
    return self.backend.cur_pfcf(ticker)

  def net_profit_margins(self, ticker):
    return self.backend.net_profit_margins(ticker)

  # Quality Metrics
  def revenues(self, ticker):
    return self.backend.revenues(ticker)

  def profits(self, ticker):
    return self.backend.profits(ticker)

  def fcfs(self, ticker):
    return self.backend.fcfs(ticker)

  def current_assets(self, ticker):
    return self.backend.current_assets(ticker)

  def current_liabilities(self, ticker):
    return self.backend.current_liabilities(ticker)

  def dilluted_shares(self, ticker):
    return self.backend.dilluted_shares(ticker)