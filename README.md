## Yamz
An easy way to manage environment specific configuration in Python using PyYAML.


### Requirements
- Python >=3.5
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

from yamz import Yamz


base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(base, 'settings.yaml')

env = Yamz(path)
prod_env = env.load("production")

prod_env.MYSQL_DB_HOST # 1.2.3.4

prod_env.YAMZ_ENV # production
```

### Contributions
If you'd like to contribute and make Yamz better, feel free to open up a PR.
I'll review it at my earliest convenience!
