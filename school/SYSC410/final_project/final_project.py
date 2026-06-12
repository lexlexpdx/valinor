# %% [markdown]
# Lex Albrandt  
# SYSC410  
# Final Project  

# %%
# Imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# %%
# Load data
file_path = "/home/lexlexpdx/Desktop/valinor/school/SYSC410/final_project/database.csv"
earthquakes_df = pd.read_csv(file_path)

# Check data for cleaning
print(earthquakes_df.info())

# Check columns with null values
print(earthquakes_df.head(20))

# %%
# Drop columns with large amounts of null values
# Also drop RMS column, not useful in this context
drop_columns = [
    "Depth Error",
    "Depth Seismic Stations",
    "Magnitude Error",
    "Magnitude Seismic Stations",
    "Azimuthal Gap",
    "Horizontal Distance",
    "Horizontal Error",
    "Root Mean Square",
    "ID"
]

earthquakes_df_cleaned = earthquakes_df.copy()
earthquakes_df_cleaned = earthquakes_df.drop(columns=drop_columns)
earthquakes_df_cleaned.info()

# %%
# Fill null values
earthquakes_df_cleaned["Magnitude Type"] = (earthquakes_df_cleaned["Magnitude Type"]
                                            .fillna("Unknown"))
earthquakes_df_cleaned.info()
earthquakes_df_cleaned.head()

# %%
# Convert date column to a datetime type
# This also coerces any values that don't match the format into NaT (null)
earthquakes_df_cleaned["Date"] = pd.to_datetime(
    earthquakes_df_cleaned["Date"],
    format="%m/%d/%Y",
    errors="coerce"
)
earthquakes_df_cleaned.info()

# %%
# 3 Rows have invalid dates, we will remove those
earthquakes_df_cleaned.dropna(subset=["Date"], inplace=True)
earthquakes_df_cleaned.info()

# %%
# Convert time column to datetime type
earthquakes_df_cleaned["Time"] = pd.to_datetime(
    earthquakes_df_cleaned["Time"],
    format="%H:%M:%S",
    errors="coerce"
)
earthquakes_df_cleaned.info()


# %%
# EDA

# histogram of all numeric columns

num_cols = ["Latitude",
            "Longitude",
            "Depth",
            "Magnitude"]
numeric_earthquake_df = earthquakes_df_cleaned[num_cols]
numeric_earthquake_df.hist(
   column=num_cols,
   bins=30,
)
dist_figtext = (
    "Figure 1: This figure gives a high-level view of distributions "
    "in the numeric columns of the earthquake dataset. Note the Depth and "
    "Magnitude columns are both skewed heavily to the right."
)
plt.figtext(0.5, 
            -0.05, 
            dist_figtext, 
            ha="center",
            wrap=True,
            fontsize=9)
plt.suptitle("Numeric Column Distributions")
plt.tight_layout()
plt.savefig("./figures/num_hist.png", bbox_inches="tight")
plt.show()



# %%
fig, ax = plt.subplots(figsize=(14, 10))

map = Basemap(
    projection="merc",
    llcrnrlat=-80,
    urcrnrlat=80,
    llcrnrlon=-180,
    urcrnrlon=180,
    lat_ts=20,
    resolution="c"
)
map.bluemarble(scale=0.2)
x, y = map(earthquakes_df_cleaned["Longitude"], earthquakes_df_cleaned["Latitude"])
map.scatter(x, y, 3, marker="o", color="purple")

parallels = map.drawparallels(
    np.arange(-60, 81, 20),
    labels=[1, 0, 0, 0],
    fontsize=10,
    color="white"
)
map.drawmeridians(
    np.arange(-180, 181, 30),
    labels=[0, 0, 0, 1],
    fontsize=10,
    color="white"
)

for _, (_, texts) in parallels.items():
    for text in texts:
        text.set_rotation(45)

ax.set_xlabel("Longitude", fontsize=14, labelpad=20)
ax.set_ylabel("Latitude", fontsize=14, labelpad=40)
ax.set_title("Global Earthquake Locations", fontsize=20, pad=20)
map_figtext = (
    "Figure 2: this figure is a scatter plot of all earthquakes "
    "from 1965-2016 with their latitude and longitude coordinates."
)
plt.figtext(0.5, 
            -0.02, 
            map_figtext, 
            wrap=True,
            ha="center")
plt.tight_layout()
plt.savefig("./figures/world_map", bbox_inches="tight")
plt.show()


# %%
plt.figure(figsize=(8, 9))

sns.scatterplot(
    earthquakes_df_cleaned,
    x="Depth",
    y="Magnitude",
    hue="Magnitude",
    palette="rocket_r"
)
plt.axhline(y=8, color="blue", linestyle="--")
plt.title("Earthquake Magnitude vs Depth")
plt.xlabel("Depth (km)")
plt.ylabel("Magnitude")

depth_scat_text = (
    "Figure 3: This scatterplot depicts all earthquakes in the "
    "dataset and their related depths. A blue, horizontal, dashed line indicates "
    "earthquakes with a magnitude of 8.0 or greater."
)
plt.figtext(0.5,
            -0.02,
            depth_scat_text,
            ha="center",
            wrap=True)

plt.tight_layout()
plt.savefig("./figures/depth_scat.png", bbox_inches="tight")
plt.show()

# %%
earthquakes_df_cleaned["Magnitude Category"] = pd.cut(
    earthquakes_df_cleaned["Magnitude"],
    bins=[5.5, 6, 6.9, 7.9, 10],
    labels=["5.5-6", "6.1-6.9", "7-7.9", "8+"],
    include_lowest=True
)

