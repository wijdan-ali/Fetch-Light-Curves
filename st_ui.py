import streamlit as st
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



st.title("Fetch Light Curves 1.0")
st.markdown(f"""
    <p>Made By <a href = "https://www.linkedin.com/in/wijdan-ali-374793288/" style = "font-weight:bold; text-decoration:none;">Wijdan Ali</a></p>
""", unsafe_allow_html=True)
st.divider()

years = []
target = st.text_input("Enter TIC ID:")
target = "TIC " + target.strip()

search_result = lk.search_lightcurve(target)
if len(target) < 5:
    st.write("Please enter a valid TIC ID of at least 5 digits")
else:
    st.write(f"Number Of Light Curves Found For This Star: {len(search_result)}")


for i in range(len(search_result)):
    this_year = int(search_result[i].year.item())
    this_line = str(i+1) + ". " + str(this_year) 
    years.append(this_line)

print(years)

option = st.selectbox(
    "Select Light Curve",
    years,
    index=None,
    placeholder="Select light curve",
    accept_new_options=True,
)
try:
    selected_index = int(option.split(".")[0]) - 1
    selected_no = int(option.split(".")[0])
    selected_year = int(option.split(".")[1].strip())
except:
    selected_index = None
    selected_no = None
    selected_year = None
st.write(f"You selected: {option}")

try:
    lc = search_result[selected_index].download(download_dir=None)
    lc = lc[lc.quality == 0] 
    lc = lc.remove_nans()
    lc = lc.remove_outliers(sigma = 5)
    lc = lc.normalize()
    lc = lc.flatten(window_length=401)
    time = lc.time.value
    flux = lc.flux.value
    mask = np.isfinite(time) & np.isfinite(flux)
    time = time[mask]
    flux = flux[mask]
    

    df = pd.DataFrame({
            "BJD - 2454833": time,
            "Normalized Flux": flux
        })
    def convert_for_download(df):
        return df.to_csv(index=False).encode("utf-8")

    try:
        csv = convert_for_download(df)
    except:
        None

    st.download_button(
        label=f"Download Light Curve {selected_no}",
        data=csv,
        file_name=f"{target.replace(' ', '_')}_{selected_year}_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )
    if st.button("Quick Preview"):
        plt.figure(figsize=(15,5))
        plt.title(f"{target} Light Curve {selected_year}")
        plt.scatter(lc.time.value, lc.flux.value, s=2, color='blue', alpha=0.2)  # scatter
        plt.plot(lc.time.value, lc.flux.value, color='red')
        plt.xticks([])
        plt.yticks([])
        st.pyplot(plt)

except:
    None


st.divider()
st.markdown(f"""
    <p> <a href = "https://www.linkedin.com/in/wijdan-ali-374793288/" style = "font-weight:bold; text-decoration:none;">Transit Light Curve Guide</a>  |  <a href = "https://wijdanali7869.wixsite.com/neoclimex" style = "font-weight:bold; text-decoration:none;">NeoClimex</a> | <a href = "mailto:wijdan.nadeem@gmail.com" style = "font-weight:bold; text-decoration:none;">Email Me</a></p>
""", unsafe_allow_html=True)

