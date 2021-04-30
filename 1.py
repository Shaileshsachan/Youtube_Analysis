import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import wordcloud

# Raed the DATA and set few Configurations
df = pd.read_csv('USvideos.csv')
PLOT_COLORS = ["#268bd2", "#0052CC", "#FF5722", "#b58900", "#003f5c"]
pd.options.display.float_format = '{:.2f}'.format
sns.set(style="ticks")
plt.rc('figure', figsize=(8, 5), dpi=100)
plt.rc('axes', labelpad=20, facecolor="#ffffff", linewidth=0.4, grid=True, labelsize=14)
plt.rc('patch', linewidth=0)
plt.rc('xtick.major', width=0.2)
plt.rc('ytick.major', width=0.2)
plt.rc('grid', color='#9E9E9E', linewidth=0.4)
plt.rc('font', family='Arial', weight='400', size=10)
plt.rc('text', color='#282828')
plt.rc('savefig', pad_inches=0.3, dpi=300)

# Handling null values in data
df["description"] = df["description"].fillna(value="")


# print(df.describe())

#        category_id        views      likes   dislikes  comment_count
# count     40949.00     40949.00   40949.00   40949.00       40949.00
# mean         19.97   2360784.64   74266.70    3711.40        8446.80
# std           7.57   7394113.76  228885.34   29029.71       37430.49
# min           1.00       549.00       0.00       0.00           0.00
# 25%          17.00    242329.00    5424.00     202.00         614.00
# 50%          24.00    681861.00   18091.00     631.00        1856.00
# 75%          25.00   1823157.00   55417.00    1938.00        5755.00
# max          43.00 225211923.00 5613827.00 1674420.00     1361580.00

# Data Visualization

def contains_capitalized_word(s):
    for w in s.split():
        if w.isupper():
            return True
        return False


# Pie Chart
df["contains_capitalized"] = df["title"].apply(contains_capitalized_word)

value_counts = df["contains_capitalized"].value_counts().to_dict()
fig, ax = plt.subplots()
_ = ax.pie([value_counts[False], value_counts[True]], labels=['No', 'Yes'],
           colors=['#003f5c', '#ffa600'], textprops={'color': '#040204'}, startangle=45)
_ = ax.axis('equal')
_ = ax.set_title('Title Contains Capitalized Word?')

# Histogram(Length of title)
df["title_length"] = df["title"].apply(lambda x: len(x))
fig_hist, ax = plt.subplots()
_ = sns.distplot(df["title_length"], kde=False, rug=False,
                 color=PLOT_COLORS[4], hist_kws={'alpha': 1}, ax=ax)
_ = ax.set(xlabel="Title Length", ylabel="No. of videos", xticks=range(0, 110, 10))

# ScatterPlot(Title length VS Views)
fig_scatter, ax = plt.subplots()
_ = ax.scatter(x=df['views'], y=df['title_length'], color=PLOT_COLORS[2], edgecolors="#000000", linewidths=0.5)
_ = ax.set(xlabel="Views", ylabel="Title Length")

# Heatmap(Views vs Likes correlation)
heatmap_labels = [x.replace('_', ' ').title() for x in list(df.select_dtypes(
    include=['number', 'bool']).columns.values)]
fig_heatmap, ax = plt.subplots(figsize=(10, 6))
_ = sns.heatmap(df.corr(), annot=True, xticklabels=heatmap_labels, yticklabels=heatmap_labels,
                cmap=sns.cubehelix_palette(as_cmap=True), ax=ax)

# WordCloud(see if some words are used meaningfully in trending video titles)
title_words = list(df["title"].apply(lambda x: x.split()))
title_words = [x for y in title_words for x in y]
wc = wordcloud.WordCloud(width=1200, height=500, collocations=False, background_color="Black",
                         colormap="tab20b").generate(" ".join(title_words))
plt.figure(figsize=(15, 10))
plt.imshow(wc, interpolation='bilinear')
_ = plt.axis("off")

plt.show()
