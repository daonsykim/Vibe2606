import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("=" * 90)
print("한국 출생아수 역사적 사건 분석 (1970-2024)")
print("=" * 90)

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

print("\n" + "▶ " * 45)
print("【시기별 특징 분석】")
print("▶ " * 45 + "\n")

# 시기별 특징 정의 (더 상세)
periods = [
    {
        'name': '가족계획 정책 시대',
        'start': 1970,
        'end': 1983,
        'color': '#FF6B6B',
        'title_color': '#C92A2A',
        'events': [
            ('1970년대 초중반', '정부 주도 "가족계획 정책"\n- 인구 억제 목표 추진\n- "셋도 많고 둘도 많고 하나만 낳아 잘 기르자" 캠페인'),
            ('1977년', '강화된 캠페인 "둘만 낳아 훌륭히 기르자"\n- 텔레비전과 라디오를 통한 대량 홍보\n- 지자체 차원의 인센티브 제공'),
            ('1983년 전후', '초저출산 달성 후 정책 전환\n- 정부가 저출산의 부작용 인식\n- 출산 장려 정책으로 방향 변경'),
        ],
        'analysis': '의도적 정책에 의한 출생아수 감소 (106만명 → 77만명, -28%)'
    },
    {
        'name': '경제 성장 & 사회 변화',
        'start': 1984,
        'end': 1996,
        'color': '#4ECDC4',
        'title_color': '#1098AD',
        'events': [
            ('1980년대 중반', '한국 경제 고도성장 시작\n- 중산층 확대, 소비 문화 발달\n- 대도시 집중화로 주택 부담 증가'),
            ('1986, 1988년', '서울 아시안게임(1986), 올림픽(1988)\n- 국가 위상 제고\n- 결혼·출산 문화의 다양화 시작'),
            ('1990년대 초', '여성 고등교육 확대 (진학률 40% → 50%)\n- 평균 결혼 연령 상향 (22세 → 25세)\n- 자녀 계획적 선택 시작'),
        ],
        'analysis': '구조적 변화로 인한 자연 감소 (77만명 → 73만명, -5%)'
    },
    {
        'name': 'IMF 외환위기 & 경제 충격',
        'start': 1997,
        'end': 2003,
        'color': '#FFB3B3',
        'title_color': '#E63946',
        'events': [
            ('1997년 11월', 'IMF 외환위기 발생\n- 국가 신용도 하락, 구조조정 본격화\n- 실업률 급증 (3% → 8.6%)'),
            ('1998-1999년', '경제 위기의 피크\n- 결혼 건수 급감 (-23.7%)\n- 임신·출산 미연기 현상 심화'),
            ('1998년 출생아수 최대 낙폭', '-9.8% 감소 (최악의 연도)\n- 사상 처음 50만명대로 급락\n- 경제 위기가 출산 의사에 미친 영향 명확'),
        ],
        'analysis': '경제 위기에 의한 급격한 충격 (67만명 → 50만명, -27%)'
    },
    {
        'name': '저출산 대책 도입 & 제한적 성과',
        'start': 2004,
        'end': 2011,
        'color': '#FFE66D',
        'title_color': '#D4A017',
        'events': [
            ('2005년 이후', '정부 "저출산·고령사회 기본계획" 본격 추진\n- 출산 장려금 지급 시작\n- 보육료 지원 확대'),
            ('2008년 글로벌 금융위기', 'Lehman Brothers 파산 충격\n- 한국 경제 또 다시 충격\n- 출산 장려 정책의 효과 제한적'),
            ('2010년대 초', '여성 경제활동 참가 본격화\n- 육아와 경력 단절의 갈등 심화\n- 결혼·출산 선택 미연기'),
        ],
        'analysis': '정책 노력에도 구조적 감소 지속 (48만명 → 47만명, -1%)'
    },
    {
        'name': '여성 진출 & 구조적 저출산 심화',
        'start': 2012,
        'end': 2019,
        'color': '#95E1D3',
        'title_color': '#06A77D',
        'events': [
            ('2015년-2017년', '지표금 상승, 교육비 증가\n- 아파트 전세금 폭등\n- 사교육비 지출 연 1,000만원대'),
            ('2018년 촛불 집회', '탈성평 운동 확산\n- 여성의 출산 의사 급락\n- 합계출산율 0.98명으로 OECD 최저 수준'),
            ('2019년', '합계출산율 0.92명\n- 한국 통계 작성 이래 최저 기록\n- 국가 존망 관련 위기 인식 확산'),
        ],
        'analysis': '구조적 저출산 심화 (47만명 → 43만명, -9%)'
    },
    {
        'name': '팬데믹 & 초저출산 극복 과제',
        'start': 2020,
        'end': 2024,
        'color': '#FF8C9E',
        'title_color': '#E63946',
        'events': [
            ('2020년 코로나19 팬데믹', '결혼식, 백일잔치 등 생활 문화 위축\n- 경제 불확실성 증가\n- 출산 의사 급락 (-10%)'),
            ('2021년-2023년', '극단적 저출산 심화\n- 2023년 출생아수 23만명 (통계 최저)\n- 매년 10% 이상 감소 추세'),
            ('2024년', '소폭 반등 (+3.6%) 하지만 여전히 위기\n- 24만명 대 회복\n- 구조적 개선 필요'),
        ],
        'analysis': '팬데믹 충격 + 구조적 위기 (27만명 → 23만명 → 24만명, -12%→+3.6%)'
    }
]

