from bigmodule import M

# <aistudiograph>

# ======================
# 1. 因子与数据准备
# ======================

# @module(comment="日线因子计算：60日均线、10日均线")
m1 = M.input_features_dai.v30(
    mode="表达式",
    expr="m_avg(close, 60) AS ma60\nm_avg(close, 10) AS ma10",
    expr_filters="list_days > 60 AND st_status = 0",
    expr_tables="cn_stock_prefactors",
    extra_fields="date,instrument,close",
    order_by="date,instrument",
    expr_drop_na=True,
    extract_data=False,
    m_name="m1"
)

# @module(comment="抽取日线因子数据")
m2 = M.extract_data_dai.v20(
    sql=m1.data,
    start_date="2018-01-01",
    start_date_bound_to_trading_date=True,
    end_date="2025-12-31",
    end_date_bound_to_trading_date=True,
    before_start_days=120,
    keep_before=False,
    debug=False,
    m_name="m2"
)

# ======================
# 2. 回测逻辑（BigTrader）
# ======================

# @param(id="m3", name="initialize")
def m3_initialize_bigquant_run(context):
    import pandas as pd
    from bigtrader.finance.commission import PerOrder

    # 手续费设置（可自行调整）
    context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))

    # 读取日线因子数据到内存
    context.daily_factors = context.data.read()  # DataFrame: date, instrument, close, ma60, ma10
    context.daily_factors['date'] = pd.to_datetime(context.daily_factors['date']).dt.date

    # 读取外部自选股 CSV：假设文件名为 watchlist.csv，且含有 instrument 列
    try:
        watch_df = pd.read_csv(/home/aiuser/work/我的文档/量化交易/股票池/自选股.csv', encoding='utf-8')
        if 'instrument' not in watch_df.columns:
            raise ValueError("watchlist.csv 中必须包含 instrument 列")
        context.watchlist_all = set(watch_df['instrument'].astype(str).tolist())
    except Exception as e:
        # 若读取失败，则不设限制（等同于无自选股筛选），但这里更安全的做法是置为空集
        context.watchlist_all = set()
        print("读取 watchlist.csv 失败，将不交易。错误：", e)

    # 每日监控股票池（昨日在60日均线下的股票）
    context.monitor_pool = set()

    # 持仓状态：记录买入日期和是否已加仓
    # 格式: { instrument: {'buy_date': date, 'added': bool} }
    context.stock_state = {}

    # 当日已买入过的股票（防止当日重复买入）
    context.today_bought = set()

    # 用于找到前一交易日：从日线数据中获取所有交易日列表
    context.all_trading_dates = sorted(context.daily_factors['date'].unique().tolist())

    # 设置分钟级回测的时间周期（9:30~收盘）
    # frequency 已在模块参数中设置为 minute，这里只需在 handle_data 中控制逻辑执行的时间点
    print("初始化完成，可交易标的数量（日线因子）：", len(context.daily_factors['instrument'].unique()))


# 辅助函数：获取最近一个小于给定日期的交易日
def get_prev_trading_date(dates_list, current_date):
    import bisect
    # dates_list 已排序
    pos = bisect.bisect_left(dates_list, current_date)
    if pos == 0:
        return None
    return dates_list[pos - 1]


# @param(id="m3", name="handle_data")
def m3_handle_data_bigquant_run(context, data):
    import pandas as pd
    from datetime import time

    if len(context.watchlist_all) == 0:
        # 没有自选股列表，直接不交易
        return

    current_dt = data.current_dt
    current_date = current_dt.date()
    current_time = current_dt.time()

    # 每天第一次触发时重置当日状态
    # BigTrader 不提供 on_new_day 回调，这里用日期变化判断
    if not hasattr(context, 'last_date') or context.last_date != current_date:
        context.last_date = current_date
        context.today_bought = set()
        context.monitor_pool = set()

        # 9:15 前后构建当日监控股票池
        # 为防止分钟级时间略有偏差，只要在 9:15~9:25 之间，并且当天还没建池，就执行一次
        # 这里简化：只要是新的一天就建池（因为回测中不会真的在 9:00 前执行）
        prev_date = get_prev_trading_date(context.all_trading_dates, current_date)
        if prev_date is None:
            return

        df_yest = context.daily_factors[context.daily_factors['date'] == prev_date]
        if df_yest.empty:
            return

        # 只考虑自选股中的标的
        df_yest = df_yest[df_yest['instrument'].isin(context.watchlist_all)]

        # 昨日收盘价在 60 日均线下方：close < ma60
        pool_df = df_yest[df_yest['close'] < df_yest['ma60']]
        context.monitor_pool = set(pool_df['instrument'].tolist())

        print(current_date, "监控池股票数（昨日在60日线下）:", len(context.monitor_pool))

    # 只在 9:30 - 15:00 (含) 且每 10 分钟执行一次核心逻辑
    if not (time(9, 30) <= current_time <= time(15, 0)):
        return

    # 每 10 分钟执行一次：分钟数为 0,10,20,30,40,50
    if current_time.minute % 10 != 0:
        return

    # 当前所有标的价格信息
    # instruments 由 BigTrader 自动维护（所有在 data 中出现过的标的）
    instruments = list(context.monitor_pool.union(set(context.get_account_positions().keys())))
    if len(instruments) == 0:
        return

    # 获取当前价格（用当前分钟 close 近似）
    prices = data.current(instruments, 'close')

    # ============ 1. 买入逻辑：60 日线突破，且当日未买入过 ============
    # 为避免未来函数，这里使用“昨日的 ma60”和当前价格比较
    prev_date = get_prev_trading_date(context.all_trading_dates, current_date)
    if prev_date is None:
        return

    df_prev = context.daily_factors[context.daily_factors['date'] == prev_date]
    if df_prev.empty:
        return
    df_prev = df_prev.set_index('instrument')

    for ins in list(context.monitor_pool):
        if ins not in df_prev.index:
            continue
        # 如果已经持仓，则跳过初次买入逻辑
        positions = context.get_account_positions()
        if ins in positions:
            continue
        # 若今天已买入过（可能是加仓），也跳过
        if ins in context.today_bought:
            continue

        price_now = prices.get(ins, None)
        if price_now is None or pd.isna(price_now):
            continue

        ma60_prev = df_prev.loc[ins, 'ma60']
        # 昨日仍在60日线下已经由建池条件保证：close_yest < ma60_prev
        # 若当前价格 >= 昨日ma60，则认为突破
        if price_now >= ma60_prev:
            # 买入100股
            try:
                context.order(ins, 100)
            except Exception as e:
                print("买入失败:", ins, e)
                continue

            context.today_bought.add(ins)
            # 记录买入日期和加仓标记
            context.stock_state[ins] = {
                'buy_date': current_date,
                'added': False
            }
            print(current_dt, "首次买入", ins, "100股, 价格:", price_now)

            # 买入后从监控池中移除，避免重复判断
            context.monitor_pool.discard(ins)

    # ============ 2. 持仓管理：5日内补仓/止损，5日后10日线跌破清仓 ============
    positions = context.get_account_positions()
    if len(positions) == 0:
        return

    # 为持仓的均线计算准备前一日数据（避免未来函数）
    df_prev_all = context.daily_factors[context.daily_factors['date'] == prev_date].set_index('instrument')

    for ins in list(positions.keys()):
        pos = positions[ins]
        if pos.current_qty <= 0:
            continue

        price_now = prices.get(ins, None)
        if price_now is None or pd.isna(price_now):
            continue

        # 成本价（包含加仓后的加权成本）
        cost_price = pos.cost_price
        if cost_price is None or cost_price == 0:
            continue

        # 跳过非自选股（防止如果有其它残留持仓）
        if ins not in context.watchlist_all:
            continue

        # 获取该股票状态
        state = context.stock_state.get(ins, None)
        if state is None:
            # 若状态缺失，则初始化
            context.stock_state[ins] = {
                'buy_date': current_date,
                'added': False
            }
            state = context.stock_state[ins]

        buy_date = state['buy_date']
        added_flag = state['added']

        holding_days = (current_date - buy_date).days + 1

        # 获取昨日的10日均线，用于趋势退出
        if ins in df_prev_all.index:
            ma10_prev = df_prev_all.loc[ins, 'ma10']
        else:
            ma10_prev = None

        # 当前相对于初始成本的涨跌幅
        return_pct_from_cost = (price_now - cost_price) / cost_price

        # ===== 2.1 5日内逻辑 =====
        if holding_days <= 5:
            # 优先检查 7% 止损（清仓）
            if return_pct_from_cost <= -0.07:
                try:
                    context.order_target_percent(ins, 0)
                    print(current_dt, "5日内7%止损清仓", ins, "价格:", price_now, "成本价:", cost_price)
                except Exception as e:
                    print("止损清仓失败:", ins, e)
                # 清仓后删除状态
                if ins in context.stock_state:
                    del context.stock_state[ins]
                continue

            # 5% 跌幅补仓（若尚未补仓过）
            if (not added_flag) and (return_pct_from_cost <= -0.05):
                # 计算能用20000元买多少股
                shares_to_add = int(20000 // price_now)
                if shares_to_add > 0:
                    try:
                        context.order(ins, shares_to_add)
                        context.today_bought.add(ins)
                        context.stock_state[ins]['added'] = True
                        print(current_dt, "5日内跌5%加仓", ins, "加仓股数:", shares_to_add, "价格:", price_now)
                    except Exception as e:
                        print("加仓失败:", ins, e)

        # ===== 2.2 持仓超过5日逻辑：跌破10日均线清仓 =====
        else:
            if ma10_prev is not None and price_now < ma10_prev:
                try:
                    context.order_target_percent(ins, 0)
                    print(current_dt, "持仓超过5日跌破10日均线清仓", ins, "价格:", price_now, "昨日ma10:", ma10_prev)
                except Exception as e:
                    print("10日均线清仓失败:", ins, e)
                if ins in context.stock_state:
                    del context.stock_state[ins]

# @module(comment="分钟级趋势加仓止损策略回测")
m3 = M.bigtrader.v43(
    data=m2.data,
    start_date="2019-01-01",
    end_date="2025-12-31",
    initialize=m3_initialize_bigquant_run,
    handle_data=m3_handle_data_bigquant_run,
    capital_base=1000000,
    frequency="minute",
    product_type="股票",
    rebalance_period_type="交易日",
    rebalance_period_days="1",
    order_price_field_buy="open",
    order_price_field_sell="open",
    benchmark="沪深300指数",
    before_start_days=0,
    volume_limit=1,
    plot_charts=True,
    debug=False,
    backtest_only=False,
    m_name="m3"
)

# </aistudiograph>
