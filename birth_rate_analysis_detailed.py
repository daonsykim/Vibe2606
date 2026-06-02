import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
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

print("=" * 60)
print("출생아수 데이터 분석 시작")
print("=" * 60)

# 1. 엑셀 파일 로드
file_path = '출생아수__합계출산율__자연증가_등_20260602141801.xlsx'
print(f"\n[1단계] 파일 로드: {file_path}")

try:
    # 모든 시트 확인
    xl_file = pd.ExcelFile(file_path)
    print(f"시트 목록: {xl_file.sheet_names}")
    
    # '데이터' 시트 로드
    df = pd.read_excel(file_path, sheet_name='데이터')
    print(f"\n원본 데이터 크기: {df.shape}")
    print(f"\n원본 데이터 구조:")
    print(df.head(3))
    print(f"\n첫 번째 컬럼 (기본항목별):")
    print(df.iloc[:, 0].tolist())
    
except Exception as e:
    print(f"파일 로드 오류: {e}")
    exit()

# 2. 데이터 클랜징
print("\n" + "=" * 60)
print("[2단계] 데이터 클랜징")
print("=" * 60)

print("\n[데이터 변환]")
print("원본 구조: 행=기본항목별(출생아수, 자연증가, 출산율 등), 열=연도(1970~2025)")
print("목표 구조: 행=연도(1970~2024), 열=기본항목별")

# 첫 번째 컬럼을 인덱스로 설정
df = df.set_index(df.columns[0])

# 출생아수만 추출
birth_data = df.loc['출생아수(명)'].copy()
print(f"\n추출된 출생아수 데이터:")
print(birth_data.head())

# 데이터프레임으로 변환 및 정리
df_clean = pd.DataFrame({
    '연도': pd.to_numeric(birth_data.index, errors='coerce'),
    '출생아수': pd.to_numeric(birth_data.values, errors='coerce')
})

# null 값 제거
df_clean = df_clean.dropna()
print(f"\nnull 제거 후: {df_clean.shape[0]}행")

# 연도순 정렬
df_clean = df_clean.sort_values('연도').reset_index(drop=True)

# 1970~2024년 데이터만 필터링
df_filtered = df_clean[(df_clean['연도'] >= 1970) & (df_clean['연도'] <= 2024)].copy()
print(f"1970~2024년 필터링 후: {df_filtered.shape[0]}행")

print(f"\n정제된 데이터 범위: {df_filtered['연도'].min():.0f}년 ~ {df_filtered['연도'].max():.0f}년")
print(f"출생아수 범위: {df_filtered['출생아수'].min():.0f}명 ~ {df_filtered['출생아수'].max():.0f}명")

# 4. 데이터 분석
print("\n" + "=" * 60)
print("[3단계] 데이터 분석")
print("=" * 60)

print(f"\n기본 통계:")
print(f"  평균 출생아수: {df_filtered['출생아수'].mean():,.0f}명")
print(f"  중앙값: {df_filtered['출생아수'].median():,.0f}명")
print(f"  최대값: {df_filtered['출생아수'].max():,.0f}명 ({df_filtered.loc[df_filtered['출생아수'].idxmax(), '연도']:.0f}년)")
print(f"  최소값: {df_filtered['출생아수'].min():,.0f}명 ({df_filtered.loc[df_filtered['출생아수'].idxmin(), '연도']:.0f}년)")
print(f"  표준편차: {df_filtered['출생아수'].std():,.0f}명")

# 연도별 증감
df_filtered['증감'] = df_filtered['출생아수'].diff()
df_filtered['증감율'] = (df_filtered['출생아수'].pct_change() * 100).round(2)

print(f"\n최근 변화 (2020-2024년):")
recent = df_filtered[df_filtered['연도'] >= 2020]
for idx, row in recent.iterrows():
    if pd.notna(row['증감']):
        print(f"  {row['연도']:.0f}년: {row['출생아수']:,.0f}명 (전년대비 {row['증감']:+,.0f}명, {row['증감율']:+.2f}%)")
    else:
        print(f"  {row['연도']:.0f}년: {row['출생아수']:,.0f}명")

# 5. 시각화
print("\n" + "=" * 60)
print("[4단계] 그래프 생성")
print("=" * 60)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# 라인 그래프
ax1.plot(df_filtered['연도'], df_filtered['출생아수'], 
         linewidth=2.5, color='#2E86AB', marker='o', markersize=4, label='출생아수')
ax1.fill_between(df_filtered['연도'], df_filtered['출생아수'], alpha=0.3, color='#2E86AB')

ax1.set_xlabel('연도', fontsize=12, fontweight='bold')
ax1.set_ylabel('출생아수 (명)', fontsize=12, fontweight='bold')
ax1.set_title('1970~2024년 한국 출생아수 추이', fontsize=14, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend(loc='upper right', fontsize=11)

# Y축 포맷 (천 단위 쉼표)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

# 증감률 그래프
colors = ['#A23B72' if x < 0 else '#F18F01' for x in df_filtered['증감율'].fillna(0)]
ax2.bar(df_filtered['연도'], df_filtered['증감율'], color=colors, alpha=0.7, label='전년대비 증감율')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax2.set_xlabel('연도', fontsize=12, fontweight='bold')
ax2.set_ylabel('증감율 (%)', fontsize=12, fontweight='bold')
ax2.set_title('연도별 출생아수 증감율', fontsize=14, fontweight='bold', pad=20)
ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
ax2.legend(loc='upper right', fontsize=11)

plt.tight_layout()

# 그래프 저장
output_file = 'birth_rate_analysis.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n그래프 저장 완료: {output_file}")

plt.show()

# 6. 정제된 데이터 저장
output_csv = 'birth_rate_cleaned_1970_2024.csv'
df_filtered[['연도', '출생아수']].to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f"정제된 데이터 저장 완료: {output_csv}")

print("\n" + "=" * 60)
print("분석 완료!")
print("=" * 60)
