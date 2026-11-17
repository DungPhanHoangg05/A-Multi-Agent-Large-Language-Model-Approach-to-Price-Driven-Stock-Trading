"""Vẽ hai hình gọn từ U09 đã khóa; không tái lấy mẫu hoặc suy luận."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
from typing import Any
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read_results() -> dict[str,Any]:
    """Chỉ nhận đúng gói và member kết quả lịch sử đã kiểm."""
    root=Path(__file__).resolve().parents[3]
    path=root/'docs/plan/week12/unified_analysis_results.zip'
    with path.open('rb') as handle:
        if hashlib.file_digest(handle,'sha256').hexdigest()!='e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9':raise ValueError('Sai gói U09')
    with zipfile.ZipFile(path) as bundle:raw=bundle.read('outputs/unified_integration/u09_analysis_r1/results.json')
    if hashlib.sha256(raw).hexdigest()!='3136ab9bdeab377196236e1a01402646257ec3beb251877702dbc86e1e67e31f':raise ValueError('Sai member kết quả')
    return json.loads(raw)

def save(fig: Any,name: str) -> None:
    """Ghi PDF vector và PNG để kiểm chữ ở kích thước bản in."""
    base=Path(__file__).with_name(name)
    fig.savefig(base.with_suffix('.pdf'),metadata={'CreationDate':None,'Title':name})
    fig.savefig(base.with_suffix('.png'),dpi=160)
    plt.close(fig)

def main() -> None:
    """Dùng nguyên point/band và count, không thêm khoảng tin cậy mới."""
    data=read_results()
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10.5,'pdf.fonttype':42})
    methods=['bayesian_v1','C2','A_tp_pool','B_semantic','MT_BICL']
    labels=['v1','C2','A','B','MT']
    fig,axes=plt.subplots(1,2,figsize=(6.25,2.6),sharey=True)
    for ax,baseline,title,color in zip(axes,['original_fix','original_common'],['A. Extension minus Native','B. Extension minus Common'],['#245b82','#a05a1b']):
        for y,method in enumerate(methods):
            r=next(x for x in data['contrasts'] if x['method']==method and x['baseline']==baseline and x['endpoint']=='account_return_percentage_points')
            value,lo,hi=[r[k] for k in ['effect_pp','band95_low_pp','band95_high_pp']]
            if not lo<=value<=hi:raise ValueError('Point/band không hợp lệ')
            ax.errorbar(value,y,xerr=[[value-lo],[hi-value]],fmt='o',color=color,capsize=3,linewidth=1.4,markersize=4)
        ax.axvline(0,color='#666',linestyle='--',linewidth=.8)
        ax.set_title(title,fontsize=10.5);ax.set_xlim(-1.2,.75);ax.set_ylim(4.5,-.5)
        ax.set_xticks([-1,-.5,0,.5]);ax.set_yticks(range(5),labels)
        ax.grid(axis='x',alpha=.2);ax.spines[['top','right']].set_visible(False)
    fig.supxlabel('Mean account-return difference (percentage points)',fontsize=10.5,y=.015)
    fig.subplots_adjust(left=.08,right=.99,top=.84,bottom=.23,wspace=.17)
    save(fig,'review_return_contrasts')
    mt=next(r for r in data['summary'] if r['method']=='MT_BICL')
    reasons=mt['policy_reasons']
    counts=[mt['bypass_forecasts'],reasons['KEEP_PROPOSED_SAME'],reasons['REJECT_NONPOSITIVE_Q10_DELTA_U'],reasons['ACCEPT_POSITIVE_Q10_DELTA_U']]
    if counts!=[108,189,5,4] or sum(counts)!=306:raise ValueError('Phân rã MT khác nguồn')
    fig,ax=plt.subplots(figsize=(6.25,1.9))
    ax.barh(range(4),counts,color=['#9caab2','#245b82','#a05a1b','#367451'])
    for y,count in enumerate(counts):ax.text(count+4,y,str(count),va='center',fontsize=11)
    ax.set_yticks(range(4),['Bypass to reference','Proposal already matches','Veto proposed change','Accept proposed change'])
    ax.set_xlim(0,220);ax.set_ylim(3.6,-.6);ax.set_xticks([0,50,100,150,200])
    ax.set_xlabel('MT forecast slots (total 306)',fontsize=10.5)
    ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
    fig.subplots_adjust(left=.40,right=.99,top=.98,bottom=.32)
    save(fig,'review_mt_resolution')
    print('Đã vẽ đúng10 return cells và306MT slots từ primary U09; không bootstrap hoặc modelrun.')

if __name__=='__main__':main()
