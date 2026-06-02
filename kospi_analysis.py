import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

CSV_PATH = 'kospi_data.csv'
OUT_PNG = 'kospi_close_2000_2019_kospi.png'
SUMMARY_CSV = 'kospi_summary_2000_2019.csv'


def analyze():
    df = pd.read_csv(CSV_PATH, parse_dates=['Date'])
    df.sort_values('Date', inplace=True)

    # 기본 컬럼 확인
    required = ['Date', 'Close']
    for c in required:
        if c not in df.columns:
            raise SystemExit(f'CSV에 필요한 열이 없습니다: {c}')

    # 클렌징: 결측, 중복, 숫자 변환
    df = df[['Date', 'Close']].copy()
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df.dropna(subset=['Date', 'Close'], inplace=True)
    df.drop_duplicates(subset=['Date'], keep='last', inplace=True)

    # 기간 필터
    df = df[(df['Date'] >= '2000-01-01') & (df['Date'] <= '2019-12-31')].copy()
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    if df.empty:
        print('해당 기간의 데이터가 없습니다.')
        return

    # 일간 수익률
    df['Return'] = df['Close'].pct_change()

    # 기본 통계
    desc = df['Close'].describe()

    # 연별 수익률 (년말 종가 사용)
    yearly = df['Close'].resample('Y').last()
    yearly_ret = yearly.pct_change().dropna()

    # 월별 변동성 (리턴의 표준편차 * sqrt(252) 소비 으로 연환산 대체)
    monthly_ret = df['Return'].resample('M').apply(lambda x: (1 + x).prod() - 1)
    monthly_vol = df['Return'].resample('M').std()

    # 누적 수익률, 연환산 수익률/변동성
    start_price = df['Close'].iloc[0]
    end_price = df['Close'].iloc[-1]
    cumulative_return = end_price / start_price - 1
    trading_days = df.shape[0]
    annual_factor = 252
    annualized_return = (1 + cumulative_return) ** (annual_factor / trading_days) - 1 if trading_days>0 else np.nan
    annualized_vol = df['Return'].std() * np.sqrt(annual_factor)

    # 최대 낙폭
    cummax = df['Close'].cummax()
    drawdown = (df['Close'] - cummax) / cummax
    max_drawdown = drawdown.min()

    # 최고/최저 값과 날짜
    highest = df['Close'].idxmax(), df['Close'].max()
    lowest = df['Close'].idxmin(), df['Close'].min()

    # 요약 데이터프레임 저장
    summary = pd.DataFrame({
        'start_price':[start_price],
        'end_price':[end_price],
        'cumulative_return':[cumulative_return],
        'annualized_return':[annualized_return],
        'annualized_vol':[annualized_vol],
        'max_drawdown':[max_drawdown],
        'highest_date':[highest[0].date()],
        'highest_price':[highest[1]],
        'lowest_date':[lowest[0].date()],
        'lowest_price':[lowest[1]]
    })

    # 연별 수익률을 CSV로 저장 (연도별)
    yearly_ret.index = yearly_ret.index.year
    yearly_ret.name = 'annual_return'
    yearly_ret.to_csv('kospi_annual_returns_2000_2019.csv')

    # 종합 요약 저장
    summary.to_csv(SUMMARY_CSV, index=False)

    # 그래프 그리기 (종가 + MA50, MA200) 및 최고/최저 주석
    rolling50 = df['Close'].rolling(50).mean()
    rolling200 = df['Close'].rolling(200).mean()

    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=(14,7))
    ax.plot(df.index, df['Close'], label='Close')
    ax.plot(rolling50, label='MA50', linewidth=1)
    ax.plot(rolling200, label='MA200', linewidth=1)

    # 최고/최저 주석
    ax.scatter([highest[0]], [highest[1]], color='red')
    ax.annotate(f'High {highest[1]:.2f}\n{highest[0].date()}', xy=(highest[0], highest[1]), xytext=(10,20), textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    ax.scatter([lowest[0]], [lowest[1]], color='green')
    ax.annotate(f'Low {lowest[1]:.2f}\n{lowest[0].date()}', xy=(lowest[0], lowest[1]), xytext=(10,-40), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    ax.set_title('KOSPI Close Price 2000-01-01 to 2019-12-31')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    # 간단 출력
    print('기간:', df.index[0].date(), '~', df.index[-1].date())
    print('시작 종가:', round(start_price,4))
    print('종료 종가:', round(end_price,4))
    print('누적 수익률:', f"{cumulative_return*100:.2f}%")
    print('연환산 수익률(근사):', f"{annualized_return*100:.2f}%")
    print('연환산 변동성(근사):', f"{annualized_vol*100:.2f}%")
    print('최대 낙폭(최저):', f"{max_drawdown*100:.2f}%")
    print('\n최고점:', highest[0].date(), highest[1])
    print('최저점:', lowest[0].date(), lowest[1])
    print('\n연별 수익률 파일:', os.path.abspath('kospi_annual_returns_2000_2019.csv'))
    print('요약 파일:', os.path.abspath(SUMMARY_CSV))
    print('그래프 파일:', os.path.abspath(OUT_PNG))


if __name__ == '__main__':
    analyze()
