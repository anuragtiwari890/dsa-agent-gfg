"""
AI Solution display component for Streamlit UI.
"""

import streamlit as st
from typing import Optional, Callable
from ...models.problem import Problem
from ...models.ai_solution import AISolution
from ...services.ai_service import AIService


class AISolutionDisplayComponent:
    """Component for displaying and generating AI solutions in Streamlit."""
    
    @staticmethod
    def display_api_key_input(ai_service: AIService) -> Optional[str]:
        """
        Display API key input section and return the key to use.
        
        Returns:
            API key to use, or None if not available
        """
        if not ai_service.is_using_env_key():
            st.info("💡 Tip: Set OPENAI_API_KEY in your .env file")
            
            # Show required input
            api_key_input = st.text_input(
                "OpenAI API Key:", 
                type="password",
                help="Enter your OpenAI API key to generate solutions."
            )
            
            return api_key_input.strip() if api_key_input.strip() else None
    
    @staticmethod
    def display_generation_section(
        problem: Problem,
        ai_service: AIService,
        on_solution_generated: Callable[[AISolution], None]
    ) -> None:
        """
        Display the AI solution generation section.
        
        Args:
            problem: Problem to generate solution for
            ai_service: AI service instance
            on_solution_generated: Callback when solution is generated
        """
        st.header("🤖 AI Generated Solution")
        
        # API key input
        # api_key = AISolutionDisplayComponent.display_api_key_input(ai_service)
        
        # Generate solution button
        if st.button("🚀 Generate AI Solution", type="secondary"):                
            with st.spinner("Generating AI solution..."):
                try:
                    solution = ai_service.generate_solution(problem)
                    
                    if solution.has_content():
                        st.success("✅ AI solution generated successfully!")
                        on_solution_generated(solution)
                    else:
                        st.error("❌ Failed to generate AI solution. Please check your API key and try again.")
                        
                except ValueError as e:
                    st.warning(f"⚠️ {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error generating solution: {str(e)}")
    
    @staticmethod
    def display_solution(
        solution: AISolution,
        on_clear_solution: Callable[[], None]
    ) -> None:
        """
        Display the generated AI solution.
        
        Args:
            solution: AI solution to display
            on_clear_solution: Callback to clear the solution
        """
        if not solution or not solution.has_content():
            return
        
        st.subheader("📝 Generated Python Solution")
        
        # Display the code
        st.code(solution.get_formatted_code(), language='python', line_numbers=True)
        
        # Tips and actions
        st.caption("💡 Tip: You can copy the code by clicking the copy icon in the top-right corner of the code block")
        
        # Clear solution button
        if st.button("🗑️ Clear Solution", type="secondary"):
            on_clear_solution()
    
    @staticmethod
    def display_ai_section(
        problem: Problem,
        ai_service: AIService,
        current_solution: Optional[AISolution],
        on_solution_generated: Callable[[AISolution], None],
        on_clear_solution: Callable[[], None]
    ) -> None:
        """
        Display the complete AI solution section.
        
        Args:
            problem: Problem to work with
            ai_service: AI service instance
            current_solution: Currently stored solution (if any)
            on_solution_generated: Callback when new solution is generated
            on_clear_solution: Callback to clear solution
        """
        # Generation section
        AISolutionDisplayComponent.display_generation_section(
            problem, ai_service, on_solution_generated
        )
        
        # Display current solution if available
        if current_solution:
            AISolutionDisplayComponent.display_solution(
                current_solution, on_clear_solution
            )
        
        st.markdown("---")
