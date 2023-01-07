from django.test import TestCase, Client

from .models import User, friend_request

# Create your tests here.
class FriendTestCase(TestCase):

    def setUp(self):
        # Create Users
        u1 = User.objects.create(username="AAA")
        u1.set_password("AAA")
        u1.save()
        u2 = User.objects.create_user("BBB", "B@B.com", "BBB")
        u3 = User.objects.create_user("CCC", "C@C.com", "CCC")
        u1.friends.add(u2)
        u2.friends.add(u1)
        u2.friends.add(u2)

        # Create requests
        friend_request.objects.create(requestor=u1, requested=u2)
        friend_request.objects.create(requestor=u2, requested=u2)
        friend_request.objects.create(requestor=u3, requested=u1)


    def test_valid_request(self):
        u1 = User.objects.get(username="AAA")
        u2 = User.objects.get(username="BBB")
        f = friend_request.objects.get(requestor=u1, requested=u2)
        self.assertTrue(f.is_valid_request())

    def test_invalid_request(self):
        u2 = User.objects.get(username="BBB")
        f = friend_request.objects.get(requestor=u2, requested=u2)
        self.assertFalse(f.is_valid_request())

    def test_valid_friends(self):
        u1 = User.objects.get(username="AAA")
        self.assertTrue(u1.is_valid_friend())

    def test_invalid_friends(self):
        u2 = User.objects.get(username="BBB")
        self.assertFalse(u2.is_valid_friend())

    def test_explore_page(self):
        c = Client()
        u1 = c.login(username="AAA", password="AAA")
        response = c.get("/explore")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["users"].count(), 3)

    def test_notification_page(self):
        c = Client()
        u1 = c.login(username="AAA", password="AAA")
        response = c.get("/notifications")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["reqs"].count(), 1)

    def test_friends_page(self):
        c = Client()
        u1 = c.login(username="AAA", password="AAA")
        response = c.get("/friends")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["friends"].count(), 1)
    