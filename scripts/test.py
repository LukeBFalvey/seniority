from seniority_lib import *
import unittest

class TestSeniorityResolver(unittest.TestCase):
    
    def setUp(self):
        self.resolver = SeniorityResolver()
    
    def test_lower_job_title(self):
        self.assertEquals(self.resolver.lower_job_title('ALL CAPS'), 'all caps')
        self.assertEquals(self.resolver.lower_job_title(1), None)

    def test_resolve_abbreviations(self):
        self.assertEquals(self.resolver.resolve_abbreviations('a v p electorate'), 'associate vice president electorate')
        
    def test_correct_spelling(self):
        self.assertEqual(self.resolver.correct_spelling('assistnt professor'), 'assistant professor')
        
    def test_get_seniority(self):
        self.assertEqual(self.resolver.get_seniority_title('assistant eterny professor'), ['assistant', 'professor'])
        
        
if __name__ == '__main__':
    unittest.main()