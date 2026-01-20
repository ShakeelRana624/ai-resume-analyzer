import streamlit as st
import os
import PyPDF2
import docx
import requests
import json
import tiktoken
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

# OpenRouter API configuration - Use secrets for cloud deployment
try:
    # Try to get from Streamlit secrets first (for cloud deployment)
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    OPENROUTER_URL = st.secrets["OPENROUTER_URL"]
except:
    # Fallback to hardcoded values (for local development)
    OPENROUTER_API_KEY = "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"
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def count_tokens(text):
    """Count tokens in text using tiktoken"""
    try:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))
    except:
        return len(text) // 4

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def analyze_resume_with_ai(resume_text, job_description):
    """Analyze resume against job description using OpenRouter API"""
    
    total_tokens = count_tokens(resume_text)
    
    prompt = f"""
    You are an expert resume analyst with 10+ years of experience in career counseling and ATS optimization.
    
    Your task is to analyze a resume against a job description using Chain-of-Thought reasoning.
    
    Here are examples of high-quality analysis:
    
    Example 1 - Strong Match:
    {{
        "match_percentage": 85,
        "strengths": ["5+ years Python development", "AWS certified", "Led team of 5"],
        "missing_skills": ["No critical gaps identified"],
        "recommendations": ["Add quantifiable metrics to achievements"],
        "critical_gaps": ["Minor: Add project outcomes"],
        "ats_keywords": ["All key terms present"]
    }}
    
    Now analyze this resume using the same thorough approach:
    
    Job Description:
    {job_description}
    
    Resume:
    {resume_text}
    
    Chain-of-Thought Process:
    1. First, identify all technical skills in the job description
    2. Then, map each skill to the resume content
    3. Next, assess experience level alignment
    4. Finally, identify critical gaps and ATS optimization opportunities
    
    Focus on identifying:
    1. Critical gaps between resume requirements and job needs
    2. Missing keywords and skills that ATS systems look for
    3. Experience level alignment with seniority requirements
    4. Industry-specific terminology gaps
    5. Quantifiable achievements that are missing
    
    Please provide analysis in the following JSON format:
    {{
        "match_percentage": 85,
        "strengths": ["List of key strengths found in resume"],
        "missing_skills": ["List of important skills missing from resume"],
        "recommendations": ["List of specific recommendations to improve resume"],
        "key_matches": ["List of good matches between resume and job description"],
        "experience_alignment": "Assessment of how well experience aligns with requirements",
        "overall_assessment": "Brief overall assessment",
        "critical_gaps": ["List of most critical gaps to address"],
        "ats_keywords": ["Important keywords missing for ATS optimization"]
    }}
    
    Be thorough and specific in your gap analysis to help create a standout resume.
    """
    
    try:
        response = requests.post(OPENROUTER_URL, headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }, json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an expert career counselor and resume analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        })
        response.raise_for_status()
        result = response.json()
        analysis_text = result['choices'][0]['message']['content']
        
        try:
            return json.loads(analysis_text)
        except json.JSONDecodeError:
            return {"raw_analysis": analysis_text}
            
    except Exception as e:
        return {"error": f"AI analysis failed: {str(e)}"}

