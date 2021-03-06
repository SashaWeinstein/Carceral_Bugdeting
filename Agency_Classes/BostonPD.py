"""
Boston PD class was given it's own file Dec 29
"""
import pandas as pd

from Police_Dept import PoliceDepartment

from LocalPD_External_Funds import BostonPD_External_Funds
from BostonPD_Non_Payroll_Operating import get_BostonPD_Non_Payroll_Operating
from BostonPD_Capital import get_BostonPD_Capital_Costs
from LocalPD_Pensions import BostonPD_Pensions
from LocalPD_Fringe import BostonPD_Fringe
from LocalPD_True_Payroll import True_Earnings


class BostonPD(PoliceDepartment):
    """"""

    def __init__(self, yr):
        PoliceDepartment.__init__(self, alias="Boston PD", official_name="Boston PD", year_range=yr)
        self.federal_expenditures_by_year = BostonPD_External_Funds()  # New August 14th

        self.non_payroll_operating_expenditures_by_year, self.fraction_all_federal, self.non_hidden_fringe, \
            self.payroll_expenditures_by_year = get_BostonPD_Non_Payroll_Operating(self)
        self.add_true_earnings()
        self.calculate_hidden_payroll()
        self.pensions = BostonPD_Pensions(self)
        self.hidden_fringe = BostonPD_Fringe(self)
        self.fringe = self.non_hidden_fringe + self.hidden_fringe
        self.non_hidden_capital_expenditures_by_year = get_BostonPD_Capital_Costs(self.year_range)
        self.capital_expenditures_by_year = self.non_hidden_capital_expenditures_by_year + \
                                            self.hidden_capital_expenditures_by_year #Refactor


    def add_true_earnings(self):
        """New July 30th. Replace expenditure numbers 2016-2019 with true earnings
        Note that for 2016 for chelsea we don't have actual payroll so I will use rough estimation, need better
         way to fix later"""
        total_earnings, self.PD_fraction_non_teacher, self.PD_fraction_total, PD_payroll = True_Earnings(self.alias)
        self.payroll = PD_payroll
        self.payroll_by_year = total_earnings * (1-self.fraction_all_federal)