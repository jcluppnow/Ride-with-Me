# pylint:disable=unused-import
# Temporary linter disable. Remove this once test cases have been defined.
"""
Tests for the Ride with Me back-end application.
"""
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from application.models import Event

class EventModelTestCases(TestCase):
    """
    Tests for the event model
    """

    def test_average_speed_negative(self):
        """Test that validation fails if the average speed is negative"""
        event = Event(average_speed=-1)

        try:
            event.full_clean()
        except ValidationError as error:
            self.assertTrue('average_speed' in error.message_dict)

    def test_average_speed_zero(self):
        """Test that validation fails if the average speed is zero"""
        event = Event(average_speed=0)

        try:
            event.full_clean()
        except ValidationError as error:
            self.assertTrue('average_speed' in error.message_dict)

    def test_average_speed_gt_zero(self):
        """Test that validation succeeds if the average speed is greater than zero"""
        event = Event(average_speed=1)

        try:
            event.full_clean()
        except ValidationError as error:
            self.assertFalse('average_speed' in error.message_dict)

    def test_max_participants_zero(self):
        """Test that validation fails if the max participants is zero"""
        event = Event(max_participants=0)

        try:
            event.full_clean()
        except ValidationError as error:
            self.assertTrue('max_participants' in error.message_dict)

    def test_max_participants_gt_zero(self):
        """Test that validation succeeds if the max participants is one"""
        event = Event(max_participants=1)

        try:
            event.full_clean()
        except ValidationError as error:
            self.assertFalse('max_participants' in error.message_dict)

    def test_starting_time_in_past(self):
        """Test that validation fails if the start time is in the past"""
        test_time = timezone.now() - timedelta(hours=1)
        event = Event(starting_time=test_time)

        try:
            event.full_clean()
        except ValidationError as error:
            self.assertTrue('starting_time' in error.message_dict)

    def test_starting_time_in_future(self):
        """Test that validation succeeds if the start time is in the future"""
        test_time = timezone.now() + timedelta(hours=1)
        event = Event(starting_time=test_time)

        try:
            event.full_clean()
        except ValidationError as error:
            self.assertFalse('starting_time' in error.message_dict)
