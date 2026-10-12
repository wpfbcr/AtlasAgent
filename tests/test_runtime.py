"""Offline regressions for forecast, FX, diagnostics, environment and export."""
import contextlib
from datetime import date
import importlib.metadata
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import http_client
import weather_client as weather
import currency_client as currency
import holiday_check as calendar
import doctor
import environment


class RequestTests(unittest.TestCase):
    def response(self, text):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value.read.return_value = text.encode()
        return response

    def test_retry_then_success_is_bounded(self):
        with patch('http_client.urllib.request.urlopen', side_effect=[TimeoutError(), self.response('{"ok": true}')]) as request, patch('http_client.time.sleep') as delay:
            self.assertEqual(http_client.fetch_json('https://example.test'), {'ok': True})
            self.assertEqual(request.call_count, 2)
            self.assertEqual(delay.call_count, 1)

    def test_failure_has_exact_retry_limit(self):
        with patch('http_client.urllib.request.urlopen', side_effect=TimeoutError()), patch('http_client.time.sleep') as delay:
            with self.assertRaises(http_client.APIError):
                http_client.fetch_json('https://example.test')
            self.assertEqual(delay.call_count, 2)

    def test_bad_request_is_not_retried(self):
        error = urllib.error.HTTPError('https://example.test', 400, 'bad', None, None)
        with patch('http_client.urllib.request.urlopen', side_effect=error) as request:
            with self.assertRaises(http_client.APIError):
                http_client.fetch_json('https://example.test')
            self.assertEqual(request.call_count, 1)

    def test_invalid_and_nonobject_json_fail_cleanly(self):
        for body in ['not json', '[]', '{"error": true,"reason":"bad date"}']:
            with self.subTest(body=body), patch('http_client.urllib.request.urlopen', return_value=self.response(body)):
                with self.assertRaises(http_client.APIError):
                    http_client.fetch_json('https://example.test')


class WeatherTests(unittest.TestCase):
    def test_trip_dates_are_requested_exactly(self):
        days = ['2026-10-19', '2026-10-20', '2026-10-21', '2026-10-22', '2026-10-23']
        with patch.object(weather, 'fetch_json', return_value={'daily': {'time': days}}) as request:
            weather.forecast(30.67, 104.07, 5, 'Asia/Shanghai', date(2026, 10, 19), today=date(2026, 10, 11))
            url = request.call_args.args[0]
            self.assertIn('start_date=2026-10-19', url)
            self.assertIn('end_date=2026-10-23', url)

    def test_out_of_range_and_invalid_days_do_not_call_service(self):
        for start, days in [(date(2026, 10, 10), 1), (date(2026, 10, 26), 2), (date(2026, 10, 11), 0), (date(2026, 10, 11), 17)]:
            with self.subTest(start=start, days=days), patch.object(weather, 'fetch_json') as request:
                with self.assertRaises(ValueError):
                    weather.forecast(0, 0, days, start=start, today=date(2026, 10, 11))
                request.assert_not_called()

    def test_missing_and_wrong_dates_are_rejected(self):
        for data in [{}, {'daily': None}, {'daily': {'time': ['2026-10-12']}}]:
            with patch.object(weather, 'fetch_json', return_value=data):
                with self.assertRaises(http_client.APIError):
                    weather.forecast(0, 0, 1, start=date(2026, 10, 11), today=date(2026, 10, 11))

    def test_null_and_missing_columns_have_visible_placeholder(self):
        output = io.StringIO()
        loc = {'name': 'Chengdu', 'country': 'China', 'timezone': 'Asia/Shanghai'}
        with contextlib.redirect_stdout(output):
            weather.print_forecast(loc, {'daily': {'time': ['2026-10-19', '2026-10-20'], 'temperature_2m_max': [None]}})
        self.assertIn('2026-10-20', output.getvalue())
        self.assertIn('暂无数据', output.getvalue())
        self.assertNotIn('晴', output.getvalue())
        self.assertNotIn('0.0', output.getvalue())

    def test_current_uses_current_fields_and_timestamp(self):
        with patch.object(weather, 'fetch_json', return_value={'current': {'time': '2026-10-11T12:00', 'temperature_2m': 20}}) as request:
            result = weather.current(30.67, 104.07, 'Asia/Shanghai')
            self.assertIn('current=temperature_2m', request.call_args.args[0])
            self.assertNotIn('daily=', request.call_args.args[0])
            self.assertEqual(result['current']['time'], '2026-10-11T12:00')

    def test_ambiguous_city_is_not_silently_chosen(self):
        results = [{'name': 'Paris', 'country_code': country, 'latitude': lat, 'longitude': 1, 'timezone': 'UTC'} for country, lat in [('FR', 48), ('US', 33)]]
        with patch.object(weather, 'fetch_json', return_value={'results': results}):
            with self.assertRaisesRegex(ValueError, 'Ambiguous'):
                weather.geocode('Paris')
            self.assertEqual(weather.geocode('Paris', 'FR')['lat'], 48)

    def test_cli_network_failure_returns_json_without_traceback(self):
        with patch.object(sys, 'argv', ['weather', 'current', '--lat', '0', '--lon', '0', '--json']), patch.object(weather, 'fetch_json', side_effect=http_client.APIError('offline')):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(weather.main(), 2)
            self.assertEqual(json.loads(output.getvalue())['status'], 'error')


