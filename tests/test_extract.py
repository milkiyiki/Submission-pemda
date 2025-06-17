import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from utils.extract import extract_fashion_data, fetching_content, scrape_fashion

class TestFashionExtraction(unittest.TestCase):
    def setUp(self):
        self.sample_html = '''
            <div class="product-details">
                <h3 class="product-title">Sample Jacket</h3>
                <div class="price-container"><span class="price">$49.99</span></div>
                <p>Rating: ⭐ 4.7 / 5</p>
                <p>3 Colors</p>
                <p>Size: L</p>
                <p>Gender: Men</p>
            </div>
        '''
        soup = BeautifulSoup(self.sample_html, 'html.parser')
        self.product_block = soup.find('div', class_='product-details')

    def test_extract_single_product(self):
        extracted = extract_fashion_data(self.product_block)
        expected = {
            "Title": "Sample Jacket",
            "Price": "$49.99",
            "Rating": "Rating: ⭐ 4.7 / 5",
            "Colors": "3 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Men"
        }
        self.assertEqual(extracted, expected)

    @patch("utils.extract.requests.Session.get")
    def test_fetching_content(self, mock_get):
        html = "<html><body><h1>Hello</h1></body></html>"
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = html.encode("utf-8")
        mock_get.return_value = mock_resp

        result = fetching_content("https://fakeurl.com")
        self.assertIn(b"Hello", result)

    @patch("utils.extract.fetching_content")
    def test_scrape_fashion(self, mock_fetching_content):
        mock_fetching_content.return_value = f'''
            <div class="product-details">
                <h3 class="product-title">Sample Hoodie</h3>
                <div class="price-container"><span class="price">$59.99</span></div>
                <p>Rating: ⭐ 4.5 / 5</p>
                <p>2 Colors</p>
                <p>Size: M</p>
                <p>Gender: Women</p>
            </div>
        '''
        result = scrape_fashion("https://fashion-studio.dicoding.dev/page{}")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("Title", result[0])
        self.assertEqual(result[0]["Title"], "Sample Hoodie")

if __name__ == "__main__":
    unittest.main()