import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash-lite')

def generate_cold_emails(industry, offer):
    """Generate 3 cold email drafts"""
    prompt = f"""
    Create 3 different cold email drafts for the following:
    
    Industry: {industry}
    Offer: {offer}
    
    Requirements:
    - Each email should be unique in tone and approach
    - Keep emails concise (150-200 words max)
    - Include compelling subject lines
    - Focus on value proposition
    - Include clear call-to-action
    - Make them personalized and industry-specific
    
    Format each email as:
    **Subject: [Subject Line]**
    [Email Body]
    
    Generate 3 distinct emails labeled as Email 1, Email 2, and Email 3.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating emails: {str(e)}"

def generate_linkedin_dms(industry, offer):
    """Generate 3 LinkedIn DM drafts"""
    prompt = f"""
    Create 3 different LinkedIn direct message drafts for the following:
    
    Industry: {industry}
    Offer: {offer}
    
    Requirements:
    - Each message should be unique in approach
    - Keep messages short and conversational (50-100 words)
    - Professional but friendly tone
    - Personalized for the industry
    - Include value proposition
    - Natural conversation starter
    - Clear but soft call-to-action
    
    Format each message clearly labeled as Message 1, Message 2, and Message 3.
    Make them feel natural and not overly salesy.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating LinkedIn DMs: {str(e)}"

def main():
    # Page configuration
    st.set_page_config(
        page_title="AI Sales Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .section-header {
        color: #2e7d32;
        border-bottom: 2px solid #2e7d32;
        padding-bottom: 5px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .output-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        color: #2e7d32;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1 class='main-header'>🤖 AI Sales Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #666;'>Generate personalized cold emails and LinkedIn DMs for your industry</p>", unsafe_allow_html=True)
    
    # Sidebar for inputs
    st.sidebar.header("📋 Input Parameters")
    
    # Input fields
    industry = st.sidebar.text_input(
        "🏢 Target Industry",
        placeholder="e.g., SaaS, E-commerce, Healthcare, Real Estate",
        help="Enter the industry you're targeting"
    )
    
    offer = st.sidebar.text_area(
        "💼 Your Offer/Service",
        placeholder="e.g., AI-powered customer service automation that reduces response time by 80%",
        help="Describe what you're offering to prospects",
        height=100
    )
    
    # Generate button
    generate_button = st.sidebar.button("🚀 Generate Sales Content", type="primary")
    
    # Main content area
    if generate_button:
        if not industry or not offer:
            st.error("⚠️ Please fill in both Industry and Offer fields")
        else:
            # Show loading message
            with st.spinner("🔄 Generating personalized sales content..."):
                # Create two columns for output
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<h2 class='section-header'>📧 Cold Email Drafts</h2>", unsafe_allow_html=True)
                    
                    # Generate cold emails
                    emails = generate_cold_emails(industry, offer)
                    
                    if "Error" not in emails:
                        st.markdown("<div class='output-container'>", unsafe_allow_html=True)
                        st.markdown(emails)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Download button for emails
                        st.download_button(
                            label="📥 Download Email Drafts",
                            data=emails,
                            file_name=f"cold_emails_{industry.lower().replace(' ', '_')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(emails)
                
                with col2:
                    st.markdown("<h2 class='section-header'>💬 LinkedIn DM Drafts</h2>", unsafe_allow_html=True)
                    
                    # Generate LinkedIn DMs
                    linkedin_dms = generate_linkedin_dms(industry, offer)
                    
                    if "Error" not in linkedin_dms:
                        st.markdown("<div class='output-container'>", unsafe_allow_html=True)
                        st.markdown(linkedin_dms)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Download button for LinkedIn DMs
                        st.download_button(
                            label="📥 Download LinkedIn DMs",
                            data=linkedin_dms,
                            file_name=f"linkedin_dms_{industry.lower().replace(' ', '_')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(linkedin_dms)
                
                # Success message
                if "Error" not in emails and "Error" not in linkedin_dms:
                    st.success("✅ Sales content generated successfully!")
                    
                    # Usage tips
                    with st.expander("💡 Tips for Using Generated Content"):
                        st.markdown("""
                        **Best Practices:**
                        - Personalize each message with recipient's name and company
                        - Research the prospect before sending
                        - A/B test different versions to see what works best
                        - Follow up strategically (don't spam)
                        - Track open rates and responses
                        - Adapt the tone based on your brand voice
                        
                        **Email Tips:**
                        - Send emails on Tuesday-Thursday, 10 AM - 2 PM
                        - Keep subject lines under 50 characters
                        - Use a professional email signature
                        
                        **LinkedIn Tips:**
                        - Connect first, then message
                        - Reference their recent posts or achievements
                        - Keep it conversational and authentic
                        """)
    
    else:
        # Welcome screen
        st.markdown("### 👋 Welcome to AI Sales Agent")
        st.markdown("""
        This tool helps you generate personalized sales content for your outreach campaigns.
        
        **How it works:**
        1. Enter your target industry in the sidebar
        2. Describe your offer or service
        3. Click "Generate Sales Content"
        4. Get 3 cold email drafts + 3 LinkedIn DM drafts
        
        **Features:**
        - ✨ AI-powered content generation
        - 🎯 Industry-specific personalization
        - 📧 Professional email templates
        - 💬 Conversational LinkedIn messages
        - 📥 Download generated content
        - 💡 Best practice tips included
        """)
        
        # Example showcase
        with st.expander("📋 See Example Output"):
            st.markdown("""
            **Example for SaaS Industry offering "AI Customer Support":**
            
            **Cold Email Sample:**
            > **Subject: Cut Your Customer Support Costs by 60%**
            > 
            > Hi [Name],
            > 
            > I noticed [Company] has been scaling rapidly in the SaaS space. With growth comes increased customer support volume - and costs.
            > 
            > We've helped similar SaaS companies reduce support costs by 60% while improving response times with our AI customer support solution.
            > 
            > Would you be interested in a 15-minute demo showing how we achieved this for [Similar Company]?
            > 
            > Best regards,
            > [Your name]
            
            **LinkedIn DM Sample:**
            > Hi [Name]! Saw your recent post about scaling customer support at [Company]. We've helped several SaaS companies automate 70% of their support tickets while keeping customers happy. Would love to share how we did it - interested in a quick chat?
            """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666; font-size: 14px;'>"
        "Built with ❤️ using Streamlit and Google Gemini AI | "
        "© 2024 AI Sales Agent"
        "</p>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()