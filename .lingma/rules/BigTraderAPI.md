---
trigger: model_decision
description: 本文档是 BigTrader 量化交易框架的完整 API 类型定义文件（bigtrader.pyi），包含了所有可用的类、方法、枚举和数据结构的详细说明。BigTrader 是 BigQuant 平台的核心交易引擎，支持回测、模拟交易和实盘交易。在编写量化程序的时候生效。
---
BigTrader API 参考
#
📖 文档说明
#

这个文档是什么
本文档是 BigTrader 量化交易框架的完整 API 类型定义文件（bigtrader.pyi），包含了所有可用的类、方法、枚举和数据结构的详细说明。BigTrader 是 BigQuant 平台的核心交易引擎，支持回测、模拟交易和实盘交易。

#

🎯 适用人群
🔰 量化新手：了解 BigTrader 的核心概念和基础用法

💻 策略开发者：查询具体 API 用法和参数说明

🚀 专业用户：全面掌握 BigTrader 的高级功能

🤖 AI 辅助开发：提供给大模型进行代码生成和解释

#

📚 如何使用这个文档？
#

方式一：按需查询
# 需要下单时，搜索 "order" 相关方法
context.order(instrument, volume, limit_price)
context.order_target_percent(instrument, target_percent)

# 需要获取数据时，查找 "IBarData" 类
data.current(instrument, 'close')
data.history(instrument, 'close', 20, '1d')
#

方式二：AI 辅助学习
将相关 API 定义复制给 AI 助手，让其：

生成示例代码

解释复杂概念

推荐最佳实践

#

方式三：系统学习
按以下顺序阅读核心概念：

枚举类型：Market, Frequency, OrderType 等

数据结构：IBarData, IPositionData, IOrderData 等

核心接口：IContext 的交易和查询方法

策略模板：HandleDataLib 的预置策略

#

💡 快速入门提示
#

基础概念速览
# 核心对象关系
Context (策略上下文)
├── Data (市场数据)
├── Portfolio (投资组合) 
├── Orders (订单管理)
└── Positions (持仓管理)

# 常用交易流程
def handle_data(context, data):
    # 1. 获取数据
    price = data.current('000001.SZ', 'close')
    
    # 2. 策略逻辑
    if 满足买入条件:
        # 3. 下单交易
        context.order_target_percent('000001.SZ', 0.5)
#

关键 API 速查
| 功能 | 主要方法 | 说明 |
|------|---------|------|
| 数据获取 | `data.current()`, `data.history()` | 获取当前和历史数据 |
| 订单交易 | `context.order()`, `context.order_target_percent()` | 下单和目标仓位 |
| 持仓查询 | `context.get_positions()`, `context.get_position()` | 查询持仓情况 |
| 账户信息 | `context.get_balance()`, `context.get_available_cash()` | 资金信息 |
#

⚠️ 重要提醒
返回值检查：多数交易方法返回错误码，0 表示成功，其他值表示失败

类型安全：严格按照类型定义传参，避免类型错误

异常处理：在实盘交易中务必做好异常处理和风控

版本兼容：API 可能随版本更新，建议定期查看更新日志

#

🔗 相关资源
策略示例：查看 BigQuant 社区的策略分享

用户手册：更详细的使用教程和最佳实践

API 更新：关注平台公告获取最新功能

#

bigtrader.pyi
以下是 BigTrader 的完整 API 类型定义

import enum
from typing import Any, Dict, List, Set, Type, Union

class Market(Enum):
    """Market Definition"""
    DEFAULT=""
    """Default market, usually not specified."""
    CN_STOCK="cn_stock"
    """China Stock Market."""
    CN_FUND="cn_fund"
    """China Fund Market."""
    CN_FUTURE="cn_future"
    """China Futures Market."""
    CN_OPTION="cn_option"
    """China Options Market."""
    CN_CBOND="cn_cbond"
    """China Convertible Bond Market."""
    CN_BOND="cn_bond"
    """China Bond Market."""
    CN_STOCK_INDEX="cn_stock_index"
    """China Stock Index Market."""
    CN_FUTURE_INDEX="cn_future_index"
    """China Futures Index Market."""
    HK_STOCK="hk_stock"
    """Hong Kong Stock Market."""
    SG_STOCK="sg_stock"
    """Singapore Stock Market."""
    US_STOCK="us_stock"
    """US Stock Market."""
    HK_STOCK_INDEX="hk_stock_index"
    """Hong Kong Stock Index Market."""
    US_STOCK_INDEX="us_stock_index"
    """US Stock Index Market."""
    CC_SPOT="cc_spot"
    """Crypto Currency Spot Market."""
    CC_FUTURE_UM="cc_future_um"
    """Crypto Currency Futures Market, settled in USD."""
    CC_FUTURE_CM="cc_future_cm"
    """Crypto Currency Futures Market, settled in Coin."""

class Frequency(Enum):
    """Data Frequency"""
    NONE=""
    """No frequency specified."""
    TICK="tick"
    """Tick data: the most granular level of market data, recording every transaction."""
    TICK2="tick2"
    """Tick2 data: a higher frequency tick data, might be platform specific."""
    MINUTE="1m"
    """1-minute bar data."""
    HOUR="1h"
    """1-hour bar data."""
    DAILY="1d"
    """Daily bar data."""
    WEEK="1w"
    """Weekly bar data."""

class AccountType(_CustomEnum):
    """Account Category"""
    NONE=""
    """Unknown account type."""
    STOCK="0"
    """Stock account (for trading stocks)."""
    FUTURE="1"
    """Futures account (for trading futures)."""
    OPTION="2"
    """Options account (for trading options)."""
    CREDIT="3"
    """Credit account (for margin trading)."""

class SubscribeFlag(_CustomIntEnum):
    """Subscription Flags for Market Data"""
    DEFAULT=0
    """Default subscription flag."""
    L1Snapshot=1
    """Level 1 Snapshot: Top of book market data, including best bid and ask prices."""
    L2Snapshot=2
    """Level 2 Snapshot: Full order book market data, showing multiple price levels."""
    L2Trade=4
    """Level 2 Trade: Detailed trade data, including every transaction."""
    L2Order=8
    """Level 2 Order: Detailed order data, including every order placement and cancellation."""
    L2OrderQueue=16
    """Level 2 Order Queue: Order queue data, showing the sequence of orders at each price level."""
    KLINE=32
    """K-line data: OHLC (Open, High, Low, Close) bar data."""

class Direction(_CustomEnum):
    """Direction (trade side) of order/trade/position."""
    NONE=""
    """No direction specified."""
    LONG="1"
    """Long position (buy to open or close short)."""
    SHORT="2"
    """Short position (sell to open or close long)."""
    BUY="1"
    """Buy order/trade."""
    SELL="2"
    """Sell order/trade."""
    NET="N"
    """Net position."""
    COVERED="C"
    """Covered position (e.g., covered call)."""

class OptionCP(_CustomEnum):
    """Option Type: Call or Put"""
    NONE=""
    """No option type specified."""
    CALL="C"
    """Call option."""
    PUT="P"
    """Put option."""

class HedgeFlag(_CustomEnum):
    """Hedge Flag for trading strategy: Speculation, Arbitrage, Hedge etc."""
    NONE=""
    """No hedge flag specified."""
    Speculation="1"
    """Speculation: Trading for profit based on price movements."""
    Arbitrage="2"
    """Arbitrage: Trading to profit from price differences in different markets or instruments."""
    Hedge="3"
    """Hedging: Trading to reduce risk from existing positions."""
    MarketMaker="5"
    """Market Maker: Providing liquidity to the market by placing buy and sell orders."""
    SpecHedge="6"
    """Speculation-Hedge (DCE Specific): First leg is speculation, second leg is hedging, specific to Dalian Commodity Exchange (DCE)."""
    HedgeSpec="7"
    """Hedge-Speculation (DCE Specific): First leg is hedging, second leg is speculation, specific to Dalian Commodity Exchange (DCE)."""

class StrikeType(_CustomEnum):
    """Option Exercise Type (Strike Style)"""
    American="A"
    """American style: option can be exercised at any time before expiration."""
    Europe="E"
    """European style: option can only be exercised at expiration date."""
    Bermuda="B"
    """Bermudan style: option can be exercised on specific dates before expiration."""

class OffsetFlag(_CustomEnum):
    """Offset Flag of order/trade: Open, Close, CloseToday, etc."""
    NONE=""
    """No offset flag specified."""
    OPEN="0"
    """Open position."""
    CLOSE="1"
    """Close position (generic close, could be close yesterday or close today depending on rules)."""
    CLOSETODAY="2"
    """Close today's position (specifically close positions opened on the same trading day)."""
    CLOSEYESTERDAY="3"
    """Close yesterday's position (specifically close positions opened before the current trading day)."""
    EXERCISE="E"
    """Option exercise."""

class OrderType(_CustomEnum):
    """Order Type: Limit order, Market order, etc."""
    LIMIT="0"
    """Limit order: An order to buy or sell at a specified price or better."""
    MARKET="U"
    """Market order (for stocks): Fill immediately at the best available prices within the top 5 bid/ask levels, and cancel any remaining quantity."""
    MKT2LMT="S"
    """Market-to-Limit order (for stocks): Fill immediately at the best available prices within the top 5 bid/ask levels, and convert any remaining quantity to a limit order at the last filled price."""
    COUNTERPARTY_PRICE="2"
    """Counterparty price order: Execute at the best price offered by the counterparty."""
    BEST_PRICE="3"
    """Best price order: Execute at the current best bid (for sell) or ask (for buy) price."""
    LAST_PRICE="4"
    """Last price order: Execute at the price of the last transaction."""
    LAST_PRICE_PLUS1="5"
    """Last price plus 1 tick order: Execute at the last transaction price plus one tick increment."""
    LAST_PRICE_MINUS1="6"
    """Last price minus 1 tick order: Execute at the last transaction price minus one tick increment."""
    ASK_PRICE1="8"
    """Ask price 1 order: Execute at the current best ask price (sell order)."""
    BID_PRICE1="C"
    """Bid price 1 order: Execute at the current best bid price (buy order)."""
    FIVELEVEL_PRICE="G"
    """Five-level price order:  Execute at the average price of the top 5 bid/ask levels."""
    LIMIT_L="L"
    """BigQuant Limit-L order: Limit order with price dynamically adjusted based on a floating ratio from the latest price."""
    LIMIT_P="P"
    """BigQuant Limit-P order: Limit order with price dynamically adjusted based on a floating ratio from the previous day's closing price."""

