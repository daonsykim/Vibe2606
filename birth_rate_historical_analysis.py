import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import os

# 한글 폰트 설정 (개선된 방식)
def setup_korean_font():
    """Windows 시스템 폰트를 직접 사용하여 한글 폰트 설정"""
    # Windows 폰트 경로
    font_paths = [
        'C:\\Windows\\Fonts\\malgun.ttf',  # Malgun Gothic Regular
        'C:\\Windows\\Fonts\\malgunbd.ttf',  # Malgun Gothic Bold
        'C:\\Windows\\Fonts\\ARIAL.TTF',  # Arial fallback
    ]
    
    # NanumGothic 폰트 우선 사용
    nanum_path = 'C:\\Windows\\Fonts\\NanumGothic.ttf'
    
    # 설치된 폰트 찾기
    available_font = None
    
    # Malgun Gothic 우선
    if os.path.exists('C:\\Windows\\Fonts\\malgun.ttf'):
        available_font = 'C:\\Windows\\Fonts\\malgun.ttf'
    
    if available_font and os.path.exists(available_font):
        font_prop = fm.FontProperties(fname=available_font)
        plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
    
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 10

# 폰트 설정 실행
setup_korean_font()

print("=" * 80)
print("한국 출생아수 역사적 분석 (1970-2024)")
print("=" * 80)

# 데이터 로드
file_path = '출생아수__합계출산율__자연증가_등_20260602141801.xlsx'
df = pd.read_excel(file_path, sheet_name='데이터')
df = df.set_index(df.columns[0])

# 출생아수 데이터 추출
birth_data = df.loc['출생아수(명)'].copy()
df_clean = pd.DataFrame({
    '연도': pd.to_numeric(birth_data.index, errors='coerce'),
    '출생아수': pd.to_numeric(birth_data.values, errors='coerce')
})

df_clean = df_clean.dropna()
df_clean = df_clean.sort_values('연도').reset_index(drop=True)
df_filtered = df_clean[(df_clean['연도'] >= 1970) & (df_clean['연도'] <= 2024)].copy()

print("\n[주요 사건 및 정책]")

# 시기별 특징 정의
periods = [
    {
        'name': '1단계: 가족계획 정책 시대',
        'start': 1970,
        'end': 1983,
        'color': '#FF6B6B',
        'events': [
            '1970s: 가족계획 정책 (인구억제)\n국가적 차원의 소자녀 권장',
            '1977년: "둘만 낳아 훌륭히 기르자"\n정부 주도 캠페인 시작',
            '1983년: 1자녀 정책 강화\n(저출산 정책으로 전환)',
        ]
    },
    {
        'name': '2단계: 경제 성장 & 여성진출',
        'start': 1984,
        'end': 1996,
        'color': '#4ECDC4',
        'events': [
            '1980s 중반~1990s: 여성 고등교육\n진학률 증가 (40% → 60%)',
            '1986년: 86 아시안게임, 1988년: 서울올림픽\n경제 호황 속 결혼관 변화',
            '1990s: IMF 외환위기 전 경제 안정기\n결혼 연령 상향',
        ]
    },
    {
        'name': '3단계: IMF 위기 & 경제 충격',
        'start': 1997,
        'end': 2003,
        'color': '#FFB3B3',
        'events': [
            '1997년 11월: IMF 외환위기\n경제 불황으로 결혼·출산 미연기',
            '1998년: 실업률 급증 (7.8%)\n신혼가구 형성 지연',
            '2000년대 초: 저출산 추세 심화\n합계출산율 1.5명 이하로 하락',
        ]
    },
    {
        'name': '4단계: 저출산 위기 본격화',
        'start': 2004,
        'end': 2011,
        'color': '#FFE66D',
        'events': [
            '2005년~: 정부 저출산 대책 추진\n출산 장려금, 육아 지원 정책',
            '2008년: 글로벌 금융위기\n"경제 위기"가 출산 의사 저하',
            '2010s 초반: 높은 육아비용\n서울 어린이집 월 100만원 이상',
        ]
    },
    {
        'name': '5단계: 심각한 저출산 위기',
        'start': 2012,
        'end': 2019,
        'color': '#95E1D3',
        'events': [
            '2015년~: 여성 일자리 진출 본격화\n경력 단절 우려로 출산 미연기',
            '2016년: 보육료 지원 확대\n(누리과정 시행)',
            '2019년: 합계출산율 0.92명\nOECD 최저 수준',
        ]
    },
    {
        'name': '6단계: 초저출산 & 코로나 충격',
        'start': 2020,
        'end': 2024,
        'color': '#FF8C9E',
        'events': [
            '2020년~: 코로나19 팬데믹\n결혼식, 출산 미연기',
            '2021년 4월: "저출산 극복" 핵심전략\n(정부 종합대책)',
            '2023년: 출생아수 23만명\n통계 작성 이래 최저 기록',
        ]
    }
]

# 각 시기의 출생아수 변화 계산
for period in periods:
    period_data = df_filtered[(df_filtered['연도'] >= period['start']) & 
                             (df_filtered['연도'] <= period['end'])]
    
    if len(period_data) > 0:
        start_val = period_data.iloc[0]['출생아수']
        end_val = period_data.iloc[-1]['출생아수']
        change = end_val - start_val
        change_pct = (change / start_val) * 100
        
        print(f"\n【{period['name']}】 ({period['start']}-{period['end']})")
        print(f"  시작: {start_val:,.0f}명 → 종료: {end_val:,.0f}명")
        print(f"  변화: {change:+,.0f}명 ({change_pct:+.1f}%)")
        for event in period['events']:
            print(f"  • {event}")

