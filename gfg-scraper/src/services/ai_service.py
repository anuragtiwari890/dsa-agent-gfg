"""
Service layer for AI solution generation.
"""

import logging
import os
from typing import Optional, List, Dict, Any

from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from ..models.problem import Problem, Comment
from ..models.ai_solution import AISolution

logger = logging.getLogger(__name__)


class AIService:
    """Service for handling AI solution generation."""
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self._load_api_key_from_env()
    
    def _load_api_key_from_env(self) -> None:
        """Load API key from environment variables."""
        env_api_key = os.getenv('OPENAI_API_KEY')
        if env_api_key and env_api_key != 'your_openai_api_key_here':
            self.api_key = env_api_key
            logger.info("OpenAI API key loaded from environment variables")
    
    def set_api_key(self, api_key: str) -> None:
        """Set the OpenAI API key."""
        if api_key and api_key.strip():
            self.api_key = api_key.strip()
            logger.info("OpenAI API key set manually")
    
    def has_api_key(self) -> bool:
        """Check if API key is available."""
        return bool(self.api_key and self.api_key.strip())
    
    def is_using_env_key(self) -> bool:
        """Check if using API key from environment."""
        env_api_key = os.getenv('OPENAI_API_KEY')
        return bool(env_api_key and env_api_key != 'your_openai_api_key_here')
    
    def _prepare_comment_context(self, comments: List[Comment]) -> str:
        """
        Prepare comment context for AI prompt.
        
        Args:
            comments: List of comments to process
            
        Returns:
            Formatted comment context string
        """
        comment_context = ""
        for i, comment in enumerate(comments[:5], 1):  # Use up to 5 comments
            user_name = comment.user_name or 'Anonymous'
            # Extract text content from HTML
            comment_text = comment.text
            if comment_text:
                # Simple HTML tag removal for context
                clean_text = BeautifulSoup(comment_text, 'html.parser').get_text()
                comment_context += f"\n\nComment {i} by {user_name}:\n{clean_text[:500]}..."  # Limit length
        
        return comment_context
    
    def _generate_ai_solution_with_langchain(
        self, 
        problem_title: str, 
        problem_statement: str, 
        comments: List[Comment]
    ) -> Optional[str]:
        """
        Generate AI solution using LangChain and OpenAI.
        
        Args:
            problem_title: Title of the problem
            problem_statement: Problem statement text
            comments: List of comments for additional context
            
        Returns:
            Generated Python code or None if generation fails
        """
        try:
            # Initialize LangChain ChatOpenAI
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.3,  # Lower temperature for more consistent code
                max_tokens=1500,
                openai_api_key=self.api_key
            )
            
            # Prepare the context from comments
            comment_context = self._prepare_comment_context(comments)
            
            # Create the prompt template using LangChain
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are a Python coding expert who provides clean, well-commented solutions to coding problems. Always respond with only Python code, proper explainations inline comments and at the very top the high level algo of the code in comments only"),
                ("human", """
                    You are a Python coding expert. Based on the following GeeksforGeeks problem and user comments/solutions, provide a clean, optimized Python solution.
                    Problem Title: {problem_title}
                    Problem Statement: {problem_statement}
                    User Comments and Solutions: {comment_context}

                    Requirements:
                    1. Provide ONLY Python code - no explanations outside the code
                    2. Use the exact class and method structure expected by GeeksforGeeks
                    3. Add comprehensive inline comments explaining the logic
                    4. Optimize for both time and space complexity
                    5. Handle edge cases appropriately
                    6. Use descriptive variable names
                    7. Add the high level algo of the code in comments only at the very top
                    8. add few example calls to the code
                    9. Follow Python best practices

                    Please provide the complete solution:
                """)
            ])
            
            # Create the chain
            chain = prompt_template | llm
            
            # Invoke the chain with the input variables
            response = chain.invoke({
                "problem_title": problem_title,
                "problem_statement": problem_statement[:1500] + "..." if len(problem_statement) > 1500 else problem_statement,
                "comment_context": comment_context
            })
            
            # Extract the generated code
            generated_code = response.content.strip()
            
            logger.debug(f"Generated code: {generated_code}")
            
            # Clean up the response - remove markdown code blocks if present
            if generated_code.startswith('```python'):
                generated_code = generated_code[9:]  # Remove ```python
            elif generated_code.startswith('```'):
                generated_code = generated_code[3:]   # Remove ```
            
            if generated_code.endswith('```'):
                generated_code = generated_code[:-3]  # Remove trailing ```
            
            generated_code = generated_code.strip()
            
            logger.info("Successfully generated AI solution using LangChain")
            return generated_code
                
        except Exception as e:
            logger.error(f"Error generating AI solution with LangChain: {e}")
            return None

    def generate_solution(self, problem: Problem) -> AISolution:
        """
        Generate an AI solution for the given problem.
        
        Args:
            problem: Problem object to generate solution for
            
        Returns:
            AISolution object with generated code
            
        Raises:
            ValueError: If API key is not set
            Exception: For AI generation errors
        """
        if not self.has_api_key():
            raise ValueError("OpenAI API key is required for AI solution generation")
        
        try:
            logger.info(f"Generating AI solution for problem: {problem.title}")
            
            # Generate solution using internal method
            solution_code = self._generate_ai_solution_with_langchain(
                problem_title=problem.title,
                problem_statement=problem.get_statement(),
                comments=problem.comments
            )
            
            if not solution_code:
                raise Exception("AI service returned empty solution")
            
            solution = AISolution(code=solution_code)
            logger.info("Successfully generated AI solution")
            return solution
            
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Error generating AI solution: {str(e)}")
            raise Exception(f"Failed to generate AI solution: {str(e)}")