class OrderStatus(_CustomIntEnum):
    """Order Status."""
    NOTTRADED=0
    """Not traded: Order has been placed but not yet filled."""
    PARTTRADED=1
    """Partially traded: Order has been partially filled."""
    ALLTRADED=2
    """All traded: Order has been completely filled."""
    PARTCANCELLED=3
    """Partially cancelled: Order has been partially cancelled, some quantity might have been traded."""
    CANCELLED=4
    """Cancelled: Order has been completely cancelled, no quantity traded."""
    REJECTED=5
    """Rejected: Order was rejected by the exchange or broker."""
    UNKNOWN=6
    """Unknown: Order status is unknown."""
    NOTTRIGGER=7
    """Not triggered: Conditional order has not yet met its trigger condition."""
    TRIGGERED=8
    """Triggered: Conditional order has met its trigger condition and is waiting to be placed."""
    WAITCONFIRM=9
    """Wait confirm: Order is waiting for confirmation from the exchange or broker."""
    NOTPLACE=10
    """Not placed: Order has been created but not yet submitted to the exchange."""
    PLACING=11
    """Placing: Order is being submitted to the exchange."""
    PENDINGPLACE=12
    """Pending place: Order is waiting to be submitted to the exchange."""
    INTERREMOVED=13
    """Removed: Order has been internally removed by the system."""
    ACCEPTED=14
    """Accepted: Order has been accepted by the server (exchange or broker)."""
    PARTPENDINGCANCEL=15
    """Partially filled pending cancel: Order is partially filled and the remaining quantity is pending cancellation."""
    PENDINGCANCEL=16
    """Pending cancel: Order cancellation request is pending."""
    EXPIRED=17
    """Expired: Order has expired and is no longer valid."""
    GENERATED=10
    """DO NOT use this"""

class OrderProperty(_CustomEnum):
    """Order Properties (attributes)"""
    NONE=""
    """No specific order property."""
    FAK="FAK"
    """Fill and Kill (FAK): Order must be filled immediately and completely, otherwise it will be cancelled."""
    FOK="FOK"
    """Fill or Kill (FOK): Order must be filled immediately and completely, otherwise it will be cancelled. Similar to FAK but usually implies the entire order must be filled."""
    Creation="Creation"
    """Creation: Order for fund creation (subscription)."""

class VMatchAt(_CustomIntEnum):
    """Virtual Matching Mechanism for Backtesting"""
    NEXT=0
    """Next bar matching: Orders are matched at the open price of the next bar after the signal."""
    CURRENT=1
    """Current bar matching: Orders are matched within the current bar, using a simplified matching logic."""

class BSFlag(_CustomIntEnum):
    """Buy/Sell Flag in Tick Data.
    
    This enum represents the Buy/Sell/Cancel flag as recorded in tick-by-tick (逐笔) market data streams within the BigQuant platform.
    It helps to identify the nature of each tick data point, indicating whether it was associated with a buy order, sell order, or order cancellation."""
    NONE=78
    """NONE flag.
    
        Represents a state where the Buy/Sell flag is not explicitly identified or available in the data.
        It can be used as a default or placeholder value when the flag information is missing."""
    BUY=66
    """BUY flag.
    
        Indicates that the tick data point is associated with a buy order.
        This means a trade or order activity occurred on the buy side of the order book."""
    SELL=83
    """SELL flag.
    
        Indicates that the tick data point is associated with a sell order.
        This means a trade or order activity occurred on the sell side of the order book."""
    CANCEL=67
    """CANCEL flag.
    
        Indicates that the tick data point is associated with an order cancellation.
        This signifies that a previously placed order was cancelled and removed from the order book."""

class FilledType(_CustomIntEnum):
    """Fill Type in Level 2 Market Data.
    
    This enum defines the types of fills or executions reported in Level 2 market data within the BigQuant platform.
    It distinguishes between different execution scenarios, such as regular fills and cancelled fills, providing insights into the nature of market transactions."""
    NONE=0
    """NONE fill type.
    
        Represents a state where the fill type is not explicitly identified or available.
        It can be used as a default value when the specific fill type is unknown or not applicable."""
    F=70
    """Regular Fill Type (F).
    
        Indicates a normal market trade execution where an order is successfully matched and filled against a counterparty.
        'F' stands for 'Filled' or 'Trade' in typical market data conventions."""
    C=67
    """Cancelled Fill Type (C).
    
        Indicates a fill that occurred as a result of an order cancellation.
        This might happen when a limit order is cancelled, and the cancellation itself triggers a partial or full fill at a certain price level, especially in specific market microstructures.
        'C' stands for 'Cancelled' in market data context."""

class IMarginRateData:
    """Margin Rate Data Class
    
    Represents the margin rate information for a specific contract, used in risk management and margin calculation within the BigQuant platform.
    This data is crucial for determining the required margin when trading leveraged instruments like futures and options."""
    exchange: str
    trading_code: str
    instrument: str
    trading_day: str
    account_id: str
    broker_id: str
    hedge_flag: str
    long_margin_ratio_by_money: float
    long_margin_ratio_by_volume: float
    short_margin_ratio_by_money: float
    short_margin_ratio_by_volume: float
    is_relative: int
    gateway_name: str

class IContractData:
    """Contract Data Class
    
    Provides detailed information about a tradable contract, including futures, stocks, options, etc., within the BigQuant system.
    This class contains all static information about a contract that is essential for trading and market analysis."""
    trading_code: str
    exchange: str
    instrument: str
    name: str
    trading_day: str
    product_code: str
    product_type: str
    multiplier: float
    price_tick: float
    list_date: str
    delist_date: str
    security_status: int
    sub_stk_type: str
    long_margin_ratio: float
    short_margin_ratio: float
    day_trading: int
    buy_unit: int
    sell_unit: int
    min_volume: int
    strike_price: float
    strike_type: StrikeType
    option_type: OptionCP
    underlying: str
    optcontract_id: str
    deliver_date: str
    strike_date: str
    margin_param1: float
    margin_param2: float
    underlying_pre_close: float
    underlying_pre_settle: float
    pre_close: float
    pre_settle: float
    upper_limit: float
    lower_limit: float

class IOrderReq:
    """Order Request Class
    
    Represents an order request to be sent to the trading engine for execution.
    This class encapsulates all necessary parameters for placing a new order, including contract details, price, quantity, and order type."""
    account_id: str
    acct_type: str
    broker_id: str
    trading_code: str
    exchange: str
    instrument: str
    order_price: float
    order_qty: int
    order_type: OrderType
    order_property: OrderProperty
    direction: Direction
    offset_flag: OffsetFlag
    covered_flag: int
    hedge_flag: str
    order_key: str
    user_id: str
    order_id: str
    front_id: int
    session_id: int
    datetime: Any
    dt: "datetime"
    name: str
    trading_day: str
    order_time: str
    order_status: OrderStatus
    status_msg: str
    contract: "IContractData"
    op_station: str
    order_cmd: str
    order_cmd_value: Any
    order_params: Any
    sim_que_volume: int
    sim_last_volume: int

class IOrderData:
    """Order Data Class
    
    Represents the current status and details of an order that has been placed into the trading system.
    This class provides real-time updates on order execution, including filled quantity, average price, and order status."""
    broker_id: str
    account_id: str
    acct_type: str
    exchange: str
    trading_code: str
    instrument: str
    trading_day: str
    order_id: str
    order_sysid: str
    bt_order_sysid: str
    direction: Direction
    offset_flag: OffsetFlag
    order_price: float
    order_qty: int
    filled_qty: int
    avg_price: float
    filled_money: float
    order_status: OrderStatus
    order_type: OrderType
    order_property: OrderProperty
    covered_flag: int
    status_msg: str
    user_id: str
    order_key: str
    insert_date: str
    order_time: str
    cancel_time: str
    order_datetime: str
    name: str
    entrust_no: str
    algo_order_id: int
    contract: Any
    is_last: bool
    front_id: int
    session_id: int
    gateway_name: str
    sim_que_volume: int
    sim_last_volume: int

class ITradeData:
    """Trade Data Class
    
    Represents a single trade execution (fill). Each trade represents a portion of an order that has been successfully matched and executed in the market.
    This class contains details about the trade price, quantity, direction, and associated order information."""
    broker_id: str
    account_id: str
    acct_type: str
    trading_code: str
    exchange: str
    instrument: str
    order_id: str
    order_sysid: str
    bt_order_sysid: str
    trade_id: str
    bt_trade_id: str
    user_id: str
    order_key: str
    direction: Direction
    offset_flag: OffsetFlag
    filled_qty: int
    filled_price: float
    filled_money: float
    trading_day: str
    hedge_flag: str
    trade_type: str
    trade_date: str
    trade_time: str
    trade_datetime: "datetime"
    name: str
    margin: float
    commission: float
    realized_pnl: float
    covered_flag: int
    is_last: bool
    contract: Any
    order_qty: int
    algo_order_id: int
    entrust_no: str
    creator: str
    gateway_name: str

class IPositionData:
    """Position Data Class
    
    Represents the current holding of a contract in a trading account.
    This class provides information on the quantity held, average cost, profit and loss, and other relevant details for position management."""
    account_id: str
    acct_type: str
    broker_id: str
    exchange: str
    trading_code: str
    instrument: str
    name: str
    direction: Direction
    current_qty: int
    frozen_qty: int
    today_frozen_qty: int
    avail_qty: int
    cost_price: float
    today_qty: int
    yd_qty: int
    position_pnl: float
    commission: float
    hedge_flag: str
    trading_day: str
    open_date: str
    open_price: float
    last_price: float
    margin: float
    market_value: float
    profit_ratio: float
    dividend_qty: int
    dividend_cash: float
    frozen_margin: float
    frozen_commission: float
    sum_buy_value: float
    sum_sell_value: float
    hold_days: int
    settle_price: float
    contract: Any
    position_key: str
    realized_pnl: float
    update_time: str
    user_id: str
    is_last: bool
    gateway_name: str

class IPortfolio:
    cash: float
    positions: dict[str, IPositionData]
    portfolio_value: float