class CurrencyTests(unittest.TestCase):
    def test_repeated_targets_and_identity_are_preserved(self):
        data = {'date': '2026-10-09', 'base': 'CNY', 'rates': {'JPY': 20, 'USD': .14}}
        with patch.object(currency, 'fetch_json', return_value=data) as request, patch.object(sys, 'argv', ['currency', 'convert', '100', '--from', 'CNY', '--to', 'JPY', '--to', 'USD', 'CNY', '--json']):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(currency.main(), 0)
            self.assertEqual(json.loads(output.getvalue())['rates'], {'JPY': 2000, 'USD': 14, 'CNY': 100})
            self.assertIn('to=JPY%2CUSD', request.call_args.args[0])

    def test_identity_requires_no_network_or_fabricated_rate_date(self):
        with patch.object(currency, 'fetch_json') as request:
            result = currency.conversion(5000, 'CNY', ['CNY'])
            self.assertEqual(result['rates'], {'CNY': 5000})
            self.assertIsNone(result['date'])
            request.assert_not_called()

    def test_unit_rates_keep_small_exchange_rates(self):
        with patch.object(currency, 'fetch_json', return_value={'date': '2026-10-09', 'base': 'JPY', 'rates': {'USD': .0061}}):
            result = currency.conversion(1, 'JPY', ['USD'], round_results=False)
            self.assertEqual(result['rates']['USD'], .0061)

    def test_invalid_amounts_rejected_before_network(self):
        for amount in [-1, float('inf'), float('nan')]:
            with patch.object(currency, 'fetch_json') as request:
                with self.assertRaises(ValueError):
                    currency.conversion(amount, 'CNY', ['USD'])
                request.assert_not_called()

    def test_missing_rates_and_dates_are_errors(self):
        for data in [{'rates': {}}, {'date': 'bad', 'base': 'CNY', 'rates': {'USD': .14}}, {'date': '2026-10-09', 'base': 'CNY', 'rates': {}}]:
            with patch.object(currency, 'fetch_json', return_value=data):
                with self.assertRaises(http_client.APIError):
                    currency.conversion(100, 'CNY', ['USD'])


class CalendarTests(unittest.TestCase):
    def test_five_chengdu_dates_and_monday_warning(self):
        result = calendar.analyze(date(2026, 10, 19), 5, '成都')
        self.assertEqual(len(result['days']), 5)
        self.assertEqual(result['days'][0]['weekday'], '周一')
        self.assertEqual(result['days'][-1]['date'], '2026-10-23')
        self.assertIn('周一闭馆', result['city_hint'])

    def test_invalid_dates_days_and_overflow_fail_cleanly(self):
        for start, days in [(date.today(), -1), (date.today(), 0), (date.today(), 367), (date.max, 2)]:
            with self.assertRaises(ValueError):
                calendar.analyze(start, days, None)
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/holiday_check.py'), '--from', '2026-02-30'], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertNotIn('Traceback', run.stderr)


class EnvironmentTests(unittest.TestCase):
    def test_moving_root_updates_only_owned_block_and_quotes_special_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            rc = Path(folder) / '.zshrc'
            rc.write_text('# my settings\nexport OTHER=abc\nexport ATLAS_ROOT=/old/manual\n')
            target = folder + '/root "quoted" $value `name`'
            environment.update_environment(rc, '/first/root')
            environment.update_environment(rc, target)
            before = rc.read_text()
            environment.update_environment(rc, target)
            self.assertEqual(rc.read_text(), before)
            self.assertEqual(before.count(environment.BEGIN), 1)
            self.assertIn('export OTHER=abc', before)
            result = subprocess.run(['bash', '-c', 'source "$1"; printf "%s" "$ATLAS_ROOT"', 'shell', str(rc)], capture_output=True, text=True)
            self.assertEqual(result.stdout, target)

    def test_incomplete_managed_block_cannot_delete_user_settings(self):
        with tempfile.TemporaryDirectory() as folder:
            rc = Path(folder) / '.zshrc'
            original = environment.BEGIN + "\n# user setting\nexport OTHER=kept\n"
            rc.write_text(original)
            with self.assertRaises(ValueError):
                environment.update_environment(rc, '/new')
            self.assertEqual(rc.read_text(), original)

    def test_legacy_block_is_migrated_and_symlink_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            real = Path(folder) / 'realrc'
            link = Path(folder) / '.zshrc'
            real.write_text('# AtlasAgent (https://github.com/wpfbcr/AtlasAgent)\nexport ATLAS_ROOT="/old"\n# other\n')
            link.symlink_to(real)
            environment.update_environment(link, '/new')
            self.assertTrue(link.is_symlink())
            self.assertIn('# other', real.read_text())
            self.assertNotIn('/old', real.read_text())


