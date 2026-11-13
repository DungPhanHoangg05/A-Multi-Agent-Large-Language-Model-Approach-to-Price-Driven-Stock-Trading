import {byId} from '../analysis/common.js';
import {formController} from './form.js';
import {resultController} from './result.js';

const config = JSON.parse(byId('backtest-config').textContent);
formController(config).init();
const result = resultController(config); result.init();
if (config.runId) result.select(config.runId);
