# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 18:16:49 2018

@author: cgokh
"""

import pandas as pd
path = 'C:/Kaggle/talkingdata/submissions/'
submission_1_name = "andy_blend_blend_lgb0730_xgb30m_weighted_blend.csv"
submission_2_name = ""
submission_3_name = "sub_skip3.csv"
submission_4_name = "sub_skip4.csv"
submission_5_name = "sub_skip5.csv"


sub_1 = pd.read_csv(path+submission_1_name)
sub_2 = pd.read_csv(path+submission_2_name)
sub_3 = pd.read_csv(path+submission_3_name)
sub_4 = pd.read_csv(path+submission_4_name)
sub_5 = pd.read_csv(path+submission_5_name)

sub_final = pd.DataFrame()
sub_final['click_id'] = sub_1['click_id']
sub_final['is_attributed'] = (sub_1['is_attributed'] + sub_2['is_attributed'])/2

sub_final.to_csv('andy_and_wordbatch_pranav_5bags_blend_blend.csv',index=False)