"""Validate a given dictionary of data or http request with a given set of rules"""

from json import JSONDecodeError
import json
from rest_framework import serializers

class Validator():

    """
    Validate a given dictionary of data or http request with a given set of rules
    """

    def __init__(self, rules, data):

        self._passed = False

        # Convert rules into a serializer object to use for validating
        self.validator = Validator.dict_to_serializer(rules)

        # Convert request into a dict
        if isinstance(data, dict):
            self.data = data
        else:
            self.data = Validator.request_to_dict(data)

        self._validated_fields = {}
        self._errors = {}

    @property
    def validated_fields(self):
        """
        Return the fields that were successfully validated
        """
        return self._validated_fields

    @property
    def passed(self):
        """
        Return whether or not all fields were vaidated successfully
        """
        return self._passed

    @property
    def errors(self):
        """
        Return errors from validation
        """
        return self._errors

    @property
    def original_data(self):
        """
        Return the original data that was passed in
        """
        return self.data

    def validate(self):
        """
        Run the validation rules against the data
        """
        validation = self.validator(data=self.data)

        self._passed = validation.is_valid()

        self._errors = validation.errors

        # Build dict out of fields that passed their validation
        for field in self.data:
            if field not in validation.errors:
                self._validated_fields[field] = self.data[field]

        # return self for method chaining
        return self

    @staticmethod
    def request_to_dict(request):
        """
        Convert an http request to a dict
        """
        data = {}

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('UTF-8'))
            except JSONDecodeError:
                # If the body is empty, then return an empty dict
                return {}

        elif request.method == 'GET':
            data = request.GET
        elif request.method == 'POST':
            data = request.POST

        return data

    @staticmethod
    def dict_to_serializer(attributes):
        """
        Convert a dict of serializer rules into a class with those fields
        """
        return type('validator', (serializers.Serializer,), attributes)