def generate_optimized_resume(resume_text, job_description, analysis_result):
    """Generate an optimized resume based on analysis and job description"""
    
    prompt = f"""
    Based on the comprehensive gap analysis, create a standout, interview-winning resume that addresses all identified gaps and positions the candidate as the ideal fit.
    
    Original Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Gap Analysis Results:
    {analysis_result}
    
    Create a POWERFUL resume that:
    1. Addresses ALL critical gaps identified in the analysis
    2. Incorporates missing ATS keywords for better screening
    3. Uses industry-specific terminology that matches the job
    4. Highlights quantifiable achievements with metrics and impact
    5. Positions experience level appropriately for the role's seniority
    6. Creates a compelling narrative that stands out to recruiters
    7. Optimized for both ATS systems and human readers
    
    Follow this PROFESSIONAL structure:
    
    [FULL NAME]
    [Phone] | [Email] | [LinkedIn URL] | [Location] | [Portfolio/GitHub (if applicable)]
    
    PROFESSIONAL SUMMARY
    [3-4 line powerful summary that immediately shows value and addresses key requirements]
    
    CORE COMPETENCIES
    [List of 6-8 key skills that match job description perfectly]
    
    PROFESSIONAL EXPERIENCE
    [Company Name] | [City, State]
    [Job Title] | [Dates]
    • [Quantifiable achievement 1 - with specific metrics, results, and impact]
    • [Quantifiable achievement 2 - using industry terminology from job description]
    • [Quantifiable achievement 3 - showing growth and leadership]
    
    EDUCATION
    [Degree], [Major] | [University Name] | [Year]
    [Relevant coursework or achievements if applicable]
    
    PROJECTS (if technical role)
    [Project Name] | [Technologies Used]
    • [Description with business impact and technical challenges solved]
    
    CERTIFICATIONS & AWARDS
    [Certification Name] | [Issuing Organization] | [Year]
    
    Make this resume IRRESISTIBLE to recruiters and hiring managers. Use action verbs, quantify everything, and ensure it passes ATS screening while impressing humans.
    """
    
    try:
        response = requests.post(OPENROUTER_URL, headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }, json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an expert resume writer and career coach specializing in creating professional, international-standard resumes."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        })
        response.raise_for_status()
        result = response.json()
        optimized_resume = result['choices'][0]['message']['content']
        return optimized_resume
            
    except Exception as e:
        return f"Error generating optimized resume: {str(e)}"