# 콘솔 출력
for idx, period in enumerate(periods, 1):
    period_data = df_filtered[(df_filtered['연도'] >= period['start']) & 
                             (df_filtered['연도'] <= period['end'])]
    
    if len(period_data) > 0:
        start_val = period_data.iloc[0]['출생아수']
        end_val = period_data.iloc[-1]['출생아수']
        change = end_val - start_val
        change_pct = (change / start_val) * 100
        
        print(f"\n┌─ PHASE {idx}: {period['name']} ({period['start']}-{period['end']})")
        print(f"│  {period['analysis']}")
        print(f"│")
        print(f"│  ├ 출생아수: {start_val:>12,.0f}명 → {end_val:>12,.0f}명")
        print(f"│  └ 변화량: {change:>12,.0f}명 ({change_pct:>+6.1f}%)")
        
        for year, description in period['events']:
            print(f"│")
            print(f"├─ 📅 {year}")
            for line in description.split('\n'):
                print(f"│   {line}")
        
        print(f"└─────────────────────────────────────────────────────")

print("\n" + "=" * 90)
print("【핵심 결론】")
print("=" * 90)
print("""
1. 1970-1983: 정부의 인구억제 정책이 성공 → 의도적 출생아수 감소

2. 1984-1996: 경제 성장과 함께 구조적 변화 시작 
   → 여성 교육·고용 증가, 결혼관·가치관 변화

3. 1997-2003: IMF 외환위기가 극적인 전환점
   → 경제 위기로 출산 미연기 현상 극심화

4. 2004-2011: 정부 저출산 대책 도입
   → 하지만 구조적 문제로 효과 미흡

5. 2012-2019: 여성 진출, 주택·교육비 부담, 탈성평 운동
   → 출산 선택의 여성화, 저출산 심화

6. 2020-2024: 팬데믹 충격 + 초저출산 위기
   → 2023년 최저치 23만명, 2024년 소폭 회복도 위기 지속

【정책 시사점】
• 경제 위기, 주택 부담, 여성 고용 불안정이 저출산의 주요 원인
• 단순 경제적 지원만으로는 근본적 해결 불가능
• 일-가정 양립, 양성평등 문화 개선 등 구조적 변화 필요
""")

print("=" * 90)
print("분석 완료!\n")
