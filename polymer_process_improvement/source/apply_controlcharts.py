
import pandas as pd
import numpy as np


from polymer_process_improvement.source.nelson_controlchart import control_chart

from polymer_process_improvement.source.control_chart import simple_controlchart


data = pd.read_csv("polymer_process_improvement/data/VSSTeamFinalData.csv", sep=",")
data


control_chart(data=data, y_name="MFI", xlabel = None, title = "Controlchart", lsl = None, usl = None, outlier = True, lines= True, mean = None, sigma = None)

info_SPCrules(3)





simple_controlchart(data=data, y_name="MFI", title = "Controlchart", xlabel=None, Phase="Phase", Phasesinplot= True, Outlier = True, plotlimit=True)

simple_controlchart(data=data, y_name="CI", xlabel=None, Phase="Phase", Phasesinplot= True, Outlier = True, plotlimit=True)

simple_controlchart(data=data, y_name="MFI", xlabel=None, Phase=None, Phasesinplot= True, Outlier = True, plotlimit=False)

