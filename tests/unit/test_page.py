import os

import pytest

from zorn import elements, errors


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
    with pytest.raises(errors.PageError):
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


def test_set_content_from_md():
    page = elements.Page('Test', 'test_page')
    page.set_content_from_md(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'md'))
    assert '<h1>This is a test</h1>' in page.body_content
    assert '<p>There is nothing to see here</p>' in page.body_content


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


def test_set_css_path_of_page():
    page = elements.Page('test', 'Test')
    page.set_css_path(True)
    assert page.css_path == './main.css'


def test_set_css_path_of_subpage():
    page = elements.SubPage('test', 'Test')
    page.set_css_path(True, 'flat')
    assert page.css_path == './main.css'
    other_page = elements.SubPage('test', 'Test')
    other_page.set_css_path(True, 'nested')
    assert other_page.css_path == '../main.css'


def test_set_css_path_of_unlinked_page():
    page = elements.UnlinkedPage('test', 'Test', ['path', 'to', 'page'])
    page.set_css_path(True)
    assert page.css_path == '../../../main.css'


def test_set_css_path_with_no_debug():
    page = elements.Page('test', 'Test')
    page.set_css_path()
    assert page.css_path == '/main.min.css'
    sub_page = elements.SubPage('test', 'Test')
    sub_page.set_css_path()
    assert sub_page.css_path == '/main.min.css'
    unlinked_page = elements.UnlinkedPage('test', 'Test', ['path', 'to', 'page'])
    unlinked_page.set_css_path()
    assert unlinked_page.css_path == '/main.min.css'
