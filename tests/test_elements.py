from zorn import elements
import pytest
import os


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
        page = elements.Page('Test', 'test', [elements.Page('Fail', 'fail')])  # noqa: ignore=F841


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
        sub_page = elements.SubPage('Test', 'test', [elements.SubPage('Test', 'test')])  # noqa: ignore=F841


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


def test_website_with_only_defaults():
    website = elements.Website({
        'root_dir': 'test_root_dir',
        'project_name': 'test_project_name',
    })
    # Test non-optional settings
    assert website.root_dir == 'test_root_dir'
    assert website.project_name == 'test_project_name'

    # Test optional settings
    assert website.debug is False
    assert website.url_style == 'flat'
    assert website.templates_dir == os.path.join(os.path.dirname(os.path.abspath(elements.__file__)), 'templates')
    assert website.markdown_dir == os.path.join(website.root_dir, 'md')
    assert website.markdown_extensions == []
    assert website.site_dir == 'test_root_dir'
    assert website.title == 'test_project_name'
    assert website.subtitle == ''
    assert website.description == ''
    assert website.author == ''
    assert website.keywords == ''
    assert website.keywords == ''
    assert website.pages == []


def test_website_with_no_defaults():
    pages = [elements.Page('Test', 'test')]
    website = elements.Website({
        'root_dir': 'test_root_dir',
        'project_name': 'test_project_name',
        'debug': True,
        'url_style': 'nested',
        'templates_dir': 'test_templates_dir',
        'markdown_dir': 'test_markdown_dir',
        'markdown_extensions': ['test_markdown_extension'],
        'site_dir': 'test_site_dir',
        'site_title': 'test_site_title',
        'site_subtitle': 'test_site_subtitle',
        'description': 'test description',
        'author': 'Test Author',
        'keywords': 'test keyword',
        'pages': pages
    })
    # Test non-optional settings
    assert website.root_dir == 'test_root_dir'
    assert website.project_name == 'test_project_name'

    # Test optional settings
    assert website.debug is True
    assert website.url_style == 'nested'
    assert website.templates_dir == 'test_templates_dir'
    assert website.markdown_dir == 'test_markdown_dir'
    assert website.markdown_extensions == ['test_markdown_extension']
    assert website.site_dir == 'test_site_dir'
    assert website.title == 'test_site_title'
    assert website.subtitle == 'test_site_subtitle'
    assert website.description == 'test description'
    assert website.author == 'Test Author'
    assert website.keywords == 'test keyword'
    assert website.pages == pages


def test_website_error_with_no_root_dir():
    with pytest.raises(elements.SettingNotFoundError):
        website = elements.Website({            # noqa: ignore=F841
            'project_name': 'test_project_name',
        })


def test_website_error_with_no_project_name():
    with pytest.raises(elements.SettingNotFoundError):
        website = elements.Website({            # noqa: ignore=F841
            'root_dir': 'test_root_dir',
        })