class IL2TradeData:
    """Level 2 Trade Data Structure.
    
    Represents the structure for tick-by-tick trade data received from Level 2 market data feeds.
    This data structure is crucial for high-frequency trading strategies and detailed market analysis as it provides granular information about each individual trade execution.
    It captures essential details such as the instrument traded, timestamp of the trade, volume, price, and various sequence numbers for tracking data flow and order book dynamics.
    
    Attributes:
        instrument (str): The trading instrument (e.g., '000001.SZ').
        datetime (datetime): The timestamp of the trade execution. This is a Python datetime object representing the exact time of the trade.
        volume (int): The volume of the trade, representing the number of shares or contracts traded in this transaction.
        price (float): The price at which the trade was executed.
        seq_num (int): The sequence number of this trade data point within the market data stream. It can be used to ensure data integrity and order.
        bid_seq_num (int): The sequence number of the best bid order at the time of this trade. Useful for reconstructing order book states.
        ask_seq_num (int): The sequence number of the best ask order at the time of this trade. Useful for reconstructing order book states.
        bs_flag (BSFlag): The Buy/Sell flag indicating the direction of the initiating order for this trade. Uses the :class:`BSFlag` enum.
        filled_type (FilledType): The type of fill or execution. Uses the :class:`FilledType` enum to specify if it's a regular fill or a cancelled fill.
        money (float): The total transaction amount for this trade, calculated as volume * price.
        time (int): The time of the trade, typically represented in milliseconds or nanoseconds since the start of the day or a specific epoch. The exact unit should be defined in the platform's data specification."""
    instrument: str
    datetime: "datetime"
    volume: int
    price: float
    seq_num: int
    bid_seq_num: int
    ask_seq_num: int
    bs_flag: BSFlag
    filled_type: FilledType
    money: float
    time: int

class IL2OrderData:
    """Level 2 Order Data Structure.
    
    Represents the structure for tick-by-tick order data from Level 2 market data feeds.
    While the name might suggest order placement data, based on the attributes, it likely represents data related to order *events* observed in the market stream,
    such as order executions or order book updates rather than original order requests. This structure provides detailed information about order-level activities in the market.
    
    Attributes:
        instrument (str): The trading instrument (e.g., '000001.SZ').
        datetime (datetime): The timestamp of the order event. This is a Python datetime object indicating when the order event was recorded.
        volume (int): The volume associated with this order event. It could represent the quantity of shares or contracts involved in an order execution or update.
        price (float): The price associated with the order event. For example, the execution price of a trade or the limit price of an order in the book.
        seq_num (int): The sequence number of this order data point in the market data stream. Useful for maintaining data order and integrity.
        bs_flag (BSFlag): The Buy/Sell flag indicating whether the order event is on the buy or sell side. Uses the :class:`BSFlag` enum.
        order_type (OrderType): The type of order associated with this event. Uses the :class:`OrderType` enum (Note: OrderType enum definition is assumed and should be available in `bigtrader`). This could specify if it was a market order, limit order, etc., related to the event.
        time (int): The time of the order event, typically in milliseconds or nanoseconds since the start of the day or a specific epoch. The exact unit should be consistent with the platform's data specification."""
    instrument: str
    datetime: "datetime"
    volume: int
    price: float
    seq_num: int
    bs_flag: BSFlag
    order_type: "OrderType"
    time: int

class ICommissionRateData:
    """Commission Rate Information Class for Instruments"""
    exchange: str
    trading_code: str
    instrument: str
    trading_day: str
    account_id: str
    broker_id: str
    open_ratio_by_money: float
    open_ratio_by_volume: float
    close_ratio_by_money: float
    close_ratio_by_volume: float
    close_today_ratio_by_money: float
    close_today_ratio_by_volume: float
    gateway_name: str

class ISlippageModel:
    """Abstract base class for slippage models in bigtrader.
    
    In quantitative trading, slippage refers to the difference between the expected price of a trade and the price at which the trade is actually executed.
    Slippage models are used in backtesting and live trading simulations to realistically estimate this difference,
    taking into account factors like market volatility, order size, and trading volume.
    
    This class defines the interface for all slippage models used in bigtrader.
    Subclasses should implement the `process_order` method to define specific slippage calculation logic."""
    def get_raw_price_field(self, is_buy: bool) -> str:
        """Get the raw price field name based on the order direction (buy or sell).
        
        This method is used internally to retrieve the configured price field
        for either buy or sell orders.
        
        Args:
            is_buy (bool): True if it's a buy order, False for a sell order.
        
        Returns:
            str: The name of the price field to be used (e.g., "open", "close")."""
        ...
    def process_order(self, data: Any, order: IOrderData) -> Union[tuple[float, int], list[tuple[float, int]]]:
        """Abstract method to process an order and simulate order matching with slippage.
        
        This method must be implemented by concrete slippage model classes.
        It takes market data and an order as input and determines the trade execution price and volume,
        potentially considering slippage based on the specific model's logic.
        
        Args:
            data (Any): Market data object. This can be either ITickData (for tick-level slippage) or IBarData (for bar-level slippage).
                        The specific type depends on the implementation of the slippage model and the backtesting/trading engine's data handling.
            order (IOrderData): The order object to be processed.
                                 It contains information about the order, such as trading code, volume, price, and order direction (buy/sell).
        
        Returns:
            Tuple[float, int] | List[Tuple[float, int]]:
            - If a single trade occurs, returns a tuple of (trade_price, trade_volume).
            - If the order is filled across multiple ticks or bars (possible for large orders or certain slippage models),
              it can return a list of tuples, where each tuple represents a partial fill with (trade_price, trade_volume).
        
        Raises:
            NotImplementedError: If the method is not implemented in a subclass."""
        ...

class ITickData:
    """Tick data class for representing real-time or historical tick-level market data in bigtrader.
    
    Tick data is the most granular level of market data, recording every individual transaction and quote update.
    This class encapsulates all the relevant information available in a tick data point,
    including price, volume, time, and order book information (bid/ask prices and volumes).
    
    This data is essential for high-frequency trading strategies and precise backtesting."""
    trading_code: str
    exchange: str
    instrument: str
    time: int
    datetime: "datetime"
    trading_day: str
    action_day: str
    volume: int
    amount: float
    last_price: float
    open_price: float
    high_price: float
    low_price: float
    pre_close: float
    pre_settlement: float
    pre_open_interest: int
    open_interest: int
    close_price: float
    settlement: float
    upper_limit: float
    lower_limit: float
    deal_number: int
    iopv: float
    bid_price1: float
    bid_price2: float
    bid_price3: float
    bid_price4: float
    bid_price5: float
    ask_price1: float
    ask_price2: float
    ask_price3: float
    ask_price4: float
    ask_price5: float
    bid_volume1: int
    bid_volume2: int
    bid_volume3: int
    bid_volume4: int
    bid_volume5: int
    ask_volume1: int
    ask_volume2: int
    ask_volume3: int
    ask_volume4: int
    ask_volume5: int
    pre_delta: float
    curr_delta: float
    gateway_name: str

class IBar:
    """Bar Data Class
    
    Represents OHLCV (Open, High, Low, Close, Volume) bar data for a specific instrument over a given period.
    This class is commonly used for time-series analysis and charting in quantitative trading strategies."""
    instrument: str
    datetime: "datetime"
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    open_interest: int
    pre_close: float
    upper_limit: float
    lower_limit: float
    adjust_factor: float
    trading_day: str
    period: str

class IBarData:
    """Provides methods to access spot value or history windows of price data.
    Also provides some utility methods to determine if an asset is alive,
    has recent trade data, etc.
    
    This is what is passed as ``data`` to the ``handle_data`` function."""
    @property
    def current_dt(self) -> "datetime":
        """Get the current datetime of the backtest, simulation or live trading.
        
        Returns:
        -------
        datetime
            The current datetime."""
        ...
    def current(self, instrument: str, fields: Union[str, list[str]]) -> Union[float, int, str, "pd.Series"]:
        """Get the current value of the given instrument for the specified fields at the current time.
        
        Parameters
        ----------
        instrument : str
            The trading instrument, e.g., '000001.SZ', '600888.SH'.
        fields : str or list[str]
            The fields to retrieve.
            Valid values are: "price", "open", "high", "low", "close", "volume", "amount", etc.
        
        Returns:
        -------
        Union[float, int, str, "pd.Series"]
            The current value(s) of the requested fields.
            Returns a single value if `fields` is a string, otherwise returns a pandas Series."""
        ...
    def get_daily_value(self, instrument: str, field: Union[str, list[str]], dt: Union[str, "datetime"]) -> Union[float, int, str, "pd.Series"]:
        """Get the daily value of the instrument for the specified field(s).
        Retrieves the latest daily data, and is more performant than the `history` function for daily data.
        
        Parameters
        ----------
        instrument : str
            The trading instrument, e.g., '000001.SZ', '600888.SH'.
        field : str or list[str]
            The field(s) to retrieve.
            Valid values are: "price", "open", "high", "low", "close", "volume", "amount", etc.
        dt : str or datetime, optional
            The date to retrieve data for. If None, defaults to the current date.
            Can be a string in 'YYYY-MM-DD' format or a datetime object.
        
        Returns:
        -------
        Union[float, int, str, "pd.Series"]
            The daily value(s) of the requested field(s).
            Returns a single value if `field` is a string, otherwise returns a pandas Series."""
        ...
    def history(self, instrument: str, fields: Union[str, list[str]], bar_count: int, frequency: str, expect_ndarray: Any) -> Union["pd.Series", "pd.DataFrame", "np.ndarray"]:
        """Get historical data for the given instrument and fields in a window.
        
        Parameters
        ----------
        instrument : str
            The trading instrument, e.g., '000001.SZ', '600888.SH'.
        fields : str or list[str]
            The fields to retrieve in history.
            Valid values are: "price", "open", "high", "low", "close", "volume", "amount", etc.
        bar_count : int
            The number of bars (data points) to retrieve.
        frequency : str
            The frequency of the data.
            "1m" for minute data (Frequency.MINUTE), "1d" for daily data (Frequency.DAILY).
        expect_ndarray : bool, optional
            Whether to return a NumPy ndarray. If False (default), returns pandas Series or DataFrame. ndarray is more efficient.
        
        Returns:
        -------
        Union["pd.Series", "pd.DataFrame", "np.ndarray"]
            Historical data in a pandas Series (if single field, single instrument),
            pandas DataFrame (if multiple fields or multiple instruments), or NumPy ndarray if `expect_ndarray=True`."""
        ...

class PerOrder:
    """Calculates commission for stock orders in the China A-share market.
    
    This commission model is designed specifically for the China A-share market and
    takes into account common commission structures in that market. It includes
    components for both buying and selling, and a minimum commission amount.
    
    Attributes:
        buy_cost (float): Commission rate for buying orders, expressed as a decimal (e.g., 0.0003 for 0.03%).
        sell_cost (float): Commission rate for selling orders, expressed as a decimal (e.g., 0.0013 for 0.13%).
            This typically includes the stamp duty which is only charged on selling in China A-share market.
        min_cost (float): Minimum commission amount charged per order, in CNY.
        tax_ratio (float, optional):  Tax rate applied to transactions. If set to `None`, no additional tax is applied.
            Note that stamp duty is included in `sell_cost`, this `tax_ratio` is for other potential taxes if needed.
            Defaults to `None`.
    
    Example:
        To create a PerOrder commission model with standard China A-share commission rates:
    
        >>> context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5.0))"""
    pass

