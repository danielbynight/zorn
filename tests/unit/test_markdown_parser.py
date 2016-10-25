import pytest

from zorn import elements, errors, markdown


def test_markdown_parser():
    page1 = elements.Page('test 1', 'test1')
    page2 = elements.Page('test 2', 'test2')
    page3 = elements.Page('test 3', 'test3')
    all_pages = [page1, page2, page3]
    parser = markdown.MarkdownParser(page1, all_pages, 'flat', True)
    assert parser.all_pages == all_pages
    assert parser.current_page == page1
    assert parser.url_style == 'flat'
    assert parser.debug is True


def test_get_path_from_page_name():
    page1 = elements.Page('test 1', 'test1')
    page2 = elements.Page('test 2', 'test2')
    page3 = elements.Page('test 3', 'test3')
    all_pages = [page1, page2, page3]
    parser = markdown.MarkdownParser(page1, all_pages, 'flat', True)
    assert parser.get_path_from_page_name('test2') == './test2.html'


def test_get_path_from_unknown_page_name():
    page1 = elements.Page('test 1', 'test1')
    page2 = elements.Page('test 2', 'test2')
    page3 = elements.Page('test 3', 'test3')
    all_pages = [page1, page2, page3]
    parser = markdown.MarkdownParser(page1, all_pages, 'flat', True)
    with pytest.raises(errors.PathNotFound):
        parser.get_path_from_page_name('test4') == './test2.html'


def test_convert_routes():
    page1 = elements.Page('test 1', 'test1')
    page2 = elements.Page('test 2', 'test2')
    page3 = elements.Page('home', 'index')
    all_pages = [page1, page2, page3]
    parser = markdown.MarkdownParser(page1, all_pages, 'flat', False)
    line = 'Click [here](@@index@@) to go home. Click [here](@@test2@@) to go somewhere else.'
    assert parser.convert_routes(line) == 'Click [here](/) to go home. Click [here](/test2) to go somewhere else.'


def test_convert_to_html():
    page1 = elements.Page('test 1', 'test1')
    page2 = elements.Page('test 2', 'test2')
    page3 = elements.Page('home', 'index')
    all_pages = [page1, page2, page3]
    parser = markdown.MarkdownParser(page1, all_pages, 'flat', False)
    md_content = 'Click [here](@@index@@) to go home.  \nClick [here](@@test2@@) to go somewhere else.'
    assert parser.convert_to_html(md_content, []) == \
        '<p>Click <a href="/">here</a> to go home.<br />\n' \
        'Click <a href="/test2">here</a> to go somewhere else.</p>'
