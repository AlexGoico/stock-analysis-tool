import simfin as sf

class SimFin_Backend:
  def __init__(self, key):
    sf.set_data_dir('~/stock_data/')
    sf.set_api_key(api_key='free')

  def net_profit_margin(self):
    pass