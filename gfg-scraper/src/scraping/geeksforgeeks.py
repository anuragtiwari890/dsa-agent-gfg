import json
import logging
import requests

from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

from .utils import create_error_message, fetch_html_data, format_problem_statement, format_comment_html, fetch


logger = logging.getLogger(__name__)
comments_base_url = "https://commentapi.geeksforgeeks.org/api/vr/1/comment"


def _extract_next_data(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag or not script_tag.string:
        logger.warning("__NEXT_DATA__ script tag not found")
        return None
    
    try:
        json_data = json.loads(script_tag.string)
        logger.debug("Successfully extracted __NEXT_DATA__ JSON")
        return json_data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse __NEXT_DATA__ JSON: {e}")
        return None


def _extract_problem_details(next_data: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "title": None,
        "statement_html": None,
        "statement_text": None,
        "problem_id": None
    }
    
    try:
        # Navigate through the JSON structure: props -> pageProps -> initialState -> problemData -> allData -> probData
        props = next_data.get('props', {})
        page_props = props.get('pageProps', {})
        initial_state = page_props.get('initialState', {})

        problem_datas = initial_state.get('problemData', {})
        all_data = problem_datas.get('allData', {})
        prob_data = all_data.get('probData', {})

        problem_question = prob_data.get('problem_question')
        logger.info(f"Found problem question: {problem_question}")

        problem_name = prob_data.get('problem_name')
        logger.info(f"Found problem name: {problem_name}")

        problem_id = prob_data.get('id')
        logger.info(f"Found problem id: {problem_id}")

        result["title"] = problem_name
        result["statement_html"] = problem_question
        result["statement_text"] = format_problem_statement(problem_question)
        result["problem_id"] = problem_id

    except Exception as e:
        logger.error(f"Error extracting problem details: {e}")
    
    return result


def fetch_comments(problem_id: str, max_comments: int = 5) -> List[Dict[str, Any]]:
    if not problem_id:
        logger.warning("No problem ID provided for comment fetching")
        return []
    
    try:
        # Construct the comment API URL
        query_params = {
            "sort_by": "time",
            "ancestry": "",
            "order_by": "dsc",
            "page": 1,
            "fetch_by": "post_id"
        }
        comment_url = f"{comments_base_url}/prob{problem_id}?{urlencode(query_params)}"
        
        # Make the API request
        response = fetch(comment_url)
        response.raise_for_status()
        
        # Parse the JSON response
        comment_data = response.json()
        
        # Extract comments from the response
        comments = []
        results = comment_data.get('results', [])
        
        for i, comment in enumerate(results[:max_comments]):
            comment_text = comment.get('text', '')
            user_name = comment.get('user_name', 'Anonymous')
            created_at = comment.get('created_at', '')
            votes = comment.get('votes', 0)
            
            # Format the comment HTML
            formatted_text = format_comment_html(comment_text)
            
            comment_dict = {
                'id': comment.get('id', f'comment_{i}'),
                'user_name': user_name,
                'text': formatted_text,
                'created_at': created_at,
                'votes': votes,
                'raw_text': comment_text  # Keep raw text for debugging
            }
            
            comments.append(comment_dict)
        
        logger.info(f"Successfully fetched {len(comments)} comments")
        return comments
        
    except requests.RequestException as e:
        logger.error(f"Error fetching comments: {e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing comment JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching comments: {e}")
        return []


def scrape_problem(url: str = None) -> Dict[str, Any]:
    soup = fetch_html_data(url)
    
    # Extract __NEXT_DATA__ JSON
    next_data = _extract_next_data(soup)
    
    if not next_data:
        logger.error("Failed to extract __NEXT_DATA__ from page")
        return {
            "url": url,
            "title": None,
            "statement_html": create_error_message(url or "Unknown URL"),
            "statement_text": "Failed to extract __NEXT_DATA__ from the page. The page structure may have changed.",
            "comments": []
        }
    
    # Extract problem details from JSON
    problem_details = _extract_problem_details(next_data)
    
    # If extraction failed, provide error message
    if not problem_details.get("statement_html"):
        logger.warning("Failed to extract problem details from __NEXT_DATA__")
        problem_details["statement_html"] = create_error_message(url or "Unknown URL", problem_details.get("title"))
        problem_details["statement_text"] = "Failed to extract problem content from __NEXT_DATA__. The JSON structure may have changed."
    
    # Fetch comments if problem_id is available
    comments = []
    problem_id = problem_details.get("problem_id")
    if problem_id:
        logger.info(f"Fetching comments for problem ID: {problem_id}")
        comments = fetch_comments(problem_id, max_comments=5)
    else:
        logger.warning("No problem ID found, skipping comment fetching")
    
    result = {
        "url": url,
        "title": problem_details.get("title"),
        "statement_html": problem_details.get("statement_html"),
        "statement_text": problem_details.get("statement_text"),
        "problem_id": problem_id,
        "comments": comments
    }
    
    logger.info("Scraping completed")
    return result
