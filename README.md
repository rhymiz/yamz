## Yamz
An easy way to manage environment specific configurations.


### Requirements
- Python >=3.6


### Why Yamz?
All the other names I managed to think of were already taken, so... here we are.


### How to use
I recommend using environments names such as: `production`, `development`, etc.,
Also, if you would like to include variables from your environment, make sure to add a `$` prefix (`$HOME`) and Yamz will make sure it's included.

Note: `global` settings will be available in all environments

- `pip install yamz`
- Configure your environment in `config.yaml` (requires PyYAML)
    ```yaml
    global:
      TEST: some_test
    production:
      HOME: $HOME
      MYSQL_DB_HOST: 1.2.3.4
      MYSQL_DB_PASS: $MYSQL_DB_PASS
    ```
- Configure your environment in `config.json`
    ```json
    {
      "global": {
        "TEST": "some_test"
      },
      "production": {
        "HOME": "$HOME",
        "MYSQL_DB_HOST": "1.2.3.4",
        "MYSQL_DB_PASS": "$MYSQL_DB_PASS"
      }
    } 
    ```

```python
import os

from yamz import Yamz
from yamz.providers.default import YamlProvider, JsonProvider

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(base, 'config.yaml')

env = Yamz(path, provider=YamlProvider) # or JsonProvider
prod_env = env.load("production")

prod_env.MYSQL_DB_HOST # 1.2.3.4

prod_env.YAMZ_ENV # production
```

### Contributions
If you'd like to contribute and make Yamz better, feel free to open up a PR.
I'll review it at my earliest convenience!
