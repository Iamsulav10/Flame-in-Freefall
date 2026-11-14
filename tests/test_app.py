import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


class AppJourneyTests(unittest.TestCase):
    def app(self):
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        self.assertFalse(app.exception)
        app.radio[0].set_value("Ask").run()
        return app

    def test_demo_question_and_source_links(self):
        app = self.app()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["answer"]["results"][0].study_id, "same")
        links = [button.proto.url for button in app.get("link_button")]
        self.assertIn("https://ntrs.nasa.gov/citations/20130000422", links)
        self.assertIn("https://psi.nasa.gov/physci/repo/data/investigations/PSI-101", links)
        self.assertTrue(any("Inspect SAME-R" in expander.label for expander in app.expander))

    def test_unsupported_question(self):
        app = self.app()
        app.text_area[0].set_value("Who won the football world cup?")
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("No matching evidence" in item.value for item in app.info))

    def test_explore_filters_and_search(self):
        app = self.app()
        app.radio[0].set_value("Explore").run()
        app.selectbox[0].select("Detection").run()
        self.assertFalse(app.exception)
        self.assertEqual([item.value for item in app.subheader], ["SAME-R"])
        app.text_input[0].set_value("droplets").run()
        self.assertTrue(any("No match" in item.value for item in app.info))

    def test_all_comparison_pairs_and_missing_values(self):
        app = self.app()
        app.radio[0].set_value("Compare").run()
        for first in ["bass", "same", "flex", "saffire"]:
            app.selectbox[0].set_value(first).run()
            for second in [i for i in ["bass", "same", "flex", "saffire"] if i != first]:
                app.selectbox[1].set_value(second).run()
                self.assertFalse(app.exception)
                self.assertTrue(any(item.value == "Not reported" for item in app.text))
        self.assertTrue(any("different materials" in item.value for item in app.info))

    def test_sources_and_privacy_view(self):
        app = self.app()
        app.radio[0].set_value("Sources & privacy").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.expander), 9)

    def test_user_html_remains_plain_text(self):
        app = self.app()
        question = '<script>alert("x")</script> smoke detection'
        app.text_area[0].set_value(question)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(item.value == question for item in app.text))
        self.assertFalse(any(question in item.value for item in app.markdown))


if __name__ == "__main__":
    unittest.main()
