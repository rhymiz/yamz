## Yamz
An easy way to manage environment specific configuration in Python using PyYAML.


### Requirements
- Python >=3.6
- PyYAML >=5.1


### Why Yamz?
All the other names I managed to think of were already taken, so... here we are.


### How to use
- `pip install yamz`
- Configure your environment in `settings.yaml`
    - I recommend using environments names such as: `production`, `development`, etc.,
    Note: `global` environment settings will be available in all environments
    - If you would like to include variables from your environment, make sure to add a `$` prefix (`$HOME`) and Yamz will make sure it's included.
    ```yaml
    global:
      TEST: some_test
    production:
      HOME: $HOME
      MYSQL_DB_HOST: 1.2.3.4
      MYSQL_DB_PASS: $MYSQL_DB_PASS
    ```


```python
import os

from yamz import Environment


base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(base, 'settings.yaml')

env = Environment(path)
prod_env = env.load("production")

prod_env.MYSQL_DB_HOST
```