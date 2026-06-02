import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 엑셀 파일 로드
file_path = Path('출생아수__합계출산율__자연증가_등_20260602141801.xlsx')
print(f"파일 로드 중: {file_path}")

# 먼저 파일의 시트 확인
xl_file = pd.ExcelFile(file_path)
print(f"\n사용 가능한 시트: {xl_file.sheet_names}")

# 첫 번째 시트 로드
df = pd.read_excel(file_path, sheet_name=0)
print(f"\n원본 데이터 형태: {df.shape}")
print(f"컬럼명: {list(df.columns)}")
print(f"\n처음 5행:")
print(df.head())
print(f"\n데이터 타입:")
print(df.dtypes)
print(f"\n결측치 정보:")
print(df.isnull().sum())

# ========================
# 데이터 클랜징
# ========================
print("\n" + "="*50)
print("데이터 클랜징 시작")
print("="*50)

# 1. 컬럼명 정리 (앞뒤 공백 제거)
df.columns = df.columns.str.strip()
print(f"\n1. 컬럼명 정리 후: {list(df.columns)}")

# 2. 첫 번째 컬럼이 연도로 보이는 경우 확인
print(f"\n2. 첫 번째 컬럼 값 샘플:")
print(df.iloc[:, 0].head(10))

# 3. 연도 컬럼 확인 및 지정
# 일반적으로 첫 번째 컬럼이 연도
year_col = df.columns[0]
print(f"\n3. 연도 컬럼으로 지정: '{year_col}'")

# 4. 데이터 타입 변환
df[year_col] = pd.to_numeric(df[year_col], errors='coerce')

# 5. 출생아수 컬럼 찾기 (여러 가능성 확인)
print(f"\n4. 모든 컬럼 확인:")
for i, col in enumerate(df.columns):
    print(f"   [{i}] {col}")

# 6. 결측치가 있는 행 제거 또는 처리
df = df.dropna(subset=[year_col])
print(f"\n5. 결측치 제거 후 행 수: {len(df)}")

# 7. 1970~2024년 범위로 필터링
df_filtered = df[(df[year_col] >= 1970) & (df[year_col] <= 2024)].copy()
df_filtered = df_filtered.sort_values(year_col)
print(f"\n6. 1970-2024년 데이터 필터링 후: {len(df_filtered)}행")
print(f"   연도 범위: {df_filtered[year_col].min()} - {df_filtered[year_col].max()}")

# ========================
# 데이터 분석
# ========================
print("\n" + "="*50)
print("데이터 분석")
print("="*50)

# 출생아수 컬럼 찾기 - 두 번째 컬럼을 출생아수로 가정
# (일반적인 통계청 형식)
birth_col = df_filtered.columns[1]
print(f"\n출생아수 컬럼: '{birth_col}'")

# 해당 컬럼의 데이터 타입 확인 및 숫자로 변환
df_filtered[birth_col] = pd.to_numeric(df_filtered[birth_col], errors='coerce')

# 결측치 재확인
print(f"\n결측치 정보 (필터링 후):")
print(df_filtered.isnull().sum())

# 분석 통계
print(f"\n출생아수 통계:")
print(f"  최대값: {df_filtered[birth_col].max():,.0f}")
print(f"  최소값: {df_filtered[birth_col].min():,.0f}")
print(f"  평균값: {df_filtered[birth_col].mean():,.0f}")
print(f"  표준편차: {df_filtered[birth_col].std():,.0f}")

# 연도별 변화
max_year = df_filtered[df_filtered[birth_col].idxmax()][year_col]
max_value = df_filtered[birth_col].max()
min_year = df_filtered[df_filtered[birth_col].idxmin()][year_col]
min_value = df_filtered[birth_col].min()

print(f"\n최고값: {int(max_year)}년 {max_value:,.0f}명")
print(f"최저값: {int(min_year)}년 {min_value:,.0f}명")

# ========================
# 그래프 시각화
# ========================
print("\n" + "="*50)
print("그래프 생성 중...")
print("="*50)

plt.figure(figsize=(14, 7))

# 라인 그래프
plt.plot(df_filtered[year_col], df_filtered[birth_col], 
         linewidth=2.5, marker='o', markersize=4, 
         color='#2E86AB', label='출생아수')

# 그래프 설정
plt.title('한국 출생아수 추이 (1970-2024)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('연도', fontsize=12, fontweight='bold')
plt.ylabel('출생아수 (명)', fontsize=12, fontweight='bold')

# 격자 추가
plt.grid(True, alpha=0.3, linestyle='--')

# x축 포매팅
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}만' if x >= 10000 else f'{int(x)}'))

# 범례
plt.legend(fontsize=11, loc='best')

# 레이아웃 조정
plt.tight_layout()

# 그래프 저장
output_file = 'birth_rate_1970_2024.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ 그래프 저장 완료: {output_file}")

# 데이터 요약 저장
summary_file = 'birth_rate_analysis_summary.txt'
with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("출생아수 분석 보고서 (1970-2024)\n")
    f.write("="*50 + "\n\n")
    f.write(f"총 데이터 행 수: {len(df_filtered)}\n")
    f.write(f"연도 범위: {int(df_filtered[year_col].min())} - {int(df_filtered[year_col].max())}\n\n")
    f.write("출생아수 통계:\n")
    f.write(f"  최대값: {df_filtered[birth_col].max():,.0f}명 ({int(max_year)}년)\n")
    f.write(f"  최소값: {df_filtered[birth_col].min():,.0f}명 ({int(min_year)}년)\n")
    f.write(f"  평균값: {df_filtered[birth_col].mean():,.0f}명\n")
    f.write(f"  표준편차: {df_filtered[birth_col].std():,.0f}\n\n")
    f.write("분석 데이터 (첫 10행):\n")
    f.write(df_filtered[[year_col, birth_col]].head(10).to_string())
    f.write("\n\n분석 데이터 (마지막 10행):\n")
    f.write(df_filtered[[year_col, birth_col]].tail(10).to_string())

print(f"✓ 분석 요약 저장 완료: {summary_file}")

plt.show()
