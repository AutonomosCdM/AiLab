import os
import pytest
from src.modules.internet_access.brave_search_tool import BraveSearchTool

def test_brave_search_initialization():
    """
    Test that BraveSearchTool can be initialized with an API key.
    """
    # Use environment variable or a test API key
    api_key = os.environ.get('BRAVE_SEARCH_API_KEY', 'test_key')
    search_tool = BraveSearchTool(api_key)
    assert search_tool is not None

def test_brave_search_query():
    """
    Test performing a basic web search.
    """
    api_key = os.environ.get('BRAVE_SEARCH_API_KEY', 'test_key')
    search_tool = BraveSearchTool(api_key)
    
    # Test a simple query
    results = search_tool.search("Python programming")
    
    # Check that we have a status key
    assert 'status' in results
    
    # If successful, check results
    if results['status'] == 'success':
        assert 'results' in results
        assert len(results['results']) > 0

def test_brave_search_result_summary():
    """
    Test the result summary generation.
    """
    api_key = os.environ.get('BRAVE_SEARCH_API_KEY', 'test_key')
    search_tool = BraveSearchTool(api_key)
    
    # Perform a search
    results = search_tool.search("Python programming")
    
    # Generate summary
    summary = search_tool.summarize_results(results)
    
    # Check summary based on status
    if results['status'] == 'success':
        assert isinstance(summary, str)
        assert "Resultados de búsqueda" in summary
    else:
        assert "Search failed" in summary or "Search request failed" in summary

def test_brave_search_error_handling():
    """
    Test error handling with an invalid API key.
    """
    # Test with empty string
    with pytest.raises(ValueError, match="Brave Search API key is required"):
        BraveSearchTool("")
        
    # Test with None
    with pytest.raises(ValueError, match="Brave Search API key is required"):
        BraveSearchTool(None)

def test_brave_search_result_parsing():
    """
    Test that search results are correctly parsed.
    """
    api_key = os.environ.get('BRAVE_SEARCH_API_KEY', 'test_key')
    search_tool = BraveSearchTool(api_key)
    
    results = search_tool.search("Machine Learning", count=3)
    
    # Check status
    assert 'status' in results
    
    # If successful, check results
    if results['status'] == 'success':
        assert len(results['results']) <= 3
        
        for result in results['results']:
            assert 'title' in result
            assert 'url' in result
            assert 'description' in result
