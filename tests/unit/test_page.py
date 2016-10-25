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
    markdown_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_project', 'md')
    page = elements.Page('index', 'index')
    page.render_html(
        {'test_content': 'This is a test.'}, templates_dir, markdown_dir, None, 'flat', False
    )
    assert page.html == 'This is a test.'


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


def test_relative_path_from_page_to_page_with_debug_off():
    from_page = elements.Page('test 1', 'test1')
    to_page = elements.Page('test 2', 'test2')
    relative_path = to_page.get_relative_path(from_page, 'flat', False)
    assert relative_path == '/test2'


def test_relative_path_from_page_to_page_with_debug_on():
    from_page = elements.Page('test 1', 'test1')
    to_page = elements.Page('test 2', 'test2')
    relative_path = to_page.get_relative_path(from_page, 'flat', True)
    assert relative_path == './test2.html'


def test_relative_path_from_page_to_sub_page_with_flat_url_style_and_debug_off():
    from_page = elements.Page('test 1', 'test1')
    to_page = elements.SubPage('test 3', 'test3')
    relative_path = to_page.get_relative_path(from_page, 'flat', False)
    assert relative_path == '/test3'


def test_relative_path_from_page_to_sub_page_with_flat_url_style_and_debug_on():
    from_page = elements.Page('test 1', 'test1')
    to_page = elements.SubPage('test 3', 'test3')
    relative_path = to_page.get_relative_path(from_page, 'flat', True)
    assert relative_path == './test3.html'


def test_relative_path_from_page_to_sub_page_with_nested_url_style_and_debug_off():
    from_page = elements.Page('test 1', 'test1')
    parent_page = elements.Page('test 2', 'test2')
    to_page = elements.SubPage('test 3', 'test3')
    to_page.parent_page = parent_page
    relative_path = to_page.get_relative_path(from_page, 'nested', False)
    assert relative_path == '/test2/test3'


def test_relative_path_from_page_to_sub_page_with_nested_url_style_and_debug_on():
    from_page = elements.Page('test 1', 'test1')
    parent_page = elements.Page('test 2', 'test2')
    to_page = elements.SubPage('test 3', 'test3')
    to_page.parent_page = parent_page
    relative_path = to_page.get_relative_path(from_page, 'nested', True)
    assert relative_path == './test2/test3.html'


def test_relative_path_from_sub_page_to_page_with_flat_url_style_and_debug_off():
    from_page = elements.SubPage('test 3', 'test3')
    to_page = elements.Page('test 1', 'test1')
    relative_path = to_page.get_relative_path(from_page, 'flat', False)
    assert relative_path == '/test1'


def test_relative_path_from_sub_page_to_page_with_flat_url_style_and_debug_on():
    from_page = elements.SubPage('test 3', 'test3')
    to_page = elements.Page('test 1', 'test1')
    relative_path = to_page.get_relative_path(from_page, 'flat', True)
    assert relative_path == './test1.html'


def test_relative_path_from_page_to_unlinked_page_with_debug_off():
    from_page = elements.Page('test 1', 'test1')
    to_page = elements.UnlinkedPage('test 2', 'test2', ['path', 'to', 'page'])
    relative_path = to_page.get_relative_path(from_page, 'flat', False)
    assert relative_path == '/path/to/page/test2'


def test_relative_path_from_page_to_unlinked_page_with_debug_on():
    from_page = elements.Page('test 1', 'test1')
    to_page = elements.UnlinkedPage('test 2', 'test2', ['path', 'to', 'page'])
    relative_path = to_page.get_relative_path(from_page, 'flat', True)
    assert relative_path == './path/to/page/test2.html'


def test_relative_path_from_subpage_to_unlinked_page_with_debug_off():
    from_page = elements.SubPage('test 1', 'test1')
    to_page = elements.UnlinkedPage('test 2', 'test2', ['path', 'to', 'page'])
    relative_path = to_page.get_relative_path(from_page, 'flat', False)
    assert relative_path == '/path/to/page/test2'


def test_relative_path_from_subpage_to_unlinked_page_with_debug_on():
    from_page = elements.SubPage('test 1', 'test1')
    to_page = elements.UnlinkedPage('test 2', 'test2', ['path', 'to', 'page'])
    relative_path = to_page.get_relative_path(from_page, 'nested', True)
    assert relative_path == '../path/to/page/test2.html'


def test_relative_path_from_unlinked_page_to_unlinked_page_with_debug_on():
    from_page = elements.UnlinkedPage('test 1', 'test1', ['path', 'to', 'the', 'page'])
    to_page = elements.UnlinkedPage('test 2', 'test2', ['another', 'one'])
    relative_path = to_page.get_relative_path(from_page, 'flat', True)
    assert relative_path == '../../../../another/one/test2.html'
