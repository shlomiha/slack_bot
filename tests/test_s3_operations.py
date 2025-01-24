import unittest
from unittest.mock import patch, MagicMock
from python_library.s3_operations import add_record, retrieve_record, download_db

class TestS3Operations(unittest.TestCase):
    @patch("my_library.s3_operations.boto3.client")
    def test_add_record(self, mock_boto3_client):
        # Mock S3 client and response
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        # Simulate fetching the CSV content from S3
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: "Name,Phone,Email\nJohn,1234567890,john@example.com\n")
        }

        # Simulate writing updated content back to S3
        bucket_name = "test-bucket"
        object_key = "test.csv"
        new_row = ["Jane", "9876543210", "jane@example.com"]

        add_record(bucket_name, object_key, new_row)

        # Verify the put_object method was called with the updated content
        mock_s3.put_object.assert_called_once()
        args, kwargs = mock_s3.put_object.call_args
        self.assertIn("Body", kwargs)
        self.assertIn("Jane,9876543210,jane@example.com", kwargs["Body"])

    @patch("my_library.s3_operations.boto3.client")
    def test_retrieve_record(self, mock_boto3_client):
        # Mock S3 client and response
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        # Simulate fetching the CSV content from S3
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: "Name,Phone,Email\nJohn,1234567890,john@example.com\n")
        }

        bucket_name = "test-bucket"
        object_key = "test.csv"
        name = "John"

        result = retrieve_record(bucket_name, object_key, name)

        # Check the retrieved record
        self.assertEqual(result, ["John", "1234567890", "john@example.com"])

    @patch("my_library.s3_operations.boto3.client")
    def test_retrieve_record_not_found(self, mock_boto3_client):
        # Mock S3 client and response
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        # Simulate fetching the CSV content from S3
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: "Name,Phone,Email\nJohn,1234567890,john@example.com\n")
        }

        bucket_name = "test-bucket"
        object_key = "test.csv"
        name = "Jane"

        result = retrieve_record(bucket_name, object_key, name)

        # Check that no record was found
        self.assertIsNone(result)

    @patch("my_library.s3_operations.boto3.client")
    def test_download_db(self, mock_boto3_client):
        # Mock S3 client and response
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        bucket_name = "test-bucket"
        object_key = "test.csv"
        local_file = "downloaded_test.csv"

        download_db(bucket_name, object_key, local_file)

        # Verify the download_file method was called with correct arguments
        mock_s3.download_file.assert_called_once_with(bucket_name, object_key, local_file)

if __name__ == "__main__":
    unittest.main()
