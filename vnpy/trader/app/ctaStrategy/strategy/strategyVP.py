# encoding: UTF-8

"""
一个ATR-RSI指标结合的交易策略，适合用在股指的1分钟和5分钟线上。

注意事项：
1. 作者不对交易盈利做任何保证，策略代码仅供参考
2. 本策略需要用到talib，没有安装的用户请先参考www.vnpy.org上的教程安装
3. 将IF0000_1min.csv用ctaHistoryData.py导入MongoDB后，直接运行本文件即可回测策略

"""

import talib
import numpy as np

from vnpy.trader.vtObject import VtBarData
from vnpy.trader.vtConstant import EMPTY_STRING
from vnpy.trader.app.ctaStrategy.ctaTemplate import CtaTemplate


########################################################################
class VPStrategy(CtaTemplate):
    """结合ATR和RSI指标的一个分钟线交易策略"""

    # conditions
    condition10 = False
    condition11 = False
    condition12 = False
    condition13 = False
    condition14 = False
    condition15 = False
    condition16 = False
    condition17 = False
    condition18 = False
    condition19 = False

    condition20 = False
    condition21 = False
    condition22 = False
    condition23 = False
    condition24 = False
    condition25 = False
    condition26 = False
    condition27 = False
    condition28 = False
    condition29 = False

    condition31 = False
    condition32 = False

    condition99 = False
    conditionPriceLimit = False

    className = 'VPStrategy'
    author = u'Angus'

    # 策略参数
    ma5Param = 5
    ma10Param = 10

    ma5Value = 0
    ma10Value = 0

    max10Profit = 0
    min10Profit = 0

    # rbKParam = ?
    iKParam = 1.66
    jMParam = 0.4

    pCost = 1000

    currentTime = 0
    runtime = 144500

    base = 300
    unitZone = 100
    drawBack= 120

    prb = 24
    pi = 4
    pj = 1

    realProfit = 0
    rPMA5 = 0
    rPMA10 = 0

    rbMAX10 = 0
    rbMIN10 = 0
    iMAX10 = 0
    iMIN10 = 0
    jMAX10 = 0
    jMIN10 = 0

    rbPrice = 0
    iPrice = 0
    jPrice = 0

    outputVars = False
    outputSignal = False
    outputAccountInfo= False

    dealUnits = 1

    # 资金参数
    marginRatio = 0.13

    initDays = 10  # 初始化数据所用的天数

    # 策略条件
    rbHighLimit = iHighLimit = jHighLimit = False
    rbLowLimit = iLowLimit = jLowLimit = False
    limitCondition = rbHighLimit & iHighLimit & jHighLimit & rbLowLimit & iLowLimit & jLowLimit

    # long and short

    def checkConditions(self):

            # long
            if self.ma5Value > self.ma10Value and self.realProfit > 700:
                self.condition10 = True
            if self.ma5Value >= self.ma10Value and 600 < self.realProfit and self.realProfit <= 700 \
                    and self.limitCondition:
                self.condition11 = True
            if self.ma5Value >= self.ma10Value and 500 < self.realProfit and self.realProfit <= 600 \
                    and self.limitCondition:
                self.condition12 = True
            if self.ma5Value >= self.ma10Value and 400 < self.realProfit and self.realProfit <= 500 \
                    and self.limitCondition:
                self.condition13 = True
            if self.ma5Value >= self.ma10Value and 300 < self.realProfit and self.realProfit <= 400 \
                    and self.limitCondition:
                self.condition14 = True
            if self.ma5Value >= self.ma10Value and 200 < self.realProfit and self.realProfit <= 300 \
                    and self.limitCondition:
                self.condition15 = True
            if self.ma5Value >= self.ma10Value and 100 < self.realProfit and self.realProfit <= 200 \
                    and self.limitCondition:
                self.condition16 = True
            if self.ma5Value >= self.ma10Value and 0 < self.realProfit and self.realProfit <= 100 \
                    and self.limitCondition:
                self.condition17 = True
            if self.ma5Value >= self.ma10Value and -100 < self.realProfit and self.realProfit <= 0 \
                    and self.limitCondition:
                self.condition18 = True
            if self.ma5Value >= self.ma10Value and self.realProfit <= -200 \
                    and self.limitCondition:
                self.condition19 = True

            # short

            if self.ma5Value < self.ma10Value and self.realProfit < 100:
                self.condition20 = True
            if self.ma5Value < self.ma10Value and 100 < self.realProfit and self.realProfit <= 200 \
                    and self.limitCondition:
                self.condition21 = True
            if self.ma5Value < self.ma10Value and 200 < self.realProfit and self.realProfit <= 300 \
                    and self.limitCondition:
                self.condition22 = True
            if self.ma5Value < self.ma10Value and 300 < self.realProfit and self.realProfit <= 400 \
                    and self.limitCondition:
                self.condition23 = True
            if self.ma5Value < self.ma10Value and 400 < self.realProfit and self.realProfit <= 500 \
                    and self.limitCondition:
                self.condition24 = True
            if self.ma5Value < self.ma10Value and 500 < self.realProfit and self.realProfit <= 600 \
                    and self.limitCondition:
                self.condition25 = True
            if self.ma5Value < self.ma10Value and 600 < self.realProfit and self.realProfit <= 700 \
                    and self.limitCondition:
                self.condition26 = True
            if self.ma5Value < self.ma10Value and 700 < self.realProfit and self.realProfit <= 800 \
                    and self.limitCondition:
                self.condition27 = True
            if self.ma5Value < self.ma10Value and 800 < self.realProfit and self.realProfit <= 900 \
                    and self.limitCondition:
                self.condition28 = True
            if self.ma5Value < self.ma10Value and self.realProfit > 900 and self.limitCondition:
                self.condition29 = True

            # pingcang
            if self.ma5Value < self.ma10Value and self.realProfit <= self.max10Profit - self.drawBack:
                self.condition31 = True
            if self.ma5Value >= self.ma10Value and self.realProfit >= self.min10Profit - self.drawBack:
                self.condition32 = True

            # runtime check
            if self.currentTime >= self.runtime:
                self.condition99 = True

            # priceLimit
            self.conditionPriceLimit = self.rbHighLimit != self.rbPrice and self.iHighLimit != self.iPrice and \
                                       self.jHighLimit != self.jPrice and self.rbLowLimit != self.rbPrice  and \
                                       self.iLowLimit != self.iPrice and self.jLowLimit != self.jPrice



    # 策略变量
    bar = None  # K线对象
    barMinute = EMPTY_STRING  # K线当前的分钟

    bufferSize = 100  # 需要缓存的数据的大小
    bufferCount = 0  # 目前已经缓存了的数据的计数
    highArray = np.zeros(bufferSize)  # K线最高价的数组
    lowArray = np.zeros(bufferSize)  # K线最低价的数组
    closeArray = np.zeros(bufferSize)  # K线收盘价的数组

    atrCount = 0  # 目前已经缓存了的ATR的计数
    atrArray = np.zeros(bufferSize)  # ATR指标的数组
    atrValue = 0  # 最新的ATR指标数值
    atrMa = 0  # ATR移动平均的数值

    rsiValue = 0  # RSI指标的数值
    rsiBuy = 0  # RSI买开阈值
    rsiSell = 0  # RSI卖开阈值
    intraTradeHigh = 0  # 移动止损用的持仓期内最高价
    intraTradeLow = 0  # 移动止损用的持仓期内最低价

    orderList = []  # 保存委托代码的列表

    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'ma5',
                 'ma10',
                 'trailingPercent']

    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos',
               'ma5Value',
               'ma10Value']

    # ----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        """Constructor"""
        super(VPStrategy, self).__init__(ctaEngine, setting)

        # 注意策略类中的可变对象属性（通常是list和dict等），在策略初始化时需要重新创建，
        # 否则会出现多个策略实例之间数据共享的情况，有可能导致潜在的策略逻辑错误风险，
        # 策略类中的这些可变对象属性可以选择不写，全都放在__init__下面，写主要是为了阅读
        # 策略时方便（更多是个编程习惯的选择）

    # ----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        self.writeCtaLog(u'%s策略初始化' % self.name)

        # 初始化RSI入场阈值
        #self.rsiBuy = 50 + self.rsiEntry
        #self.rsiSell = 50 - self.rsiEntry

        # 载入历史数据，并采用回放计算的方式初始化策略数值
        initData = self.loadBar(self.initDays)
        for bar in initData:
            self.onBar(bar)

        self.putEvent()

    # ----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'%s策略启动' % self.name)
        self.putEvent()

    # ----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'%s策略停止' % self.name)
        self.putEvent()

    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        # 计算K线
        tickMinute = tick.datetime.minute

        if tickMinute != self.barMinute:
            if self.bar:
                self.onBar(self.bar)

            bar = VtBarData()
            bar.vtSymbol = tick.vtSymbol
            bar.symbol = tick.symbol
            bar.exchange = tick.exchange

            bar.open = tick.lastPrice
            bar.high = tick.lastPrice
            bar.low = tick.lastPrice
            bar.close = tick.lastPrice

            bar.date = tick.date
            bar.time = tick.time
            bar.datetime = tick.datetime  # K线的时间设为第一个Tick的时间

            self.bar = bar  # 这种写法为了减少一层访问，加快速度
            self.barMinute = tickMinute  # 更新当前的分钟
        else:  # 否则继续累加新的K线
            bar = self.bar  # 写法同样为了加快速度

            bar.high = max(bar.high, tick.lastPrice)
            bar.low = min(bar.low, tick.lastPrice)
            bar.close = tick.lastPrice

    # ----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        # 撤销之前发出的尚未成交的委托（包括限价单和停止单）
        for orderID in self.orderList:
            self.cancelOrder(orderID)
        self.orderList = []

        # 保存K线数据
        self.closeArray[0:self.bufferSize - 1] = self.closeArray[1:self.bufferSize]
        self.highArray[0:self.bufferSize - 1] = self.highArray[1:self.bufferSize]
        self.lowArray[0:self.bufferSize - 1] = self.lowArray[1:self.bufferSize]

        self.closeArray[-1] = bar.close
        self.highArray[-1] = bar.high
        self.lowArray[-1] = bar.low

        self.bufferCount += 1
        if self.bufferCount < self.bufferSize:
            return

        # 计算指标数值
        self.atrValue = talib.ATR(self.highArray,
                                  self.lowArray,
                                  self.closeArray,
                                  self.atrLength)[-1]
        self.atrArray[0:self.bufferSize - 1] = self.atrArray[1:self.bufferSize]
        self.atrArray[-1] = self.atrValue

        self.atrCount += 1
        if self.atrCount < self.bufferSize:
            return

        self.atrMa = talib.MA(self.atrArray,
                              self.atrMaLength)[-1]
        self.rsiValue = talib.RSI(self.closeArray,
                                  self.rsiLength)[-1]

        # 判断是否要进行交易

        # 当前无仓位
        if self.pos == 0:
            self.intraTradeHigh = bar.high
            self.intraTradeLow = bar.low

            # ATR数值上穿其移动平均线，说明行情短期内波动加大
            # 即处于趋势的概率较大，适合CTA开仓
            if self.atrValue > self.atrMa:
                # 使用RSI指标的趋势行情时，会在超买超卖区钝化特征，作为开仓信号
                if self.rsiValue > self.rsiBuy:
                    # 这里为了保证成交，选择超价5个整指数点下单
                    self.buy(bar.close + 5, self.fixedSize)

                elif self.rsiValue < self.rsiSell:
                    self.short(bar.close - 5, self.fixedSize)

        # 持有多头仓位
        elif self.pos > 0:
            # 计算多头持有期内的最高价，以及重置最低价
            self.intraTradeHigh = max(self.intraTradeHigh, bar.high)
            self.intraTradeLow = bar.low
            # 计算多头移动止损
            longStop = self.intraTradeHigh * (1 - self.trailingPercent / 100)
            # 发出本地止损委托，并且把委托号记录下来，用于后续撤单
            orderID = self.sell(longStop, abs(self.pos), stop=True)
            self.orderList.append(orderID)

        # 持有空头仓位
        elif self.pos < 0:
            self.intraTradeLow = min(self.intraTradeLow, bar.low)
            self.intraTradeHigh = bar.high

            shortStop = self.intraTradeLow * (1 + self.trailingPercent / 100)
            orderID = self.cover(shortStop, abs(self.pos), stop=True)
            self.orderList.append(orderID)

        # 发出状态更新事件
        self.putEvent()

    # ----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        pass

    # ----------------------------------------------------------------------
    def onTrade(self, trade):
        # 发出状态更新事件
        self.putEvent()


    def caculateRealProfit(self,rbdata,idata,jdata):
        #计算利润
        self.realProfit = rbdata-(self.iKParam*idata + self.jKParam*jdata+self.pCost)
        return

