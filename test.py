import unittest

from .wikipedia_search import get_random_wiki_page, get_split_content, calculate_tfidf, rank_relevant_articles

class TestRandomPage(unittest.TestCase):
    def test_get_page(self):
        
        page1 = get_random_wiki_page()

        self.assertNotEqual(page1.text, "")

    def test_different_pages(self):
        
        page1 = get_random_wiki_page()
        page2 = get_random_wiki_page()

        self.assertNotEqual(page1.text, page2.text)

class TestSplitContent(unittest.TestCase):
    def test_get_data(self):

        N = 5
        titles, h2s, h3s, paragraphs = get_split_content(N)
        
        self.assertEqual(len(titles), N)
        self.assertEqual(len(h2s), N)
        self.assertEqual(len(h3s), N)
        self.assertEqual(len(paragraphs), N)

class TestTfidf(unittest.TestCase):
    def test_get_tfidf_values(self):

        ''' Values for the test sentences
        are        0.000000  0.317806  0.000000
        each       0.000000  0.241700  0.191320
        for        0.349578  0.187701  0.148577
        it         0.000000  0.000000  0.251562
        making     0.000000  0.317806  0.000000
        of         0.000000  0.000000  0.251562
        return     0.000000  0.000000  0.251562
        returned   0.000000  0.317806  0.000000
        right      0.000000  0.317806  0.000000
        runs       0.000000  0.000000  0.251562
        same       0.000000  0.000000  0.503125
        sentences  0.450145  0.000000  0.191320
        should     0.000000  0.000000  0.251562
        sure       0.000000  0.317806  0.000000
        testing    0.591887  0.000000  0.000000
        text       0.000000  0.317806  0.000000
        tfidf      0.450145  0.000000  0.191320
        the        0.349578  0.375403  0.445730
        time       0.000000  0.317806  0.000000
        values     0.000000  0.241700  0.191320
        with       0.000000  0.000000  0.251562
        ''' 

        test_sentences = ["Testing sentences for the tfidf", "Making sure the right values are returned for the text each time", "For each of the tfidf runs with the same sentences it should return the same values"]
        df = calculate_tfidf(test_sentences)

        self.assertEqual(df[0][0], 0)
        self.assertEqual(df[2][1], 0.1913196914824386)
        self.assertEqual(df[1][4], 0.31780584226035524)
        self.assertEqual(df[2][10], 0.503124805647583)

class TestRankArticles(unittest.TestCase):
    def test_article_rank(self):

        N = 3
        test_sentences = ["Testing sentences for the tfidf", "Making sure the right values are returned for the text each time", "For each of the tfidf runs with the same sentences it should return the same values"]
        wiki_df = calculate_tfidf(test_sentences)
        similarity_scores = rank_relevant_articles("tfidf testing the values are right", wiki_df, N)

        self.assertEqual(similarity_scores[0], 0.5373951611180742)
        self.assertEqual(similarity_scores[1], 0.49049589273438005)
        self.assertEqual(similarity_scores[2], 0.26111874782736955)

if __name__ == '__main__':
    unittest.main()