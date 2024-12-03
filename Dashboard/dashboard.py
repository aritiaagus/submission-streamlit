import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

# Load the dataS
data = pd.read_csv("Dashboard/all_data.csv")

# membuat filter dengan widget date serta menambahkan logo perusahaan
data['dteday'] = pd.to_datetime(data['dteday'])

# Display image in the sidebar
st.header('JH BIKE SHARING DASHBOARD')

# Sidebar for date filtering
with st.sidebar:
    # Menambahkan logo perusahaan
    st.header("JH BIKE COPORATION")
    st.image("Dashboard/BIKE.png")

     # Mengambil start_date & end_date dari date_input
    min_date = data['dteday'].min()
    max_date = data['dteday'].max()
    start_date, end_date = st.date_input(
        "Rentang Waktu:",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# data yang telah difilter ini selanjutnya akan disimpan dalam filtered_data
filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & 
                     (data['dteday'] <= pd.to_datetime(end_date))]

# Daily usage line chart
daily_data = filtered_data.groupby('dteday')['cnt'].sum().reset_index()

# Total bike usage metric
st.subheader("Overview")
total_bike_usage = filtered_data['cnt'].sum()
st.metric(label="Total Penyewaan Sepeda", value=f"{total_bike_usage:,} Sepeda")

st.subheader('Order Harian')
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_data['dteday'], daily_data['cnt'], marker='o', linestyle='-', color='b')
ax.set_xlabel("Tanggal", fontsize=14)
ax.set_ylabel("Penyewaan Sepeda", fontsize=14)
ax.grid(True)
plt.xticks(rotation=45)

st.pyplot(fig)

# Barcharts for categorical variables
st.subheader("Penyewaan Sepeda Berdasarkan Kategori")

# Fungsi create barcharts
def create_barchart(data, category, title, xlabel):
    grouped_data = data.groupby(category)['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=category, y='cnt', data=grouped_data, ax=ax, palette='viridis')
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel("Penyewaan Sepeda", fontsize=14)
    return fig

# Bar chart Musim
st.write("**Penyewaan Sepeda Berdasarkan Musim**")
season_labels = {
    1: "Winter",
    2: "Spring",
    3: "Summer",
    4: "Fall"
}
filtered_data['season_label'] = filtered_data['season'].map(season_labels)
fig_season = create_barchart(filtered_data, 'season_label', "", "Musim")
st.pyplot(fig_season)

# Bar chart Hari Kerja
st.write("**Penyewaan Sepeda Berdasarkan Hari Kerja**")
st.pyplot(create_barchart(filtered_data, 'workingday', "","Hari Kerja (0=Tidak, 1=Iya)"))

# Barplots Suhu, Kecepatan Angin, dan Kelembaban Berdasarkan Cuaca
st.subheader("Rata-rata Suhu, Kecepatan Angin, dan Kelembaban Berdasarkan Cuaca")

# Memberi label Cuaca
weathersit_labels = {
    1: "Clear",
    2: "Mist",
    3: "Light Rain",
    4: "Heavy Rain"
}
filtered_data['weathersit_label'] = filtered_data['weathersit'].map(weathersit_labels)

# Group data berdasarkan cuaca
avg_weather_data = filtered_data.groupby('weathersit_label')[['temp', 'windspeed', 'hum']].mean().reset_index()

# Membuat 3 kolom bar charts
col1, col2, col3 = st.columns(3)

# Bar chart Suhu
with col1:
    st.write("**Rata-rata Suhu**")
    fig_temp, ax_temp = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x='weathersit_label',
        y='temp',
        data=avg_weather_data,
        palette='viridis',
        ax=ax_temp
    )
    ax_temp.set_xlabel("Cuaca")
    ax_temp.set_ylabel("Rata-rata Suhu")
    plt.xticks(rotation=45)
    st.pyplot(fig_temp)

# Bar chart Kecepatan Angin
with col2:
    st.write("**Rata-rata Kecepatan Angin**")
    fig_windspeed, ax_windspeed = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x='weathersit_label',
        y='windspeed',
        data=avg_weather_data,
        palette='viridis',
        ax=ax_windspeed
    )
    ax_windspeed.set_xlabel("Cuaca")
    ax_windspeed.set_ylabel("Rata-rata Kecepatan Angin")
    plt.xticks(rotation=45)
    st.pyplot(fig_windspeed)

# Bar chart Kelembaban
with col3:
    st.write("**Rata-rata Kelembaban**")
    fig_hum, ax_hum = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x='weathersit_label',
        y='hum',
        data=avg_weather_data,
        palette='viridis',
        ax=ax_hum
    )
    ax_hum.set_xlabel("Cuaca")
    ax_hum.set_ylabel("Rata-rata Kelembaban")
    plt.xticks(rotation=45)
    st.pyplot(fig_hum)

# Bar chart Jam
st.subheader("Popular Time Penyewaan Sepeda")
st.pyplot(create_barchart(filtered_data, 'hr', "", "Hour"))

#Menambahkan kesimpulan
with st.expander("SEE CONCLUSION"):
    st.write(
        """
        1. **Bagaimana jumlah penyewaan sepeda sepanjang waktu?**

Jumlah rata-rata penyewaan sepeda pada data *day_df* adalah **4504**, serta pada data *hour_df* adalah **189**. Terlihat dari grafik linechart jumlah penyewaan sepeda menurun pada akhir tahun dimana saat itu sedang musim winter, kemudian tren kembali naik dimusim selanjutnya. Berdasarkan grafik barchart jumlah terbanyak penyewaan sepeda sepanjang waktu terdapat pada musim summer dengan keadaan cuaca clear serta dihari kerja pagi di waktu hari dan sore hari. **Rekomendasi** yang dapat diberikan kepada pengembang bisnis adalah merencanakan operasional dimana stok sepeda ditambah setelah musim dingin dan dapat melakukan perawatan sepeda serta melakukan promosi pada musim dingin saat penyewaan mulai menurun.

2. **Kondisi cuaca seperti apa yang paling mempengaruhi jumlah peminjaman?**

Terlihat dari barchart banyak sedikitnya penyewaan ternyata sangat bergantung kepada kondisi cuaca. Berdasarkan explor data yang telah dilakukan diperoleh cuaca yang paling banyak mendapatkan penyewaan adalah **clear** dengan banyak penyewaan untuk data *day_df* sebanyak 451 dengan suhu max ternormalisasi mencapai 0.86, serta untuk data *hour_df* sebanyak sebanyak 848 dengan suhu max ternormalisasi mencapai 1.00. Sedangkan cuaca yang memiliki penyewaan ***paling sedikit*** adalah **Light Rain**	sebanyak 21 untuk data *day_df*, serta **Heavy Rain**	sebanyak 3 untuk data *hour_df*. Sehingga dapat disimpulkan cuaca yang buruk seperti light rain bahkan heavy rain sangat berdampak kepada penyewaan sepeda. **Rekomendasi** yang dapat diberikan kepada pengembang bisnis adalah meninjau ulang layanan agar lebih fleksibel agar orang dapat dengan mudah mengakses tempat selama cuaca buruk, serta dilakukan promosi keunggulan sepeda dengan melengkapi fasilitas seperti diberikan pakaian pelindung agar penyewa tidak kebasahan menggunakan sepeda saat cuaca buruk.
"""
    )

#Menambahkan caption copyright
st.caption('Copyright (c) Jh 2024')
