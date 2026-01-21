import pytest
from main import BooksCollector


@pytest.mark.parametrize("valid_name", [
    "Война и мир",
    "К" * 40,
])
def test_add_new_book_adds_book_with_empty_genre(valid_name):
    collector = BooksCollector()
    collector.add_new_book(valid_name)

    assert valid_name in collector.get_books_genre()
    assert collector.get_book_genre(valid_name) == ""


@pytest.mark.parametrize("invalid_name", [
    "",
    "A" * 41,
])
def test_add_new_book_does_not_add_invalid_names(invalid_name):
    collector = BooksCollector()
    collector.add_new_book(invalid_name)

    assert invalid_name not in collector.get_books_genre()


def test_add_new_book_does_not_add_duplicates():
    collector = BooksCollector()
    book_title = "Повтор"

    collector.add_new_book(book_title)
    collector.add_new_book(book_title)

    assert list(collector.get_books_genre().keys()).count(book_title) == 1


def test_set_book_genre_sets_valid_genre():
    collector = BooksCollector()
    book_title = "Фантастическая книга"

    collector.add_new_book(book_title)
    collector.set_book_genre(book_title, "Фантастика")

    assert collector.get_book_genre(book_title) == "Фантастика"


def test_set_book_genre_does_not_set_invalid_genre():
    collector = BooksCollector()
    book_title = "Книга без жанра"

    collector.add_new_book(book_title)
    collector.set_book_genre(book_title, "Несуществующий жанр")

    # жанр не должен измениться и остаётся пустой строкой
    assert collector.get_book_genre(book_title) == ""


def test_set_book_genre_does_not_set_for_unknown_book():
    collector = BooksCollector()

    collector.set_book_genre("Неизвестная книга", "Фантастика")

    assert collector.get_book_genre("Неизвестная книга") is None


def test_get_books_with_specific_genre_returns_correct_books():
    collector = BooksCollector()
    fantasy_book_1 = "Звёздный путь"
    fantasy_book_2 = "Галактические войны"
    comedy_book = "Смешная история"

    collector.add_new_book(fantasy_book_1)
    collector.add_new_book(fantasy_book_2)
    collector.add_new_book(comedy_book)

    collector.set_book_genre(fantasy_book_1, "Фантастика")
    collector.set_book_genre(fantasy_book_2, "Фантастика")
    collector.set_book_genre(comedy_book, "Комедии")

    result = collector.get_books_with_specific_genre("Фантастика")

    assert set(result) == {fantasy_book_1, fantasy_book_2}


def test_get_books_with_specific_genre_returns_empty_list_for_invalid_genre():
    collector = BooksCollector()

    result = collector.get_books_with_specific_genre("Несуществующий жанр")

    assert result == []


def test_get_books_genre_returns_full_dictionary():
    collector = BooksCollector()
    books_list = ["Книга 1", "Книга 2", "Книга 3"]

    for title in books_list:
        collector.add_new_book(title)

    result = collector.get_books_genre()

    assert set(result.keys()) == set(books_list)


def test_get_books_for_children_filters_age_restricted_genres():
    collector = BooksCollector()

    child_book = "Мультяшка"
    horror_book = "Страшилка"
    detective_book = "Расследование"
    no_genre_book = "Без жанра"

    collector.add_new_book(child_book)
    collector.add_new_book(horror_book)
    collector.add_new_book(detective_book)
    collector.add_new_book(no_genre_book)

    collector.set_book_genre(child_book, "Мультфильмы")
    collector.set_book_genre(horror_book, "Ужасы")
    collector.set_book_genre(detective_book, "Детективы")

    result = collector.get_books_for_children()

    assert child_book in result
    assert horror_book not in result
    assert detective_book not in result
    assert no_genre_book not in result



def test_add_book_in_favorites_adds_only_existing_book():
    collector = BooksCollector()
    book_title = "Любимая книга"

    collector.add_new_book(book_title)
    collector.add_book_in_favorites(book_title)

    assert collector.get_list_of_favorites_books() == [book_title]


def test_add_book_in_favorites_does_not_add_duplicates():
    collector = BooksCollector()
    book_title = "Повтор любимой"

    collector.add_new_book(book_title)
    collector.add_book_in_favorites(book_title)
    collector.add_book_in_favorites(book_title)

    assert collector.get_list_of_favorites_books() == [book_title]


def test_add_book_in_favorites_does_not_add_unknown_book():
    collector = BooksCollector()

    collector.add_book_in_favorites("Неизвестная книга")

    assert collector.get_list_of_favorites_books() == []


def test_delete_book_from_favorites_removes_book():
    collector = BooksCollector()
    book_title = "Удаляемая книга"

    collector.add_new_book(book_title)
    collector.add_book_in_favorites(book_title)
    collector.delete_book_from_favorites(book_title)

    assert collector.get_list_of_favorites_books() == []


def test_delete_book_from_favorites_ignores_unknown_book():
    collector = BooksCollector()

    collector.delete_book_from_favorites("Неизвестная книга")

    assert collector.get_list_of_favorites_books() == []
