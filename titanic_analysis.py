import sys
import os

def main():
    try:
        import pandas as pd
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        import seaborn as sns
        import urllib.request
    except Exception:
        print("필요한 패키지가 설치되어 있지 않습니다.")
        print("다음 명령으로 설치하세요:")
        print("    pip install pandas matplotlib seaborn")
        sys.exit(1)

    # 한글 폰트 우선순위: Windows 기본 'Malgun Gothic' 우선, 없으면 NanumGothic 자동 다운로드
    preferred_fonts = ['Malgun Gothic', 'NanumGothic']
    available = {f.name for f in fm.fontManager.ttflist}
    chosen_font = None
    for name in preferred_fonts:
        if name in available:
            chosen_font = name
            break

    font_path = None
    if chosen_font is None:
        print('한글 폰트가 시스템에 없습니다. NanumGothic을 다운로드합니다...')
        try:
            font_url = 'https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf'
            font_path = os.path.join(os.path.dirname(__file__), 'NanumGothic-Regular.ttf')
            if not os.path.exists(font_path):
                urllib.request.urlretrieve(font_url, font_path)
            fm.fontManager.addfont(font_path)
            fm._rebuild()
            chosen_font = 'NanumGothic'
            print('NanumGothic 설치 완료.')
        except Exception as e:
            print('폰트 다운로드에 실패했습니다. 한글이 깨질 수 있습니다:', e)

    # font_path: 실제 폰트 파일 경로를 찾음
    if chosen_font:
        # 이미 다운로드한 경우 font_path가 설정되어 있을 수 있음
        if font_path is None:
            for f in fm.fontManager.ttflist:
                if f.name == chosen_font:
                    font_path = f.fname
                    break
    mpl.rcParams['axes.unicode_minus'] = False

    # FontProperties 준비 및 전역 설정 적용
    fp = None
    font_name = None
    if font_path and os.path.exists(font_path):
        try:
            fp = fm.FontProperties(fname=font_path)
            font_name = fp.get_name()
            mpl.rcParams['font.family'] = 'sans-serif'
            mpl.rcParams['font.sans-serif'] = [font_name]
            mpl.rcParams['font.serif'] = [font_name]
            mpl.rcParams['font.monospace'] = [font_name]
            mpl.rcParams['axes.unicode_minus'] = False
            mpl.rcParams['axes.titlesize'] = 14
            mpl.rcParams['axes.labelsize'] = 12
            mpl.rcParams['xtick.labelsize'] = 10
            mpl.rcParams['ytick.labelsize'] = 10
            plt.rc('font', family='sans-serif')
            print('사용 폰트:', font_name, '파일:', font_path)
        except Exception as e:
            print('FontProperties 설정 실패:', e)
            fp = None
            font_name = None
    else:
        print('한글 폰트 파일을 찾을 수 없거나 경로가 올바르지 않습니다:', font_path)

    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    print(f"데이터를 로드합니다: {url}")
    df = pd.read_csv(url)

    # 성별별 생존 비율 계산 (백분율)
    survival_by_sex = df.groupby('Sex')['Survived'].mean() * 100
    survival_by_sex = survival_by_sex.sort_values(ascending=False)

    print("성별별 생존 비율 (%):")
    print(survival_by_sex.round(2))

    # 시각화
    sns.set_style('whitegrid')
    plt.figure(figsize=(6, 4))
    ax = sns.barplot(x=survival_by_sex.index, y=survival_by_sex.values, palette=['#1f77b4', '#ff7f0e'])
    ax.set_ylim(0, 100)
    if fp:
        ax.set_ylabel('생존 비율 (%)', fontproperties=fp)
        ax.set_xlabel('성별', fontproperties=fp)
        ax.set_title('타이타닉 성별 생존 비율', fontproperties=fp)
    else:
        ax.set_ylabel('생존 비율 (%)')
        ax.set_xlabel('성별')
        ax.set_title('타이타닉 성별 생존 비율')

    for p in ax.patches:
        height = p.get_height()
        if fp:
            ax.annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontproperties=fp)
        else:
            ax.annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom')

    output_file = 'titanic_survival_by_sex_fixed.png'
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"그래프를 저장했습니다: {output_file}")
    try:
        plt.show()
    except Exception:
        pass

if __name__ == '__main__':
    main()