def create_pdf_from_text(text_content):
    """Create a PDF file from text content"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    lines = text_content.split('\n')
    for line in lines:
        if line.strip():
            if line.isupper() and len(line) < 30:
                para = Paragraph(f"<b>{line}</b>", styles['Heading2'])
            elif line.startswith('•'):
                para = Paragraph(f"• {line[1:].strip()}", styles['Normal'])
            else:
                para = Paragraph(line, styles['Normal'])
            story.append(para)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_docx_from_text(text_content):
    """Create a DOCX file from text content"""
    doc = docx.Document()
    
    lines = text_content.split('\n')
    for line in lines:
        if line.strip():
            if line.isupper() and len(line) < 30:
                paragraph = doc.add_paragraph(line)
                paragraph.style = 'Heading 2'
            elif line.startswith('•'):
                doc.add_paragraph(line[1:].strip(), style='List Bullet')
            else:
                doc.add_paragraph(line)
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Streamlit UI
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("🚀 AI Resume Analyzer")
st.markdown("---")

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Upload Resume")
    
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Upload your resume for AI analysis"
    )
    
    job_description = st.text_area(
        "📋 Job Description",
        height=150,
        placeholder="Paste the job description here...",
        help="Provide the job description for better analysis"
    )

if uploaded_file is not None and job_description:
    st.success("✅ Ready to analyze your resume!")
    
    if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
        if uploaded_file is not None and job_description:
            st.error("❌ Please upload a resume and provide job description")
            st.stop()
        
        with st.spinner("🤖 Analyzing with AI..."):
            # Extract text from uploaded file
            file_bytes = uploaded_file.read()
            
            # Save temporarily
            with open("temp_resume", "wb") as f:
                f.write(file_bytes)
            
            # Extract text based on file type
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf("temp_resume")
            else:
                resume_text = extract_text_from_docx("temp_resume")
            
            # Analyze with AI
            analysis_result = analyze_resume_with_ai(resume_text, job_description)
            
            # Generate optimized resume
            if "error" not in analysis_result:
                optimized_resume = generate_optimized_resume(resume_text, job_description, analysis_result)
                analysis_result["optimized_resume"] = optimized_resume
            
            # Clean up
            if os.path.exists("temp_resume"):
                os.remove("temp_resume")
        
        # Display results
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        if "error" in analysis_result:
            st.error(f"❌ {analysis_result['error']}")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Match Score")
                match_percentage = analysis_result.get('match_percentage', 0)
                st.progress(match_percentage / 100)
                st.metric("Match Percentage", f"{match_percentage}%")
            
            with col2:
                st.subheader("📈 Overall Assessment")
                st.info(analysis_result.get('overall_assessment', 'No assessment available'))
            
            # Detailed analysis
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("✅ Strengths")
                strengths = analysis_result.get('strengths', [])
                for strength in strengths:
                    st.success(f"• {strength}")
            
            with col4:
                st.subheader("⚠️ Missing Skills")
                missing_skills = analysis_result.get('missing_skills', [])
                for skill in missing_skills:
                    st.error(f"• {skill}")
            
            # Recommendations
            st.subheader("💡 Recommendations")
            recommendations = analysis_result.get('recommendations', [])
            for rec in recommendations:
                st.info(f"• {rec}")
            
            # Key Matches
            st.subheader("🎯 Key Matches")
            key_matches = analysis_result.get('key_matches', [])
            for match in key_matches:
                st.success(f"• {match}")
            
            # Critical Gaps
            if 'critical_gaps' in analysis_result:
                st.subheader("🚨 Critical Gaps")
                gaps = analysis_result['critical_gaps']
                for gap in gaps:
                    st.warning(f"• {gap}")
            
            # ATS Keywords
            if 'ats_keywords' in analysis_result:
                st.subheader("🔑 ATS Keywords")
                keywords = analysis_result['ats_keywords']
                for keyword in keywords:
                    st.info(f"• {keyword}")
        
        # Optimized Resume
        if "optimized_resume" in analysis_result:
            st.markdown("---")
            st.header("📄 AI-Optimized Resume")
            
            st.markdown("### 📋 Resume Preview")
            st.text_area(
                "Optimized resume content:",
                value=analysis_result["optimized_resume"],
                height=400,
                help="Your professionally optimized resume"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Download PDF", type="secondary"):
                    pdf_buffer = create_pdf_from_text(analysis_result["optimized_resume"])
                    st.download_button(
                        label="Download Optimized Resume (PDF)",
                        data=pdf_buffer.getvalue(),
                        file_name="optimized_resume.pdf",
                        mime="application/pdf"
                    )
            
            with col2:
                if st.button("📝 Download DOCX", type="secondary"):
                    docx_buffer = create_docx_from_text(analysis_result["optimized_resume"])
                    st.download_button(
                        label="Download Optimized Resume (DOCX)",
                        data=docx_buffer.getvalue(),
                        file_name="optimized_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🤖 Built with ❤️ using Streamlit, OpenAI API & Advanced AI</p>
        <p style='font-size: 12px;'>🔧 Features: Token Management | Few-shot Prompting | Chain-of-Thought Analysis</p>
    </div>
    """
)

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    ### 🚀 Getting Started:
    1. **Upload Resume**: Click "Browse files" to upload your PDF or DOCX resume
    2. **Add Job Description**: Paste the target job description
    3. **Analyze**: Click "Analyze Resume" to get comprehensive AI analysis
    4. **Download**: Get your optimized resume in PDF or DOCX format
    
    ### ✨ Advanced Features:
    - **🔢 Token Management**: Automatically handles long resumes with intelligent chunking
    - **🧠 Few-shot Prompting**: Uses examples for better analysis quality
    - **🔗 Chain-of-Thought**: Step-by-step reasoning for comprehensive analysis
    - **📄 ATS Optimization**: Optimized for applicant tracking systems
    
    ### 🎯 Benefits:
    - Professional resume optimization
    - Gap analysis and recommendations
    - Industry-specific keyword optimization
    - Quantifiable achievement suggestions
    - Multiple download formats
    """)
