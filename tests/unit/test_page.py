import os

import pytest

from zorn import elements


def test_page():
    page = elements.Page('Test', 'test')
    assert page.title == 'Test'
    assert page.file_name == 'test'
    assert page.sub_pages == []


def test_page_with_sub_pages():
    sub_page = elements.SubPage('Sub Test', 'subtest')
    page = elements.Page('Test', 'test', [sub_page])
    assert page.title == 'Test'
    assert page.file_name == 'test'
    assert page.sub_pages == [sub_page]


def test_page_raises_error_if_sub_page_is_not_a_sub_page():
    with pytest.raises(elements.PageError):
        elements.Page('Test', 'test', [elements.Page('Fail', 'fail')])


def test_page_generate_content_menu_with_flat_url_style():
    page = elements.Page('Test', 'test', [
        elements.SubPage('Sub Page 1', 'subpage1'),
        elements.SubPage('Sub Page 2', 'subpage2'),
        elements.SubPage('Sub Page 3', 'subpage3'),
    ])
    result_menu = '#Test\n- [Sub Page 1](./subpage1.html)\n- [Sub Page 2](./subpage2.html)\n- [Sub Page 3](' \
                  './subpage3.html)\n'
    assert result_menu == page.generate_content_menu('flat')


def test_page_generate_content_menu_with_nested_url_style():
    page = elements.Page('Test', 'test', [
        elements.SubPage('Sub Page 1', 'subpage1'),
        elements.SubPage('Sub Page 2', 'subpage2'),
        elements.SubPage('Sub Page 3', 'subpage3'),
    ])
    result_menu = '#Test\n- [Sub Page 1](./test/subpage1.html)\n- [Sub Page 2](./test/subpage2.html)\n- [Sub Page ' \
                  '3](./test/subpage3.html)\n'
    assert result_menu == page.generate_content_menu('nested')


def test_page_casting_to_string():
    page = elements.Page('Test', 'test')
    assert str(page) == 'Test'


def test_page_render_html():
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    test_content = elements.Page.render_html({'test_content': 'This is a test.'}, templates_dir)
    assert test_content == 'This is a test.'


def test_subpage():
    sub_page = elements.SubPage('Test', 'test')
    assert sub_page.title == 'Test'
    assert sub_page.file_name == 'test'


def test_subpage_cannot_have_subpages():
    with pytest.raises(TypeError):
        elements.SubPage('Test', 'test', [elements.SubPage('Test', 'test')])


def test_unlinkedpage():
    unlinked_page = elements.UnlinkedPage('Test', 'test', ['path', 'to', 'page'])
    assert unlinked_page.title == 'Test'
    assert unlinked_page.file_name == 'test'
    assert unlinked_page.path == ['path', 'to', 'page']


def test_unlinkedpage_with_path_as_string():
    unlinked_page = elements.UnlinkedPage('Test', 'test', 'path/to/page')
    assert unlinked_page.title == 'Test'
    assert unlinked_page.file_name == 'test'
    assert unlinked_page.path == ['path', 'to', 'page']


def test_unlinkedpage_without_path():
    unlinked_page = elements.UnlinkedPage('Test', 'test')
    assert unlinked_page.title == 'Test'
    assert unlinked_page.file_name == 'test'
    assert unlinked_page.path == []
