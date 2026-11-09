"""Oracle scalar cho kinh tế, account và bootstrap circular pilot đã khóa."""

from __future__ import annotations

import unittest
import numpy as np
import pandas as pd

from core.backtest_engine import compute_round_trip_net_return
from core.free_pilot_statistics import (classification,cycle_ratios,account,selected_date_indices,
                                        estimates,family_interval,bootstrap)


class PilotStatisticsTests(unittest.TestCase):
    def test_confusion_and_undefined_are_not_zero_filled(self) -> None:
        result=classification([1,0,1,0],[1,1,0,0])
        self.assertEqual(result['confusion_matrix'],[[1,1],[1,1]])
        self.assertEqual(result['accuracy'],.5); self.assertEqual(result['balanced_accuracy'],.5)
        self.assertEqual(result['mcc'],0.); self.assertEqual(result['f1_positive'],.5)
        cash=classification([0,0],[0,0])
        self.assertIsNone(cash['balanced_accuracy']); self.assertIsNone(cash['mcc']); self.assertIsNone(cash['f1_positive'])
        self.assertEqual(cash['n_defined']['balanced_accuracy'],0)

    def test_ratios_are_cycle_only_and_zero_downside_is_null(self) -> None:
        result=cycle_ratios([.1,-.1,0.])
        self.assertEqual(result['cycle_sharpe'],0.)
        self.assertEqual(result['cycle_sortino_lpm2'],0.)
        self.assertIsNone(result['annualized_sharpe'])
        self.assertIsNone(cycle_ratios([.1,.1])['cycle_sortino_lpm2'])

    def fixture(self) -> tuple:
        days=pd.bdate_range('2023-07-03',periods=8)
        frame=pd.DataFrame({'Datetime':days,'Open':100.,'Close':100.})
        cycles=[]
        for i,action in ((0,'LONG'),(4,'CASH')):
            cycles.append({'date':str(days[i].date()),'entry_date':str(days[i+1].date()),'exit_date':str(days[i+3].date()),
                           'r_net':compute_round_trip_net_return(100.,100.),'action':action})
        return frame,cycles

    def test_account_matches_independent_cash_math_and_keeps_gap_sessions(self) -> None:
        frame,cycles=self.fixture(); result=account(cycles,frame)
        expected=50_000_000 * (.999*.9975)/(1.001*1.0025)
        self.assertAlmostEqual(result['final_vnd'],expected,places=6)
        self.assertEqual(result['held_sessions'],3); self.assertEqual(result['cash_sessions'],5)
        self.assertEqual(len(result['daily_nav_vnd']),8)
        self.assertEqual(result['cycles'][1]['shares'],0.)
        self.assertAlmostEqual(result['daily_mdd_pct'],(1-expected/50_000_000)*100.)

    def test_daily_mark_to_market_differs_from_cycle_end_drawdown(self) -> None:
        frame,cycles=self.fixture(); frame.loc[1,'Close']=150.; frame.loc[2,'Close']=80.
        result=account(cycles,frame)
        self.assertGreater(result['daily_mdd_pct'],40.)
        self.assertLess(result['cycle_end_mdd_pct'],1.)

    def test_wrong_label_overlap_and_invalid_action_raise(self) -> None:
        frame,cycles=self.fixture()
        cycles[0]['r_net']=0.
        with self.assertRaises(ValueError): account(cycles,frame)
        frame,cycles=self.fixture(); cycles[0]['action']='SHORT'
        with self.assertRaises(ValueError): account(cycles,frame)

    def test_indices_are_reproducible_and_circular_pairs_never_cross_year(self) -> None:
        a=selected_date_indices(); b=selected_date_indices()
        self.assertEqual(a.shape,(10000,2,6)); np.testing.assert_array_equal(a,b)
        np.testing.assert_array_equal(a[:,:,1::2],(a[:,:,::2]+1)%6)
        self.assertFalse(np.array_equal(a[:,0],a[:,1]))

    def test_bootstrap_estimates_match_scalar_account_and_confusion_oracle(self) -> None:
        r=np.tile(np.array([.02,-.03,.01,-.01,.04,-.02])[None,:,None],(2,1,4))
        r[1]*=.7; y=r>0
        a=np.zeros((2,6,4,6),dtype=bool)
        a[:,:,:,1]=True; a[:,::2,:,2]=True; a[0,:,:,3]=True; a[:,:,::2,4]=True; a[:,1::2,:,5]=True
        idx=np.array([[[0,1,0,1,5,0],[4,5,0,1,2,3]],[[2,3,4,5,0,1],[0,1,2,3,4,5]]])
        got_return,got_ba=estimates(a,r,y,idx)
        for draw in range(2):
            macro=[]; bas=[]
            for method in range(6):
                accounts=[]; tp=tn=fp=fn=0
                for year in range(2):
                    for symbol in range(4):
                        nav=1.
                        for date in idx[draw,year]:
                            pred=bool(a[year,date,symbol,method]); actual=bool(y[year,date,symbol])
                            nav*=1.+(r[year,date,symbol] if pred else 0.)
                            tp+=int(pred and actual); tn+=int(not pred and not actual)
                            fp+=int(pred and not actual); fn+=int(not pred and actual)
                        accounts.append((nav-1.)*100.)
                macro.append(sum(accounts)/8.)
                bas.append((tp/(tp+fn)+tn/(tn+fp))*50.)
            np.testing.assert_allclose(got_return[draw],np.array(macro[1:])-macro[0],atol=1e-12)
            np.testing.assert_allclose(got_ba[draw],np.array(bas[1:])-bas[0],atol=1e-12)

    def test_macro_account_is_not_compounding_across_symbols(self) -> None:
        a=np.zeros((2,6,4,6),dtype=bool); a[:,:,:,1]=True
        r=np.zeros((2,6,4)); r[0,0,0]=.1; r[0,0,1]=-.1
        returns,_=estimates(a,r,r>0,np.broadcast_to(np.arange(6),(1,2,6)))
        self.assertAlmostEqual(returns[0,0],0.,places=12)

    def test_family_centering_uses_all_five_and_lost_draws_not_redrawn(self) -> None:
        point=np.arange(5,dtype=float); draws=np.tile(point+3.,(10000,1))
        result=family_interval(point,draws,metric='return')
        self.assertEqual(result['half_width'],3.)
        draws[9499:,0]=np.nan
        result=family_interval(point,draws,metric='BA')
        self.assertIsNone(result['ci']); self.assertEqual(result['joint_finite_draws'],9499)
        self.assertEqual(result['lost_class_or_nonfinite_draws'],501)

    def test_one_class_ba_family_is_null_without_redraw(self) -> None:
        r=np.full((2,6,4),-.01); a=np.zeros((2,6,4,6),dtype=bool)
        result=bootstrap(a,r,r>0)
        self.assertEqual(result['balanced_accuracy']['joint_finite_draws'],0)
        self.assertIsNone(result['balanced_accuracy']['ci'])
        self.assertEqual(result['return']['half_width'],0.)


if __name__=='__main__': unittest.main()
