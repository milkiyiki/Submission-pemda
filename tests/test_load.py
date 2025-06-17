import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import store_to_csv, store_to_postgre, store_to_sheets

class LoadFunctionalityTests(unittest.TestCase):

    def setUp(self):
        self.sample_data = pd.DataFrame({
            'Title': ['Product A', 'Product B'],
            'Price': [1600000, 2000000],
            'Rating': [4.5, 4.0],
            'Colors': [3, 2],
            'Size': ['M', 'L'],
            'Gender': ['Men', 'Women'],
            'Extraction_Timestamp': ['2024-06-12 12:00:00', '2024-06-12 12:00:00']
        })

    def test_csv_storage(self):
        try:
            store_to_csv(self.sample_data)
        except Exception as err:
            self.fail(f"store_to_csv raised an unexpected error: {err}")

    @patch("utils.load.create_engine")
    def test_postgre_storage(self, mock_engine_creator):
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_engine_creator.return_value = mock_engine

        try:
            store_to_postgre(
                self.sample_data,
                "postgresql+psycopg2://postgres:postgres@localhost:5432/fashiondb"
            )
        except Exception as err:
            self.fail(f"store_to_postgre raised an unexpected error: {err}")

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_google_sheets_storage(self, mock_creds_loader, mock_build_func):
        fake_service = MagicMock()
        fake_sheet = MagicMock()
        value_handler = MagicMock()
        value_handler.update.return_value.execute.return_value = {}

        fake_sheet.values.return_value = value_handler
        fake_service.spreadsheets.return_value = fake_sheet
        mock_build_func.return_value = fake_service
        mock_creds_loader.return_value = MagicMock()

        try:
            store_to_sheets(self.sample_data)
            value_handler.update.assert_called_once()
        except Exception as err:
            self.fail(f"store_to_sheets raised an unexpected error: {err}")

if __name__ == "__main__":
    unittest.main()