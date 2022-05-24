"""
Contains mock objects
"""

class MockReverseGeocoder(): # pylint: disable=too-few-public-methods
    """Mock ReverseGeocoder with search function"""

    @staticmethod
    def search(arg): # pylint: disable=unused-argument
        """
        Return hardcoded search result
        """
        return [{
            'name': 'Suburb',
            'admin1': 'City'
        }]
