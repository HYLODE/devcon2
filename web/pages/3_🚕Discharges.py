from typing import List
import streamlit as st
import requests
from annotated_text import annotated_text

# Load data
response = requests.get("http://api:8401/discharges/predictions/")
data = response.json()

st.set_page_config(
    page_title="Discharge watcher",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("Live discharge monitor")
note = data[0].get("note", "")

# def partition_on_kw(last: str, kw: str, label: str="keyword", color=None) -> List:
#     annotated = []
#     while last:
#         first, keyword, last = list(last.partition(kw))
#         annotated.append(first)
#         if not keyword:
#             break
#         if keyword and color:
#             keyword = (keyword, label, color)
#         else:
#             keyword = (keyword, label)
#         annotated.append(keyword)
#     return annotated


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

separators = ["home", "discharge"]
kws = ["++", "+++"]
colors = ["#FB0081", "#75D100"]
sep_col = zip(separators, kws, colors)

parts = [note]  # start with the original string as the only element in the list

for sep, kw, col in sep_col:
    new_parts = []
    while parts:
        new_parts.extend(split_with_separator(parts.pop(0), sep, kw, col))
    parts = new_parts

print(parts)
annotated_text(parts)