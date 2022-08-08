# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 00:24:53 2022

@author: Russa
"""

import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_excel(r"FILE PATH")

Ben = df[df.Column2.str.contains('بن')]
Bent = df[df.Column2.str.contains('بنت')]
abu = df[df.Column2.str.contains('ابو')]

x = ["ﻦﺑ","ﺖﻨﺑ","ﻮﺑﺍ"]
y = [len(Ben.index)/100, len(Bent.index)/100, len(abu.index)/100]

width = 0.35
fig, ax = plt.subplots()

pps = ax.bar(x, y, width, align='center')
plt.xlabel("The frequent words")
plt.ylabel("The frequent ratio")

for p in pps:
   height = p.get_height()
   ax.text(x=p.get_x() + p.get_width() / 2, y=height+.10,
      s="{}%".format(height),
      ha='center')

plt.show()

print("done")