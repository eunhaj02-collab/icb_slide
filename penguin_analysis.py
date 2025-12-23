import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from io import StringIO

warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 시스템 폰트 확인 후 한글 지원 폰트 설정
import matplotlib.font_manager as fm
import os

# NotoSansCJK 폰트 설정 시도
font_paths = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
]

for font_path in font_paths:
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.family'] = 'Noto Sans CJK JP'
        break
else:
    # 폰트가 없으면 기본 설정 유지
    try:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    except:
        pass

# 펭귄 데이터셋 로드
penguins = sns.load_dataset('penguins')

# 결과를 저장할 마크다운 내용
markdown_content = StringIO()

# 제목
markdown_content.write("# 펭귄 데이터셋 분석 보고서\n\n")

# 1. 데이터셋 정보
markdown_content.write("## 1. 데이터셋 개요\n\n")
markdown_content.write(f"**데이터셋 크기**: {penguins.shape[0]} 행, {penguins.shape[1]} 열\n\n")

markdown_content.write("### 데이터 구조\n")
markdown_content.write("```\n")
markdown_content.write(penguins.head(10).to_string())
markdown_content.write("\n```\n\n")

# 2. 기본 통계
markdown_content.write("## 2. 기본 통계\n\n")
markdown_content.write("### 수치형 변수 통계\n")
markdown_content.write(penguins.describe().to_string())
markdown_content.write("\n\n")

markdown_content.write("### 범주형 변수 빈도\n")
markdown_content.write("#### 종(Species)\n")
markdown_content.write(penguins['species'].value_counts().to_string())
markdown_content.write("\n\n")

markdown_content.write("#### 섬(Island)\n")
markdown_content.write(penguins['island'].value_counts().to_string())
markdown_content.write("\n\n")

markdown_content.write("#### 성별(Sex)\n")
markdown_content.write(penguins['sex'].value_counts().to_string())
markdown_content.write("\n\n")

# 결측치 정보
markdown_content.write("### 결측치 정보\n")
markdown_content.write(penguins.isnull().sum().to_string())
markdown_content.write("\n\n")

# 3. 시각화
markdown_content.write("## 3. 데이터 시각화 (10개 이상)\n\n")

# Figure 1: 종별 펭귄 개수 (막대그래프)
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
sns.countplot(data=penguins, x='species', palette='Set2')
plt.title('Penguin Count by Species')
plt.xlabel('Species')
plt.ylabel('Count')

plt.subplot(1, 2, 2)
penguins.groupby('species').size().plot(kind='bar', color=['#66c2a5', '#fc8d62', '#8da0cb'])
plt.title('Species Distribution')
plt.xlabel('Species')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_01_species_count.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 1: 종별 펭귄 개수\n")
markdown_content.write("![Species Count](graph_01_species_count.png)\n\n")

# 막대그래프 관련 통계 - 교차표 및 피봇테이블
markdown_content.write("**종별 통계 - 교차표(Crosstab)**\n")
crosstab_species_island = pd.crosstab(penguins['species'], penguins['island'])
markdown_content.write(crosstab_species_island.to_string())
markdown_content.write("\n\n")

markdown_content.write("**종과 성별 교차표(Crosstab)**\n")
crosstab_species_sex = pd.crosstab(penguins['species'], penguins['sex'])
markdown_content.write(crosstab_species_sex.to_string())
markdown_content.write("\n\n")

markdown_content.write("**종별 신체 측정값 피봇테이블(Pivot Table)**\n")
pivot_bill_length = penguins.pivot_table(values='bill_length_mm', index='species', aggfunc=['mean', 'min', 'max'])
markdown_content.write(pivot_bill_length.to_string())
markdown_content.write("\n\n")

# Figure 2: 체질량별 펭귄 개수 (막대그래프)
plt.figure(figsize=(10, 5))
sns.countplot(data=penguins, x='species', hue='island', palette='husl')
plt.title('Penguin Count by Species and Island')
plt.xlabel('Species')
plt.ylabel('Count')
plt.legend(title='Island')
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_02_species_island.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 2: 종과 섬별 펭귄 개수\n")
markdown_content.write("![Species and Island](graph_02_species_island.png)\n\n")

# Figure 3: 부리 길이 분포 (히스토그램)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(penguins['bill_length_mm'].dropna(), bins=30, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Distribution of Bill Length')
plt.xlabel('Bill Length (mm)')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
for species in penguins['species'].unique():
    data = penguins[penguins['species'] == species]['bill_length_mm']
    plt.hist(data, bins=20, alpha=0.6, label=species)