large_quakes_mask = earthquakes_df_cleaned["Magnitude Category"] == "8+"
large_quakes_df = earthquakes_df_cleaned[large_quakes_mask]
large_quakes_df

# %%

plt.figure(figsize=(6, 4))
sns.boxplot(
    data=large_quakes_df,
    x="Depth"
)
x_ticks = np.arange(0, 700, 200)
plt.xticks(x_ticks)
plt.title("Depth Distribution for 8+ Magnitude Earthquakes")
plt.xlabel("Depth (km)")
boxplot_figtext = (
    "Figure 4: This boxplot shows the distribution for earthquakes and their "
    "corresponding depths. Note that this is very strongly skewed toward shallower "
    "depths, with only a few of the stronges earthquakes occuring at greater depths."
)
plt.figtext(0.5, -0.1, boxplot_figtext, wrap=True, ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("./figures/depth_box.png", bbox_inches="tight")
plt.show()


# %%
count_per_year_df = (
    earthquakes_df_cleaned
    .groupby(
        [earthquakes_df_cleaned["Date"].dt.year,
        "Magnitude Category"]
    )
    .size()
    .reset_index(name="count")
)
count_per_year_df.columns = ["Year", "Magnitude Category", "Count"]

mags_5_6_mask = count_per_year_df["Magnitude Category"].isin(["5.5-6", "6.1-6.9"])
mags_5_6_df = count_per_year_df[mags_5_6_mask]

mag_mask = count_per_year_df["Magnitude Category"].isin(["7-7.9", "8+"])
extreme_earthquakes_per_year_df = count_per_year_df[mag_mask]

fig, (ax1, ax2) = plt.subplots(
    nrows=2,
    ncols=1,
    figsize=(14, 14)
)

# Plot 1
sns.lineplot(
    mags_5_6_df,
    x="Year",
    y="Count",
    hue="Magnitude Category",
    ax=ax1
)
year_ticks = np.arange(1965, 2017, 2)
ax1.set_xticks(year_ticks)
ax1.tick_params(axis="x", rotation=45)
ax1.set_title("Moderate to Strong Earthquakes per Year", fontsize=16)
ax1.set_ylabel("Count", fontsize=12, labelpad=10)
ax1.set_xlabel("Year", fontsize=12, labelpad=10)

handles, labels = ax1.get_legend_handles_labels()
ax1.legend_.remove()

# Plot 2
sns.lineplot(
    extreme_earthquakes_per_year_df,
    x="Year",
    y="Count",
    hue="Magnitude Category",
    ax=ax2
)

ax2.set_xticks(year_ticks)
ax2.tick_params(axis="x", rotation=45)
ax2.set_title("Major Earthquakes per Year", fontsize=16)
ax2.set_ylabel("Count", fontsize=12, labelpad=10)
ax2.set_xlabel("Year", fontsize=12, labelpad=10)
ax2.legend_.remove()

fig.legend(
    handles,
    labels,
    title="Magnitude Category",
    loc="upper center",
    ncol=len(labels),
    bbox_to_anchor=(0.5, 0.95)
)
plt.subplots_adjust(hspace=0.3)
plt.savefig("./figures/count_by_year.png", bbox_inches="tight")
plt.show()


# %%
# Import ML stuffs
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# %%
target = "Magnitude Category"

feature_cols = [
    "Latitude", "Longitude", "Depth",
    "Type", "Magnitude Type", "Source",
    "Location Source", "Magnitude Source", "Status"
]

ml_df = earthquakes_df_cleaned.copy()

ml_df["Year"] = ml_df["Date"].dt.year
ml_df["Month"] = ml_df["Date"].dt.month
ml_df["Hour"] = ml_df["Time"].dt.hour

feature_cols += ["Year", "Month", "Hour"]

X_feat = ml_df[feature_cols]
y_tar = ml_df[target]

numeric_cols = [
    "Latitude", "Longitude", "Depth",
    "Year", "Month", "Hour"]

categorical_cols = [
    "Type", "Magnitude Type", "Source",
    "Location Source", "Magnitude Source", "Status"
]

preprocess = ColumnTransformer(
    transformers=[
        ("num", SimpleImputer(strategy="median"), numeric_cols),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical_cols)
    ]
)

model = Pipeline([
    ("preprocess", preprocess),
    ("clf", RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    ))
])

X_feat_train, X_feat_test, y_tar_train, y_tar_test = train_test_split(
    X_feat, 
    y_tar,
    test_size=0.2,
    random_state=42,
    stratify=y_tar
)

model.fit(X_feat_train, y_tar_train)
preds = model.predict(X_feat_test)

# %%
report_dict = classification_report(y_tar_test, preds, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose().round(3)
fig, ax = plt.subplots(figsize=(8, 3))
ax.axis("off")

table = ax.table(
    cellText=report_df.values,
    colLabels=report_df.columns,
    rowLabels=report_df.index,
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.3, 1.5)
plt.title("Classification Report", pad=12)
plt.savefig("./figures/classification_report.png", bbox_inches="tight")

# %%
conf_mat = confusion_matrix(y_tar_test, preds)
disp = ConfusionMatrixDisplay(
    confusion_matrix=conf_mat,
    display_labels=model.classes_
)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix for Random Forest Classifier")
plt.tight_layout()
plt.savefig("./figures/confustion_matrix.png", bbox_inches="tight")
plt.show()
# %%
