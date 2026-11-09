"""Kiểm consumer không nhận partial, sai label pairing hoặc hash tự khai."""

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import numpy as np

from core.free_pilot_analysis import tensor,normalized,output,verify_binding
from core.historical_evaluation_journal import RunBook,load,save
from core.historical_evaluation_protocol import PRIMARY,CORE4,binding,digest


class PilotConsumerTests(unittest.TestCase):
    def rows(self) -> list[dict]:
        return [{'id':f'{y}-{d}-{s}','year':y,'date':f'{y}-07-{d+1:02d}','symbol':s,'method':m,
                 'action':'CASH','r_net':.01 if d%2 else -.01,'y':int(d%2==1)}
                for y in (2023,2024) for d in range(6) for s in CORE4 for m in PRIMARY]

    def test_exact_common_panel_and_partial_rejection(self) -> None:
        rows=self.rows(); a,r,y=tensor(rows)
        self.assertEqual(a.shape,(2,6,4,6)); self.assertEqual(r.shape,(2,6,4))
        with self.assertRaises(ValueError): tensor(rows[:-1])
        with self.assertRaises(ValueError): tensor(rows+[deepcopy(rows[0])])

    def test_label_mismatch_between_methods_is_rejected(self) -> None:
        rows=self.rows(); rows[1]['r_net']=.9
        with self.assertRaises(ValueError): tensor(rows)

    def test_journal_requires_complete_identity_and_original_parent_hash(self) -> None:
        with TemporaryDirectory() as folder:
            book=RunBook(Path(folder),{'fixture':True})
            with self.assertRaises(ValueError): output(book,'one')
            book.execute('one',{'source':'fixture'},lambda _: {'action':'CASH'})
            inputs,value=output(book,'one'); self.assertEqual(value['action'],'CASH')
            doc=load(book.path('one')); doc['inputs']['source']='tamper'; save(book.path('one'),doc)
            with self.assertRaises(ValueError): output(book,'one')

    def test_binding_checks_actual_file_bytes(self) -> None:
        with TemporaryDirectory() as folder:
            root=Path(folder); (root/'data').write_bytes(b'original')
            proof=binding(root,'data'); verify_binding(root,proof)
            (root/'data').write_bytes(b'changed')
            with self.assertRaises(ValueError): verify_binding(root,proof)

    def test_json_normalization_native_scalars_and_undefined(self) -> None:
        value=normalized({'a':np.int64(3),'b':np.float64(float('nan')),'c':np.bool_(True)})
        self.assertEqual(value,{'a':3,'b':None,'c':True})
        self.assertIs(type(value['a']),int); self.assertIs(type(value['c']),bool)


if __name__=='__main__': unittest.main()
