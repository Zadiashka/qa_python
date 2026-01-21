import pytest
from main import BooksCollector


@pytest.mark.parametrize("book_name", [
    "Война и мир",
    "К" * 40,
])
def test_add_new_book_success(book_name):
    collector = BooksCollector()
    collector.add_new_book(book_name)
    assert book_name in collector.get_books_genre()
    assert collector.get_book_genre(book_name) == ""


@pytest.mark.parametrize("invalid_name", [
    "",
    "A" * 41,
])
def test_add_new_book_invalid_length(invalid_name):
    collector = BooksCollector()
    collector.add_new_book(invalid_name)
    assert invalid_name not in collector.get_books_genre()


def test_add_new_book_duplicate_not_added():
    collector = BooksCollector()
    name = "Дубль"
    collector.add_new_book(name)
    collector.add_new_book(name)
    assert list(collector.get_books_genre().keys()).count(name) == 1


def test_set_book_genre_success_and_invalid_genre():
    collector = BooksCollector()
    name = "Фантастическая книга"
    collector.add_new_book(name)

    collector.set_book_genre(name, "Фантастика")
    assert collector.get_book_genre(name) == "Фантастика"

    collector.set_book_genre(name, "Неизвестный жанр")
    assert collector.get_book_genre(name) == "Фантастика"


def test_set_book_genre_for_nonexistent_book():
    collector = BooksCollector()
    collector.set_book_genre("Нет такой книги", "Фантастика")
    assert collector.get_book_genre("Нет такой книги") is None


def test_get_books_with_specific_genre():
    collector = BooksCollector()
    b1 = "Книга A"
    b2 = "Книга B"
    b3 = "Книга C"
    collector.add_new_book(b1)
    collector.add_new_book(b2)
    collector.add_new_book(b3)

    collector.set_book_genre(b1, "Фантастика")
    collector.set_book_genre(b2, "Фантастика")
    collector.set_book_genre(b3, "Комедии")

    books_fantasy = collector.get_books_with_specific_genre("Фантастика")
    assert set(books_fantasy) == {b1, b2}
    assert collector.get_books_with_specific_genre("Не жанр") == []


def test_get_books_genre_returns_full_dict():
    collector = BooksCollector()
    names = ["A", "B", "C"]
    for n in names:
        collector.add_new_book(n)
    d = collector.get_books_genre()
    assert isinstance(d, dict)
    assert set(d.keys()) == set(names)


def test_get_books_for_children_excludes_age_rated():
    collector = BooksCollector()
    kid = "Мультяшка"
    horror = "Ужастик"
    detective = "Детективчик"
    no_genre = "Без жанра"

    collector.add_new_book(kid)
    collector.add_new_book(horror)
    collector.add_new_book(detective)
    collector.add_new_book(no_genre)

    collector.set_book_genre(kid, "Мультфильмы")
    collector.set_book_genre(horror, "Ужасы")
    collector.set_book_genre(detective, "Детективы")

    children_books = collector.get_books_for_children()
    assert kid in children_books
    assert horror not in children_books
    assert detective not in children_books
    assert no_genre not in children_books


def test_favorites_add_delete_and_list_behaviour():
    collector = BooksCollector()
    book = "Любимая книга"
    other = "Не в словаре"

    collector.add_new_book(book)
    collector.add_book_in_favorites(book)
    assert collector.get_list_of_favorites_books() == [book]

    collector.add_book_in_favorites(book)
    assert collector.get_list_of_favorites_books() == [book]

    collector.add_book_in_favorites(other)
    assert other not in collector.get_list_of_favorites_books()

    collector.delete_book_from_favorites(book)
    assert collector.get_list_of_favorites_books() == []

    collector.delete_book_from_favorites("Что-то ещё")
    assert collector.get_list_of_favorites_books() == []
