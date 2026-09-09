import unittest
from backend.ai_assistant import process_chat_message, generate_expert_response, extract_khasra_numbers
from backend.routes import chat_with_assistant, get_chat_suggestions
from fastapi import HTTPException

class TestAIAssistant(unittest.TestCase):

    def test_extract_khasra_numbers(self):
        k1 = extract_khasra_numbers("What is the dispute with Khasra 102?")
        self.assertIn("102", k1)

        k2 = extract_khasra_numbers("Check Survey No. 105/2 and plot 44")
        self.assertTrue("105/2" in k2 or "105" in k2)
        self.assertIn("44", k2)

        k3 = extract_khasra_numbers("खसरा संख्या 101 की जानकारी दें")
        self.assertIn("101", k3)

    def test_record_lookup_khasra_102_disputed(self):
        res = process_chat_message("Tell me about Khasra 102", role="REVENUE_OFFICER")
        self.assertIn("reply", res)
        self.assertIn("102", res["reply"])
        self.assertIn("DISPUTED", res["reply"])
        self.assertTrue(len(res["suggested_actions"]) >= 2)
        # Check action labels
        action_labels = [a["label"] for a in res["suggested_actions"]]
        self.assertTrue(any("Cadastral Map" in lbl for lbl in action_labels))
        self.assertTrue(any("Inspect Record" in lbl for lbl in action_labels))

    def test_record_lookup_khasra_101_clear(self):
        res = process_chat_message("Is Khasra 101 clear and free of disputes?", role="CITIZEN_FARMER")
        self.assertIn("reply", res)
        self.assertIn("101", res["reply"])
        self.assertIn("Rajesh Verma", res["reply"])
        self.assertTrue("CLEAR" in res["reply"] or "विवाद-मुक्त" in res["reply"] or "Clear" in res["reply"])

    def test_demarcation_and_boundary_overlap(self):
        res = process_chat_message("How do I resolve boundary encroachment and get demarcation?", role="REVENUE_OFFICER")
        self.assertIn("reply", res)
        reply = res["reply"]
        self.assertTrue("Section 24" in reply or "Demarcation" in reply or "सीमांकन" in reply)
        self.assertTrue("ETS" in reply or "Electronic Total Station" in reply or "Survey" in reply)
        action_tabs = [a.get("tab") for a in res["suggested_actions"] if "tab" in a]
        self.assertTrue("disputes" in action_tabs or "map" in action_tabs)

    def test_mutation_dakhil_kharij(self):
        res = process_chat_message("What is the process for land mutation (Dakhil Kharij)?", role="CITIZEN_FARMER")
        self.assertIn("reply", res)
        reply = res["reply"]
        self.assertTrue("Mutation" in reply or "नामांतरण" in reply or "दाखिल-खारिज" in reply)
        self.assertTrue("Form 35" in reply or "Sale Deed" in reply or "Khatauni" in reply or "दस्तावेज़" in reply)

    def test_bank_loan_diligence(self):
        res = process_chat_message("Can this land be mortgaged for a bank loan?", role="BANK_OFFICER")
        self.assertIn("reply", res)
        reply = res["reply"]
        self.assertTrue("Bank" in reply or "Mortgage" in reply or "Encumbrance" in reply or "ऋण" in reply)
        self.assertTrue("Non-Encumbrance" in reply or "EC" in reply or "Title" in reply)

    def test_hindi_query_handling(self):
        res = process_chat_message("मेरी जमीन पर मेड़ का विवाद है, धारा 24 सीमांकन कैसे कराएं?", role="CITIZEN_FARMER")
        self.assertIn("reply", res)
        reply = res["reply"]
        # Verify Hindi response
        self.assertTrue("सीमांकन" in reply or "राजस्व" in reply or "पैमाइश" in reply)

    def test_routes_chat_and_suggestions(self):
        # Test endpoint function
        res = chat_with_assistant({"message": "Status of Khasra 102", "user_role": "REVENUE_OFFICER"})
        self.assertIn("reply", res)
        self.assertIn("suggested_actions", res)

        # Test empty message error
        with self.assertRaises(HTTPException):
            chat_with_assistant({"message": "   "})

        # Test suggestions
        sugg = get_chat_suggestions("CITIZEN_FARMER")
        self.assertEqual(sugg["role"], "CITIZEN_FARMER")
        self.assertTrue(len(sugg["suggestions"]) >= 5)

    def test_faq_matching_khasra_number(self):
        res = process_chat_message("What is a Khasra number?", role="CITIZEN_FARMER")
        self.assertIn("reply", res)
        self.assertEqual(res.get("matched_faq_id"), "faq-rec-02")
        self.assertEqual(res.get("faq_category"), "Land Records")
        self.assertEqual(res.get("source"), "bhoomi-faq-knowledge-engine")
        self.assertTrue(len(res["suggested_questions"]) >= 1)

    def test_faq_matching_daughters_inheritance(self):
        res = process_chat_message("Can daughters inherit ancestral agricultural land?", role="CITIZEN_FARMER")
        self.assertIn("reply", res)
        self.assertEqual(res.get("matched_faq_id"), "faq-inh-03")
        self.assertEqual(res.get("faq_category"), "Inheritance")

    def test_faq_api_routes(self):
        from backend.routes import get_faq_categories, get_popular_faqs, search_faq_database, get_faq_by_id
        
        # Categories
        cats = get_faq_categories()
        self.assertEqual(len(cats["categories"]), 14)
        
        # Popular
        pop = get_popular_faqs()
        self.assertEqual(len(pop["popular_faqs"]), 18)
        
        # Search
        search_res = search_faq_database(q="khasra")
        self.assertTrue(search_res["count"] >= 1)
        
        # Get by ID
        faq = get_faq_by_id("faq-rec-02")
        self.assertEqual(faq["id"], "faq-rec-02")
        
        # 404 for invalid ID
        with self.assertRaises(HTTPException):
            get_faq_by_id("faq-nonexistent-999")

if __name__ == "__main__":
    unittest.main()