class PerContract:
    """Calculates commission for futures or other contract-based transactions based on a per-contract cost.
    
    This commission model is suitable for futures, options, and other instruments where
    commissions are typically charged per contract traded. It allows for different commission
    rates for different underlying symbols and supports separate rates for opening, closing, and
    closing today positions, which is common in futures markets.
    
    The commission cost can be defined either as a fixed amount per contract or as a percentage
    of the contract value (though in the current implementation, it's configured as a percentage-like rate).
    
    Parameters:
        cost (dict[str, tuple[float, float, float]]): A dictionary mapping root symbols (e.g., 'IF', 'AU') to commission costs.
            The value for each root symbol is a tuple of three floats representing the commission rate for:
            - Opening a position
            - Closing a position (normal close)
            - Closing a position opened and closed on the same day (close today).
    
            The commission rate should be a decimal representing the percentage of transaction value,
            e.g., `0.000023` for 0.0023%.
    
    Example:
                `cost={'IF': (0.000023, 0.000115, 0.000023), 'AU': (0.0001, 0.0002, 0.0001)}`
                This means for 'IF' contracts:
                    - Opening commission rate is 0.0023%
                    - Closing commission rate is 0.0115%
                    - Close today commission rate is 0.0023%
                And for 'AU' contracts:
                    - Opening and close_today rate is 0.01%
                    - Closing rate is 0.02%
    
    Raises:
        Exception: If `cost` is not a dictionary or if the values in the dictionary are not tuples of length 3.
    
    Note:
        - This commission model is designed to be used with BigTrader's backtesting and trading engine.
        - The root symbol is typically the first part of the instrument ID (e.g., 'IF' from 'IF2312.CCFX').
        - BigTrader's context object (`context`) is usually used to set the commission model in a strategy.
          For example: `context.set_commission(futures_commission=PerContract(cost={'IF':(0.000023, 0.000115, 0.000023)}))`"""
    @property
    def cost_per_contract(self) -> dict[str, tuple[float, float, float]]:
        """Returns the dictionary of per-contract commission costs.
        
        This property allows access to the configured commission costs for each root symbol.
        
        Returns:
            dict[str, tuple[float, float, float]]: A dictionary where keys are root symbols and values
                are tuples of commission rates (open, close, close_today)."""
        ...

