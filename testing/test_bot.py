import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return '', str(e), 1

def log_result(logfile, test_name, passed, output, error):
    with open(logfile, 'a') as f:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'test': test_name,
            'passed': passed,
            'output': output,
            'error': error
        }
        f.write(json.dumps(log_entry) + '\n')

def main():
    logfile = os.path.join(os.path.dirname(__file__), 'test_results.log')
    if os.path.exists(logfile):
        os.remove(logfile)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    main_py = os.path.join(base_dir, 'src', 'main.py')
    fg_csv = os.path.join(base_dir, 'fear_greed_index.csv')
    hist_csv = os.path.join(base_dir, 'historical_data.csv')
    tests = [
        # Market order
        {
            'name': 'Market Order',
            'cmd': f'python "{main_py}" --fear-greed-file "{fg_csv}" market BTCUSDT BUY 0.01',
            'expect': 'orderId',
        },
        # Limit order
        {
            'name': 'Limit Order',
            'cmd': f'python "{main_py}" --fear-greed-file "{fg_csv}" limit BTCUSDT SELL 0.01 60000',
            'expect': 'orderId',
        },
        # Stop-Limit order (should error if price triggers immediately)
        {
            'name': 'Stop-Limit Order Immediate Trigger',
            'cmd': f'python "{main_py}" --fear-greed-file "{fg_csv}" stop_limit BTCUSDT BUY 0.01 62000 61000',
            'expect': 'Order would immediately trigger',
        },
        # Stop-Market order (should error if price triggers immediately)
        {
            'name': 'Stop-Market Order Immediate Trigger',
            'cmd': f'python "{main_py}" --fear-greed-file "{fg_csv}" stop_limit BTCUSDT BUY 0.01 61000 --market',
            'expect': 'Order would immediately trigger',
        },
        # OCO order (should error as unsupported)
        {
            'name': 'OCO Order Unsupported',
            'cmd': f'python "{main_py}" --fear-greed-file "{fg_csv}" oco BTCUSDT SELL 0.01 60000 59000 58900',
            'expect': 'OCO orders are not supported',
        },
        # TWAP order
        {
            'name': 'TWAP Order',
            'cmd': f'python "{main_py}" --fear-greed-file "{fg_csv}" twap BTCUSDT BUY 0.03 60000 5 3',
            'expect': 'orders',
        },
        # Grid order (should skip if F&G index condition not met)
        {
            'name': 'Grid Order F&G Skip',
            'cmd': f'python "{main_py}" --fear-greed-file "{fg_csv}" grid BTCUSDT BUY 0.01 59000 61000 5',
            'expect': 'skipped',
        },
        # Analyze trades (should output metrics)
        {
            'name': 'Analyze Trades',
            'cmd': f'python "{main_py}" analyze_trades "{hist_csv}"',
            'expect': 'num_buy_trades',
        },
        # Analyze trades (should error on missing file)
        {
            'name': 'Analyze Trades Missing File',
            'cmd': f'python "{main_py}" analyze_trades "{os.path.join(base_dir, "missing_file.csv")}"',
            'expect': 'File not found',
        },
    ]
    all_passed = True
    for test in tests:
        output, error, code = run_command(test['cmd'])
        passed = test['expect'] in output or test['expect'] in error
        log_result(logfile, test['name'], passed, output, error)
        print(f"{test['name']}: {'PASSED' if passed else 'FAILED'}")
        if not passed:
            print(f"  Output: {output}\n  Error: {error}")
            all_passed = False
    print(f"\nTest log written to {logfile}")
    if not all_passed:
        sys.exit(1)

if __name__ == '__main__':
    main()
