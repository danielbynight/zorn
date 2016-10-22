import os
import shutil

import pytest

from zorn import elements


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
        website = elements.Website({  # noqa: ignore=F841
            'project_name': 'test_project_name',
        })


def test_website_error_with_no_project_name():
    if 'ZORN_SETTINGS' in os.environ:
        del os.environ['ZORN_SETTINGS']
    with pytest.raises(elements.SettingNotFoundError):
        website = elements.Website({  # noqa: ignore=F841
            'root_dir': 'test_root_dir',
        })


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