class IContext:
    """IContext interface class, defines the abstract methods for the bigtrader strategy context.
    StrategyContext will inherit from IContext and implement the concrete context for backtesting/live trading environments."""
    data: Union["pd.DataFrame", Any]
    options: dict[str, Any]
    user_store: dict[str, Any]
    start_date: str
    end_date: str
    first_trading_date: str
    trading_day_index: int
    logger: structlog.stdlib.BoundLogger

    @property
    def trading_calendar(self) -> TradingCalendar:
        """Get the trading calendar object.
        
        Returns:
            TradingCalendar: The trading calendar object."""
        ...
    def get_trading_day(self) -> str:
        """Get the current trading day.
        
        Returns:
            str: Current trading day in 'YYYY-mm-dd' format."""
        ...
    def add_trading_days(self, date: str, days: int) -> "pd.Timestamp":
        """Add a specified number of trading days to a given date.
        
        This function navigates through a pre-defined list of trading dates
        to find a date that is exactly 'days' trading days away from the input date.
        It handles edge cases for dates beyond the available range.
        
        Parameters:
        -----------
        date : str
            The starting date in string format
        days : int
            Number of trading days to add (positive) or subtract (negative)
        
        Returns:
        --------
        pd.Timestamp
            The resulting date after adding/subtracting the specified number of trading days"""
        ...
    def get_prev_trading_day(self, cur_trading_day: str) -> str:
        """Get the previous trading day.
        
        Args:
            cur_trading_day (str, optional): The current trading day in 'YYYY-mm-dd' format.
                                             If not provided, defaults to the current trading day.
        
        Returns:
            str: The previous trading day in 'YYYY-mm-dd' format."""
        ...
    def get_next_trading_day(self, cur_trading_day: str) -> str:
        """Get the next trading day.
        
        Args:
            cur_trading_day (str, optional): The current trading day in 'YYYY-mm-dd' format.
                                             If not provided, defaults to the current trading day.
        
        Returns:
            str: The next trading day in 'YYYY-mm-dd' format."""
        ...
    def have_night_trading(self, trading_day: str) -> bool:
        """Check if a given trading day has night trading sessions.
        
        Args:
            trading_day (str): The trading day to check in 'YYYY-mm-dd' format.
        
        Returns:
            bool: True if the trading day has night trading, False otherwise."""
        ...
    @property
    def portfolio(self) -> IPortfolio:
        """Get the strategy's portfolio object.
        
        Provides access to account balances, positions, and other portfolio-related information.
        
        Returns:
            IPortfolio: The strategy's portfolio object."""
        ...
    def add_account(self, acct_type: AccountType, account_id: str, capital_base: float = "", **kwargs: Any) -> None:
        """[Backtest] Initialize an additional backtest trading account.
        
        This method is used in backtesting to create and manage multiple trading accounts
        (e.g., for different asset types).
        
        Args:
            acct_type (AccountType): The type of account to add (e.g., AccountType.STOCK, AccountType.FUTURE, AccountType.OPTION).
            account_id (str, optional): A custom ID for the account. If not provided, a default ID will be generated. Defaults to "".
            capital_base (float, optional): The initial capital for the backtest account. Defaults to 1e06.
            **kwargs: Additional keyword arguments for account initialization."""
        ...
    def login_account(self, account_setting: dict) -> None:
        """[Live Trading] Attempt to log in to a trading account.
        
        This method is used in live trading to authenticate and connect to a brokerage account.IPositionData
        
        Args:
            account_setting (dict): A dictionary containing account login credentials and settings.
                                     The specific keys required depend on the brokerage."""
        ...
    def get_balance(self, account_id: str) -> float:
        """Get the total balance of a trading account.
        
        Args:
            account_id (str, optional): The ID of the account. If not specified, the default account is used. Defaults to "".
        
        Returns:
            float: The total balance of the account."""
        ...
    def get_available_cash(self, account_id: str) -> float:
        """Get the available cash balance of a trading account.
        
        This is the amount of cash available for placing new orders.
        
        Args:
            account_id (str, optional): The ID of the account. If not specified, the default account is used. Defaults to "".
        
        Returns:
            float: The available cash balance of the account."""
        ...
    def get_position(self, instrument: str, direction: Direction, create_if_none: bool = Direction.NONE, account_id: str = True) -> Union[IPositionData, None]:
        """Get the Position object for a specific instrument and direction in an account.
        
        Args:
            instrument (str): The instrument (e.g., '000001.SZ', 'rb2010.SHF').
            direction (Direction, optional): The direction of the position (Direction.LONG, Direction.SHORT, or Direction.NONE for net position). Defaults to Direction.NONE.
            create_if_none (bool, optional): If True, a new Position object will be created if one does not exist. Defaults to True.
            account_id (str, optional): The ID of the account. If not specified, the default account is used. Defaults to "".
        
        Returns:
            IPositionData: The Position object for the specified instrument and direction.
                      Returns None if no position exists and create_if_none is False."""
        ...
    def get_positions(self, instruments: Union[list[str], None], account_id: str = None) -> dict[str, IPositionData]:
        """Get all positions or positions for specific instruments in an account.
        
        Args:
            instruments (Union[List[str], None], optional): A list of instrument to retrieve positions for.
                                                       If None, all positions in the account are returned. Defaults to None.
            account_id (str, optional): The ID of the account. If not specified, the default account is used. Defaults to "".
        
        Returns:
            Dict[str, IPositionData]: A dictionary of Position objects, keyed by instrument."""
        ...
    def set_initial_positions(self, initial_positions: list, account_id: str) -> None:
        """[Backtest] Set initial positions for a backtest account in bulk.
        
        This method is used in backtesting to pre-populate an account with positions at the start of the backtest.
        
        Args:
            initial_positions (list): A list of initial position objects or dictionaries defining initial positions.
                                      The exact format depends on the Position object structure.
            account_id (str, optional): The ID of the account. If not specified, the default account is used. Defaults to ""."""
        ...
    def order(self, instrument: str, volume: int, limit_price: Union[float, None], offset_flag: Union[OffsetFlag, None] = None, order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place a new order.
        
        This is the most general order placement function, allowing for various order parameters.
        
        Args:
            instrument (str): The instrument (e.g., '000001.SZ', 'rb2010.SHF').
            volume (int): The order volume. Positive for buy, negative for sell.
            limit_price (Union[float, None], optional): The limit price for a limit order. If None, a market order is assumed if order_type is MARKET. Defaults to None.
            offset_flag (Union[OffsetFlag, None], optional): For futures, the position offset (OffsetFlag.OPEN, OffsetFlag.CLOSE, OffsetFlag.CLOSETODAY).
                                                    If None, the system will automatically determine open or close. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET).
                                                     If None, defaults to OrderType.LIMIT. Defaults to None.
            **kwargs: Optional keyword arguments, such as order_property, hedge_flag, etc., specific to the exchange or broker.
        
        Returns:
            int: 0 for success, otherwise an error code. Use `get_error_msg(error_id)` to get detailed error message."""
        ...
    def order_percent(self, instrument: str, percent: float, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place an order by percentage of available capital.
        
        Args:
            instrument (str): The instrument.
            percent (float): The percentage of available capital to use for the order (e.g., 0.1 for 10%).
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def order_value(self, instrument: str, value: float, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place an order by target value in currency.
        
        Args:
            instrument (str): The instrument.
            value (float): The target value of the order in account currency (e.g., 10000 for 10000 CNY).
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def order_target(self, instrument: str, target: float, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place an order to reach a target position volume.
        
        Calculates the volume needed to reach the specified target position and places an order accordingly.
        
        Args:
            instrument (str): The instrument.
            target (float): The target position volume.
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def order_target_percent(self, instrument: str, target: float, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place an order to reach a target position as a percentage of capital.
        
        Calculates the volume needed to reach the specified target percentage of capital and places an order accordingly.
        
        Args:
            instrument (str): The instrument.
            target (float): The target position as a percentage of capital (e.g., 0.1 for 10%).
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def order_target_value(self, instrument: str, target: float, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place an order to reach a target position value in currency.
        
        Calculates the volume needed to reach the specified target position value and places an order accordingly.
        
        Args:
            instrument (str): The instrument.
            target (float): The target position value in account currency (e.g., 10000 for 10000 CNY).
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def place_order(self, req: IOrderReq, **kwargs: Any) -> int:
        """Place an order using an IOrderReq object.
        
        This method allows for placing orders using a pre-constructed IOrderReq object,
        providing more control over order parameters.
        
        Args:
            req (IOrderReq): An IOrderReq object containing order details.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def buy_open(self, instrument: str, volume: int, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place a buy-open order.
        
        Specifically places a buy order to open a new position (or increase an existing long position).
        For futures and options, this explicitly sets the offset to OPEN.
        
        Args:
            instrument (str): The instrument.
            volume (int): The order volume (positive).
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def buy_close(self, instrument: str, volume: int, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place a buy-close order.
        
        Specifically places a buy order to close an existing short position.
        For futures and options, this explicitly sets the offset to CLOSE.
        
        Args:
            instrument (str): The instrument.
            volume (int): The order volume (positive).
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def sell_open(self, instrument: str, volume: int, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place a sell-open order.
        
        Specifically places a sell order to open a new position (or increase an existing short position).
        For futures and options, this explicitly sets the offset to OPEN.
        
        Args:
            instrument (str): The instrument.
            volume (int): The order volume (positive for sell, so use positive volume for selling).
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def sell_close(self, instrument: str, volume: int, limit_price: Union[float, None], order_type: Union[OrderType, None] = None, **kwargs: Any) -> int:
        """Place a sell-close order.
        
        Specifically places a sell order to close an existing long position.
        For futures and options, this explicitly sets the offset to CLOSE.
        
        Args:
            instrument (str): The instrument.
            volume (int): The order volume (positive for sell, so use positive volume for selling).
            limit_price (Union[float, None], optional): The limit price for a limit order. Defaults to None.
            order_type (Union[OrderType, None], optional): The order type (OrderType.LIMIT, OrderType.MARKET). Defaults to None.
            **kwargs: Optional keyword arguments.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def exercise(self, instrument: str, volume: int, **kwargs: Any) -> None:
        """Place an option exercise order.
        
        Args:
            instrument (str): The option contract instrument.
            volume (int): The volume of options to exercise.
            **kwargs: Optional keyword arguments."""
        ...
    def order_reverse_repo(self, value_or_percent: float, n: int, rate: Union[float, None] = 1, **kwargs: Any) -> None:
        """Place a reverse repurchase agreement (repo) order.
        
        Lends cash to earn interest.
        
        Args:
            value_or_percent (float): Amount to lend. If <= 1.0, interpreted as a percentage of available cash. Otherwise, interpreted as a monetary value.
            n (int, optional): Number of days for the repo. Defaults to 1.
            rate (Union[float, None], optional): Trading rate. Defaults to 1.1 (e.g., 1.1 for 10% annualized rate if n=1).
            **kwargs: Optional keyword arguments."""
        ...
    def cancel_order(self, order_param: Union[Union[str, IOrderData], IOrderReq]) -> int:
        """Cancel an existing order.
        
        Args:
            order_param (Union[str, IOrderData, IOrderReq]): Order identifier. Can be order_key (string), IOrderData object, or CancelOrderReq object.
        
        Returns:
            int: 0 for success, otherwise an error code."""
        ...
    def cancel_all(self, only_from_this: bool, account_id: str = False) -> None:
        """Cancel all open orders.
        
        Args:
            only_from_this (bool, optional): If True, only cancel orders placed by the current strategy instance. Defaults to False.
            account_id (str, optional): The ID of the account to cancel orders in. If not specified, the default account is used. Defaults to ""."""
        ...
    def get_open_orders(self, instrument: str, only_from_this: bool) -> list[Union[IOrderData, IOrderReq]]:
        """Get a list of open (unfilled or partially filled) orders for a instrument.
        
        Args:
            instrument (str): The instrument to query orders for.
            only_from_this (bool, optional): If True, only include orders placed by the current strategy instance. Defaults to False.
        
        Returns:
            List[Union[IOrderData, IOrderReq]]: A list of IOrderData or IOrderReq objects representing open orders."""
        ...
    def get_orders(self, instrument: str, only_from_this: bool) -> list[IOrderData]:
        """Get a list of all orders (open and filled) for a instrument.
        
        Args:
            instrument (str): The instrument to query orders for.
            only_from_this (bool, optional): If True, only include orders placed by the current strategy instance. Defaults to False.
        
        Returns:
            List[IOrderData]: A list of IOrderData objects representing all orders."""
        ...
    def get_order(self, order_param: str, account_id: str) -> Union[IOrderData, None]:
        """Get a specific order by its identifier.
        
        Args:
            order_param (str): Order identifier, can be order_key or bt_order_sysid.
            account_id (str, optional): The ID of the account the order belongs to. If not specified, the default account is used. Defaults to "".
        
        Returns:
            IOrderData: The IOrderData object for the specified order, or None if not found."""
        ...
    def get_trades(self, instrument: str, only_from_this: bool = "") -> list[ITradeData]:
        """Get a list of all trades (filled orders).
        
        Args:
            instrument (str, optional): The instrument to filter trades by. If empty, returns all trades. Defaults to "".
            only_from_this (bool, optional): If True, only include trades executed by the current strategy instance. Defaults to False.
        
        Returns:
            List[ITradeData]: A list of ITradeData objects representing executed trades."""
        ...
    def get_pending_order_reqs(self, account_id: str) -> list[IOrderReq]:
        """Get a list of today's pending order requests.
        
        Pending order requests are orders that have been submitted but not yet fully processed by the system.
        
        Args:
            account_id (str, optional): The ID of the account. If not specified, the default account is used. Defaults to "".
        
        Returns:
            List[IOrderReq]: A list of IOrderReq objects representing pending order requests."""
        ...
    def get_last_order_key(self) -> str:
        """Get the order_key of the most recently successfully placed order.
        
        Returns:
            str: The order_key of the last successful order, or None if no successful order has been placed yet."""
        ...
    def subscribe(self, instruments: Union[str, list[str]], subscribe_flags: SubscribeFlag) -> None:
        """Subscribe to market data for specified instruments.
        
        Args:
            instruments (Union[str, List[str]]): A single instrument or a list of instrument to subscribe to.
            subscribe_flags (SubscribeFlag, optional): Flags to specify the type of market data to subscribe to.
                                                     Defaults to SubscribeFlag.DEFAULT, which subscribes to data based on frequency settings.
                                                     Other flags include:
                                                        * SubscribeFlag.LEVEL1_SNAPSHOT (1): Level 1 snapshot data (handle_tick)
                                                        * SubscribeFlag.LEVEL2_SNAPSHOT (2): Level 2 snapshot data (handle_tick)
                                                        * SubscribeFlag.LEVEL2_TRADE (4): Level 2 trade data (handle_l2trade)
                                                        * SubscribeFlag.LEVEL2_ORDER (8): Level 2 order data (handle_l2order)
                                                     Combine flags using bitwise OR, e.g., `SubscribeFlag.LEVEL2_SNAPSHOT | SubscribeFlag.LEVEL2_TRADE` for Level 2 snapshot and trade data."""
        ...
    def unsubscribe(self, instruments: Union[str, list[str]], subscribe_flags: SubscribeFlag) -> None:
        """Unsubscribe from market data for specified instruments.
        
        Args:
            instruments (Union[str, List[str]]): A single instrument or a list of instrument to unsubscribe from.
            subscribe_flags (SubscribeFlag, optional): Flags to specify the type of market data to unsubscribe from.
                                                     Should match the flags used during subscription. Defaults to SubscribeFlag.DEFAULT."""
        ...
    def subscribe_bar(self, instruments: Union[list[str], str], period: str, callback: Union[Callable, None], history_window: Union[int, None] = None) -> None:
        """Subscribe to bar (OHLCV) market data for specified instruments and period.
        
        Args:
            instruments (Union[List[str], str]): A single instrument or a list of instrument to subscribe to.
            period (str): The bar period, e.g., '1m' for 1-minute bars, '5m' for 5-minute bars, '1d' for daily bars.
            callback (Union[Callable, None], optional): A callback function to be executed when new bar data is received.
                                                        The callback function should accept two arguments: `context` (the strategy context) and `bar` (the bar data).
                                                        Example: `handle_bar(context, bar)`. Defaults to None (using default handle_bar).
            history_window (Union[int, None], optional): The maximum history window size to maintain for historical bar data.
                                                         Useful for strategies that need to access historical data using methods like `data.history()`.
                                                         Defaults to None (no history window)."""
        ...
    def get_contract(self, instrument: str) -> IContractData:
        """Get contract details for a given instrument.
        
        Args:
            instrument (str): The instrument (e.g., '000001.SZ', 'rb2010.SHF').
        
        Returns:
            IContractData: A IContractData object containing contract information, or None if not found."""
        ...
    def get_all_contracts(self, product_code: str, **kwargs: Any) -> dict[str, IContractData]:
        """Get all available contract data, optionally filtered by product code.
        
        Args:
            product_code (str, optional): Filter contracts by product code (e.g., 'rb' for rebar futures). Defaults to "".
            **kwargs: Additional keyword arguments for filtering or options.
        
        Returns:
            Dict[str, IContractData]: A dictionary of IContractData objects, keyed by instrument."""
        ...
    def get_option_contracts(self, underlying: str) -> list[IContractData]:
        """Get all option contracts for a given underlying asset.
        
        Args:
            underlying (str): The underlying asset instrument (e.g., 'a2309.DCE' for future options, '000016.SH' for index options, '510050.SH' for ETF options).
        
        Returns:
            List[OptionContractData]: A list of OptionContractData objects."""
        ...
    def get_option_strike_prices(self, underlying: str, strike_year_month: int) -> list[float]:
        """Get all strike prices for options of a given underlying asset and expiration month.
        
        Args:
            underlying (str): The underlying asset instrument.
            strike_year_month (int): The expiration year and month in 'YYYYmm' format (e.g., 202009 for September 2020).
        
        Returns:
            List[float]: A list of strike prices for the specified options."""
        ...
    def get_atm_option_contract(self, underlying: str, strike_year_month: int, underlying_price: float, option_type: OptionCP, adjust_flag: str) -> IContractData:
        """Get the at-the-money (ATM) option contract for a given underlying asset, expiration month, and option type.
        
        Args:
            underlying (str): The underlying asset instrument.
            strike_year_month (int): The expiration year and month in 'YYYYmm' format.
            underlying_price (float): The current price of the underlying asset.
            option_type (OptionCP): The option type (OptionCP.CALL or OptionCP.PUT).
            adjust_flag (str, optional): Adjustment flag. Defaults to "A".  (Meaning might be specific to data provider)
        
        Returns:
            OptionContractData: The OptionContractData object for the ATM option contract, or None if not found."""
        ...
    def get_dominant(self, product_code: Union[str, list[str]]) -> Union[str, dict[str, str]]:
        """Get the dominant contract instrument for a given product code or list of product codes.
        
        Dominant contract usually refers to the most actively traded contract for a given product (e.g., the main futures contract).
        
        Args:
            product_code (Union[str, List[str]]): A single product code (e.g., 'rb' for rebar futures) or a list of product codes.
        
        Returns:
            Union[str, Dict[str, str]]: If a single product code is provided, returns the dominant contract instrument as a string.
                                       If a list of product codes is provided, returns a dictionary mapping product codes to their dominant contract instruments."""
        ...
    def current_tick(self, instrument: str) -> ITickData:
        """Get the latest tick market data for a given instrument.
        
        Args:
            instrument (str): The instrument.
        
        Returns:
            ITickData: A ITickData object containing the latest tick data, or None if no tick data is available."""
        ...
    def get_margin_rate(self, instrument: str, account_id: str) -> IMarginRateData:
        """Get the margin rate data for a given instrument and account.
        
        Args:
            instrument (str): The instrument.
            account_id (str, optional): The ID of the account. If not specified, the default account is used. Defaults to "".
        
        Returns:
            IMarginRateData: A IMarginRateData object containing margin rate information, or None if not available."""
        ...
    def get_commission(self, instrument: str, account_id: str) -> ICommissionRateData:
        """Get the commission rate data for a given instrument and account.
        
        Args:
            instrument (str): The instrument.
            account_id (str, optional): The ID of the account. If not specified, the default account is used. Defaults to "".
        
        Returns:
            ICommissionRateData: A ICommissionRateData object containing commission rate information, or None if not available."""
        ...
    def set_commission(self, equities_commission: Union[float, None], futures_commission: Union[float, None] = None, options_commission: Union[float, None] = None, account_id: str = None) -> None:
        """[Backtest] Set custom commission models for backtesting.
        
        Args:
            equities_commission (Union[float, None], optional): Commission rate for equities. Defaults to None (using default model).
            futures_commission (Union[float, None], optional): Commission rate for futures. Defaults to None (using default model).
            options_commission (Union[float, None], optional): Commission rate for options. Defaults to None (using default model).
            account_id (str, optional): The ID of the account to apply the commission settings to. If not specified, the default account is used. Defaults to ""."""
        ...
    def set_margin_rate(self, instrument: str, margin_ratio: float, account_id: str) -> None:
        """[Backtest] Set a custom margin ratio for a specific instrument in backtesting.
        
        Args:
            instrument (str): The instrument.
            margin_ratio (float): The margin ratio (e.g., 0.1 for 10% margin).
            account_id (str, optional): The ID of the account to apply the margin setting to. If not specified, the default account is used. Defaults to ""."""
        ...
    def set_slippage(self, tick_slippage: Union[ISlippageModel, None], bar_slippage: Union[ISlippageModel, None] = None, us_equities: Union[ISlippageModel, None] = None, account_id: str = None) -> None:
        """[Backtest] Set custom slippage models for backtesting.
        
        Args:
            tick_slippage (ISlippageModel, optional): Slippage model for tick data. Model type is implementation-dependent. Defaults to None (using default model).
            bar_slippage (ISlippageModel, optional): Slippage model for bar data. Model type is implementation-dependent. Defaults to None (using default model).
            us_equities (ISlippageModel, optional): Slippage model for US equities (deprecated/legacy parameter?). Defaults to None.
            account_id (str, optional): The ID of the account to apply the slippage settings to. If not specified, the default account is used. Defaults to ""."""
        ...
    def set_slippage_value(self, slippage_type: Union[str, None], slippage_value: float = None, volume_limit: Union[int, None] = 0, account_id: str = None) -> None:
        """[Backtest] Set a fixed slippage value for backtesting.
        
        Args:
            slippage_type (Union[str, None], optional): Type of slippage to apply (e.g., 'fixed_value', 'percentage'). Type string is implementation-dependent. Defaults to None.
            slippage_value (float, optional): The slippage value. Interpretation depends on `slippage_type`. Defaults to 0.
            volume_limit (Union[int, None], optional): Volume limit for applying the slippage value. Slippage might be different for volumes above this limit. Defaults to None.
            account_id (str, optional): The ID of the account to apply the slippage setting to. If not specified, the default account is used. Defaults to ""."""
        ...
    def set_slippage_by_name(self, slippage_name: str, account_id: str) -> None:
        """[Backtest] Set custom slippage model by name for backtesting.
        
        Args:
            slippage_name (str): The slippage name like 'fixed'
            account_id (str, optional): The ID of the account to apply the slippage setting to. If not specified, the default account is used. Defaults to ""."""
        ...
    def set_vmatch_at(self, val: Union[int, VMatchAt]) -> None:
        """[Backtest] Set the virtual matching (vmatch) time mode for tick-based backtesting.
        
        This setting controls when orders are matched against market data in tick-based backtests.
        
        Args:
            val (Union[int, VMatchAt]): The vmatch mode. Can be an integer or a VMatchAt enum value.
                                          Possible values might include:
                                            * VMatchAt.CURRENT_BAR (0): Match orders at the current tick/bar time.
                                            * VMatchAt.NEXT_BAR_OPEN (1): Match orders at the next bar's open price.
                                          Refer to documentation for all possible values."""
        ...
    def set_stock_t1(self, on: int) -> None:
        """[Backtest] Enable or disable T+1 settlement for stock trading in backtesting.
        
        T+1 settlement means that stock trades are settled one trading day after the trade date.
        
        Args:
            on (int): 1 to enable T+1 settlement, 0 to disable."""
        ...
    def set_dividend_reinvestment(self, on: int) -> None:
        """[Backtest] Enable or disable dividend reinvestment in backtesting.
        
        If enabled, dividends received from stock holdings are automatically reinvested to purchase more shares of the same stock.
        
        Args:
            on (int): 1 to enable dividend reinvestment, 0 to disable."""
        ...
    def record_log(self, level: str, content: str, account_id: str) -> None:
        """Record account log.
        
        Use this method to record your trading log, which will display on render chart.
        
        Args:
            level (str): The log level like DEBUG/INFO/WARN/ERROR.
            content (str): The log content.
            account_id (str, optional): The ID of the account to apply the slippage setting to. If not specified, the default account is used. Defaults to ""."""
        ...
    def get_error_msg(self, error_id: int) -> str:
        """Get the error message corresponding to a given error ID.
        
        Use this method to retrieve detailed error messages for error codes returned by order placement and other functions.
        
        Args:
            error_id (int): The error ID.
        
        Returns:
            str: The error message string, or None if the error ID is not recognized."""
        ...

from typing import Any

class PerOrder:
    """Calculates commission for stock orders in the China A-share market.
    
    This commission model is designed specifically for the China A-share market and
    takes into account common commission structures in that market. It includes
    components for both buying and selling, and a minimum commission amount.
    
    Attributes:
        buy_cost (float): Commission rate for buying orders, expressed as a decimal (e.g., 0.0003 for 0.03%).
        sell_cost (float): Commission rate for selling orders, expressed as a decimal (e.g., 0.0013 for 0.13%).
            This typically includes the stamp duty which is only charged on selling in China A-share market.
        min_cost (float): Minimum commission amount charged per order, in CNY.
        tax_ratio (float, optional):  Tax rate applied to transactions. If set to `None`, no additional tax is applied.
            Note that stamp duty is included in `sell_cost`, this `tax_ratio` is for other potential taxes if needed.
            Defaults to `None`.
    
    Example:
        To create a PerOrder commission model with standard China A-share commission rates:
    
        >>> context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5.0))"""
    pass

class PerContract:
    """Calculates commission for futures or other contract-based transactions based on a per-contract cost.
    
    This commission model is suitable for futures, options, and other instruments where
    commissions are typically charged per contract traded. It allows for different commission
    rates for different underlying symbols and supports separate rates for opening, closing, and
    closing today positions, which is common in futures markets.
    
    The commission cost can be defined either as a fixed amount per contract or as a percentage
    of the contract value (though in the current implementation, it's configured as a percentage-like rate).
    
    Parameters:
        cost (dict[str, tuple[float, float, float]]): A dictionary mapping root symbols (e.g., 'IF', 'AU') to commission costs.
            The value for each root symbol is a tuple of three floats representing the commission rate for:
            - Opening a position
            - Closing a position (normal close)
            - Closing a position opened and closed on the same day (close today).
    
            The commission rate should be a decimal representing the percentage of transaction value,
            e.g., `0.000023` for 0.0023%.
    
    Example:
                `cost={'IF': (0.000023, 0.000115, 0.000023), 'AU': (0.0001, 0.0002, 0.0001)}`
                This means for 'IF' contracts:
                    - Opening commission rate is 0.0023%
                    - Closing commission rate is 0.0115%
                    - Close today commission rate is 0.0023%
                And for 'AU' contracts:
                    - Opening and close_today rate is 0.01%
                    - Closing rate is 0.02%
    
    Raises:
        Exception: If `cost` is not a dictionary or if the values in the dictionary are not tuples of length 3.
    
    Note:
        - This commission model is designed to be used with BigTrader's backtesting and trading engine.
        - The root symbol is typically the first part of the instrument ID (e.g., 'IF' from 'IF2312.CCFX').
        - BigTrader's context object (`context`) is usually used to set the commission model in a strategy.
          For example: `context.set_commission(futures_commission=PerContract(cost={'IF':(0.000023, 0.000115, 0.000023)}))`"""
    @property
    def cost_per_contract(self) -> dict[str, tuple[float, float, float]]:
        """Returns the dictionary of per-contract commission costs.
        
        This property allows access to the configured commission costs for each root symbol.
        
        Returns:
            dict[str, tuple[float, float, float]]: A dictionary where keys are root symbols and values
                are tuples of commission rates (open, close, close_today)."""
        ...

from typing import Any, Literal

class Performance:
    """Performance class for storing and rendering backtest or trading performance results."""
    raw_perf: "pd.DataFrame"
    account_raw_performances: list[dict]
    market: Market
    frequency: Frequency

    def render(self, render_type: Literal["chart", "table"], round_num: Any = "chart", table_max_rows: Any = 3) -> None:
        """Renders the performance results, either as a chart or a table.
        
        Args:
            render_type (Literal["chart", "table"], optional): Type of rendering ('chart' or 'table'). Defaults to "chart".
            round_num (int, optional): Number of decimal places for rounding. Defaults to 3.
            table_max_rows (int, optional): Maximum rows to display in table. Defaults to 1000."""
        ...

import enum
from typing import Any

def get_run_mode() -> RunMode:
    """Get the current running mode of the application.
    
    Returns:
        RunMode: The current running mode, determined from environment
                 variable 'RUN_MODE'. Defaults to RunMode.BACKTEST if
                 not specified."""
    ...

def in_backtest_mode(mode: RunMode = None) -> bool:
    """Check if the application is running in backtest mode.
    
    Args:
        mode (RunMode, optional): The mode to check. If None, the current
                                  running mode will be used. Defaults to None.
    
    Returns:
        bool: True if in backtest mode, False otherwise."""
    ...

def in_paper_trading_mode(mode: RunMode = None) -> bool:
    """Check if the application is running in paper trading mode.
    
    Args:
        mode (RunMode, optional): The mode to check. If None, the current
                                  running mode will be used. Defaults to None.
    
    Returns:
        bool: True if in paper trading mode, False otherwise."""
    ...

def in_live_trading_mode(mode: RunMode = None) -> bool:
    """Check if the application is running in live trading mode.
    
    Args:
        mode (RunMode, optional): The mode to check. If None, the current
                                  running mode will be used. Defaults to None.
    
    Returns:
        bool: True if in live trading mode, False otherwise."""
    ...

def trading_date(backtest_date: str = None) -> str:
    """Get the current trading date.
    
    In backtest mode, returns the provided backtest_date.
    In paper trading or live trading mode, returns the current trading date
    from the environment variable 'TRADING_DATE'.
    
    Args:
        backtest_date (str, optional): The date to use in backtest mode.
                                       Defaults to None.
    
    Returns:
        str: The current trading date.
    
    Example:
        trading_date("2024-04-03")"""
    ...

class RunMode(Enum):
    """Execution mode of the trading platform."""
    BACKTEST="backtest"
    """Backtesting mode: simulate trading using historical data."""
    PAPER_TRADING="papertrading"
    """Paper trading mode: simulate live trading without real money."""
    LIVE_TRADING="live_trading"
    """Live trading mode: execute trades in the real market with real money."""

from typing import Any, Callable, List, Literal, Optional, Union

@Runner.hook
def run(*, market: Market = Market.CN_STOCK, frequency: Frequency = Frequency.DAILY, instruments: Union[list[str], None] = None, start_date: str = "", end_date: str = "", data: Optional["pd.DataFrame"] = None, capital_base: float = 1000000.0, initialize: Union[Callable[["IContext"], None], None] = None, before_trading_start: Union[Callable[["IContext", "IBarData"], None], None] = None, handle_data: Union[Callable[["IContext", "IBarData"], None], None] = None, handle_trade: Union[Callable[["IContext", "ITradeData"], None], None] = None, handle_order: Union[Callable[["IContext", "IOrderData"], None], None] = None, handle_tick: Union[Callable[["IContext", "ITickData"], None], None] = None, handle_l2order: Union[Callable[["IContext", "IL2TradeData"], None], None] = None, handle_l2trade: Union[Callable[["IContext", "IL2OrderData"], None], None] = None, after_trading: Union[Callable[["IContext", "IBarData"], None], None] = None, benchmark: Literal["000300.SH", "000905.SH", "000852.SH", "000903.SH", "000001.SH", "000016.SH", "000688.SH", "399001.SZ", "399006.SZ", "399330.SZ", "899050.BJ"] = "000300.SH", options_data: Union[Any, None] = None, before_start_days: int = 0, volume_limit: float = 1, order_price_field_buy: Literal[ "open", "close", "twap_1", "twap_2", "twap_3", "twap_4", "twap_5", "twap_6", "twap_7", "twap_8", "twap_9", "twap_10", "twap_11", "vwap_1", "vwap_2", "vwap_3", "vwap_4", "vwap_5", "vwap_6", "vwap_7", "vwap_8", "vwap_9", "vwap_10", "vwap_11"] = "open", order_price_field_sell: Literal[ "open", "close", "twap_1", "twap_2", "twap_3", "twap_4", "twap_5", "twap_6", "twap_7", "twap_8", "twap_9", "twap_10", "twap_11", "vwap_1", "vwap_2", "vwap_3", "vwap_4", "vwap_5", "vwap_6", "vwap_7", "vwap_8", "vwap_9", "vwap_10", "vwap_11"] = "open", user_data: Union[Union[UserDataFeed, dict], None] = None, engine: Union[Literal["py", "cpp", "vt"], None] = None, logger: structlog.BoundLogger = None, backtest_only: bool = False, _runner: Union[Runner, None] = None) -> Performance:
    """Executes a backtest or trading session with the bigtrader engine.
    
    This is the main function to initiate a backtest, paper trading, or live trading session on the BigQuant platform.
    It orchestrates the entire process from data loading to engine execution and performance evaluation.
    
    Args:
        market (Market): The market to trade in. Defaults to `Market.CN_STOCK`.
        frequency (Frequency): The frequency of data bars (e.g., daily, minute). Defaults to `Frequency.DAILY`.
        instruments (Optional[List[str]]): List of instruments to trade. If None, uses all instruments in the data. Defaults to None.
        start_date (str): Start date for backtest/trading in "YYYY-MM-DD" format. Defaults to "".
        end_date (str): End date for backtest/trading in "YYYY-MM-DD" format. Defaults to "".
        data (Optional[pd.DataFrame]): User-provided data for signals/factors. Defaults to None.
        capital_base (float): Initial capital for the account. Defaults to 1.0e6.
        initialize (Optional[Callable[[IContext], None]]): User-defined initialization function. Defaults to None.
        initialize (Optional[Callable[[IContext], None]]): User-defined initialization function. The initialization function is executed once each time the program starts. In backtest mode: executed once at the start of the backtest; in daily simulation trading: executed once at the start of each day's simulation trading; in live trading mode: executed once at startup. It is recommended to perform factor/signal calculations here, such as using `dai.query` / pandas DataFrame, etc., for batch loading and vectorized computations, which is generally 10-100 times faster than handling data in `handle_data`. For example, `context.data = dai.query("SELECT date, instrument, close / m_lag(close, 1) AS return_0 FROM cn_stock_bar1d ORDER BY date, return_0 DESC", filters={"date": [pd.to_datetime(context.start_date) + pd.Timedelta(days=10), context.end_date]}).df()`. Defaults to None.
        before_trading_start (Optional[Callable[[IContext, IBarData], None]]): Function called before each trading day starts. Defaults to None.
        handle_data (Optional[Callable[[IContext, IBarData], None]]): Main function called for each data bar, where trading logic is implemented. Defaults to None.
        handle_trade (Optional[Callable[[IContext, ITradeData], None]]): Function called when a trade is executed. Defaults to None.
        handle_order (Optional[Callable[[IContext, IOrderData], None]]): Function called when an order status updates. Defaults to None.
        handle_tick (Optional[Callable[[IContext, ITickData], None]]): Function called for each tick data update. Defaults to None.
        handle_l2order (Optional[Callable[[IContext, IL2TradeData], None]]): Function called for each Level-2 order book update. Defaults to None.
        handle_l2trade (Optional[Callable[[IContext, IL2OrderData], None]]): Function called for each Level-2 trade update. Defaults to None.
        after_trading (Optional[Callable[[IContext, IBarData], None]]): Function called after each trading day ends. Defaults to None.
        benchmark (Literal): Benchmark index for performance evaluation. Defaults to "000300.SH".
        options_data (Optional[Any]): Placeholder for options data. Defaults to None.
        before_start_days (int): Days to pre-load historical data before start_date. Defaults to 0.
        volume_limit (float): Volume limit factor for orders. Defaults to 1.
        order_price_field_buy (Literal[ "open", "close", "twap_1", "twap_2", "twap_3", "twap_4", "twap_5", "twap_6", "twap_7", "twap_8", "twap_9", "twap_10", "twap_11", "vwap_1", "vwap_2", "vwap_3", "vwap_4", "vwap_5", "vwap_6", "vwap_7", "vwap_8", "vwap_9", "vwap_10", "vwap_11"]): Price field to use for buy orders. Defaults to "open".
        order_price_field_sell (Literal[ "open", "close", "twap_1", "twap_2", "twap_3", "twap_4", "twap_5", "twap_6", "twap_7", "twap_8", "twap_9", "twap_10", "twap_11", "vwap_1", "vwap_2", "vwap_3", "vwap_4", "vwap_5", "vwap_6", "vwap_7", "vwap_8", "vwap_9", "vwap_10", "vwap_11"]): Price field to use for sell orders. Defaults to "close".
        user_data (Optional[Union[UserDataFeed, dict]]): User-defined data feed. Defaults to None.
        engine (Optional[Literal]): Execution engine to use ("py", "cpp", "vt"). Defaults to None (auto-select).
        logger (Optional[structlog.BoundLogger]): Logger instance for logging. Defaults to None (default logger).
        backtest_only (bool): Flag for backtesting only mode. Defaults to False.
    
    Returns:
        Performance: A `Performance` object containing the results of the backtest or trading session, including
            raw performance data, account performances, market and frequency information, and logger."""
    ...

from typing import Any, Union

class RebalancePeriod:
    """A class representing the rebalancing periods for a trading strategy."""
    def select_rebalance_data(self, data: pd.DataFrame, date_col: Any) -> pd.DataFrame: ...
    def build(self, start_date: Union[str, pd.Timestamp], end_date: Union[Union[str, pd.Timestamp], None], extra_days: int = None, _trading_dates: Any = 500) -> None:
        """Build rebalance period
        
        Parameters:
            start_date (Union[str, pd.Timestamp]): The start date of the period for rebalancing.
            end_date (Union[str, pd.Timestamp]): The end date of the period for rebalancing.
            extra_days (int): The number of days to extend before start_date and after end_date for trading days querying."""
        ...
    def is_signal_date(self, date: Union[Union[Union[str, pd.Timestamp], datetime.date], pd.Series]) -> Union[bool, pd.Series]:
        """是否信号日(调仓日前一天生成信号)"""
        ...
    def is_trival(self) -> int:
        """是否平凡的，如果是，表示可以忽略，比如 交易日每天调仓的情况"""
        ...

class NaturalDaysRebalance(RebalancePeriod):
    """自然日调仓类。根据指定的起始日期、结束日期和天数间隔计算调仓日期。"""
    pass

class WeeklyRebalance(RebalancePeriod):
    """周期调仓类。根据指定的起始日期、结束日期和星期几计算调仓日期。"""
    pass

class MonthlyRebalance(RebalancePeriod):
    """月度自然日调仓类。根据指定的起始日期、结束日期和每月的某一天计算调仓日期。"""
    pass

class QuarterlyRebalance(RebalancePeriod):
    """季度自然日调仓类。根据指定的起始日期、结束日期和季度的某一天计算调仓日期。"""
    pass

class YearlyRebalance(RebalancePeriod):
    """年度自然日调仓类。根据指定的起始日期、结束日期和年度的某一天计算调仓日期。"""
    pass

class TradingDaysRebalance(RebalancePeriod):
    """交易日调仓类。根据指定的起始日期、结束日期和交易日天数间隔计算调仓日期。"""
    def is_trival(self) -> Any:
        """如果交易日每天调仓，则是平凡的"""
        ...

class WeeklyTradingDaysRebalance(RebalancePeriod):
    """交易日周期调仓类。根据指定的起始日期、结束日期和周内的交易日计算调仓日期。"""
    pass

class MonthlyTradingDaysRebalance(RebalancePeriod):
    """交易日月度调仓类。根据指定的起始日期、结束日期和月内的交易日计算调仓日期。"""
    pass

class QuarterlyTradingDaysRebalance(RebalancePeriod):
    """交易日季度调仓类。根据指定的起始日期、结束日期和季内的交易日计算调仓日期。"""
    pass

class YearlyTradingDaysRebalance(RebalancePeriod):
    """交易日年度调仓类。根据指定的起始日期、结束日期和年内的交易日计算调仓日期。"""
    pass


class HandleDataLib:
    """常用的 handle_data 函数库，提供可配置的交易场景实现"""

    @staticmethod
    def handle_data_weight_based(
        context: "IContext",
        data: "IBarData",
        show_progress: str = None,
    ) -> None:
        """Rebalance portfolio based on weights defined in context.data(date, instrument, [weight]).

        Usage:
            In initialize function:
                1. Calculate data or factors to weights, save to context.data
                2. [Optional] Rebalance period: context.data = bigtrader.TradingDaysRebalance(5, context=context).select_rebalance_data(context.data)
                3. [Optional] Market timing/position weight: Calculate overall position weight based on market conditions, multiply to individual stock weights

            Rebalancing logic:
                Rebalance according to weight column in context.data. Skip non-rebalancing days.

        Parameters
        ----------
        context : IContext
            The strategy context object that contains data and portfolio information
        data : IBarData
            Current bar data containing market information
        show_progress: str, optional
            Show progress: e.g. "%Y-%m"

        Returns:
        -------
        None

        Notes:
        -----
        - If context.data is not defined, the function returns without any action
        - If context.rebalance_period is defined, only rebalances on signal dates
        - 'weight' column is preferred over 'position' column for portfolio allocation
        - If neither weight nor position is specified, equal weight allocation is used

        Source code
        -----
        [bigquant github](https://github.com/BigQuant/bigquant)
        """
        if show_progress is not None:
            if not hasattr(context, "last_progress"):
                context.last_progress = None
            current_progress = data.current_dt.strftime(show_progress)
            if context.last_progress != current_progress:
                context.logger.info(f"Processing {current_progress}...")
                context.last_progress = current_progress

        if not hasattr(context, "data") or context.data is None:
            return
        # 检查是否为调仓日
        if (
            hasattr(context, "rebalance_period")
            and context.rebalance_period is not None
            and isinstance(context.rebalance_period, RebalancePeriod)
            and not context.rebalance_period.is_signal_date()
        ):
            return

        df_today = context.data[context.data["date"] == data.current_dt.strftime("%Y-%m-%d")]
        if len(df_today) == 1 and df_today["instrument"].iloc[0] is None:
            # 非调仓日
            return

        # 卖出不再持有的股票
        for instrument in set(context.get_positions()) - set(df_today["instrument"]):
            context.order_target_percent(instrument, 0)

        # 买入或调整目标持仓
        for _, row in df_today.iterrows():
            instrument = row["instrument"]
            if "weight" in row:
                weight = float(row["weight"])
            elif "position" in row:
                # @deprecated, use 'weight' instead
                weight = float(row["position"])
            else:
                # if weight is not set, use equal weight
                weight = 1 / len(df_today)
            context.order_target_percent(instrument, weight)

    @staticmethod
    def handle_data_signal_based(  # noqa: C901
        context: "IContext",
        data: "IBarData",
        max_hold_days: int = None,
        take_profit: float = None,
        stop_loss: float = None,
        max_open_weights_per_day: float = None,
        show_progress: str = None,
    ) -> None:
        """Rebalance portfolio based on signals in context.data.

        Assumes context.data contains columns: date, instrument, signal, weight
        where signal indicates buy(1), hold(0), or sell(-1) signals.

        Usage:
            In initialize function:
                1. Calculate trading signals, save to context.data

            Rebalancing logic:
                1. Sell stocks with signal = -1
                2. Buy stocks with signal = 1 (if not already held)
                3. Keep current positions for stocks with signal = 0

        Parameters
        ----------
        context : IContext
            The strategy context object that contains data and portfolio information
        data : IBarData
            Current bar data containing market information
        max_hold_days : int, optional
            Maximum number of days to hold a position before selling
        take_profit : float, optional
            Percentage gain at which to take profits (e.g., 0.1 for 10%)
        stop_loss : float, optional
            Percentage loss at which to cut losses (e.g., 0.05 for 5%)
        show_progress: str, optional
            Show progress: e.g. "%Y-%m"

        Returns:
        -------
        None

        Raises:
        ------
        Exception
            If the "signal" column is not found in context.data

        Notes:
        -----
        - If context.data is not defined, the function returns without any action
        - If context.rebalance_period is defined, only rebalances on signal dates
        - Position management includes max holding period, profit taking, and stop loss

        Source code
        -----
        [bigquant github](https://github.com/BigQuant/bigquant)
        """
        if show_progress is not None:
            if not hasattr(context, "last_progress"):
                context.last_progress = None
            current_progress = data.current_dt.strftime(show_progress)
            if context.last_progress != current_progress:
                context.logger.info(f"Processing {current_progress}...")
                context.last_progress = current_progress

        if not hasattr(context, "data") or context.data is None:
            return
        # 检查是否为调仓日
        if hasattr(context, "rebalance_period") and context.rebalance_period is not None and not context.rebalance_period.is_signal_date():
            return

        df_today = context.data[context.data["date"] == data.current_dt.strftime("%Y-%m-%d")]

        if "signal" not in df_today.columns:
            raise Exception("not found signal column in context.data")
        if "weight" not in df_today.columns:
            raise Exception("not found weight column in context.data")

        if len(df_today) == 0 or (len(df_today) == 1 and df_today["instrument"].iloc[0] is None):
            return

        # 处理持仓到期/止盈/止损
        if max_hold_days is not None:
            for _, position in context.get_positions().items():
                # 检查是否到期
                if position.hold_days >= max_hold_days:
                    context.record_log("INFO", f"{position.instrument} has been held for {position.hold_days} days, executing position close")
                    context.order_target_percent(position.instrument, 0)
        if take_profit is not None:
            for _, position in context.get_positions().items():
                # 检查是否止盈
                profit_ratio = position.last_price / position.cost_price - 1
                if profit_ratio >= take_profit:
                    context.record_log("INFO", f"{position.instrument} profit {profit_ratio:.2%}, triggering take profit")
                    context.order_target_percent(position.instrument, 0)
        if stop_loss is not None:
            for _, position in context.get_positions().items():
                # 检查是否止损
                loss_ratio = position.last_price / position.cost_price - 1
                if loss_ratio <= -stop_loss:
                    context.record_log("INFO", f"{position.instrument} loss {-loss_ratio:.2%}, triggering stop loss")
                    context.order_target_percent(position.instrument, 0)

        # 处理平仓信号
        sell_instruments = df_today[df_today["signal"] == -1]["instrument"].tolist()
        for instrument in sell_instruments:
            if instrument in context.get_positions():
                context.order_target_percent(instrument, 0)

        # 处理开仓信号 (weight 为正表示开多，为负表示开空)
        buy_df = df_today[df_today["signal"] == 1]
        open_weights = 0.0
        for _, row in buy_df.iterrows():
            weight = float(row["weight"])
            context.order_target_percent(row["instrument"], weight)
            if max_open_weights_per_day is not None:
                open_weights += abs(weight)
                if open_weights >= max_open_weights_per_day:
                    break

# <bigtrader-examples>

# <example title="简单的股票买入持有策略">
from bigquant import bigtrader


def initialize(context: bigtrader.IContext):
    context.set_commission(bigtrader.PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))


def handle_data(context: bigtrader.IContext, data: bigtrader.IBarData):
    if context.trading_day_index == 0:
        context.order_target_percent("000001.SZ", 1)


performance = bigtrader.run(
    market=bigtrader.Market.CN_STOCK,
    frequency=bigtrader.Frequency.DAILY,
    instruments=["000001.SZ"],
    start_date="2025-01-01",
    end_date="2025-03-07",
    capital_base=1000000,
    initialize=initialize,
    handle_data=handle_data,
)

performance.render()
# </example>


# <example title="根据机器学习预测分数来交易">
def initialize(context: bigtrader.IContext):
    import numpy as np

    # context.data = dai.DataSource("some").read_bdb()
    # 根据机器学习预测的 score 来调仓(输入数据已经按 score 有序)：持有前10只，权重 1.0 / log2(排序位置 + 4)
    context.data = context.data.groupby("date", group_keys=False).head(10).reset_index(drop=True)
    context.data["weight"] = (
        context.data.groupby("date")["score"]
        .rank(method="first", ascending=False)
        .pipe(lambda x: 1 / np.log2(x + 4))
        .groupby(context.data["date"])
        .transform(lambda x: x / x.sum())
    )

    # 调仓周期：5个交易日
    context.data = bigtrader.TradingDaysRebalance(5, context=context).select_rebalance_data(context.data)


def handle_data(context: bigtrader.IContext, data: bigtrader.IBarData):
    # bigtrader内置函数: 根据 context.data["signal"] 触发信号，持有 context.data["weight"] 仓位
    return bigtrader.HandleDataLib.handle_data_weight_based(context, data, show_progress="%Y-%m")


# </example>

# </bigtrader-examples>

