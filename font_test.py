import matplotlib.font_manager as fm
import os
fp = None
for f in fm.fontManager.ttflist[:20]:
    print(f.name)

# check NanumGothic in list
found = [f for f in fm.fontManager.ttflist if 'Nanum' in f.name or 'NanumGothic' in f.name]
print('Nanum found count:', len(found))
if found:
    print('Example font file:', found[0].fname)

print('Done')
