from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

"""
Mocking with patch:
1) Mock is used to change the default return value of a method at certain parts of the code.
2) This is mainly used in unit tests where we want to mock when certain parts of the code that require external connections. For example, we may want to mock that a database is connected without actually connecting.
3) This can also be used to counting the number of calls made to a method.
Sometimes databases can take long time to connect. 

We may not want to actually connect to a database while testing. In such cases, we can mock a database connection. To do this, we have to dig into the source code to find out what happens when connections['default'] is called. The connections attribute is defined in Django/db/__init__.py as 
"connections = ConnectionHandler()" 
connections['default'] calls the __getitem__ method in ConnectionHandler class(which is defined in jango/db/utils and import to Django/db/__init__.py). In this case, we see that the __getitem__ method has been redefined in the ConnectionHandler class by patch for macking its value, as following code.
"""

class CommandsTestCase(TestCase):

    # check if the command works when db is available
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)
    
    # check if command works when db is not connected.
    # by default, we ll have sleep function to wait for 1s if database is not available
    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts):
        # make the patch return error for first five calls
        # and return true on sixth call
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)