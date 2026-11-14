import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from evidence import load_data, study_by_id
from insights import INSIGHTS, evidence_coverage, ranked_insights, ranking_breakdown

APP = Path(__file__).resolve().parents[1] / 'app.py'

class InsightTests(unittest.TestCase):
    def test_every_interpretation_has_existing_source_basis(self):
        data = load_data()
        for insight in INSIGHTS.values():
            self.assertTrue(insight['basis'])
            for ref in insight['basis']:
                claim = data['claims'][ref]
                self.assertIn(claim['source_id'], data['sources'])
                self.assertTrue(claim['locator'])

    def test_rank_arithmetic_and_demo(self):
        data = load_data()
        for query in ['smoke detection', 'solid flame spread', 'liquid droplet suppression']:
            rows = ranked_insights(query, data)
            self.assertTrue(rows)
            for result, _ in rows:
                self.assertEqual(sum(ranking_breakdown(query, data, result).values()), result.score)
        self.assertEqual(ranked_insights('smoke detection', data)[0][0].study_id, 'same')
        self.assertEqual(ranked_insights('football champions', data), [])
        self.assertEqual(evidence_coverage(data, study_by_id(data, 'flex'))['Published statements'], 0)

    def test_insights_journey_and_gravity_limit(self):
        app = AppTest.from_file(str(APP)).run()
        self.assertFalse(app.exception)
        self.assertIn('SAME-R', app.subheader[0].value)
        self.assertTrue(any('Prepared Team Thu' in x.value for x in app.caption))
        links = [x.proto.url for x in app.get('link_button')]
        self.assertIn('https://ntrs.nasa.gov/citations/20140006579', links)
        app.selectbox[2].select('Moon surface').run()
        self.assertFalse(app.exception)
        self.assertTrue(any('do not validate' in x.value for x in app.warning))
        app.selectbox[0].select('Liquid droplet suppression').run()
        self.assertFalse(app.exception)
        self.assertTrue(any('FLEX' in x.value for x in app.subheader))
        app.selectbox[0].select('Custom question').run()
        app.text_input[0].set_value('football champions').run()
        self.assertTrue(any('No matching evidence' in x.value for x in app.info))
        self.assertEqual(len(app.subheader), 0)

    def test_weak_overlap_withholds_interpretation(self):
        app = AppTest.from_file(str(APP)).run()
        app.text_input[0].set_value('smoke football astronomy champions').run()
        self.assertFalse(app.exception)
        self.assertFalse(any('Prepared Team Thu' in x.value for x in app.caption))

if __name__ == '__main__':
    unittest.main()
