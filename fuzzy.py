import numpy as np
import math
import re
import matplotlib.pyplot as plt
from tkinter import messagebox

class FuzzyInferenceSystem:
 
    def __init__(self,type_memfun=1):
	    self.__type_memfun = type_memfun
	    self.res = ""	
        	
    def set_glu(self, val_low, val_med, val_high):
	    self._glu_low = val_low
	    self._glu_med = val_med
	    self._glu_high = val_high

    def set_ins(self, val_low, val_med, val_high):
	    self._ins_low = val_low
	    self._ins_med = val_med
	    self._ins_high = val_high

    def set_bmi(self, val_low, val_med, val_high):
	    self._bmi_low = val_low
	    self._bmi_med = val_med
	    self._bmi_high = val_high

    def set_dpf(self, val_low, val_med, val_high):
	    self._dpf_low = val_low
	    self._dpf_med = val_med
	    self._dpf_high = val_high

    def set_age(self, val_low, val_med, val_high):
	    self._age_low = val_low
	    self._age_med = val_med
	    self._age_high = val_high

    def set_uri(self, val_low, val_med, val_high):
	    self._uri_low = val_low
	    self._uri_med = val_med
	    self._uri_high = val_high   	

    def set_dm(self, val_vlow, val_low, val_med, val_high, val_vhigh):
	    self._dm_vlow = val_vlow
	    self._dm_low = val_low
	    self._dm_med = val_med
	    self._dm_high = val_high
	    self._dm_vhigh = val_vhigh
    def set_functype(self, type_func):
	    self.__type_memfun = type_func	    

    def make_rules(self, str_rulefile):
	    """
		step 3: create fuzzy rules
	    :return:
	    """
	    try:
		    with open(str_rulefile) as f:
			    file_contents = (re.split(r'\n\n',f.read()))    #split text file by using every double whitespace
			    self.__ruleBase = []
			    self.__ruleOpr = []
			    for rule in file_contents:
				    x = re.search("(RULE|rule) (?P<RuleID>[0-9]*): IF GLU = (?P<Value1>[0-1A-Za-z_]+) (?P<Operator1>AND|OR) INS = (?P<Value2>[0-1A-Za-z_]+) (?P<Operator2>AND|OR) BMI = (?P<Value3>[0-1A-Za-z_]+) (?P<Operator3>AND|OR) DPF = (?P<Value4>[0-1A-Za-z_]+) (?P<Operator4>AND|OR) AGE = (?P<Value5>[0-1A-Za-z_]+) (?P<Operator5>AND|OR) URI = (?P<Value6>[0-1A-Za-z_]+) THEN DM = (?P<Value>[0-1A-Za-z]+)." , rule)
			    
				    if x is None:
					    return False
				    else:
					    ID = x.group("RuleID")
					    values = [x.group("Value1"), x.group("Value2"), x.group("Value3"), x.group("Value4"), x.group("Value5"), x.group("Value6"), x.group("Value")]
					    operator = [x.group("Operator1"), x.group("Operator2"), x.group("Operator3"), x.group("Operator4"), x.group("Operator5")] 
					    self.__ruleBase.append(values)
					    self.__ruleOpr.append(operator)
	    except Exception as e:
		    messagebox.showerror("Error", e)
	    return True
    def func_glu(self, level, x_val):	# level is fuzzyNumber(e,g : low, medium, high)
	    y_val = 0
	    if self.__type_memfun == 1:	# in case of triangle func type
		    if level == 'LOW':		# in case of low variable
			    y_val = max(min(1, (self._glu_low[2] - x_val)/(self._glu_low[2] - self._glu_low[1])), 0.01)
		    elif level == 'MED':		# in case of med variable
			    y_val = max(min((x_val - self._glu_med[0])/(self._glu_med[1] - self._glu_med[0]), (self._glu_med[2] - x_val)/(self._glu_med[2] - self._glu_med[1])), 0.01)
		    elif level == 'HIGH':		# in case of high variable
			    y_val = max(min((x_val - self._glu_high[0])/(self._glu_high[1] - self._glu_high[0]), 1), 0)
	    elif self.__type_memfun == 2:	# in case of trapezoidal func type
		    if level ==	'LOW':
			    y_val = max(min(1, (self._glu_low[3] - x_val)/(self._glu_low[3] - self._glu_low[2])), 0.01)
		    elif level == 'MED':
			    y_val = max(min((x_val - self._glu_med[0])/(self._glu_med[1] - self._glu_med[0]), 1, (self._glu_med[3] - x_val)/(self._glu_med[3] - self._glu_med[2])), 0.01)
		    elif level == 'HIGH':
			    y_val = max(min((x_val - self._glu_high[0])/(self._glu_high[1] - self._glu_high[0]), 1), 0.01)
	    elif self.__type_memfun == 3:	# in case of gaussian func type   
		    if level ==	'LOW':
			    y_val = math.exp(-(x_val-self._glu_low[0])**2/(2*self._glu_low[1]*self._glu_low[1])) + 0.01
		    elif level == 'MED':
			    y_val = math.exp(-(x_val-self._glu_med[0])**2/(2*self._glu_med[1]*self._glu_med[1])) + 0.01
		    elif level == 'HIGH':
			    y_val = math.exp(-(x_val-self._glu_high[0])**2/(2*self._glu_high[1]*self._glu_high[1])) + 0.01
	    return y_val
    def func_ins(self, level, x_val):	# level is fuzzyNumber(e,g : low, medium, high)
	    y_val = 0
	    if self.__type_memfun == 1:	# in case of triangle func type
		    if level ==	'LOW':		# in case of low variable
			    y_val = max(min(1, (self._ins_low[2] - x_val)/(self._ins_low[2] - self._ins_low[1])), 0.01)
		    elif level == 'MED':		# in case of med variable
			    y_val = max(min((x_val - self._ins_med[0])/(self._ins_med[1] - self._ins_med[0]), (self._ins_med[2] - x_val)/(self._ins_med[2] - self._ins_med[1])), 0.01)
		    elif level == 'HIGH':		# in case of high variable
			    y_val = max(min((x_val - self._ins_high[0])/(self._ins_high[1] - self._ins_high[0]), 1), 0.01)
	    elif self.__type_memfun == 2:	# in case of trapezoidal func type
		    if level ==	'LOW':
			    y_val = max(min( 1, (self._ins_low[3] - x_val)/(self._ins_low[3] - self._ins_low[2])), 0.01)
		    elif level == 'MED':
			    y_val = max(min((x_val - self._ins_med[0])/(self._ins_med[1] - self._ins_med[0]), 1, (self._ins_med[3] - x_val)/(self._ins_med[3] - self._ins_med[2])), 0.01)
		    elif level == 'HIGH':
			    y_val = max(min((x_val - self._ins_high[0])/(self._ins_high[1] - self._ins_high[0]), 1), 0.01)
	    elif self.__type_memfun == 3:	# in case of gaussian func type   
		    if level ==	'LOW':
			    y_val = math.exp(-(x_val-self._ins_low[0])**2/(2*self._ins_low[1]*self._ins_low[1])) + 0.01
		    elif level == 'MED':
			    y_val = math.exp(-(x_val-self._ins_med[0])**2/(2*self._ins_med[1]*self._ins_med[1])) + 0.01
		    elif level == 'HIGH':
			    y_val = math.exp(-(x_val-self._ins_high[0])**2/(2*self._ins_high[1]*self._ins_high[1])) + 0.01  
	    return y_val
    def func_bmi(self, level, x_val):	# level is fuzzyNumber(e,g : low, medium, high)
	    y_val = 0
	    if self.__type_memfun == 1:	# in case of triangle func type
		    if level == 'LOW':		# in case of low variable
			    y_val = max(min(1, (self._bmi_low[2] - x_val)/(self._bmi_low[2] - self._bmi_low[1])), 0.01)
		    elif level == 'MED':		# in case of med variable
			    y_val = max(min((x_val - self._bmi_med[0])/(self._bmi_med[1] - self._bmi_med[0]), (self._bmi_med[2] - x_val)/(self._bmi_med[2] - self._bmi_med[1])), 0.01)
		    elif level == 'HIGH':		# in case of high variable
			    y_val = max(min((x_val - self._bmi_high[0])/(self._bmi_high[1] - self._bmi_high[0]), 1), 0.01)
	    elif self.__type_memfun == 2:	# in case of trapezoidal func type
		    if level ==	'LOW':
			    y_val = max(min(1, (self._bmi_low[3] - x_val)/(self._bmi_low[3] - self._bmi_low[2])), 0.01)
		    elif level == 'MED':
			    y_val = max(min((x_val - self._bmi_med[0])/(self._bmi_med[1] - self._bmi_med[0]), 1, (self._bmi_med[3] - x_val)/(self._bmi_med[3] - self._bmi_med[2])), 0.01)
		    elif level == 'HIGH':
			    y_val = max(min((x_val - self._bmi_high[0])/(self._bmi_high[1] - self._bmi_high[0]), 1), 0.01)
	    elif self.__type_memfun == 3:	# in case of gaussian func type   
		    if level ==	'LOW':
			    y_val = math.exp(-(x_val-self._bmi_low[0])**2/(2*self._bmi_low[1]*self._bmi_low[1])) + 0.01
		    elif level == 'MED':
			    y_val = math.exp(-(x_val-self._bmi_med[0])**2/(2*self._bmi_med[1]*self._bmi_med[1])) + 0.01
		    elif level == 'HIGH':
			    y_val = math.exp(-(x_val-self._bmi_high[0])**2/(2*self._bmi_high[1]*self._bmi_high[1])) + 0.01 
	    return y_val
    def func_dpf(self, level, x_val):	# level is fuzzyNumber(e,g : low, medium, high)
	    y_val = 0
	    if self.__type_memfun == 1:	# in case of triangle func type
		    if level ==	'LOW':		# in case of low variable
			    y_val = max(min(1, (self._dpf_low[2] - x_val)/(self._dpf_low[2] - self._dpf_low[1])), 0.01)
		    elif level == 'MED':		# in case of med variable
			    y_val = max(min((x_val - self._dpf_med[0])/(self._dpf_med[1] - self._dpf_med[0]), (self._dpf_med[2] - x_val)/(self._dpf_med[2] - self._dpf_med[1])), 0.01)
		    elif level == 'HIGH':		# in case of high variable
			    y_val = max(min((x_val - self._dpf_high[0])/(self._dpf_high[1] - self._dpf_high[0]), 1), 0.01)
	    elif self.__type_memfun == 2:	# in case of trapezoidal func type
		    if level ==	'LOW':
			    y_val = max(min(1, (self._dpf_low[3] - x_val)/(self._dpf_low[3] - self._dpf_low[2])), 0.01)
		    elif level == 'MED':
			    y_val = max(min((x_val - self._dpf_med[0])/(self._dpf_med[1] - self._dpf_med[0]), 1, (self._dpf_med[3] - x_val)/(self._dpf_med[3] - self._dpf_med[2])), 0.01)
		    elif level == 'HIGH':
			    y_val = max(min((x_val - self._dpf_high[0])/(self._dpf_high[1] - self._dpf_high[0]), 1), 0.01)
	    elif self.__type_memfun == 3:	# in case of gaussian func type   
		    if level ==	'LOW':
			    y_val = math.exp(-(x_val-self._dpf_low[0])**2/(2*self._dpf_low[1]*self._dpf_low[1])) + 0.01
		    elif level == 'MED':
			    y_val = math.exp(-(x_val-self._dpf_med[0])**2/(2*self._dpf_med[1]*self._dpf_med[1])) + 0.01
		    elif level == 'HIGH':
			    y_val = math.exp(-(x_val-self._dpf_high[0])**2/(2*self._dpf_high[1]*self._dpf_high[1])) + 0.01 
	    return y_val
    def func_age(self, level, x_val):	# level is fuzzyNumber(e,g : low, medium, high)
	    y_val = 0
	    if self.__type_memfun == 1:	# in case of triangle func type
		    if level ==	'LOW':		# in case of low variable
			    y_val = max(min(1, (self._age_low[2] - x_val)/(self._age_low[2] - self._age_low[1])), 0.01)
		    elif level == 'MED':		# in case of med variable
			    y_val = max(min((x_val - self._age_med[0])/(self._age_med[1] - self._age_med[0]), (self._age_med[2] - x_val)/(self._age_med[2] - self._age_med[1])), 0.01)
		    elif level == 'HIGH':		# in case of high variable
			    y_val = max(min((x_val - self._age_high[0])/(self._age_high[1] - self._age_high[0]), 1), 0.01)
	    elif self.__type_memfun == 2:	# in case of trapezoidal func type
		    if level ==	'LOW':
			    y_val = max(min(1, (self._age_low[3] - x_val)/(self._age_low[3] - self._age_low[2])), 0.01)
		    elif level == 'MED':
			    y_val = max(min((x_val - self._age_med[0])/(self._age_med[1] - self._age_med[0]), 1, (self._age_med[3] - x_val)/(self._age_med[3] - self._age_med[2])), 0.01)
		    elif level == 'HIGH':
			    y_val = max(min((x_val - self._age_high[0])/(self._age_high[1] - self._age_high[0]), 1), 0.01)
	    elif self.__type_memfun == 3:	# in case of gaussian func type   
		    if level ==	'LOW':
			    y_val = math.exp(-(x_val-self._age_low[0])**2/(2*self._age_low[1]*self._age_low[1])) + 0.01
		    elif level == 'MED':
			    y_val = math.exp(-(x_val-self._age_med[0])**2/(2*self._age_med[1]*self._age_med[1])) + 0.01
		    elif level == 'HIGH':
			    y_val = math.exp(-(x_val-self._age_high[0])**2/(2*self._age_high[1]*self._age_high[1])) + 0.01 
	    return y_val
    def func_uri(self, level, x_val):	# level is fuzzyNumber(e,g : low, medium, high)
	    y_val = 0
	    if self.__type_memfun ==	1:	# in case of triangle func type
		    if level ==	'LOW':		# in case of low variable
			    y_val = max(min(1, (self._uri_low[2] - x_val)/(self._uri_low[2] - self._uri_low[1])), 0.01)
		    elif level == 'MED':		# in case of med variable
			    y_val = max(min((x_val - self._uri_med[0])/(self._uri_med[1] - self._uri_med[0]), (self._uri_med[2] - x_val)/(self._uri_med[2] - self._uri_med[1])), 0.01)
		    elif level == 'HIGH':		# in case of high variable
			    y_val = max(min((x_val - self._uri_high[0])/(self._uri_high[1] - self._uri_high[0]), 1), 0.01)
	    elif self.__type_memfun == 2:	# in case of trapezoidal func type
		    if level ==	'LOW':
			    y_val = max(min(1, (self._uri_low[3] - x_val)/(self._uri_low[3] - self._uri_low[2])), 0.01)
		    elif level == 'MED':
			    y_val = max(min((x_val - self._uri_med[0])/(self._uri_med[1] - self._uri_med[0]), 1, (self._uri_med[3] - x_val)/(self._uri_med[3] - self._uri_med[2])), 0.01)
		    elif level == 'HIGH':
			    y_val = max(min((x_val - self._uri_high[0])/(self._uri_high[1] - self._uri_high[0]), 1), 0.01)
	    elif self.__type_memfun == 3:	# in case of gaussian func type   
		    if level ==	'LOW':
			    y_val = math.exp(-(x_val-self._uri_low[0])**2/(2*self._uri_low[1]*self._uri_low[1])) + 0.01
		    elif level == 'MED':
			    y_val = math.exp(-(x_val-self._uri_med[0])**2/(2*self._uri_med[1]*self._uri_med[1])) + 0.01
		    elif level == 'HIGH':
			    y_val = math.exp(-(x_val-self._uri_high[0])**2/(2*self._uri_high[1]*self._uri_high[1])) + 0.01  
	    return y_val
    def func_dm(self, level, x_val):	# level is fuzzyNumber(e,g : 0->vlow, 1->low, 2->medium, 3->high, 4->vhigh)
	    y_val = 0
	    if self.__type_memfun == 1:	# in case of triangle func type
		    if level == 'VERYLOW':
			    y_val = max(min(1, (self._dm_vlow[2] - x_val)/(self._dm_vlow[2] - self._dm_vlow[1])), 0.01)
		    elif level == 'LOW':		# in case of low variable
			    y_val = max(min((x_val - self._dm_low[0])/(self._dm_low[1] - self._dm_low[0]), (self._dm_low[2] - x_val)/(self._dm_low[2] - self._dm_low[1])), 0.01)
		    elif level == 'MED':		# in case of med variable
			    y_val = max(min((x_val - self._dm_med[0])/(self._dm_med[1] - self._dm_med[0]), (self._dm_med[2] - x_val)/(self._dm_med[2] - self._dm_med[1])), 0.01)
		    elif level == 'HIGH':		# in case of high variable
			    y_val = max(min((x_val - self._dm_high[0])/(self._dm_high[1] - self._dm_high[0]), (self._dm_high[2] - x_val)/(self._dm_high[2] - self._dm_high[1])), 0.01)
		    elif level == 'VERYHIGH':		# in case of high variable
			    y_val = max(min((x_val - self._dm_vhigh[0])/(self._dm_vhigh[1] - self._dm_vhigh[0]), 1), 0.01)	    
	    elif self.__type_memfun == 2:	# in case of trapezoidal func type
		    if level ==	'VERYLOW':
			    y_val = max(min(1, (self._dm_vlow[3] - x_val)/(self._dm_vlow[3] - self._dm_vlow[2])), 0.01)
		    elif level == 'LOW':
			    y_val = max(min((x_val - self._dm_low[0])/(self._dm_low[1] - self._dm_low[0]), 1, (self._dm_low[3] - x_val)/(self._dm_low[3] - self._dm_low[2])), 0.01)
		    elif level == 'MED':
			    y_val = max(min((x_val - self._dm_med[0])/(self._dm_med[1] - self._dm_med[0]), 1, (self._dm_med[3] - x_val)/(self._dm_med[3] - self._dm_med[2])), 0.01)
		    elif level == 'HIGH':
			    y_val = max(min((x_val - self._dm_high[0])/(self._dm_high[1] - self._dm_high[0]), 1, (self._dm_high[3] - x_val)/(self._dm_high[3] - self._dm_high[2])), 0.01)
		    elif level == 'VERYHIGH':
			    y_val = max(min((x_val - self._dm_vhigh[0])/(self._dm_vhigh[1] - self._dm_vhigh[0]), 1), 0.01)	    
	    elif self.__type_memfun == 3:	# in case of gaussian func type   
		    if level == 'VERYLOW':
			    y_val = math.exp(-(x_val-self._dm_vlow[0])**2/(2*self._dm_vlow[1]*self._dm_vlow[1])) + 0.01
		    elif level == 'LOW':
			    y_val = math.exp(-(x_val-self._dm_low[0])**2/(2*self._dm_low[1]*self._dm_low[1])) + 0.01	    
		    elif level == 'MED':
			    y_val = math.exp(-(x_val-self._dm_med[0])**2/(2*self._dm_med[1]*self._dm_med[1])) + 0.01
		    elif level == 'HIGH':
			    y_val = math.exp(-(x_val-self._dm_high[0])**2/(2*self._dm_high[1]*self._dm_high[1])) + 0.01
		    elif level == 'VERYHIGH':
			    y_val = math.exp(-(x_val-self._dm_vhigh[0])**2/(2*self._dm_vhigh[1]*self._dm_vhigh[1])) + 0.01	  
	    return y_val
    def func_defuzzy(self, mu_out, y_out, x_val):
	    """
	    Here, the variable'y_out' is list of level of DM. e,g:['VERYLOW', 'LOW', 'MED', 'HIGH', 'VERYLOW', 'VERYHIGH']  
	    and the variable 'mu_out' is list of maximum value of membership function for each DM level e,g: [0.3, 0.23, 0.5, 0.6, 0.99, 0.42]
	    x_val is real value in (0, 1) which is range of DM level
	    """
	    tempout = []
	    for i in range(0, len(self.__ruleBase)):
		    tempout.append(mu_out[i] * self.func_dm(y_out[i], x_val)) 
	    out_val = max(tempout)
	    return out_val
    def mamdianiInference(self, glu_val, ins_val, bmi_val, dpf_val, age_val, uri_val):
	    mu_out = []		#list of fittness for all rules
	    y_out = []		#list of output for all rules    E,g: ['VERYLOW', 'LOW', 'MED', 'HIGH', 'VERYLOW', 'VERYHIGH']
	    
	    #----- Calculation of fittness for each rules.------#	    
	    for r in range (0, len(self.__ruleBase)):
		    y_glu = self.func_glu(self.__ruleBase[r][0], glu_val)	# fittness of glu in conditional part at r'th rule (Singletone fuzzification was used for input)
		    y_ins = self.func_ins(self.__ruleBase[r][1], ins_val)
		    y_bmi = self.func_bmi(self.__ruleBase[r][2], bmi_val)
		    y_dpf = self.func_dpf(self.__ruleBase[r][3], dpf_val)
		    y_age = self.func_age(self.__ruleBase[r][4], age_val)
		    y_uri = self.func_uri(self.__ruleBase[r][5], uri_val)
		    y = [y_glu, y_ins, y_bmi, y_dpf, y_age, y_uri]
		    
		    strInf = str("%.2f" % (y[0]))	# string for conditional part of r'th rule.
		    for i in range (0, 5):		# merge all variables with it's operators(AND, OR)  For example, strInf will be '0.3OR0.4AND0.33OR0.8OR0.1AND0.9'
			    strInf = strInf + self.__ruleOpr[r][i] + str("%.2f"%(y[i + 1]))
		    tokenOR = (re.split(r'OR',strInf))	# First, the merged condition is splitted into "OR" tokens E,g: tokenOR = ['0.3', '0.4AND0.33', '0.8', '0.1AND0.9']
		    out_val = []			# values for 'or' array  of conditional part
		    for toke in tokenOR:
			    tokenAND = (re.split(r'AND',toke))	    # Second, OR tokens is splitted into "AND" tokens separately  E,g: in second tokenOR , tokenAND will be ['0.4', '0.33']
			    mintoken = min(tokenAND)
			    out_val.append(float(mintoken))
		    
		    y_max = max(out_val)		# Fittness of r'th rule
		    mu_out.append(y_max)	
		    y_out.append(self.__ruleBase[r][6])
		    
	    #---- Max Defuzzification------#
	    ymax = 0
	    maxID = 0
	    for i in range(len(self.__ruleBase)):
		    if mu_out[i] > ymax:
		    	ymax = mu_out[i]
		    	maxID = i
	    y_out_defuzzyres = y_out[maxID] 
	    
	    # ----- centroid Defuzzification(mean of area) ------#
	    steps = 200
	    x_axis = np.linspace(0, 1, steps)
	    y_axis = []
	    for i in range(0,steps):
		    y_axis.append(self.func_defuzzy(mu_out, y_out, x_axis[i]))
	    """
	    plt.plot(x_axis, y_axis, color='blue')	    
	    plt.legend()
	    plt.title("Graph for Defuzzification")
	    plt.show()
	    """
	    numerator_values = []
	    denominator_values = []
	    for i in range(0, steps):
		    numerator_values.append(x_axis[i] * y_axis[i])
		    denominator_values.append(y_axis[i])
	    y_out_defuzzyres = sum(numerator_values)/sum(denominator_values)

	    return y_out_defuzzyres, x_axis, y_axis

