import {renderReport,normalizeIndicator} from './report.js';

// Cùng bố cục Original; báo cáo từ journal được dựng bằng text node, không dùng ảnh/session job khác.
for (const id of ['indicatorContent','alphaContent','commonAlphaContent','patternContent','trendContent','sentimentContent']) {
  const node = document.getElementById(id);
  if (node) {
    node.classList.add('auto-beautify');
    renderReport(node,id==='indicatorContent' ? normalizeIndicator(node.textContent) : node.textContent);
  }
}