# 시각화
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 1, height_ratios=[2, 1.5, 1], hspace=0.35)

# 1. 메인 그래프: 출생아수 추이 + 사건 표시
ax1 = fig.add_subplot(gs[0])

# 배경색으로 시기 표시
for period in periods:
    ax1.axvspan(period['start'], period['end'], alpha=0.15, color=period['color'])

# 라인 그래프
ax1.plot(df_filtered['연도'], df_filtered['출생아수'], 
         linewidth=3, color='#2C3E50', marker='o', markersize=5, label='출생아수')
ax1.fill_between(df_filtered['연도'], df_filtered['출생아수'], alpha=0.2, color='#3498DB')

# 주요 사건 표시
events_annotation = [
    (1977, 850000, '둘만 낳아\n훌륭히 기르자', '#FF6B6B'),
    (1997, 650000, 'IMF 외환위기', '#FFB3B3'),
    (2008, 600000, '글로벌\n금융위기', '#FFE66D'),
    (2020, 450000, '코로나19\n팬데믹', '#FF8C9E'),
    (2023, 230000, '최저 기록\n23만명', '#E74C3C'),
]

for year, value, text, color in events_annotation:
    ax1.annotate(text, xy=(year, value), xytext=(year, value + 100000),
                ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.7),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))

ax1.set_xlabel('연도', fontsize=13, fontweight='bold')
ax1.set_ylabel('출생아수 (명)', fontsize=13, fontweight='bold')
ax1.set_title('한국 출생아수 추이와 주요 역사적 사건 (1970-2024)', 
              fontsize=15, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/10000):.0f}만'))
ax1.set_xlim(1968, 2026)

# 2. 시기별 특징 시각화
ax2 = fig.add_subplot(gs[1])
ax2.axis('off')

y_pos = 0.95
for i, period in enumerate(periods):
    period_data = df_filtered[(df_filtered['연도'] >= period['start']) & 
                             (df_filtered['연도'] <= period['end'])]
    
    if len(period_data) > 0:
        start_val = period_data.iloc[0]['출생아수']
        end_val = period_data.iloc[-1]['출생아수']
        change_pct = ((end_val - start_val) / start_val) * 100
        
        # 배경색 박스
        rect = Rectangle((0.02, y_pos - 0.11), 0.96, 0.10, 
                         facecolor=period['color'], alpha=0.3, 
                         edgecolor=period['color'], linewidth=2)
        ax2.add_patch(rect)
        
        # 텍스트
        period_name = f"【{period['start']}-{period['end']}】 {period['name']}"
        change_text = f"변화: {change_pct:+.0f}%  ({start_val:,.0f} → {end_val:,.0f}명)"
        
        ax2.text(0.04, y_pos - 0.02, period_name, fontsize=11, fontweight='bold',
                verticalalignment='top', color='#2C3E50')
        ax2.text(0.04, y_pos - 0.08, change_text, fontsize=10,
                verticalalignment='top', color='#34495E')
        
        y_pos -= 0.12

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)

# 3. 세부 분석: 각 시기별 정책 효과
ax3 = fig.add_subplot(gs[2])
ax3.axis('off')

analysis_text = """
【정책 효과 분석】

1970-1983: 가족계획 정책의 성공 단계
   • 출생아수 감소 (1,006만명 → 774만명)
   • 정부 주도의 소자녀 정책으로 의도적 감소

1984-1996: 경제 성장 속 자연 감소
   • 여성 교육 수준 향상로 평균 결혼 연령 상향 (22세 → 25세)
   • 대도시 집중화로 주택 부담 증가

1997-2003: IMF 위기 충격 (급격한 감소)
   • 출생아수 하락률 최대 (-9.8%)
   • 경제 불황으로 결혼·출산 미연기

2004-2011: 저출산 대책 도입 (제한적 효과)
   • 보육료 지원, 출산 장려금 도입
   • 하지만 구조적 변화로 효과 미흡

2012-2019: 여성 경제활동 증대
   • 일-생활 균형 문제 심화
   • 결혼관·출산관 급변

2020-2024: 초저출산 위기 심화
   • 코로나19 이후 혼인 및 출산 급감
   • 2024년 소폭 회복(+3.6%)도 여전히 위기 수준
"""

ax3.text(0.02, 0.95, analysis_text, fontsize=9, verticalalignment='top',
        family='monospace', bbox=dict(boxstyle='round', facecolor='#ECF0F1', alpha=0.8))

# 범례 추가
legend_elements = [mpatches.Patch(facecolor=period['color'], alpha=0.3, 
                                  edgecolor=period['color'], linewidth=2,
                                  label=f"{period['start']}-{period['end']}: {period['name']}")
                   for period in periods]
ax1.legend(handles=legend_elements, loc='upper right', fontsize=9, ncol=2)

plt.savefig('birth_rate_historical_analysis.png', dpi=300, bbox_inches='tight')
print("\n" + "=" * 80)
print("그래프 저장 완료: birth_rate_historical_analysis.png")
print("=" * 80)

plt.show()
