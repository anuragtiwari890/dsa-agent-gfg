import re
import requests
from typing import Optional
from bs4 import BeautifulSoup, NavigableString, Tag
import html
import logging

logger = logging.getLogger(__name__)


def fetch_html_data(url: str) -> BeautifulSoup:
    response = fetch(url)
    return BeautifulSoup(response.content, 'html.parser')


def fetch(url: str) -> dict:
    logger.info(f"Fetching data for URL: {url}")

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.request("GET", url, headers=headers, data=payload, timeout= 10)
    return response


def format_problem_statement(html):
    soup = BeautifulSoup(html, 'html.parser')

    def recurse(node):
        text = ''
        for elem in node.children:
            if isinstance(elem, NavigableString):
                text += str(elem)
            elif isinstance(elem, Tag):
                if elem.name == 'br':
                    text += '\n'
                elif elem.name in ['p', 'div']:
                    inner = recurse(elem).strip()
                    if inner:
                        text += inner + '\n\n'
                elif elem.name == 'pre':
                    # Preserve pre block line by line
                    pre_content = elem.get_text()
                    pre_lines = pre_content.strip().split('\n')
                    text += '\n\n'.join(line.strip() for line in pre_lines) + '\n\n'
                    text += '--------------------------------\n\n'
                elif elem.name == 'strong':
                    text += '**' + recurse(elem) + '**'
                elif elem.name == 'span':
                    text += recurse(elem)
                else:
                    text += recurse(elem)
        return text

    return recurse(soup).strip()


def format_comment_html(comment_html: str) -> str:
    if not comment_html:
        return ""
    
    # Start with the original HTML
    formatted_html = comment_html
    
    # Handle escaped characters
    formatted_html = formatted_html.replace('\\t', '\t')  # Convert escaped tabs to actual tabs
    formatted_html = formatted_html.replace('\\n', '\n')  # Convert escaped newlines
    
    # Convert tabs to 4 non-breaking spaces for consistent indentation
    formatted_html = formatted_html.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
    
    # Handle <br/> tags for consistency
    formatted_html = formatted_html.replace('<br/>', '<br>')
    
    # Add styling for code blocks with preserved whitespace
    formatted_html = formatted_html.replace('<pre', '<pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; font-family: \'Courier New\', monospace; line-height: 1.4;"')
    formatted_html = formatted_html.replace('<code', '<code style="background-color: #f5f5f5; padding: 2px 4px; border-radius: 3px; font-family: \'Courier New\', monospace; white-space: pre;"')
    
    # Parse with BeautifulSoup but preserve spacing
    soup = BeautifulSoup(formatted_html, 'html.parser')
    
    # Convert back to string - BeautifulSoup handles entities properly
    final_html = str(soup)
    
    # Decode HTML entities to get the Unicode characters, then re-encode non-breaking spaces for HTML
    final_html = html.unescape(final_html)
    
    # Convert the Unicode non-breaking space characters (\u00a0) back to HTML entities for proper display
    final_html = final_html.replace('\u00a0', '&nbsp;')
    
    # Add line breaks after paragraphs for better spacing
    final_html = final_html.replace('</p>', '</p><br>')
    
    return final_html


def create_error_message(url: str, title: Optional[str] = None) -> str:
    error_html = f"""
    <div class="extraction-error" style="
        background-color: #fff3cd; 
        border: 1px solid #ffeaa7; 
        border-radius: 8px; 
        padding: 20px; 
        margin: 10px 0;
        font-family: Arial, sans-serif;
    ">
        <h3 style="color: #856404; margin-top: 0;">⚠️ Content Extraction Failed</h3>
        <p><strong>URL:</strong> <a href="{url}" target="_blank">{url}</a></p>
        {f'<p><strong>Title:</strong> {title}</p>' if title else ''}
        <p><strong>Issue:</strong> Unable to extract the problem statement from __NEXT_DATA__. This may be due to:</p>
        <ul style="color: #856404;">
            <li>Changes in GeeksforGeeks' JSON structure</li>
            <li>Different problem page format</li>
            <li>Network connectivity issues</li>
            <li>Missing or malformed __NEXT_DATA__ content</li>
        </ul>
        <p><strong>Recommendation:</strong> Visit the URL directly in your browser to view the content.</p>
    </div>
    """
    return error_html.strip()

def validate_gfg_url(url: str) -> bool:
    if not url.startswith("https://www.geeksforgeeks.org/problems/"):
        raise ValueError(f"Invalid URL: {url}")

    return True
