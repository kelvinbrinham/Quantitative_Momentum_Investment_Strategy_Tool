'''
test 3
'''
import numpy as np
import pandas as pd
import math as mth
import requests as rq
import linecache
from scipy import stats
import json as js
import datetime as dt


print(isinstance(8, str))

for column_cells in worksheet.columns:
    length = max(len(as_text(cell.value)) for cell in column_cells)
    worksheet.column_dimensions[column_cells[0].column].width = length

    Momentum_strategy_ws.column_dimensions[column_cells[0].column].width = length
