from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 基础环境
    env: str = "dev"

    # LLM 相关
    llm_provider: str = "deepseek"
    deepseek_model: str = "deepseek-chat"
    llm_timeout: int = 45

    # Key
    DEEPSEEK_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"  # ✅ 防止将来再炸


settings = Settings()