import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Load data from CSV
day_df_filtered = pd.read_csv('data/day_fil.csv')
hour_df_filtered = pd.read_csv('data/hour_fil.csv')

# Grafik 1
def plot1():
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='weathersit', y='cnt', data=day_df_filtered, estimator=sum, errorbar=None, color='lightgray')
    sns.barplot(x='weathersit', y='cnt', data={'weathersit': [4], 'cnt': [0]}, estimator=sum, ax=ax)
    plt.title('Jumlah Penyewaan Sepeda berdasarkan Kondisi Cuaca', fontsize=16)
    plt.xlabel('Kondisi Cuaca', fontsize=14)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='baseline', fontsize=12, color='black')
    plt.xticks(ticks=[0, 1, 2, 3], labels=['Cerah', 'Berawan', 'Hujan/Salju Ringan', 'Hujan/Salju Berat'])
    max_value = max([p.get_height() for p in ax.patches])
    for p in ax.patches:
        if p.get_height() == max_value:
            p.set_facecolor('green')
    st.pyplot(plt)

    st.markdown(
"""Berdasarkan grafik "Jumlah Penyewaan Sepeda berdasarkan Kondisi Cuaca", didapatkan hasil sebagai berikut.
  * **Cerah**: Penyewaan sepeda paling banyak terjadi saat cuaca cerah, dengan total sebanyak 1.949.429 penyewaan. Ini menunjukkan bahwa cuaca cerah sangat mendukung aktivitas bersepeda.
  * **Berawan**: Saat cuaca berawan, jumlah penyewaan sepeda menurun menjadi 893.856. Meskipun lebih rendah dibandingkan cuaca cerah, angka ini masih menunjukkan bahwa cukup banyak orang yang memilih untuk bersepeda meskipun cuaca tidak sepenuhnya cerah.
  * **Hujan/Salju Ringan**: Saat cuaca berubah menjadi hujan atau salju ringan, jumlah penyewaan sepeda turun drastis menjadi 37,246. Ini menunjukkan bahwa cuaca buruk dapat mengurangi minat orang untuk bersepeda.
  * **Hujan/Salju Berat**: Saat hujan atau salju berat, tidak ada penyewaan sepeda yang tercatat sama sekali. Ini menunjukkan bahwa cuaca ekstrem seperti ini dapat menghentikan aktivitas bersepeda sepenuhnya.

  Dengan demikian, dapat disimpulkan bahwa cuaca memiliki pengaruh yang signifikan terhadap persebaran jumlah penyewa sepeda. Cuaca cerah mendukung aktivitas bersepeda, sementara cuaca buruk dapat mengurangi atau bahkan menghentikan aktivitas tersebut.""")
    

