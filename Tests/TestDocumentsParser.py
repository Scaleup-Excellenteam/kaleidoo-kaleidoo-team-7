# Tests/TestDocumentsParser.py

import unittest
from unittest.mock import patch, MagicMock, ANY
import sys
import os

# Adjust the path to include the project root if necessary
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DocumentsParser import (
    extract_text_from_file,
    preprocess_image
)
from PIL import Image, ImageEnhance, ImageFilter


class TestDocumentsParser(unittest.TestCase):
    def setUp(self):
        """
        Set up mocks that are common across multiple test methods.
        """
        # Patch os.path.isfile to always return True by default
        patcher_isfile = patch('DocumentsParser.os.path.isfile', return_value=True)
        self.mock_isfile = patcher_isfile.start()
        self.addCleanup(patcher_isfile.stop)

        # Patch text_processor.add_text
        patcher_add_text = patch('DocumentsParser.text_processor.add_text')
        self.mock_add_text = patcher_add_text.start()
        self.addCleanup(patcher_add_text.stop)

    def test_extract_text_docx(self):
        """
        Test extraction of text from a DOCX file with two headings.
        Ensures that text_processor.add_text is called once for the first entry
        and that the function returns both entries correctly.
        """
        sample_docx = '/path/to/sample.docx'
        
        # Create mock paragraphs
        mock_para1 = MagicMock()
        mock_para1.text = "Heading 1 Title"
        mock_para1.style.name = "Heading 1"

        mock_para2 = MagicMock()
        mock_para2.text = "Paragraph content for heading 1."
        mock_para2.style.name = "Normal"

        mock_para3 = MagicMock()
        mock_para3.text = "Another Heading 1 Title"
        mock_para3.style.name = "Heading 1"

        mock_para4 = MagicMock()
        mock_para4.text = "Paragraph content for heading 2."
        mock_para4.style.name = "Normal"

        mock_doc = MagicMock()
        mock_doc.paragraphs = [mock_para1, mock_para2, mock_para3, mock_para4]

        with patch('DocumentsParser.Document', return_value=mock_doc):
            text, file_type = extract_text_from_file(sample_docx)

            # Verify the returned file type
            self.assertEqual(file_type, "docx")

            # Define expected formatted entries
            expected_entries = [
                "Title: sample.docx | Page: 1 | Content: Paragraph content for heading 1.",
                "Title: Another Heading 1 Title | Page: 2 | Content: Paragraph content for heading 2."
            ]
            expected_text = "\n".join(expected_entries)

            # Verify the returned text matches expected entries
            self.assertEqual(text, expected_text)

            # Verify that add_text was called once with the first entry
            self.mock_add_text.assert_called_once_with(expected_entries[0])

            # Ensure that add_text was not called with the second entry
            self.mock_add_text.assert_any_call(expected_entries[0])
            self.assertEqual(self.mock_add_text.call_count, 1)

    def test_pptx_extraction(self):
        """
        Test extraction of text from a PPTX file.
        """
        sample_pptx = '/path/to/sample.pptx'
        # Create mock shapes with text
        mock_shape1 = MagicMock()
        mock_shape1.text = "Slide 1 Text"

        mock_shape2 = MagicMock()
        mock_shape2.text = "Slide 1 Additional Text"

        mock_shape3 = MagicMock()
        mock_shape3.text = ""

        mock_slide1 = MagicMock()
        mock_slide1.shapes = [mock_shape1, mock_shape2, mock_shape3]

        mock_shape4 = MagicMock()
        mock_shape4.text = "Slide 2 Text"

        mock_slide2 = MagicMock()
        mock_slide2.shapes = [mock_shape4]

        mock_prs = MagicMock()
        mock_prs.slides = [mock_slide1, mock_slide2]

        with patch('DocumentsParser.Presentation', return_value=mock_prs):
            text, file_type = extract_text_from_file(sample_pptx)
            self.assertEqual(file_type, "pptx")
            expected_entries = [
                "Title: sample.pptx | Page: 1 | Content: Slide 1 Text Slide 1 Additional Text",
                "Title: sample.pptx | Page: 2 | Content: Slide 2 Text"
            ]
            expected_text = "\n".join(expected_entries) + "\n"  # Added trailing newline
            self.assertEqual(text, expected_text)
            self.mock_add_text.assert_any_call(expected_entries[0])
            self.mock_add_text.assert_any_call(expected_entries[1])
            self.assertEqual(self.mock_add_text.call_count, 2)

    def test_pdf_extraction(self):
        """
        Test extraction of text from a PDF file.
        """
        sample_pdf = '/path/to/sample.pdf'
        # Create mock pages
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "PDF Page 1 Text"

        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "PDF Page 2 Text"

        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 2
        mock_doc.load_page.side_effect = [mock_page1, mock_page2]

        with patch('DocumentsParser.fitz.open', return_value=mock_doc):
            text, file_type = extract_text_from_file(sample_pdf)
            self.assertEqual(file_type, "pdf")
            expected_entries = [
                "Title: sample.pdf | Page: 1 | Content: PDF Page 1 Text",
                "Title: sample.pdf | Page: 2 | Content: PDF Page 2 Text"
            ]
            expected_text = "\n".join(expected_entries) + "\n"
            self.assertEqual(text, expected_text)
            self.mock_add_text.assert_any_call(expected_entries[0])
            self.mock_add_text.assert_any_call(expected_entries[1])
            self.assertEqual(self.mock_add_text.call_count, 2)

    def test_unsupported_file(self):
        """
        Test handling of unsupported file types.
        Ensures that extract_text_from_file returns empty text,
        sets file_type to "unsupported", and does not call text_processor.add_text.
        """
        unsupported_file = '/path/to/sample.xyz'

        # Patch os.path.splitext to return '.xyz' as the file extension
        with patch('DocumentsParser.os.path.splitext', return_value=('sample', '.xyz')):
            text, file_type = extract_text_from_file(unsupported_file)

            # Assert that the file_type is "unsupported"
            self.assertEqual(file_type, "unsupported", "File type should be 'unsupported' for .xyz extension.")

            # Assert that the returned text is an empty string
            self.assertEqual(text, "", "Text should be empty for unsupported file types.")

            # Assert that text_processor.add_text was not called
            self.mock_add_text.assert_not_called()

    def test_empty_pdf_extraction(self):
        """
        Test extraction from an empty PDF file.
        """
        sample_pdf = '/path/to/empty.pdf'
        empty_text = ""

        # Create a mock PDF with no text
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 0

        with patch('DocumentsParser.fitz.open', return_value=mock_doc):
            text, file_type = extract_text_from_file(sample_pdf)
            self.assertEqual(file_type, "pdf")
            self.assertIsNone(text)
            self.mock_add_text.assert_not_called()

    def test_preprocess_image(self):
        """
        Test the image preprocessing function.
        """
        sample_image = '/path/to/sample_image.jpg'
        expected_preprocessed_image = MagicMock(spec=Image.Image)

        # Mock the Image.open and subsequent methods
        with patch('DocumentsParser.Image.open', return_value=MagicMock(spec=Image.Image)) as mock_open:
            mock_image = mock_open.return_value
            mock_image.convert.return_value = mock_image
            mock_image.filter.return_value = mock_image
            mock_contrast = MagicMock(spec=ImageEnhance.Contrast)
            with patch('DocumentsParser.ImageEnhance.Contrast', return_value=mock_contrast):
                mock_contrast.enhance.return_value = expected_preprocessed_image
                # Mock the point method on expected_preprocessed_image
                expected_preprocessed_image.point.return_value = expected_preprocessed_image

                preprocessed_image = preprocess_image(sample_image)

                # Assertions to ensure each step was called correctly
                mock_open.assert_called_once_with(sample_image)
                mock_image.convert.assert_called_once_with('L')
                mock_image.filter.assert_called_once_with(ANY)  # Using ANY for flexibility
                mock_contrast.enhance.assert_called_once_with(2)
                expected_preprocessed_image.point.assert_called_once_with(ANY, '1')  # Using ANY for the lambda
                self.assertEqual(preprocessed_image, expected_preprocessed_image)

    def test_extract_text_from_image_preprocessing_failed(self):
        """
        Test extraction from an image when preprocessing fails.
        """
        sample_image = '/path/to/sample_image.jpg'

        with patch('DocumentsParser.preprocess_image', return_value=None) as mock_preprocess_image:
            text, file_type = extract_text_from_file(sample_image)
            # Since preprocess_image is called once in the current code
            self.assertEqual(mock_preprocess_image.call_count, 1)
            mock_preprocess_image.assert_called_with(sample_image)
            self.assertEqual(file_type, "preprocessing_failed")
            self.assertEqual(text, "")
            self.mock_add_text.assert_not_called()

    def test_preprocess_image_exception(self):
        """
        Test that preprocess_image handles exceptions gracefully.
        """
        sample_image = '/path/to/sample_image.jpg'

        with patch('DocumentsParser.Image.open', side_effect=Exception("Mocked exception")):
            preprocessed_image = preprocess_image(sample_image)
            self.assertIsNone(preprocessed_image)
            self.mock_add_text.assert_not_called()


if __name__ == '__main__':
    unittest.main()