if __name__ == '__main__':
        fuzzy = FuzzyInferenceSystem(1)
        glu_low_var, glu_med_var, glu_high_var = [56, 100, 125], [68.2, 117, 145], [109.9, 146, 198]
        ins_low_var, ins_med_var, ins_high_var = [0, 55.11, 87.67], [63.63, 98.42, 191.6], [95.34, 188.3, 586]
        bmi_low_var, bmi_med_var, bmi_high_var = [18, 22, 30.8], [31.07, 37.07, 45.01], [36.43, 44.43, 67]
        dpf_low_var, dpf_med_var, dpf_high_var = [0.085, 0.5322, 1.132], [0.547, 1.03, 1.717], [1.09, 1.476, 2.4]
        age_young_var, age_med_var, age_old_var = [24, 25, 26], [25, 26, 27], [26, 27, 30]
        uri_low_var, uri_med_var, uri_high_var = [0.5, 50, 800], [500, 1300, 2000], [1500, 2500, 5000]
        dm_vlow_var, dm_low_var, dm_med_var, dm_high_var, dm_vhigh_var = [0, 0.1, 0.2], [0.1524, 0.2524, 0.3], [0.287, 0.333, 0.3997], [0.355, 0.623, 0.762], [0.731, 0.831, 1]
        filename = input("input the file for Rules: ")	
        fuzzy.set_glu(glu_low_var, glu_med_var, glu_high_var)
        fuzzy.set_ins(ins_low_var, ins_med_var, ins_high_var)
        fuzzy.set_bmi(bmi_low_var, bmi_med_var, bmi_high_var)
        fuzzy.set_dpf(dpf_low_var, dpf_med_var, dpf_high_var)
        fuzzy.set_age(age_young_var, age_med_var, age_old_var)
        fuzzy.set_uri(uri_low_var, uri_med_var, uri_high_var)
        fuzzy.set_dm(dm_vlow_var, dm_low_var, dm_med_var, dm_high_var, dm_vhigh_var)
        fuzzy.make_rules(filename)
        output = fuzzy.mamdianiInference(100, 55.1, 22, 1.03, 26, 1300)
        print("DM level is ", str("%.2f" % output))
            
  
    
    
	
	