# Grafik 2
def plot2():
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 10))
    seasonal_analysis = day_df_filtered.groupby('season')[['casual', 'registered', 'cnt']].sum()
    plt.subplot(2, 2, 1)
    casual_plot = sns.barplot(x=seasonal_analysis.index, y=seasonal_analysis['casual'], color='lightgray')
    plt.title('Jumlah Penyewaan Sepeda oleh Pengguna Kasual per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Penyewa Kasual')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for p in casual_plot.patches:
        if p.get_height() == seasonal_analysis['casual'].max():
            p.set_facecolor('skyblue')
        casual_plot.annotate(f'{p.get_height():.0f}', 
                            (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha = 'center', va = 'center', 
                            xytext = (0, 9), 
                            textcoords = 'offset points')
    plt.xticks(ticks=[0, 1, 2, 3], labels=['Semi', 'Panas', 'Gugur', 'Salju'])
    plt.subplot(2, 2, 2)
    registered_plot = sns.barplot(x=seasonal_analysis.index, y=seasonal_analysis['registered'], color='lightgray')
    plt.title('Jumlah Penyewaan Sepeda oleh Pengguna Terdaftar per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Penyewa Terdaftar')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for p in registered_plot.patches:
        if p.get_height() == seasonal_analysis['registered'].max():
            p.set_facecolor('lightgreen')
        registered_plot.annotate(f'{p.get_height():.0f}', 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                ha = 'center', va = 'center', 
                                xytext = (0, 9), 
                                textcoords = 'offset points')
    plt.xticks(ticks=[0, 1, 2, 3], labels=['Semi', 'Panas', 'Gugur', 'Salju'])
    plt.subplot(2, 2, 3)
    cnt_plot = sns.barplot(x=seasonal_analysis.index, y=seasonal_analysis['cnt'], color='lightgray')
    plt.title('Jumlah Penyewaan Sepeda secara Keseluruhan per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Total Penyewa')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for p in cnt_plot.patches:
        if p.get_height() == seasonal_analysis['cnt'].max():
            p.set_facecolor('salmon')
        cnt_plot.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points')
    plt.xticks(ticks=[0, 1, 2, 3], labels=['Semi', 'Panas', 'Gugur', 'Salju'])
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown(
"""Berdasarkan analisis data penyewaan sepeda, kita dapat menyimpulkan pengaruh musim terhadap jumlah penyewa sepeda sebagai berikut:
  * **Pengguna Kasual**: Pada musim gugur, jumlah penyewaan kasual mencapai puncaknya. Musim panas dan salju juga menunjukkan jumlah penyewaan yang tinggi, sedangkan musim semi memiliki jumlah penyewaan kasual yang lebih rendah.
  * **Pengguna Terdaftar**: Pada musim gugur, jumlah penyewaan terdaftar tertinggi terjadi, dan kemudian diikuti oleh musim salju dan panas. Sedangkan musim semi memiliki jumlah penyewaan terdaftar yang lebih rendah.
  * **Total Keduanya**: Secara keseluruhan, jumlah penyewaan sepeda paling tinggi terjadi pada musim gugur, kemudian diikuti oleh musim salju dan panas, baru kemudian musim semi. Ini sama seperti data pada **Pengguna Terdaftar**.

  Jadi, musim mempengaruhi pola penyewaan sepeda, dengan musim gugur menjadi puncak aktivitas penyewaan.""")

@st.cache_data
def denormalize_temp(df):
    df['temp'] *= 41
    return df

# Grafik 3
def plot3():
    plt.figure(figsize=(12, 8))
    hour_df_filtered_copy = hour_df_filtered.copy()
    # hour_df_filtered_copy = denormalize_temp(hour_df_filtered_copy)
    columns_to_load = ['cnt', 'temp']
    k = 3
    centroids = hour_df_filtered_copy[columns_to_load].sample(n=k, random_state=42).values
    for _ in range(10):
        distances = np.vstack([np.linalg.norm(hour_df_filtered_copy[columns_to_load].values - centroid, axis=1) for centroid in centroids])
        labels = np.argmin(distances, axis=0)
        centroids = np.array([hour_df_filtered_copy[columns_to_load][labels == i].mean(axis=0) for i in range(k)])
    hour_df_filtered_copy['cluster'] = labels
    for cluster in range(k):
        cluster_data = hour_df_filtered_copy[hour_df_filtered_copy['cluster'] == cluster]
        plt.scatter(cluster_data['cnt'], cluster_data['temp'], label=f'Cluster {cluster}')
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red', s=200, label='Centroids')
    plt.xlabel('Jumlah Penyewa Sepeda')
    plt.ylabel('Temperatur (°C)')
    plt.title('K-Means Clustering')
    plt.legend()
    st.pyplot(plt)

    st.markdown(
"""Berdasarkan grafik "K-Means Clustering", kita dapat menyimpulkan bahwa terdapat hubungan positif antara temperatur dan jumlah penyewa sepeda. Ketika temperatur meningkat, jumlah penyewa sepeda juga cenderung meningkat. Grafik ini memperlihatkan tiga kluster data yang menunjukkan pola penyewaan pada suhu yang berbeda:
  * **Kluster 1** (Oranye): Menunjukkan jumlah penyewaan sepeda yang lebih rendah pada temperatur lebih rendah.
  * **Kluster 2** (Hijau): Menunjukkan jumlah penyewaan sepeda sedang pada temperatur sedang.
  * **Kluster 0** (Biru): Menunjukkan peningkatan signifikan dalam jumlah penyewaan sepeda pada temperatur lebih tinggi.

  Secara umum, ketika suhu naik, aktivitas penyewaan sepeda juga meningkat.""")

if __name__ == '__main__':
    st.title('Bike Rental Data Visualization')
    st.write('Nama: Syafiq Ziyadul Arifin')
    st.write('Email: szarifin20041@gmail.com')
    st.write('ID Dicoding: safiq53')

    tab1, tab2, tab3 = st.tabs(["Grafik 1", "Grafik 2", "Grafik 3"])

    with tab1:
        st.subheader('Grafik 1: Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
        plot1()

    with tab2:
        st.subheader('Grafik 2: Analisis Musiman untuk Pengguna Kasual, Terdaftar, dan Total Keduanya')
        plot2()

    with tab3:
        st.subheader('Grafik 3: Jumlah Penyewaan Sepeda Berdasarkan Temperatur')
        plot3()

    st.caption('Copyright © 2024')
