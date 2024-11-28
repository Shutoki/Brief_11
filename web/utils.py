import streamlit as st
import pandas as pd
import numpy as np
from path import DATA_CSV


def load_data() :
    data = pd.read_csv(DATA_CSV)
    lowercase= lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data