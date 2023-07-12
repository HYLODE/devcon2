# streamlit_app.py
import time

import altair as alt
import pandas as pd
import sqlalchemy as sa
import streamlit as st

# Must be the first streamlit call in the app
st.set_page_config(
   page_title="Ex-stream-ly Cool App",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

# The order of the calls to Streamlit defines the order of components on the
# page so even if we specify the header and the footer now, and backwards the
# footer will appear above the page content
placeholder_for_header = st.empty()
placeholder_for_header.header("Hello from Postgres")

placeholder_for_content = st.empty()

# Uses st.cache_resource to only run once.
@st.cache_resource
def create_engine_ids():
    """Return SQLAlchemy Engine"""
    return sa.create_engine(
        f"postgresql://{st.secrets.emap_ids.username}:"
        f"{st.secrets.emap_ids.password}@"
        f"{st.secrets.emap_ids.host}:"
        f"{st.secrets.emap_ids.port}/"
        f"{st.secrets.emap_ids.database}"
    )

engine = create_engine_ids()

n_rows = 300
start_row, stop_row = 0, 99
i = 5
q = f"SELECT unid, messagedatetime from ids ORDER BY unid DESC  LIMIT {n_rows};"

while True:
    df = pd.read_sql(q, engine)
    df = df[start_row:stop_row]
    df["messagedatetime"] = pd.to_datetime(df["messagedatetime"])
    df_grouped = df.groupby(pd.Grouper(key='messagedatetime', freq='10S')).size()  # grouping by hour
    df_grouped = df_grouped.to_frame(name="n").reset_index()

    with placeholder_for_content.container():
        # st.bar_chart(df_grouped)
        chart = alt.Chart(df_grouped).mark_bar().encode(
            alt.X("messagedatetime:T", 
                  axis=alt.Axis(format="%H:%M:%S"), title="Message timestamp"),
            alt.Y("n:Q")
        )
        st.altair_chart(chart)
        st.markdown("Most _recent_ values from the IDS!")
        st.dataframe(df.head(3))
        st.write("👆 ... these are rows from a Postgres Database")

    start_row, stop_row = start_row + i, stop_row + i
    time.sleep(5)


