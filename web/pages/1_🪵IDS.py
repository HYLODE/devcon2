# streamlit_app.py
"""
Proof of principle streamlit app providing IDS monitoring as a side effect
"""

import time

import altair as alt
import pandas as pd
import pandera as pa
import sqlalchemy as sa
import streamlit as st

from pandera.typing import Series

# Must be the first streamlit call in the app
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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


@st.cache_data
def get_query_30d(_engine):
    """
    Return a summary of messages from the last 30d
    """
    q = sa.text("""
    SELECT
    DATE_TRUNC('hour', messagedatetime) AS hour
    ,senderapplication
    ,COUNT(*) AS n
    FROM tbl_ids_master
    WHERE messagedatetime > NOW() - INTERVAL '30 DAYS'
    GROUP BY hour, senderapplication
    ORDER BY hour, senderapplication
    """)
    return pd.read_sql(q, _engine)



def get_query_recent(_engine, query_window_seconds):
    # Don't cache this else it won't update
    # Prep the query and interpolate parameters safely
    q = sa.text("""
    SELECT
    unid
    ,messagedatetime
    ,messagetype
    ,senderapplication
    FROM tbl_ids_master
    WHERE messagedatetime > NOW() - INTERVAL ':query_window_seconds SECONDS'
    ORDER BY unid DESC
    """)
    q = q.bindparams(query_window_seconds=query_window_seconds)
    return pd.read_sql(q, _engine)

class IdsShortSchema(pa.DataFrameModel):
    """Define what you expect to be returned from the IDS"""

    unid: Series[int]
    messagedatetime: Series[pa.DateTime]
    messagetype: Series[str]
    senderapplication: Series[str]

    @pa.check("messagedatetime", name="Assert timestamps are timezone naive")
    def tz_naive_check(cls, col) -> bool:
        """Timestamps must be timezone naive to match the specification in the IDS"""
        if col.dt.tz is not None:
            raise pa.errors.SchemaError()
        return True

ENGINE = create_engine_ids()
SAMPLE_PERIOD = 15
QUERY_WINDOW_SECONDS = 60 * SAMPLE_PERIOD
SAMPLE_PERIOD_STR = f"{SAMPLE_PERIOD}S"

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        try:
            if st.session_state["password"] == st.secrets["password"]:
                st.session_state["password_correct"] = True
                # commented out to store the password
                # del st.session_state["password"]  # don't store password
            else:
                st.session_state["password_correct"] = False
        except KeyError as e:
            st.warning("Password not set")
            st.session_state["password_correct"] = False


    st.header("Welcome to the EMAP monitoring dashboard")
    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Please enter the password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    
    df_30d = get_query_30d(ENGINE)

    chart_30d = (
        alt.Chart(df_30d)
        .mark_bar()
        .encode(
            alt.X(
                "hour:T",
                axis=alt.Axis(format="%Y-%m-%d"),
                title="Message timestamp",
            ),
            alt.Y("n:Q").title("Message count"),
            color=alt.Color("senderapplication").scale(
                scheme="viridis"
            )
        )
    )


    # The order of the calls to Streamlit defines the order of components on the
    # page so even if we specify the header and the footer now, and backwards the
    # footer will appear above the page content
    st.header("EMAP Immutable Data Store monitor")
    st.write("The IDS is the log of HL7 messages captured by EMAP")

    col1, col2 = st.columns(2)

    with col1.container():
        st.altair_chart(chart_30d)
        st.markdown("Messages over the last 30 days")

    chart_now = col2.empty()

    while True:
        # Load data
        df = get_query_recent(ENGINE, QUERY_WINDOW_SECONDS)
        IdsShortSchema.validate(df)
        # IDS stores datestimes naively - 
        df["messagedatetime"] = pd.to_datetime(
            df["messagedatetime"]).dt.round(SAMPLE_PERIOD_STR
            )

        # Need to produce a localized timestamp but with a type that does not hold the timezone information
        now = pd.Timestamp.now(tz="Europe/London").tz_localize(None)
        time_skeleton = pd.Series(pd.date_range(
            end=now, 
            periods=int(QUERY_WINDOW_SECONDS/SAMPLE_PERIOD),
            freq=SAMPLE_PERIOD_STR,
            )).dt.round(SAMPLE_PERIOD_STR)
        time_skeleton.name = "messagedatetime"
        
        df_grouped = df.groupby([
            "messagedatetime",
            "senderapplication",
        ]).size()  
        df_grouped = df_grouped.to_frame(name="n").reset_index()

        df_chart = pd.merge(time_skeleton, df_grouped, how="left", on="messagedatetime")

        with chart_now.container():

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
                    color=alt.Color("senderapplication").scale(
                        scheme="viridis"
                    )
                )
            )

            st.altair_chart(chart)
            st.markdown(f"Most _recent_ values from the IDS! Updates every {SAMPLE_PERIOD} seconds")
            st.markdown("NB: Note the non-timezone aware timestamps 😔")
            st.dataframe(df.head(3))
            st.write("👆 Sample rows")

        time.sleep(SAMPLE_PERIOD)
