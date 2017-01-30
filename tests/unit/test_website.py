import os
import shutil

import pytest

from zorn import elements, errors


def test_website_with_only_defaults():
    website = elements.Website({
        'root_dir': 'test_root_dir',
        'project_name': 'test_project_name',
    })
    # Test non-optional settings
    assert website.settings.root_dir == 'test_root_dir'
    assert website.settings.project_name == 'test_project_name'

    # Test optional settings
    assert website.settings.debug is False
    assert website.settings.url_style == 'flat'
    assert website.settings.templates_dir == os.path.join(os.path.dirname(os.path.abspath(elements.__file__)),
                                                          'templates')
    assert website.settings.markdown_dir == os.path.join(website.settings.root_dir, 'md')
    assert website.settings.markdown_extensions == []
    assert website.settings.title == 'test_project_name'
    assert website.settings.subtitle == ''
    assert website.settings.description == ''
    assert website.settings.author == ''
    assert website.settings.keywords == ''
    assert website.settings.keywords == ''
    assert website.settings.pages == []


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
        'site_title': 'test_site_title',
        'site_subtitle': 'test_site_subtitle',
        'description': 'test description',
        'author': 'Test Author',
        'keywords': 'test keyword',
        'pages': pages
    })
    # Test non-optional settings
    assert website.settings.root_dir == 'test_root_dir'
    assert website.settings.project_name == 'test_project_name'

    # Test optional settings
    assert website.settings.debug is True
    assert website.settings.url_style == 'nested'
    assert website.settings.templates_dir == 'test_templates_dir'
    assert website.settings.markdown_dir == 'test_markdown_dir'
    assert website.settings.markdown_extensions == ['test_markdown_extension']
    assert website.settings.title == 'test_site_title'
    assert website.settings.subtitle == 'test_site_subtitle'
    assert website.settings.description == 'test description'
    assert website.settings.author == 'Test Author'
    assert website.settings.keywords == 'test keyword'
    assert website.settings.pages == pages


def test_website_error_with_no_root_dir():
    with pytest.raises(errors.SettingNotFoundError):
        elements.Website({'project_name': 'test_project_name'})


def test_website_error_with_no_project_name():
    if 'ZORN_SETTINGS' in os.environ:
        del os.environ['ZORN_SETTINGS']
    with pytest.raises(errors.SettingNotFoundError):
        elements.Website({'root_dir': 'test_root_dir'})


def test_generate_empty_page():
    pages = [elements.Page('Test', 'test_page')]
    website = elements.Website({
        'root_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project'),
        'project_name': 'test_project_name',
        'pages': pages
    })
    website.generate_pages()
    assert os.path.exists(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'fixtures',
        'test_project',
        'test_page.html'
    ))
    os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'test_page.html'))


def test_page_title_printed_to_the_page():
    pages = [elements.Page('Test', 'test_page')]
    website = elements.Website({
        'root_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project'),
        'project_name': 'test_project_name',
        'pages': pages,
        'site_title': 'Site Title',
    })
    website.generate_pages()
    page_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project',
                             'test_page.html')
    with open(page_path, 'r') as f:
        page_content = f.read()
    assert '<title>Site Title - Test</title>' in page_content
    os.remove(page_path)


def test_generate_page_with_markdown():
    pages = [elements.Page('Test', 'test_page')]
    website = elements.Website({
        'root_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project'),
        'project_name': 'test_project_name',
        'pages': pages,
        'markdown_dir': (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'md')),
    })
    website.generate_pages()
    page_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'test_page.html')
    with open(page_path, 'r') as f:
        page_content = f.read()
    assert '<h1>This is a test</h1>' in page_content
    assert '<p>There is nothing to see here</p>' in page_content
    os.remove(page_path)


def test_generate_subpage():
    pages = [elements.Page('Test Page', 'test_page', [elements.SubPage('Test SubPage', 'test_subpage')])]
    website = elements.Website({
        'root_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project'),
        'project_name': 'test_project_name',
        'pages': pages
    })
    website.generate_pages()
    page_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'test_page.html')
    subpage_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'test_subpage.html'
    )
    assert os.path.exists(page_path)
    assert os.path.exists(subpage_path)
    os.remove(page_path)
    os.remove(subpage_path)


def test_generate_subpage_nested():
    pages = [elements.Page('Test Page', 'test_page', [elements.SubPage('Test SubPage', 'test_subpage')])]
    website = elements.Website({
        'root_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project'),
        'project_name': 'test_project_name',
        'pages': pages,
        'url_style': 'nested',
    })
    website.generate_pages()
    page_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'test_page.html')
    subpage_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'test_page', 'test_subpage.html'
    )
    assert os.path.exists(page_path)
    assert os.path.exists(subpage_path)
    os.remove(page_path)
    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'test_page'))


def test_generate_unlinked_page():
    pages = [elements.UnlinkedPage('Unlinked Page', 'unlinked_page', ['sub_dir'])]
    website = elements.Website({
        'root_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project'),
        'project_name': 'test_project_name',
        'pages': pages,
    })
    website.generate_pages()
    subpage_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'sub_dir', 'unlinked_page.html'
    )
    assert os.path.exists(subpage_path)
    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'sub_dir'))


def test_website_set_parent_pages():
    pages = [
        elements.Page('Test 1', 'test1', [elements.SubPage('sp11', 'sp11'), elements.SubPage('sp12', 'sp12')]),
        elements.Page('Test 2', 'test2', [elements.SubPage('sp21', 'sp21'), elements.SubPage('sp22', 'sp22')]),
    ]
    website = elements.Website({
        'root_dir': 'test_root_dir',
        'project_name': 'test_project_name',
        'pages': pages
    })
    sub_pages = [page for page in website.settings.pages if type(pages) is elements.SubPage]
    for sub_page in sub_pages:
        assert sub_page.parent_page is None
    website._set_parent_pages()
    sub_pages = [page for page in website.settings.pages if type(pages) is elements.SubPage]
    for sub_page in sub_pages:
        assert sub_page.parent_page in ['test1', 'test2']
