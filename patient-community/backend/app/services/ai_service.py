import os
from openai import OpenAI
from ..config import settings
from PIL import Image
import PyPDF2

# 延迟初始化OpenAI客户端
client = None

def get_openai_client():
    global client
    if client is None:
        client = OpenAI()
    return client

def extract_text_from_pdf(file_path: str) -> str:
    """从PDF提取文本"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"PDF提取错误: {e}")
        return ""

def extract_text_from_image(file_path: str) -> str:
    """从图片提取文本（使用GPT-4 Vision）"""
    try:
        # 这里可以使用OCR或GPT-4 Vision
        # 简化处理，返回提示信息
        return f"图片文件: {os.path.basename(file_path)}"
    except Exception as e:
        print(f"图片提取错误: {e}")
        return ""

async def extract_medical_info(file_path: str, file_type: str) -> dict:
    """使用AI提取病历关键信息"""
    try:
        # 根据文件类型提取文本
        if file_type.lower() == '.pdf':
            text_content = extract_text_from_pdf(file_path)
        elif file_type.lower() in ['.jpg', '.jpeg', '.png']:
            text_content = extract_text_from_image(file_path)
        else:
            text_content = ""
        
        if not text_content:
            return {
                "disease_name": "未识别",
                "symptoms": "无法提取",
                "diagnosis_date": None,
                "treatment_plan": "无法提取",
                "medications": "无法提取"
            }
        
        # 使用OpenAI API提取结构化信息
        prompt = f"""
请从以下病历文本中提取关键信息，以JSON格式返回：
- disease_name: 疾病名称
- symptoms: 症状描述
- diagnosis_date: 诊断日期（YYYY-MM-DD格式）
- treatment_plan: 治疗方案
- medications: 用药情况

病历内容：
{text_content[:2000]}

请只返回JSON格式的数据，不要包含其他说明文字。
"""
        
        ai_client = get_openai_client()
        response = ai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "你是一个专业的医疗信息提取助手，擅长从病历中提取结构化信息。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        
        # 解析返回的JSON
        import json
        try:
            result = json.loads(result_text)
        except:
            # 如果解析失败，返回默认值
            result = {
                "disease_name": "待确认",
                "symptoms": text_content[:200],
                "diagnosis_date": None,
                "treatment_plan": "待补充",
                "medications": "待补充"
            }
        
        return result
        
    except Exception as e:
        print(f"AI提取错误: {e}")
        return {
            "disease_name": "提取失败",
            "symptoms": str(e),
            "diagnosis_date": None,
            "treatment_plan": "提取失败",
            "medications": "提取失败"
        }
