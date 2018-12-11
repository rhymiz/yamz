## Yamz
A hacky way to manage environment specific configuration in Python using PyYAML.


### Why Yamz?
All the other names I managed to think of were already taken, so... here we are.


### How to use
- `pip install yamz`
- Configure your environment in `settings.yaml`
    - I recommend using environments names such as: `production`, `development`, etc.,
    Note: `global` environment settings will be available in all environments
    - If you want to include variables from your environment, make sure to add a `$` prefix (`$HOME`) and Yamz will make sure it's included.
    ```yaml
    production:
      HOME: $HOME
      MYSQL_DB_HOST: 1.2.3.4
      MYSQL_DB_PASS: $MYSQL_DB_PASS
    ```


```python
from yamz import Environment

env = Environment("[BASE_PATH]", "settings.yaml")
prod_env = env.load("production")

prod_env.MYSQL_DB_HOST
```