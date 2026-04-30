from bigmodule import M, I

# <aistudiograph>

# @param(id="m5", name="initialize")
# 交易引擎：初始化函数，只执行一次
def m5_initialize_bigquant_run(context):
    from bigtrader.finance.commission import PerOrder
    import sys

    # 系统已经设置了默认的交易手续费和滑点，要修改手续费可使用如下函数
    context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # ✅ 不再对 context.data 排序,因为我们会在 before_trading_start 中动态生成数据
    # context.data.sort_values('score_rank', inplace=True)  # ← 注释掉这行
    
    # ✅ 初始化每日目标股票列表
    context.today_target_stocks = []
    
    # ✅ 如果需要,可以保留 context.data 作为基础数据池
    # 例如: 用于获取所有可交易股票的列表
    if hasattr(context, 'data') and context.data is not None:
        print('=' * 50, flush=True)
        print('context.data 列名:', context.data.columns.tolist(), flush=True)
        print('context.data 总行数:', len(context.data), flush=True)
        print('数据日期范围:', context.data['date'].min(), '至', context.data['date'].max(), flush=True)
        
        # 打印前5行示例
        print('\n--- 前5行数据示例 ---', flush=True)
        print(context.data.head(5), flush=True)
        print('=' * 50, flush=True)
    else:
        print('⚠️ 注意: context.data 为空,将在 before_trading_start 中从DAI实时查询数据', flush=True)
    
    sys.stdout.flush()


# @param(id="m5", name="before_trading_start")
# 交易引擎：每个单位时间开盘前调用一次。
def m5_before_trading_start_bigquant_run(context, data):
    """
    盘前处理：每天开盘前动态计算因子并生成当日交易股票清单
    
    执行时机：每个交易日开盘前(9:00-9:15)执行一次
    适用场景：需要基于最新数据实时计算因子的策略
    """
    import dai
    import pandas as pd
    from datetime import timedelta
    
    current_date = data.current_dt.strftime('%Y-%m-%d')
    context.logger.info(f"=== {current_date} 盘前因子计算开始 ===")
    
    # try:
        # ========== 方法1: 从 DAI 数据库实时查询最新数据 ==========
        # 获取前一交易日日期(用于计算需要滞后一天的因子)
        # prev_trading_day = context.get_prev_trading_day(current_date)
        
        # 示例1: 查询最新的股票基本面数据
        # fundamental_data = dai.query(f"""
        #     SELECT 
        #         instrument,
        #         pe_ttm,
        #         pb_lf,
        #         total_market_cap,
        #         float_market_cap,
        #         roe_avg
        #     FROM cn_stock_prefactors_community
        #     WHERE date = '{prev_trading_day}'
        #     AND pe_ttm > 0
        #     AND pe_ttm < 100
        #     AND total_market_cap > 1e9
        #     ORDER BY float_market_cap ASC
        # """).df()
        
        # 示例2: 查询最新的技术指标
        # tech_data = dai.query(f"""
        #     SELECT 
        #         instrument,
        #         close,
        #         volume,
        #         c_ma(close, 5) AS ma5,
        #         c_ma(close, 20) AS ma20,
        #         c_ma(close, 60) AS ma60,
        #         c_rsi(close, 14) AS rsi14
        #     FROM cn_stock_factors
        #     WHERE date = '{prev_trading_day}'
        #     AND instrument IN ('000001.SZ', '600519.SH', '000858.SZ')  -- 可以限定股票池
        # """).df()
        
        # ========== 方法2: 基于已有 context.data 进行动态筛选 ==========
        # 如果你的基础数据已经在 m4 中准备好,这里只做动态筛选和排序
        
        # # 获取历史窗口数据(例如过去20天)用于计算动量等因子
        # lookback_days = 20
        # start_date_obj = data.current_dt - timedelta(days=lookback_days * 2)  # *2考虑非交易日
        # start_date = start_date_obj.strftime('%Y-%m-%d')
        
        # 从 context.data 中提取最近的数据
        # recent_data = context.data[
        #     (context.data['date'] >= start_date) & 
        #     (context.data['date'] <= current_date)
        # ].copy()
        
        # if len(recent_data) == 0:
        #     context.logger.warning(f"{current_date} 无可用数据,跳过今日交易")
        #     context.today_target_stocks = []
        #     return
        
        # ========== 动态计算因子示例 ==========
        
        # 示例A: 计算每只股票的近期收益率(动量因子)
        # 需要先pivot成宽表方便计算
    #     pivot_close = recent_data.pivot_table(
    #         index='date', 
    #         columns='instrument', 
    #         values='close',  # 假设你的数据中有close字段
    #         aggfunc='last'
    #     ).fillna(method='ffill')
        
    #     if len(pivot_close) >= 5:
    #         # 计算5日收益率
    #         returns_5d = (pivot_close.iloc[-1] / pivot_close.iloc[-5]) - 1
            
    #         # 添加到当日数据
    #         today_data = recent_data[recent_data['date'] == current_date].copy()
    #         today_data['momentum_5d'] = today_data['instrument'].map(returns_5d)
            
    #         # 示例B: 综合评分 = 原始score + 动量调整
    #         if 'score' in today_data.columns:
    #             today_data['final_score'] = (
    #                 today_data['score'] * 0.7 + 
    #                 today_data['momentum_5d'].rank(pct=True) * 0.3
    #             )
    #         else:
    #             today_data['final_score'] = today_data['momentum_5d']
            
    #         # ========== 生成当日交易清单 ==========
    #         # 按综合评分排序,取前N只
    #         stock_count = 5  # 持仓数量
    #         today_data = today_data.sort_values('final_score', ascending=False)
    #         target_stocks = today_data.head(stock_count).copy()
            
    #         # 计算等权重仓位
    #         target_stocks['position'] = 1.0 / stock_count
            
    #         # 保存到context,供handle_data使用
    #         context.today_target_stocks = target_stocks
            
    #         context.logger.info(
    #             f"✅ {current_date} 生成{len(target_stocks)}只目标股票: "
    #             f"{target_stocks['instrument'].tolist()}"
    #         )
    #         context.logger.info(
    #             f"   评分范围: {target_stocks['final_score'].min():.4f} - "
    #             f"{target_stocks['final_score'].max():.4f}"
    #         )
    #     else:
    #         context.logger.warning(f"数据不足,无法计算动量因子")
    #         context.today_target_stocks = []
    
    # except Exception as e:
    #     context.logger.error(f"盘前因子计算失败: {str(e)}")
    #     import traceback
    #     context.logger.error(traceback.format_exc())
    #     context.today_target_stocks = []


