import os
from dotenv import load_dotenv
import sys

load_dotenv()

from typing import List, Dict

def load_env_vars(var_names: List[str]) -> Dict[str, str]:
    load_dotenv()
    env_vars: Dict[str, str] = {}
    for var in var_names:
        value = os.getenv(var)
        if value is None:
            print(f"Environment variable {var} not found. Exiting.")
            sys.exit(1)
        env_vars[var] = value
    return env_vars

required_vars: List[str] = ["JWT_KEY", "JWT_ALGORITHM", "DATABASE_URL", "OPENAI_API_KEY"]
env_vars: Dict[str, str] = load_env_vars(required_vars)
