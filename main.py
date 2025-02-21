from object import Market

if __name__ == "__main__":
    markets = Market.getMarkets()
    market = markets[0]
    boxs = market.getBoxs()
    for box in boxs:
        box.showBox() 