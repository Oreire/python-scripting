import unittest
from PyCode.order_calculator import calculate_final_price
from unittest.mock import patch
import builtins


class TestCalculateFinalPrice(unittest.TestCase):
    def test_basic_calculation(self):
        """Test calculation with simple known values"""
        result = calculate_final_price(quantity=5, unit_price=10, tax_percentage=20)
        self.assertAlmostEqual(result["subtotal"], 50.0)
        self.assertAlmostEqual(result["tax_amount"], 10.0)
        self.assertAlmostEqual(result["final_price"], 60.0)

    def test_zero_tax(self):
        """Test when tax is zero"""
        result = calculate_final_price(quantity=2, unit_price=30, tax_percentage=0)
        self.assertEqual(result["tax_amount"], 0.0)
        self.assertEqual(result["final_price"], 60.0)

    def test_high_tax(self):
        """Test when tax is unusually high"""
        result = calculate_final_price(quantity=1, unit_price=100, tax_percentage=100)
        self.assertEqual(result["tax_amount"], 100.0)
        self.assertEqual(result["final_price"], 200.0)

    def test_zero_quantity(self):
        """Test when quantity is zero"""
        result = calculate_final_price(quantity=0, unit_price=50, tax_percentage=10)
        self.assertEqual(result["subtotal"], 0.0)
        self.assertEqual(result["tax_amount"], 0.0)
        self.assertEqual(result["final_price"], 0.0)

    def test_negative_quantity(self):
        """Test when quantity is negative"""
        result = calculate_final_price(quantity=-3, unit_price=20, tax_percentage=10)
        self.assertLess(result["subtotal"], 0)
        self.assertLess(result["final_price"], 0)

    def test_negative_unit_price(self):
        """Test when unit price is negative"""
        result = calculate_final_price(quantity=2, unit_price=-50, tax_percentage=15)
        self.assertLess(result["subtotal"], 0)
        self.assertLess(result["final_price"], 0)

    def test_negative_tax(self):
        """Test when tax percentage is negative"""
        result = calculate_final_price(quantity=2, unit_price=100, tax_percentage=-10)
        self.assertLess(result["tax_amount"], 0)
        self.assertLess(result["final_price"], result["subtotal"])

    def test_large_quantity_and_price(self):
        """Test with large values to check for overflow or rounding issues"""
        result = calculate_final_price(quantity=10000, unit_price=999.99, tax_percentage=5)
        self.assertGreater(result["final_price"], 0)
        self.assertAlmostEqual(result["tax_amount"], result["subtotal"] * 0.05, places=2)

    def test_float_precision(self):
        """Test with float values for precision"""
        result = calculate_final_price(quantity=3, unit_price=19.99, tax_percentage=7.5)
        expected_subtotal = 3 * 19.99
        expected_tax = expected_subtotal * 0.075
        expected_final = expected_subtotal + expected_tax
        self.assertAlmostEqual(result["subtotal"], expected_subtotal, places=2)
        self.assertAlmostEqual(result["tax_amount"], expected_tax, places=2)
        self.assertAlmostEqual(result["final_price"], expected_final, places=2)

    def test_missing_arguments(self):
        """Test when required arguments are missing"""
        with self.assertRaises(TypeError):
            calculate_final_price(quantity=2, unit_price=100)  # missing tax_percentage

    def test_non_numeric_inputs(self):
        """Test when inputs are non-numeric"""
        with self.assertRaises(TypeError):
            calculate_final_price(quantity="two", unit_price=100, tax_percentage=10)
        with self.assertRaises(TypeError):
            calculate_final_price(quantity=2, unit_price="hundred", tax_percentage=10)
        with self.assertRaises(TypeError):
            calculate_final_price(quantity=2, unit_price=100, tax_percentage="ten")

    def test_none_inputs(self):
        """Test when inputs are None"""
        with self.assertRaises(TypeError):
            calculate_final_price(quantity=None, unit_price=100, tax_percentage=10)
        with self.assertRaises(TypeError):
            calculate_final_price(quantity=2, unit_price=None, tax_percentage=10)
        with self.assertRaises(TypeError):
            calculate_final_price(quantity=2, unit_price=100, tax_percentage=None)


class TestRunOrderCalculator(unittest.TestCase):
    @patch.object(builtins, 'input', side_effect=["2", "50", "10"])
    def test_run_order_calculator(self, mock_input):
        """Test CLI input flow using mocked input"""
        from PyCode.order_calculator import run_order_calculator
        result = run_order_calculator()
        self.assertEqual(result["quantity"], 2)
        self.assertEqual(result["unit_price"], 50.0)
        self.assertEqual(result["tax_percentage"], 10.0)
        self.assertEqual(result["subtotal"], 100.0)
        self.assertEqual(result["tax_amount"], 10.0)
        self.assertEqual(result["final_price"], 110.0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