plt.title('Bill Length Distribution by Species')
plt.xlabel('Bill Length (mm)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_03_bill_length_dist.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 3: 부리 길이 분포\n")
markdown_content.write("![Bill Length Distribution](graph_03_bill_length_dist.png)\n\n")

# Figure 4: 산점도 (부리 길이 vs 부리 깊이)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=penguins, x='bill_length_mm', y='bill_depth_mm', hue='species', s=100, palette='Set2')
plt.title('Bill Length vs Bill Depth by Species')
plt.xlabel('Bill Length (mm)')
plt.ylabel('Bill Depth (mm)')
plt.legend(title='Species')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_04_bill_scatter.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 4: 부리 길이 vs 부리 깊이 산점도\n")
markdown_content.write("![Bill Scatter](graph_04_bill_scatter.png)\n\n")

# Figure 5: 박스플롯 (종별 체질량)
plt.figure(figsize=(10, 6))
sns.boxplot(data=penguins, x='species', y='body_mass_g', palette='Set2')
plt.title('Body Mass Distribution by Species')
plt.xlabel('Species')
plt.ylabel('Body Mass (g)')
plt.grid(alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_05_body_mass_box.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 5: 종별 체질량 박스플롯\n")
markdown_content.write("![Body Mass Boxplot](graph_05_body_mass_box.png)\n\n")

# Figure 6: 바이올린 플롯
plt.figure(figsize=(12, 6))
sns.violinplot(data=penguins, x='species', y='flipper_length_mm', hue='sex', palette='Set2', split=True)
plt.title('Flipper Length by Species and Sex (Violin Plot)')
plt.xlabel('Species')
plt.ylabel('Flipper Length (mm)')
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_06_flipper_violin.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 6: 종과 성별 날개 길이 바이올린 플롯\n")
markdown_content.write("![Flipper Violin Plot](graph_06_flipper_violin.png)\n\n")

# Figure 7: 상관계수 히트맵
plt.figure(figsize=(8, 6))
numeric_cols = penguins.select_dtypes(include=[np.number]).columns
correlation_matrix = penguins[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, square=True, 
            linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Numeric Features')
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_07_correlation.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 7: 수치형 변수 상관계수 히트맵\n")
markdown_content.write("![Correlation Matrix](graph_07_correlation.png)\n\n")

# Figure 8: 부리 깊이 분포 (히스토그램)
plt.figure(figsize=(10, 6))
sns.histplot(data=penguins, x='bill_depth_mm', hue='species', kde=True, palette='Set2')
plt.title('Bill Depth Distribution by Species')
plt.xlabel('Bill Depth (mm)')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_08_bill_depth_hist.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 8: 부리 깊이 분포\n")
markdown_content.write("![Bill Depth Distribution](graph_08_bill_depth_hist.png)\n\n")

# Figure 9: 페어플롯 (Pairplot 선택 변수)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

# Bill Length vs Body Mass
axes[0].scatter(penguins['bill_length_mm'], penguins['body_mass_g'], c=pd.Categorical(penguins['species']).codes, cmap='Set2', s=50)
axes[0].set_xlabel('Bill Length (mm)')
axes[0].set_ylabel('Body Mass (g)')
axes[0].set_title('Bill Length vs Body Mass')
axes[0].grid(alpha=0.3)

# Flipper Length vs Body Mass
axes[1].scatter(penguins['flipper_length_mm'], penguins['body_mass_g'], c=pd.Categorical(penguins['species']).codes, cmap='Set2', s=50)
axes[1].set_xlabel('Flipper Length (mm)')
axes[1].set_ylabel('Body Mass (g)')
axes[1].set_title('Flipper Length vs Body Mass')
axes[1].grid(alpha=0.3)

# Island distribution
island_counts = penguins['island'].value_counts()
axes[2].bar(island_counts.index, island_counts.values, color=['#66c2a5', '#fc8d62', '#8da0cb'])
axes[2].set_title('Penguin Count by Island')
axes[2].set_ylabel('Count')
axes[2].tick_params(axis='x', rotation=45)

# Sex distribution
sex_counts = penguins['sex'].value_counts()
axes[3].bar(sex_counts.index, sex_counts.values, color=['#66c2a5', '#fc8d62'])
axes[3].set_title('Penguin Count by Sex')
axes[3].set_ylabel('Count')

plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_09_pairplot.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 9: 주요 변수 간 관계\n")
markdown_content.write("![Pairplot](graph_09_pairplot.png)\n\n")

# Figure 10: 체질량 분포 (히스토그램)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(penguins['body_mass_g'].dropna(), bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
plt.title('Distribution of Body Mass')
plt.xlabel('Body Mass (g)')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
sns.boxplot(data=penguins, x='sex', y='body_mass_g', palette='Set2')
plt.title('Body Mass by Sex')
plt.xlabel('Sex')
plt.ylabel('Body Mass (g)')
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_10_body_mass_dist.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 10: 체질량 분포\n")
markdown_content.write("![Body Mass Distribution](graph_10_body_mass_dist.png)\n\n")

# Figure 11: 리니어 플롯 (섬별 평균 체질량)
plt.figure(figsize=(10, 6))
island_mass = penguins.groupby('island')['body_mass_g'].mean()
plt.plot(island_mass.index, island_mass.values, marker='o', linewidth=2, markersize=10, color='steelblue')
plt.title('Average Body Mass by Island')
plt.xlabel('Island')
plt.ylabel('Average Body Mass (g)')
plt.grid(alpha=0.3)
for i, v in enumerate(island_mass.values):
    plt.text(i, v + 20, f'{v:.0f}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_11_island_mass_line.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 11: 섬별 평균 체질량 라인 플롯\n")
markdown_content.write("![Island Mass Line Plot](graph_11_island_mass_line.png)\n\n")

# Figure 12: 카운트 플롯 (성별)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.countplot(data=penguins, x='sex', palette='Set2')
plt.title('Penguin Count by Sex')
plt.xlabel('Sex')
plt.ylabel('Count')

plt.subplot(1, 2, 2)
sns.countplot(data=penguins, x='species', hue='sex', palette='Set1')
plt.title('Penguin Count by Species and Sex')
plt.xlabel('Species')
plt.ylabel('Count')
plt.legend(title='Sex')
plt.tight_layout()
plt.savefig('/workspaces/icb_slide/graph_12_sex_count.png', dpi=100, bbox_inches='tight')
plt.close()
markdown_content.write("### 그래프 12: 성별 펭귄 개수\n")
markdown_content.write("![Sex Count](graph_12_sex_count.png)\n\n")

# 4. 교차표 및 피봇테이블 분석
markdown_content.write("## 4. 교차표 및 피봇테이블 분석\n\n")

markdown_content.write("### 교차표 (Crosstab) 분석\n\n")

markdown_content.write("#### 섬별 성별 교차표\n")
crosstab_island_sex = pd.crosstab(penguins['island'], penguins['sex'])
markdown_content.write(crosstab_island_sex.to_string())
markdown_content.write("\n\n")

markdown_content.write("#### 섬별 성별 교차표 (비율)\n")
crosstab_island_sex_pct = pd.crosstab(penguins['island'], penguins['sex'], normalize='index') * 100
markdown_content.write(crosstab_island_sex_pct.round(2).to_string())
markdown_content.write("\n\n")

markdown_content.write("### 피봇테이블 (Pivot Table) 분석\n\n")

markdown_content.write("#### 종별 평균 신체 측정값\n")
pivot_all = penguins.pivot_table(
    values=['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'],
    index='species',
    aggfunc='mean'
)
markdown_content.write(pivot_all.round(2).to_string())
markdown_content.write("\n\n")

markdown_content.write("#### 종과 성별별 평균 부리 길이\n")
pivot_bill_species_sex = penguins.pivot_table(
    values='bill_length_mm',
    index='species',
    columns='sex',
    aggfunc='mean'
)
markdown_content.write(pivot_bill_species_sex.round(2).to_string())
markdown_content.write("\n\n")

markdown_content.write("#### 종과 성별별 평균 체질량\n")
pivot_mass_species_sex = penguins.pivot_table(
    values='body_mass_g',
    index='species',
    columns='sex',
    aggfunc='mean'
)
markdown_content.write(pivot_mass_species_sex.round(2).to_string())
markdown_content.write("\n\n")

markdown_content.write("#### 섬별 평균 날개 길이\n")
pivot_flipper_island = penguins.pivot_table(
    values='flipper_length_mm',
    index='island',
    columns='species',
    aggfunc='mean'
)
markdown_content.write(pivot_flipper_island.round(2).to_string())
markdown_content.write("\n\n")

# 5. 기타 통계
markdown_content.write("## 5. 추가 통계 분석\n\n")

markdown_content.write("### 성별 통계\n")
markdown_content.write(penguins.groupby('sex')[numeric_cols].describe().round(2).to_string())
markdown_content.write("\n\n")

markdown_content.write("### 섬별 통계\n")
markdown_content.write(penguins.groupby('island')[numeric_cols].describe().round(2).to_string())
markdown_content.write("\n\n")

# 마크다운 파일 저장
with open('/workspaces/icb_slide/penguin_analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content.getvalue())

print("분석 완료!")
print("마크다운 파일이 저장되었습니다: penguin_analysis_report.md")
print("생성된 그래프:")
print("- graph_01_species_count.png")
print("- graph_02_species_island.png")
print("- graph_03_bill_length_dist.png")
print("- graph_04_bill_scatter.png")
print("- graph_05_body_mass_box.png")
print("- graph_06_flipper_violin.png")
print("- graph_07_correlation.png")
print("- graph_08_bill_depth_hist.png")
print("- graph_09_pairplot.png")
print("- graph_10_body_mass_dist.png")
print("- graph_11_island_mass_line.png")
print("- graph_12_sex_count.png")
