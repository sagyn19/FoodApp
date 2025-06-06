from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Item, Review
from .forms import ReviewForm

from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class ItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_str_method(self):
        item = Item.objects.create(meal="Pizza", price=100, author=self.user)
        self.assertEqual(str(item), "Pizza")


class ReviewFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            'name': 'John Doe',
            'content': 'Great food!',
            'rating': 5,
            'email': 'john@example.com'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = ReviewForm(data={})
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_menu_list_view(self):
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty content for now
            content_type='image/jpeg'
        )

        item = Item.objects.create(
            meal="Greek Salad",
            meal_type="Salads",
            description="Fresh and tasty",
            price=7.50,
            author=self.user,
            image=image,
        )
        response = self.client.get(reverse('menu_item', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Greek Salad")

    def test_review_submission_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('submit_review'), {
            'name': 'John',
            'content': 'Tasty!',
            'rating': 4,
            'email': 'john@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect
