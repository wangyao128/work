import pandas as pd

from bigmodule import M

# <aistudiograph>

# @param(id="m4", name="initialize")
# 交易引擎：初始化函数，只执行一次
def m4_initialize_bigquant_run(context):    
    import math

    from bigtrader.finance.commission import PerOrder
    import numpy as np
    # 系统已经设置了默认的交易手续费和滑点，要修改手续费可使用如下函数
    context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    # 设置买入的股票数量，这里买入预测股票列表排名靠前的5只
    stock_count = 5
    # 每只的股票的权重，如下的权重分配会使得靠前的股票分配多一点的资金，[0.339160, 0.213986, 0.169580, ..]
    context.stock_weights = np.array([1/np.log(i+2) for i in range(stock_count)])
    context.stock_weights = context.stock_weights / np.sum(context.stock_weights)
    # 设置每只股票占用的最大资金比例
    context.max_cash_per_instrument = 0.2
    context.options['hold_days'] = 5


# @param(id="m4", name="before_trading_start")
# 交易引擎：每个单位时间开盘前调用一次。
def m4_before_trading_start_bigquant_run(context, data):
    # 盘前处理，订阅行情等
    pass


# @param(id="m4", name="handle_tick")
# 交易引擎：tick数据处理函数，每个tick执行一次
def m4_handle_tick_bigquant_run(context, tick):
    pass

# @param(id="m4", name="handle_data")
def m4_handle_data_bigquant_run(context, data):
    # 按日期过滤得到今日的预测数据
    ranker_prediction = context.data[context.data.date == data.current_dt.strftime('%Y-%m-%d')]
    # 按照position排序
    ranker_prediction.sort_values(["date", "position"], inplace=True)
    ranker_prediction.reset_index(drop=True, inplace=True)

    # 1. 资金分配
    # 平均持仓时间是hold_days，每日都将买入股票，每日预期使用 1/hold_days 的资金
    # 实际操作中，会存在一定的买入误差，所以在前hold_days天，等量使用资金；之后，尽量使用剩余资金（这里设置最多用等量的1.5倍）
    is_staging = context.trading_day_index < context.options['hold_days'] # 是否在建仓期间（前 hold_days 天）
    cash_avg = context.portfolio.portfolio_value / context.options['hold_days']
    cash_for_buy = min(context.portfolio.cash, (1 if is_staging else 1.5) * cash_avg)
    cash_for_sell = cash_avg - (context.portfolio.cash - cash_for_buy)
    positions = {e: p.amount * p.last_sale_price
                for e, p in context.portfolio.positions.items()}

    # 2. 生成卖出订单：hold_days天之后才开始卖出；对持仓的股票，按机器学习算法预测的排序末位淘汰
    if not is_staging and cash_for_sell > 0:
        equities = {e: e for e, p in context.portfolio.positions.items()}
        instruments = list(reversed(list(ranker_prediction.instrument[ranker_prediction.instrument.apply(
                lambda x: x in equities)])))
        for instrument in instruments:
            context.order_target(instrument, 0)
            cash_for_sell -= positions[instrument]
            if cash_for_sell <= 0:
                break

    # 3. 生成买入订单：按机器学习算法预测的排序，买入前面的stock_count只股票
    buy_cash_weights = context.stock_weights
    buy_instruments = list(ranker_prediction.instrument[:len(buy_cash_weights)])
    max_cash_per_instrument = context.portfolio.portfolio_value * context.max_cash_per_instrument
    for i, instrument in enumerate(buy_instruments):
        cash = cash_for_buy * buy_cash_weights[i]
        if cash > max_cash_per_instrument - positions.get(instrument, 0):
            # 确保股票持仓量不会超过每次股票最大的占用资金量
            cash = max_cash_per_instrument - positions.get(instrument, 0)
        if cash > 0:
            context.order_value(instrument, cash)

# @param(id="m4", name="handle_trade")
# 交易引擎：成交回报处理函数，每个成交发生时执行一次
def m4_handle_trade_bigquant_run(context, trade):
    pass

# @param(id="m4", name="handle_order")
# 交易引擎：委托回报处理函数，每个委托变化时执行一次
def m4_handle_order_bigquant_run(context, order):
    pass

# @param(id="m4", name="after_trading")
# 交易引擎：盘后处理函数，每日盘后执行一次
def m4_after_trading_bigquant_run(context, data):
    pass

# @module(position="-386,-139", comment='通过SQL调用数据、因子和表达式等构建策略逻辑', comment_collapsed=False)
m1 = M.input_features_dai.v6(
    sql="""SELECT * FROM data_b1e5e42cfad011ee91919abbc8449809
ORDER BY date, position"""
)

# @module(position="-341,-3", comment='抽取数据，设置数据开始时间和结束时间，并绑定模拟交易', comment_collapsed=False)
m2 = M.extract_data_dai.v7(
    sql=m1.data,
    start_date='2021-12-06',
    start_date_bound_to_trading_date=True,
    end_date='2024-04-10',
    end_date_bound_to_trading_date=True,
    before_start_days=90,
    debug=False
)

# @module(position="-254,139", comment='交易，日线，设置初始化函数和K线处理函数，以及初始资金、基准等', comment_collapsed=False)
m4 = M.bigtrader.v14(
    data=m2.data,
    start_date='',
    end_date='',
    initialize=m4_initialize_bigquant_run,
    before_trading_start=m4_before_trading_start_bigquant_run,
    handle_tick=m4_handle_tick_bigquant_run,
    handle_data=m4_handle_data_bigquant_run,
    handle_trade=m4_handle_trade_bigquant_run,
    handle_order=m4_handle_order_bigquant_run,
    after_trading=m4_after_trading_bigquant_run,
    capital_base=1000000,
    frequency='daily',
    product_type='股票',
    before_start_days=0,
    volume_limit=1,
    order_price_field_buy='open',
    order_price_field_sell='close',
    benchmark='000300.SH',
    plot_charts=True,
    disable_cache=False,
    debug=False,
    backtest_only=False,
    m_cached=False
)
# </aistudiograph>
