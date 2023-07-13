from django.db import models, DataError

from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    """
           This class represents an Order. \n
           Attributes:
           -----------
           param book: foreign key Book
           type book: ForeignKey
           param user: foreign key CustomUser
           type user: ForeignKey
           param created_at: Describes the date when the order was created. Can't be changed.
           type created_at: int (timestamp)
           param end_at: Describes the actual return date of the book. (`None` if not returned)
           type end_at: int (timestamp)
           param plated_end_at: Describes the planned return period of the book (2 weeks from the moment of creation).
           type plated_end_at: int (timestamp)
       """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, blank=True)
    plated_end_at = models.DateTimeField(default=None)

    def __str__(self):
        """
        Magic method is redefined to show all information about Order.
        :return: book id, book name, book description, book count, book authors
        """
        if not self.end_at:
            return f"'id': {self.book.id}, 'user': {repr(self.user)}, 'book': {repr(self.book)}, " \
                f"'created_at': '{self.created_at}', 'end_at': {self.end_at}, " \
                f"'plated_end_at': '{self.plated_end_at}'"
        else:
            return f"'id': {self.book.id}, 'user': {repr(self.user)}, 'book': {repr(self.book)}, " \
                f"'created_at': '{self.created_at}', 'end_at': '{self.end_at}', " \
                f"'plated_end_at': '{self.plated_end_at}'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Order object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        """
        :return: dict contains order id, book id, user id, order created_at, order end_at, order plated_end_at
        :Example:
        | {
        |   'id': 8,
        |   'book': 8,
        |   'user': 8',
        |   'created_at': 1509393504,
        |   'end_at': 1509393504,
        |   'plated_end_at': 1509402866,
        | }
        """
        return {
            'id': self.id,
            'book': self.book.id,
            'user': self.user.id,
            'created_at': int(self.created_at.timestamp()),
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
            'plated_end_at': int(self.plated_end_at.timestamp()),
        }

    @staticmethod
    def create(user, book, plated_end_at=None):
        """
        :param user: the user who took the book
        :type user: CustomUser
        :param book: the book they took
        :type book: Book
        :param plated_end_at: planned return of data
        :type plated_end_at: int (timestamp)
        :return: a new order object which is also written into the DB
        """
        # create the set with unique books by previous orders
        orders = Order.objects.all()
        books = set()
        for order in orders:
            if not order.end_at:
                books.add(order.book.id)
        if book.id in books and book.count == 1:
            raise ValueError
        try:
            order = Order(user=user, book=book, plated_end_at=plated_end_at)
            order.end_at = None
            order.save()
            return order
        except ValueError:
            return None

    @staticmethod
    def get_by_id(order_id):
        """
        :param order_id:
        :type order_id: int
        :return: the object of the order, according to the specified id or None in case of its absence
        """
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        """
        Updates order in the database with the specified parameters.
        :param plated_end_at: new plated_end_at
        :type plated_end_at: int (timestamp)
        :param end_at: new end_at
        :type plated_end_at: int (timestamp)
        :return: None
        """
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        """
        :return: all orders
        """
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        """
        :return: all orders that do not have a return date (end_at)
        """
        return list(Order.objects.filter(end_at__isnull=True))

    @staticmethod
    def delete_by_id(order_id):
        """
        :param order_id: an id of a user to be deleted
        :type order_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            order_to_delete = Order.objects.get(pk=order_id)
            order_to_delete.delete()
            return True
        except Order.DoesNotExist:
            return False
