"""
LLM 服务 - 封装所有 LLM 调用
"""
from typing import Optional
from app.config import get_settings


class LLMService:
    """LLM 调用服务"""

    def __init__(self):
        self.settings = get_settings()
        self._initialize_client()

    def _initialize_client(self):
        """初始化 LLM 客户端"""
        provider = self.settings.llm_provider.lower()
        api_key = self.settings.llm_api_key

        if not api_key:
            raise ValueError(
                f"LLM_API_KEY 环境变量未设置。"
                f"请设置 {provider.upper()} API 密钥。"
            )

        if provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
            except ImportError:
                raise ImportError("请安装 openai 包: pip install openai")

        elif provider == "claude":
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=api_key)
            except ImportError:
                raise ImportError("请安装 anthropic 包: pip install anthropic")

        elif provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.client = genai
            except ImportError:
                raise ImportError("请安装 google-generativeai 包: pip install google-generativeai")

        else:
            raise ValueError(f"不支持的 LLM 提供商: {provider}")

    async def translate(self, text: str, source_lang: str = "en", target_lang: str = "zh") -> str:
        """
        翻译文本

        Args:
            text: 要翻译的文本
            source_lang: 源语言（默认英文）
            target_lang: 目标语言（默认中文）

        Returns:
            翻译后的文本
        """
        prompt = f"""请将以下英文翻译成中文。只返回翻译结果，不要添加任何额外说明。

英文：{text}

中文："""

        return await self._call_llm(prompt)

    async def explain_grammar(self, text: str, selected_text: Optional[str] = None) -> str:
        """
        解释语法

        Args:
            text: 完整句子
            selected_text: 选中的部分文本（如果为 None，则解释整句）

        Returns:
            语法解释
        """
        if selected_text:
            prompt = f"""请解释以下英文句子中指定部分的语法：

完整句子：{text}
指定部分：{selected_text}

请详细解释这部分的语法结构和用法。"""
        else:
            prompt = f"""请详细解释以下英文句子的语法结构：

句子：{text}

请从句子成分（主语、谓语、宾语等）和时态等方面详细解释。"""

        return await self._call_llm(prompt)

    async def explain_vocabulary(
        self,
        word: str,
        context: str,
        explanation_type: str = "context_meaning"
    ) -> str:
        """
        解释词汇

        Args:
            word: 要解释的单词
            context: 单词所在的句子
            explanation_type: 解释类型
                - context_meaning: 这个单词在此上下文中的含义
                - common_meanings: 常见含义
                - familiar_new: 熟词生义

        Returns:
            词汇解释
        """
        if explanation_type == "context_meaning":
            prompt = f"""请解释单词 "{word}" 在以下句子中的含义：

句子：{context}

请只返回这个单词在此上下文中的含义，不需要其他解释。"""

        elif explanation_type == "common_meanings":
            prompt = f"""请解释单词 "{word}"：

句子：{context}

请列出该单词的常见含义，以及在上述句子中具体是什么意思。"""

        else:  # familiar_new
            prompt = f"""这是一个"熟词生义"解释请求。单词 "{word}" 是一个常见单词，但在以下句子中可能有不寻常的用法：

句子：{context}

请解释它在此句子中的特殊含义或用法。"""

        return await self._call_llm(prompt)

    async def _call_llm(self, prompt: str) -> str:
        """
        调用 LLM

        Args:
            prompt: 提示词

        Returns:
            LLM 的响应
        """
        provider = self.settings.llm_provider.lower()

        try:
            if provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.settings.llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                return response.choices[0].message.content

            elif provider == "claude":
                response = self.client.messages.create(
                    model=self.settings.llm_model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text

            elif provider == "gemini":
                model = self.client.GenerativeModel(self.settings.llm_model)
                response = model.generate_content(prompt)
                return response.text

        except Exception as e:
            raise RuntimeError(f"LLM 调用失败: {str(e)}")


# 全局 LLM 服务实例
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """获取 LLM 服务单例"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
