from django.test import TestCase, Client
from lists.models import Item, List
from django.core.exceptions import ValidationError

class ListAndItemModelTest(TestCase):
    Client = Client()

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')


class ListModelTest(TestCase):
    Client = Client()

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list = list_, text = '')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create();
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text = 'bla', list = list_)
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_items_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text = 'bla', list = list1)
        item = Item(list = list2, text='bla')
        item.full_clean() #should not raise

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(text = 'i1', list=list_)            
        item2 = Item.objects.create(text = 'item 2', list=list_)            
        item3 = Item.objects.create(text = 'i3', list=list_)            
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')