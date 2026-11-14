import json
import unittest
from gemini_client import RequestBudget, synthesize
from evidence import load_data

class GeminiTests(unittest.TestCase):
    def setUp(self):
        self.data = load_data()
        self.config = {'GEMINI_ENABLED': True, 'GEMINI_API_KEY': 'test-placeholder', 'GEMINI_MODEL': 'gemini-test'}
        self.items = [{'kind': 'summary', 'text': 'Smoke particle sizes were measured.', 'claim_ids': ['same_purpose']}, {'kind': 'limitation', 'text': 'These data do not certify a detector.', 'claim_ids': ['same_detection']}]

    def transport(self, items=None, finish='STOP'):
        return lambda *args: {'candidates': [{'finishReason': finish, 'content': {'parts': [{'text': json.dumps({'items': self.items if items is None else items})}]}}]}

    def test_success_uses_fixed_host_and_only_selected_evidence(self):
        def send(url, payload, key):
            self.assertEqual(url, 'https://generativelanguage.googleapis.com/v1beta/models/gemini-test:generateContent')
            self.assertNotIn('tools', payload)
            self.assertNotIn(key, json.dumps(payload))
            self.assertLess(payload['generationConfig']['maxOutputTokens'], 2000)
            return self.transport()(url, payload, key)
        result = synthesize('smoke detection', self.data, self.config, send, RequestBudget())
        self.assertEqual(result['ai_items'], self.items)
        self.assertIn('Gemini', result['mode'])

    def test_disabled_missing_key_and_unsupported_never_call(self):
        def fail(*args):
            self.fail('Must not call a provider')
        for config in [{}, {**self.config, 'GEMINI_ENABLED': False}, {**self.config, 'GEMINI_API_KEY': ''}]:
            self.assertFalse(synthesize('smoke detection', self.data, config, fail)['ai_items'])
        self.assertFalse(synthesize('football champions', self.data, self.config, fail)['ai_items'])

    def test_failures_return_local_evidence_and_hide_exception(self):
        def fail(*args):
            raise TimeoutError('sensitive error details')
        for transport in [fail, self.transport(finish='MAX_TOKENS'), self.transport([])]:
            result = synthesize('smoke detection', self.data, self.config, transport, RequestBudget())
            self.assertTrue(result['claim_ids'])
            self.assertFalse(result['ai_items'])
            self.assertNotIn('sensitive', str(result))

    def test_invalid_citations_numbers_links_rejected(self):
        for changes in [{'claim_ids':['invented']}, {'text':'Set oxygen to 99 percent.'}, {'text':'https://evil.example'}, {'text':'<script>bad</script>'}, {'kind':'instruction'}]:
            items = [{**self.items[0], **changes}, self.items[1]]
            result = synthesize('smoke detection', self.data, self.config, self.transport(items), RequestBudget())
            self.assertFalse(result['ai_items'])

    def test_model_cannot_change_host(self):
        config = {**self.config, 'GEMINI_MODEL':'../evil?key=x'}
        self.assertFalse(synthesize('smoke detection', self.data, config, lambda *a: self.fail())['ai_items'])

    def test_process_limits(self):
        budget = RequestBudget()
        for i in range(5): self.assertTrue(budget.reserve(i))
        self.assertFalse(budget.reserve(5))
        self.assertTrue(budget.reserve(61))
        budget = RequestBudget()
        for i in range(100): self.assertTrue(budget.reserve(i * 61))
        self.assertFalse(budget.reserve(6100))
        self.assertTrue(budget.reserve(86401))

class GeminiInterfaceTests(unittest.TestCase):
    def test_enabled_provider_requires_opt_in_and_renders_safely(self):
        from pathlib import Path
        from unittest.mock import patch
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'))
        app.secrets['GEMINI_ENABLED'] = True
        app.secrets['GEMINI_API_KEY'] = 'test-placeholder'
        app.secrets['GEMINI_MODEL'] = 'gemini-test'
        app.run().radio[0].set_value('Ask').run()
        with patch('gemini_client.synthesize') as synth:
            app.button[0].click().run()
            synth.assert_not_called()
        self.assertFalse(app.exception)
        app.session_state['requests'] = []
        with patch('gemini_client.synthesize', return_value={
            'mode':'Gemini-generated synthesis', 'notice':'', 'results':[], 'claim_ids':[],
            'ai_items':[{'kind':'summary', 'text':'Smoke evidence is relevant.', 'claim_ids':['same_detection']}]
        }) as synth:
            app.checkbox[0].check().run()
            app.button[0].click().run()
            synth.assert_called_once()
        self.assertFalse(app.exception)
        self.assertTrue(any(x.value == 'Smoke evidence is relevant.' for x in app.text))
