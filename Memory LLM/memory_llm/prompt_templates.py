"""
System Prompt Templates and Management
Customizable prompt templates for different scenarios
"""

from typing import Dict, List, Optional
from datetime import datetime


class PromptTemplate:
    """System prompt template"""
    
    def __init__(self, name: str, base_prompt: str, 
                 variables: Optional[Dict[str, str]] = None):
        """
        Args:
            name: Template name
            base_prompt: Base prompt text (can contain variables in {variable} format)
            variables: Default variable values
        """
        self.name = name
        self.base_prompt = base_prompt
        self.variables = variables or {}
    
    def render(self, **kwargs) -> str:
        """
        Fill template with variables
        
        Args:
            **kwargs: Variable values
            
        Returns:
            Generated prompt
        """
        merged_vars = {**self.variables, **kwargs}
        return self.base_prompt.format(**merged_vars)


class PromptManager:
    """Manages prompt templates"""
    
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_default_templates()
    
    def _load_default_templates(self) -> None:
        """Load default templates"""
        
        # 1. Customer Service
        self.add_template(
            name="customer_service",
            base_prompt="""You are a professional customer service assistant for {company_name} company.

Your task:
- Approach customers kindly and helpfully
- Remember past interactions and create context
- Solve problems quickly and effectively
- Redirect to human representative when necessary

Communication Style:
- Use {tone} tone
- Give short and clear answers
- Show empathy
- Be professional

Important Rules:
- Never lie
- Don't speculate on topics you don't know
- Keep customer satisfaction in the foreground
- Ask if there's any other help at the end of each response

You are currently working on {current_date}.
""",
            variables={
                "company_name": "Our Company",
                "tone": "friendly and professional",
                "current_date": datetime.now().strftime("%Y-%m-%d")
            }
        )
        
        # 2. Technical Support
        self.add_template(
            name="tech_support",
            base_prompt="""You are a technical support expert for {product_name}.

Your Expertise Areas:
- Problem diagnosis and resolution
- Step-by-step guidance
- Technical documentation
- Debugging

Approach:
- First understand the problem completely
- Start with simple solutions
- Explain step by step
- Explain technical terms when necessary

User Level: {user_level}

Response Format:
1. Summarize the problem
2. List possible causes
3. Provide solution steps
4. Check results

Log level: {log_level}
""",
            variables={
                "product_name": "Our Product",
                "user_level": "intermediate level",
                "log_level": "detailed"
            }
        )
        
        # 3. Personal Assistant
        self.add_template(
            name="personal_assistant",
            base_prompt="""Sen {user_name} için kişisel dijital asistansın.

Görevlerin:
- Günlük planlamasına yardım
- Hatırlatmalar
- Bilgi toplama ve özetleme
- Öneri ve tavsiyeler

Kişiselleştirme:
- Kullanıcının tercihlerini öğren
- Alışkanlıklarını hatırla
- Proaktif önerilerde bulun
- Önceliklere göre sırala

Çalışma Saatleri: {work_hours}
Zaman Dilimi: {timezone}
Tercih Edilen Dil: {language}

Yaklaşım:
- Verimlilik odaklı
- Minimal ve net
- Proaktif
- Esnek

Veri Gizliliği: {privacy_level}
""",
            variables={
                "user_name": "Kullanıcı",
                "work_hours": "09:00-18:00",
                "timezone": "Europe/Istanbul",
                "language": "Türkçe",
                "privacy_level": "yüksek"
            }
        )
        
        # 4. Business Customer Service
        self.add_template(
            name="business_customer_service",
            base_prompt="""Sen {company_name} şirketinin kurumsal müşteri hizmetleri asistanısın.

Kurumsal Müşteri Yaklaşımı:
- Profesyonel ve çözüm odaklı
- SLA'lara uygun hızlı yanıt
- Teknik sorunlara derin destek
- Çoklu kanal entegrasyonu

Şirket Bilgileri:
- Kuruluş Yılı: {founded_year}
- Çalışan Sayısı: {employee_count}
- Sektör: {industry}

Öncelik Seviyesi: {priority_level}
SLA Süresi: {sla_hours} saat
""",
            variables={
                "company_name": "Kurumsal Şirket",
                "founded_year": "2010",
                "employee_count": "500+",
                "industry": "Teknoloji",
                "priority_level": "yüksek",
                "sla_hours": "4"
            }
        )
    
    def add_template(self, name: str, base_prompt: str, 
                    variables: Optional[Dict[str, str]] = None) -> None:
        """
        Add new template
        
        Args:
            name: Template name
            base_prompt: Prompt text
            variables: Default variables
        """
        self.templates[name] = PromptTemplate(name, base_prompt, variables)
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """
        Get template
        
        Args:
            name: Template name
            
        Returns:
            PromptTemplate or None
        """
        return self.templates.get(name)
    
    def render_prompt(self, template_name: str, **kwargs) -> str:
        """
        Render template
        
        Args:
            template_name: Template name
            **kwargs: Variable values
            
        Returns:
            Generated prompt
        """
        template = self.get_template(template_name)
        if template:
            return template.render(**kwargs)
        raise ValueError(f"Template '{template_name}' not found")
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(self.templates.keys())
    
    def get_template_variables(self, template_name: str) -> Dict[str, str]:
        """
        Return template variables
        
        Args:
            template_name: Template name
            
        Returns:
            Variables dictionary
        """
        template = self.get_template(template_name)
        if template:
            return template.variables.copy()
        return {}


# Global instance for ready use
prompt_manager = PromptManager()

