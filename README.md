# commitmsg-ai-check
pre-commit git hooks to use AI to check commit messages(Support OpenAI-compatible platforms)

git config for ai

```yaml
git config --add ai.base.url {baseUrl}

git config --add ai.model {model}

git config --add ai.api.key {key}
```

See [pre-commit] for instructions

install hook-type must be commit-msg

```yaml
    pre-commit install --hook-type commit-msg
```

Sample `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/KoiX1024/commitmsg-ai-check
    rev: 1.0.0
    hooks:
    -   id: commitmsg-ai-check
```
[temporarily-disabling-hooks]



[temporarily-disabling-hooks]: https://pre-commit.com/#temporarily-disabling-hooks
[pre-commit]: https://pre-commit.com
