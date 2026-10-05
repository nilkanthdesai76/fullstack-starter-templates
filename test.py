import os
import sys

def test_fastapi_syntax():
    with open("fastapi-starter/main.py", "r") as f:
        code = f.read()
    compile(code, "fastapi-starter/main.py", "exec")
    print("✅ FastAPI syntax validated")

def test_docker_compose_syntax():
    with open("docker-compose/docker-compose.yml", "r") as f:
        content = f.read()
    assert "services:" in content
    assert "api:" in content
    assert "db:" in content
    assert "redis:" in content
    print("✅ docker-compose.yml validated")

def test_supabase_syntax():
    with open("supabase-wrapper/supabase.js", "r") as f:
        content = f.read()
    assert "export function initSupabase" in content
    assert "class SupabaseAuthHelper" in content
    assert "class SupabaseStorageHelper" in content
    print("✅ supabase.js wrapper validated")

if __name__ == "__main__":
    test_fastapi_syntax()
    test_docker_compose_syntax()
    test_supabase_syntax()
    print("\nAll fullstack-starter-templates validated successfully!")
