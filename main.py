#importing libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import base64
import matplotlib.pyplot as plt
#page setup
st.set_page_config(page_title ="Stock Price App ₹",page_icon="💵",layout="centered")
st.logo("images/page_logo.png")

st.title('S&P 500 App 💵')
st.markdown("""
 -> This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* -> **Python libraries:** base64, pandas, streamlit, matplotlib, yfinance
* -> **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')
@st.cache_data(ttl=86400)
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    dataframe = pd.read_html(url,header=0)
    df = dataframe[0]
    return df


df = load_data()
# sector = df.groupby("GICS SECTOR")

sorted_sector_unique = sorted(df["GICS Sector"].unique())
selected_sector = st.sidebar.multiselect('Sector',sorted_sector_unique,default=sorted_sector_unique[0])
df_selected_sector = df[(df["GICS Sector"].isin(selected_sector))]

st.header(" **Display Companies in Selected Sector** ")
st.write("Data DImension: "+str(df_selected_sector.shape[0])+ " rows & "+str(df_selected_sector.shape[1])+" columns.")
st.dataframe(df_selected_sector)

#download csv option
def file_download(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href
st.markdown(file_download(df_selected_sector),unsafe_allow_html=True)

#yfinance Section

data = yf.download(
    tickers=list(df_selected_sector[:10].Symbol),
    period="ytd",
    interval="1d",
    group_by="ticker",
    auto_adjust=True,
    prepost=True,
    threads=True,
    # proxy=True
)

def price_plot(symbol):
    if symbol in data:
        df = pd.DataFrame(data[symbol].Close)
        df['Date'] = df.index

        # Create a specific figure object
        fig, ax = plt.subplots()
        ax.fill_between(df.Date, df.Close, color='cyan', alpha=0.3)
        ax.plot(df.Date, df.Close, color="cyan", alpha=0.8)
        ax.set_xticklabels(df.Date, rotation=90)
        ax.set_title(symbol, fontweight='bold')
        ax.set_xlabel("Date", fontweight="bold")
        ax.set_ylabel("Closing Price", fontweight='bold')

        # Pass the figure to Streamlit
        st.pyplot(fig)
    else:
        st.warning(f"Data for {symbol} is not available.")


num_company = st.sidebar.slider("No. of Companies",1,10)
if st.button("Plot"):
    st.header("Stock Closing Price")
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
        
        
hide_st_style = '''
<style>
#mainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}
</style>
'''

st.markdown(hide_st_style,unsafe_allow_html = True)