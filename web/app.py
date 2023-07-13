# streamlit_app.py
import time

import altair as alt
import pandas as pd
import pandera as pa
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
placeholder_for_header.header("EMAP IDS Monitor")
st.write("IDS = Immutable Data Store")

placeholder_for_content = st.empty()


# Uses st.cache_resource to only run once.
@st.cache_resource
def create_engine_ids():
    """Return SQLAlchemy Engine"""
    return sa.create_engine(
        f"postgresql+psycopg2://{st.secrets.emap_ids.username}:"
        f"{st.secrets.emap_ids.password}@"
        f"{st.secrets.emap_ids.host}:"
        f"{st.secrets.emap_ids.port}/"
        f"{st.secrets.emap_ids.database}"
    )


engine = create_engine_ids()

sample_period = 15
query_window_seconds = 60 * sample_period
sample_period_str = f"{sample_period}S"

q = f"""
SELECT
 unid
,messagedatetime
,messagetype
,senderapplication
FROM tbl_ids_master
WHERE messagedatetime > NOW() - INTERVAL '{query_window_seconds} SECONDS'
ORDER BY unid DESC
"""

# TODO: second plot to explore a more complete pull
# TODO: polars

while True:
    # Load data
    df = pd.read_sql(q, engine)
    # IDS stores datestimes naively - 
    df["messagedatetime"] = pd.to_datetime(
        df["messagedatetime"]).dt.round(sample_period_str
        )

    # Group and merge onto an axis running back from now
    # Define now according to timezone, but then strip so the 'local' time is ready for merge
    now = pd.Timestamp.now(tz="Europe/London").tz_localize(None)
    time_skeleton = pd.Series(pd.date_range(
        end=now, 
        periods=int(query_window_seconds/sample_period),
        freq=sample_period_str,
        )).dt.round(sample_period_str)
    time_skeleton.name = "messagedatetime"
    
    df_grouped = df.groupby([
        "messagedatetime",
        "senderapplication",
    ]).size()  
    df_grouped = df_grouped.to_frame(name="n").reset_index()

    df_chart = pd.merge(time_skeleton, df_grouped, how="left", on="messagedatetime")

    with placeholder_for_content.container():

        chart = (
            alt.Chart(df_chart)
            .mark_bar()
            .encode(
                alt.X(
                    "messagedatetime:T",
                    axis=alt.Axis(format="%H:%M:%S"),
                    title="Message timestamp",
                ),
                alt.Y("n:Q").title("Message count"),
                color="senderapplication"
            )
        )

        st.altair_chart(chart)
        st.markdown("Most _recent_ values from the IDS!")
        st.dataframe(df.head(3))
        st.write("👆 ... these are rows from a Postgres Database")

    time.sleep(sample_period)