# @param(id="m5", name="handle_tick")
# 交易引擎：tick数据处理函数，每个tick执行一次
def m5_handle_tick_bigquant_run(context, tick):
    pass

# @param(id="m5", name="handle_data")
def m5_handle_data_bigquant_run(context, data):
    """
    盘中交易逻辑：使用盘前生成的动态股票清单进行交易
    
    注意：由于我们在 before_trading_start 中已经生成了当日目标股票,
    这里不再依赖 context.rebalance_period,而是每天都根据最新因子交易
    """
    import pandas as pd
    
    current_date = data.current_dt.strftime('%Y-%m-%d')
    
    # ✅ 检查是否有盘前生成的目标股票清单
    if not hasattr(context, 'today_target_stocks') or len(context.today_target_stocks) == 0:
        context.logger.warning(f"{current_date} 无目标股票,跳过交易")
        return
    
    target_stocks = context.today_target_stocks
    target_instruments = set(target_stocks['instrument'].tolist())
    
    # ========== 1. 卖出不在目标列表中的股票 ==========
    holding_instruments = list(context.get_account_positions().keys())
    
    for instrument in holding_instruments:
        if instrument not in target_instruments:
            rv = context.order_target_percent(instrument, 0)
            if rv == 0:
                context.logger.info(f"📤 卖出: {instrument}")
            else:
                context.logger.error(f"❌ 卖出失败: {instrument}, 错误码: {rv}")
    
    # ========== 2. 买入/调整目标股票仓位 ==========
    for _, row in target_stocks.iterrows():
        instrument = row['instrument']
        position = float(row['position'])
        
        # 检查当前持仓
        current_pos = context.get_position(instrument)
        current_weight = 0
        if current_pos and current_pos.amount > 0:
            current_weight = current_pos.market_value / context.portfolio.portfolio_value
        
        # 如果仓位差异超过阈值才调整(避免频繁交易)
        if abs(position - current_weight) > 0.01:  # 1%阈值
            rv = context.order_target_percent(instrument, position)
            if rv == 0:
                context.logger.info(
                    f"📥 买入/调仓: {instrument}, "
                    f"目标仓位: {position:.2%}, "
                    f"当前仓位: {current_weight:.2%}"
                )
            else:
                context.logger.error(
                    f"❌ 买入失败: {instrument}, 错误码: {rv}, "
                    f"错误信息: {context.get_error_msg(rv)}"
                )
    
    context.logger.info(f"=== {current_date} 交易执行完成 ===")


# @param(id="m5", name="handle_trade")
# 交易引擎：成交回报处理函数，每个成交发生时执行一次
def m5_handle_trade_bigquant_run(context, trade):
    pass

# @param(id="m5", name="handle_order")
# 交易引擎：委托回报处理函数，每个委托变化时执行一次
def m5_handle_order_bigquant_run(context, order):
    pass

# @param(id="m5", name="after_trading")
# 交易引擎：盘后处理函数，每日盘后执行一次
def m5_after_trading_bigquant_run(context, data):
    pass

# @module(position="-396,-742", comment="""使用基本信息对股票池过滤""")
m1 = M.cn_stock_basic_selector.v8(
    exchanges=["""上交所""", """深交所"""],
    st_statuses=["""正常"""],
    drop_suspended=True,
    m_name="""m1"""
)

