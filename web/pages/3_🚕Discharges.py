import streamlit as st
import requests
from annotated_text import annotated_text
import time
import random
import arrow

SEPS = ["discharge", "home today", "home"]
KWS = ["++", "+++", "+"]
COLORS = ["#FB0081", "#75D100", "#FF6600"]
SEPARATORS = zip(SEPS, KWS, COLORS)

def make_separator_variants(separators):
    separators_plus = list()
    for sep, kw, color in separators:
        lower_, upper_, title_ = sep.lower(), sep.upper(), sep.title()
        separators_plus.append((lower_, kw, color))
        separators_plus.append((upper_, kw, color))
        separators_plus.append((title_, kw, color))
    return separators_plus

def split_with_separator(s, sep, keyword, col):
    if not isinstance(s, str):
        return [s]
    parts = s.split(sep)
    # create tuples for the separators
    separators = [(sep, keyword, col)] * (len(parts) - 1)
    # interleave the parts and separators
    result = [None]*(len(parts)+len(separators))
    result[::2] = parts
    result[1::2] = separators
    return result


separators = make_separator_variants(SEPARATORS)

st.set_page_config(
    page_title="Discharge watcher",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# st.header("test")
# column1, column2 = st.columns(2)
# with
# column1.header("foo")
# column2.header("bar")

st.header("Live discharge monitor")
col1, col2 = st.columns(2)
ce1 = col1.empty()
ce2 = col2.empty()

# Load data
# response = requests.get("http://api:8401/discharges/predictions/")
# data = response.json()
# i = 0

while True:
    # this is a terrible quick hack just to do live updates
    response = requests.get("http://api:8401/discharges/predictions/")
    data = response.json()
    i = 0
    with ce1.container():
        st.header("Prediction")
        now = arrow.utcnow().to("Europe/London").format("D MMM, h:ma")
        st.markdown(f"{now}")
        discharge_prob = data[i].get("discharge_probability")
        st.markdown(f"Review note for discharge rank {discharge_prob:.0%}")
        st.write(i)

    note = data[i].get("note", "")
    parts = [note]  # start with the original string as the only element in the list

    for sep, kw, color in separators:
        new_parts = []
        while parts:
            new_parts.extend(split_with_separator(parts.pop(0), sep, kw, color))
        parts = new_parts

    with ce2.container():
        st.header("Note")
        annotated_text(parts)
    
    i = (i+1) % len(data)
    snooze = random.lognormvariate(0,1)
    time.sleep(snooze)

