import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

print("=" * 80)
print("시스템 가용 한글 폰트 확인")
print("=" * 80)

# 모든 설치된 폰트 확인
fonts = fm.findSystemFonts()
print(f"\n총 설치된 폰트 수: {len(fonts)}\n")

# 한글 폰트 찾기
korean_fonts = []
for font_path in fonts:
    try:
        font_name = fm.FontProperties(fname=font_path).get_name()
        if font_name and any(char in font_name for char in ['Gothic', 'Song', 'Serif', '고', '굴', '명']):
            korean_fonts.append((font_name, font_path))
            print(f"✓ {font_name}")
            print(f"  경로: {font_path}\n")
    except:
        pass

if not korean_fonts:
    print("\n⚠️ 한글 폰트가 감지되지 않았습니다.")
    print("\n시스템에 설치된 모든 폰트:")
    font_names = set()
    for font_path in fonts[:50]:  # 처음 50개만 표시
        try:
            font_name = fm.FontProperties(fname=font_path).get_name()
            if font_name and font_name not in font_names:
                font_names.add(font_name)
                print(f"  - {font_name}")
        except:
            pass

print("\n" + "=" * 80)
print("현재 matplotlib 기본 폰트")
print("=" * 80)
print(f"현재 설정: {plt.rcParams['font.family']}")