# @module(position="-398,-652", comment="""因子特征""")
m2 = M.input_features_dai.v30(
    input_1=m1.data,
    mode="""表达式""",
    expr="""-- DAI SQL 算子/函数: https://bigquant.com/wiki/doc/dai-PLSbc1SbZX#h-%E5%87%BD%E6%95%B0
-- 数据&字段: 数据文档 https://bigquant.com/data/home
-- 数据使用: 表名.字段名, 对于没有指定表名的列，会从 expr_tables 推断

float_market_cap AS score
-- 使用 float 类型。默认是高精度 decimal.Decimal, 不能和float直接相乘""",
    expr_filters="""-- DAI SQL 算子/函数: https://bigquant.com/wiki/doc/dai-PLSbc1SbZX#h-%E5%87%BD%E6%95%B0
-- 数据&字段: 数据文档 https://bigquant.com/data/home

c_pct_rank(total_market_cap) > 0.20
c_pct_rank(pe_ttm) < 0.40
pe_ttm > 0 

""",
    expr_tables="""cn_stock_prefactors_community""",
    extra_fields="""date, instrument""",
    order_by="""date, instrument""",
    expr_drop_na=True,
    sql="""-- 使用DAI SQL获取数据，构建因子等，如下是一个例子作为参考
-- DAI SQL 语法: https://bigquant.com/wiki/doc/dai-PLSbc1SbZX#h-sql%E5%85%A5%E9%97%A8%E6%95%99%E7%A8%8B

SELECT

    -- 在这里输入因子表达式
    -- DAI SQL 算子/函数: https://bigquant.com/wiki/doc/dai-PLSbc1SbZX#h-%E5%87%BD%E6%95%B0
    -- 数据&字段: 数据文档 https://bigquant.com/data/home

    c_rank(volume) AS rank_volume,
    close / m_lag(close, 1) as return_0,

    -- 日期和股票代码
    date, instrument
FROM
    -- 预计算因子 cn_stock_factors https://bigquant.com/data/datasources/cn_stock_factors
    cn_stock_factors
WHERE
    -- WHERE 过滤，在窗口等计算算子之前执行
    -- 剔除ST股票
    st_status = 0
QUALIFY
    -- QUALIFY 过滤，在窗口等计算算子之后执行，比如 m_lag(close, 3) AS close_3，对于 close_3 的过滤需要放到这里
    -- 去掉有空值的行
    COLUMNS(*) IS NOT NULL
-- 按日期和股票代码排序，从小到大
ORDER BY date, instrument
""",
    extract_data=False,
    m_name="""m2"""
)

# @module(position="-399,-556", comment="""持股数量、打分到仓位""")
m3 = M.score_to_position.v7(
    input_1=m2.data,
    score_field="""score ASC""",
    hold_count=5,
    position_expr="""-- DAI SQL 算子/函数: https://bigquant.com/wiki/doc/dai-PLSbc1SbZX#h-%E5%87%BD%E6%95%B0
-- 在这里输入表达式, 每行一个表达式, 输出仓位字段必须命名为 position, 模块会进一步做归一化
-- 排序倒数: 1 / score_rank AS position
-- 对数下降: 1 / log2(score_rank + 1) AS position
-- TODO 拟合、最优化 ..

-- 等权重分配
1 AS position
""",
    total_position=1,
    extract_data=False,
    m_name="""m3"""
)

# @module(position="-401,-456", comment="""抽取预测数据""")
m4 = M.extract_data_dai.v20(
    sql=m3.data,
    start_date="""2024-01-01""",
    start_date_bound_to_trading_date=True,
    end_date="""2024-12-31""",
    end_date_bound_to_trading_date=True,
    before_start_days=90,
    keep_before=False,
    debug=False,
    m_name="""m4"""
)

# @module(position="-403,-344", comment="""交易，日线，设置初始化函数和K线处理函数，以及初始资金、基准等""")
m5 = M.bigtrader.v58(
    data=m4.data,
    start_date="""""",
    end_date="""""",
    initialize=m5_initialize_bigquant_run,
    before_trading_start=m5_before_trading_start_bigquant_run,
    handle_tick=m5_handle_tick_bigquant_run,
    handle_data=m5_handle_data_bigquant_run,
    handle_trade=m5_handle_trade_bigquant_run,
    handle_order=m5_handle_order_bigquant_run,
    after_trading=m5_after_trading_bigquant_run,
    capital_base=1000000,
    frequency="""daily""",
    product_type="""股票""",
    rebalance_period_type="""交易日""",
    rebalance_period_days="""5""",
    rebalance_period_roll_forward=True,
    backtest_engine_mode="""标准模式""",
    before_start_days=0,
    volume_limit=1,
    order_price_field_buy="""open""",
    order_price_field_sell="""open""",
    benchmark="""沪深300指数""",
    plot_charts="""全部显示""",
    debug=False,
    backtest_only=False,
    m_name="""m5"""
)
# </aistudiograph>