class DoctorTests(unittest.TestCase):
    def test_required_failure_returns_nonzero_and_special_path_is_valid_json(self):
        with tempfile.TemporaryDirectory() as folder:
            env = os.environ.copy()
            env['ATLAS_ROOT'] = folder + '/missing"root'
            run = subprocess.run(['bash', str(ROOT / 'scripts/atlas-agent'), 'doctor', '--json', '--offline'], capture_output=True, text=True, env=env)
            self.assertEqual(run.returncode, 1)
            result = json.loads(run.stdout)
            self.assertEqual(result['status'], 'unavailable')
            self.assertFalse(result['scripts'])
            self.assertEqual(result['atlas_root'], env['ATLAS_ROOT'])

    def test_all_nine_skills_and_optional_pdf_are_classified(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(doctor, 'pdf_probe', return_value={'ok': False, 'detail': 'optional dependency missing'}), patch.object(doctor, 'run_probe', return_value={'ok': True, 'detail': ''}):
            dest = Path(folder) / '.codex/skills'
            shutil.copytree(ROOT / 'skills', dest)
            result, code = doctor.diagnose(ROOT, folder)
            self.assertEqual(code, 0)
            self.assertEqual(result['status'], 'degraded')
            self.assertTrue(result['installed_skills']['codex']['ok'])
            (dest / 'currency/SKILL.md').unlink()
            result, code = doctor.diagnose(ROOT, folder)
            self.assertEqual(result['installed_skills']['codex']['missing'], ['currency'])

    def test_online_failure_cannot_report_success(self):
        with patch.object(doctor, 'pdf_probe', return_value={'ok': True, 'detail': ''}), patch.object(doctor, 'run_probe', return_value={'ok': False, 'detail': 'offline'}):
            result, code = doctor.diagnose(ROOT, '/nonexistent')
            self.assertEqual(code, 1)
            self.assertEqual(result['status'], 'unavailable')


try:
    import md2pdf
    import pymupdf
    PDF_AVAILABLE = True
except (ImportError, SystemExit):
    PDF_AVAILABLE = False


@unittest.skipUnless(PDF_AVAILABLE, 'Optional PDF test dependencies require requirements-dev.txt')
class PDFTests(unittest.TestCase):
    def setUp(self):
        try:
            self.font = md2pdf.find_font()
        except ValueError as exc:
            self.skipTest(str(exc))
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name) / 'notes.md.folder'
        self.folder.mkdir()

    def export(self, text):
        source = self.folder / 'input.md'
        source.write_text(text, encoding='utf-8')
        output = Path(md2pdf.convert_file(source, self.font))
        self.assertEqual(output, source.with_suffix('.pdf'))
        reader = pymupdf.open(output)
        self.addCleanup(reader.close)
        text = '\n'.join(page.get_text() for page in reader)
        self.assertNotIn('\x00', text, 'Extraction must preserve actual Unicode text')
        return reader, text

    def test_continuous_lines_and_special_directory_preserve_content(self):
        reader, text = self.export('第一行连续正文\n第二行连续正文\nThird line without blank\n')
        self.assertIn('第二行连续正文', text)
        self.assertIn('Third line without blank', text)

    def test_long_table_and_labels_are_not_truncated(self):
        long = '上午熊猫基地，下午文殊院，晚间返回酒店。' * 12 + '尾部唯一标记'
        reader, text = self.export('| 日期 | 完整行程 | 标签 |\n|---|---|---|\n| D1 | ' + long + ' | 🟢 🟡 🔴 ⚠️ ⭐⭐⭐ |\n')
        self.assertIn('尾部唯一标记', text)
        self.assertIn('[符合已知限制]', text)
        self.assertIn('[需调整并确认]', text)
        self.assertIn('★★★', ''.join(text.split()))

    def test_multipage_table_repeats_heading_and_preserves_last_row(self):
        rows = ['| 日期标题 | 行程内容标题 |', '|---|---|']
        rows.extend('| D{} | {} |'.format(i, '内容完整保留。' * 10) for i in range(50))
        reader, text = self.export('\n'.join(rows))
        self.assertGreater(len(reader), 1)
        self.assertIn('D49', text)
        for page in reader:
            self.assertIn('日期标题', page.get_text())

    def test_table_escaped_pipe_and_empty_first_heading(self):
        reader, text = self.export('| | 内容 |\n|---|---|\n| D1 | 左\\|右 |\n')
        self.assertIn('左|右', text)
        self.assertIn('D1', text)


if __name__ == '__main__':
    unittest.main()
