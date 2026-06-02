import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

CSV_PATH = 'kospi_data.csv'
OUT_PNG = 'sp500_close_2000_2019.png'

def main():
    # 읽기 및 기본 정리
    df = pd.read_csv(CSV_PATH, parse_dates=['Date'])
    df.sort_values('Date', inplace=True)
    if 'Close' not in df.columns:
        raise SystemExit('CSV에 Close 열이 없습니다.')
    df = df[['Date', 'Close']].dropna()

    # 기간 필터 (2000-01-01 ~ 2019-12-31)
    mask = (df['Date'] >= '2000-01-01') & (df['Date'] <= '2019-12-31')
    df = df.loc[mask].copy()
    df.set_index('Date', inplace=True)

    if df.empty:
        print('해당 기간에 데이터가 없습니다.')
        return

    # 리턴 및 통계
    df['Return'] = df['Close'].pct_change()
    start_price = df['Close'].iloc[0]
    end_price = df['Close'].iloc[-1]
    cumulative_return = end_price / start_price - 1
    trading_days = df.shape[0]
    annual_factor = 252
    annualized_return = (1 + cumulative_return) ** (annual_factor / trading_days) - 1 if trading_days>0 else np.nan
    annualized_vol = df['Return'].std() * np.sqrt(annual_factor)
    rolling50 = df['Close'].rolling(50).mean()
    rolling200 = df['Close'].rolling(200).mean()
    cummax = df['Close'].cummax()
    drawdown = (df['Close'] - cummax) / cummax
    max_drawdown = drawdown.min()

    # 출력
    print('기간:', df.index[0].date(), '~', df.index[-1].date())
    print('시작 종가:', round(start_price, 4))
    print('종료 종가:', round(end_price, 4))
    print('누적 수익률:', f"{cumulative_return*100:.2f}%")
    print('연환산 수익률(근사):', f"{annualized_return*100:.2f}%")
    print('연환산 변동성(근사):', f"{annualized_vol*100:.2f}%")
    print('최대 낙폭(최저):', f"{max_drawdown*100:.2f}%")
    print('\n최근 5행:')
    print(df.tail())

    # 그래프
    plt.style.use('seaborn-darkgrid')
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df['Close'], label='Close')
    plt.plot(rolling50, label='MA50', linewidth=1)
    plt.plot(rolling200, label='MA200', linewidth=1)
    plt.title('Close Price 2000-01-01 to 2019-12-31')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=150)
    plt.close()

    print('\n그래프를 생성하고 저장했습니다:', os.path.abspath(OUT_PNG))

if __name__ == '__main__':
    main()
