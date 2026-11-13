import {renderReport} from './report.js';

// Cùng bố cục Original; báo cáo từ journal được dựng bằng text node, không dùng ảnh/session job khác.
for (const id of ['indicatorContent','alphaContent','patternContent','trendContent','sentimentContent']) {
  const node = document.getElementById(id);
  if (node) renderReport(node,node.textContent);
}
