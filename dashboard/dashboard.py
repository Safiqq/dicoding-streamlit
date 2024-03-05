import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import streamlit as st

# Get the current working directory
current_dir = os.path.dirname(__file__)

st.subheader('Your Analyst')
st.write('Nama: Syafiq Ziyadul Arifin')
st.write('Email: szarifin20041@gmail.com')
st.write('ID Dicoding: safiq53')

# Load data from CSV
day_df = pd.read_csv('data/day.csv')

# Select numeric columns from the DataFrame
day_numeric_columns = day_df.select_dtypes(include=np.number).columns
day_numeric_df = day_df[day_numeric_columns]

# Dictionary to store outliers for each numeric column
day_outliers_dict = {}

# Iterate over each numeric column to identify outliers
for column in day_numeric_columns:
    # Calculate the first and third quartiles
    q25, q75 = np.percentile(day_df[column], 25), np.percentile(day_df[column], 75)

    # Calculate the interquartile range (IQR)
    iqr = q75 - q25

    # Define the cutoff values for outliers
    cut_off = iqr * 1.5
    day_minimum, day_maximum = q25 - cut_off, q75 + cut_off

    # Identify outliers for the current column
    day_outliers = day_df[(day_df[column] < day_minimum) | (day_df[column] > day_maximum)][column]

    # Store outliers in the dictionary
    day_outliers_dict[column] = day_outliers

# Print the identified outliers for each column
for column, outliers_series in day_outliers_dict.items():
    if not outliers_series.empty:
        print(outliers_series)
        print("\n")

# Create a copy of the original DataFrame for filtering outliers
day_df_filtered = day_df.copy()

# Iterate over each column and its corresponding outliers
for column, outliers_series in day_outliers_dict.items():
    # Check if the column has outliers
    if not outliers_series.empty:
        # Get the indices of the outliers
        outliers_index = outliers_series.index

        # Identify duplicated indices among outliers
        duplicates_mask = outliers_index.duplicated(keep='first')

        # Retain only the unique indices (keep the first occurrence)
        unique_outliers_index = outliers_index[~duplicates_mask]

        # Drop rows with unique outlier indices from the filtered DataFrame
        day_df_filtered = day_df_filtered.drop(index=unique_outliers_index, errors='ignore')

# The resulting day_df_filtered will have outliers removed based on the specified logic

# Grafik 1
def plot_weather_graph():
    custom_palette = sns.color_palette("pastel", n_colors=3)
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))  # Create a Matplotlib figure explicitly

    sns.barplot(x='weathersit', y='cnt', data=day_df_filtered, estimator=sum, errorbar=None, palette=custom_palette, dodge=False, hue='weathersit', ax=ax)

    plt.title('Jumlah Penyewaan Sepeda berdasarkan Kondisi Cuaca', fontsize=16)
    plt.xlabel('Kondisi Cuaca', fontsize=14)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='baseline', fontsize=12, color='black')

    st.pyplot(fig)  # Pass the figure explicitly to st.pyplot()

    st.subheader("Conclusion")
    st.write("Berdasarkan perbandingan tinggi rendahnya bar-bar pada grafik, dapat disimpulkan bahwa jumlah penyewaan sepeda mencapai puncak tertingginya ketika kondisi cuaca adalah Clear, Few clouds, atau Partly cloudy. Sebaliknya, jumlah penyewaan sepeda mencapai titik terendah, dengan nilai 0, saat kondisi cuaca adalah Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog.")
    st.write("Hal ini menunjukkan bahwa kondisi cuaca yang bersih, cerah, dan sebagian berawan lebih mendukung aktivitas bersepeda, sedangkan kondisi cuaca yang buruk seperti hujan deras, petir, kabut, salju, dan kabut dapat menghambat atau bahkan mencegah orang untuk menyewa sepeda.")
    st.write("Dengan demikian, pemilik atau operator penyewaan sepeda dapat menggunakan informasi ini untuk mengoptimalkan layanan mereka, seperti meningkatkan promosi atau ketersediaan sepeda selama cuaca cerah dan mengurangi ekspektasi selama kondisi cuaca buruk.")

# Grafik 2
def plot_seasonal_analysis():
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))

    seasonal_analysis = day_df_filtered.groupby('season')[['casual', 'registered', 'cnt']].mean()

    sns.barplot(x=seasonal_analysis.index, y=seasonal_analysis['casual'], color='skyblue', ax=axes[0, 0])
    axes[0, 0].set_title('Jumlah Casual Users per Musim')
    axes[0, 0].set_xlabel('Musim')
    axes[0, 0].set_ylabel('Jumlah Casual Users')
    axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)

    sns.barplot(x=seasonal_analysis.index, y=seasonal_analysis['registered'], color='lightgreen', ax=axes[0, 1])
    axes[0, 1].set_title('Jumlah Registered Users per Musim')
    axes[0, 1].set_xlabel('Musim')
    axes[0, 1].set_ylabel('Jumlah Registered Users')
    axes[0, 1].grid(axis='y', linestyle='--', alpha=0.7)

    sns.barplot(x=seasonal_analysis.index, y=seasonal_analysis['cnt'], color='salmon', ax=axes[1, 0])
    axes[1, 0].set_title('Jumlah Total Users per Musim')
    axes[1, 0].set_xlabel('Musim')
    axes[1, 0].set_ylabel('Jumlah Total Users')
    axes[1, 0].grid(axis='y', linestyle='--', alpha=0.7)

    # Hide the last subplot (bottom-right)
    axes[1, 1].axis('off')

    plt.tight_layout()

    st.pyplot(fig)

    st.subheader("Conclusion")
    st.write("Berdasarkan grafik, dapat disimpulkan bahwa jumlah perental sepeda mencapai puncak tertinggi pada musim Fall, diikuti oleh musim Summer, Winter, dan Spring. Hal ini mungkin disebabkan oleh suhu rata-rata yang cukup nyaman pada musim gugur. Suhu yang tidak terlalu panas seperti musim panas atau terlalu dingin seperti musim dingin membuat kondisi cuaca menjadi lebih menyenangkan untuk bersepeda.")
    st.write("Pada musim gugur, banyak orang mungkin lebih tertarik untuk melakukan aktivitas di luar ruangan, termasuk bersepeda, karena suhu yang lebih sejuk dan cuaca yang stabil. Sebaliknya, musim panas, meskipun memiliki jumlah perental sepeda yang tinggi, mungkin memiliki suhu yang lebih tinggi dan potensi kelembapan yang dapat mempengaruhi tingkat kenyamanan bersepeda.")
    st.write("Kondisi cuaca yang menyenangkan pada musim gugur menjadi faktor utama yang mendorong banyak orang untuk menyewa sepeda, dan pemahaman ini dapat membantu penyedia layanan sepeda untuk mengoptimalkan strategi pemasaran dan penyediaan sepeda selama musim-musim tertentu.")

# Streamlit App
def main():
    st.title('Bike Rental Data Visualization')

    st.header('Grafik 1: Jumlah Penyewaan Sepeda berdasarkan Kondisi Cuaca')
    plot_weather_graph()

    st.header('Grafik 2: Analisis Musiman untuk Casual, Registered, dan Total Users')
    plot_seasonal_analysis()

if __name__ == '__main__':
    main()
