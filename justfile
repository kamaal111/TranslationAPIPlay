set export

DEVCONTAINER := ".devcontainer"
DEVCONTAINER_VIRTUAL_ENVIRONMENT :=  DEVCONTAINER / ".venv"

run-dev:
    #!/bin/zsh

    just install-python-modules $DEVCONTAINER_VIRTUAL_ENVIRONMENT
    . $DEVCONTAINER_VIRTUAL_ENVIRONMENT/bin/activate
    uvicorn app.main:app --reload

initialize-gcloud:
    #!/bin/zsh

    gcloud init
    gcloud auth application-default login

create-api-key-dev project-id suffix:
    #!/bin/zsh

    . $DEVCONTAINER_VIRTUAL_ENVIRONMENT/bin/activate
    python scripts/create_api_keys.py --project_id {{ project-id }} --suffix {{ suffix }}

setup-dev-container: copy-to-container setup-zsh-environment
    #!/bin/zsh

    just setup-python-environment $DEVCONTAINER_VIRTUAL_ENVIRONMENT

initialize-dev-container: copy-git-config-from-outside-container set-environment

[private]
install-python-modules virtual-environment:
    #!/bin/zsh

    VIRTUAL_ENVIRONMENT="{{ virtual-environment }}"

    . $VIRTUAL_ENVIRONMENT/bin/activate
    poetry install

[private]
setup-python-environment virtual-environment:
    #!/bin/zsh

    VIRTUAL_ENVIRONMENT="{{ virtual-environment }}"
    if [ ! -d $VIRTUAL_ENVIRONMENT ]
    then
        python -m venv $VIRTUAL_ENVIRONMENT
    fi

    . $VIRTUAL_ENVIRONMENT/bin/activate

    pip install poetry
    poetry install
    just install-python-modules "{{ virtual-environment }}"
    pre-commit install

[private]
setup-zsh-environment:
    #!/bin/zsh

    . ~/.zshrc

    if [ ! -f $ZSH/oh-my-zsh.sh ]
    then
        echo "Installing Oh My Zsh"
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    fi

    if [ ! -d ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions ]
    then
        echo "Installing zsh-autosuggestions"
        git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
    fi

    if [ ! -d ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting ]
    then
        echo "Installing zsh-syntax-highlighting"
        git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
    fi

    echo "Updating zsh configuration"
    cp -f $DEVCONTAINER/.zshrc ~/.zshrc
    cp -f $DEVCONTAINER/.zshenv ~/.zshenv

[private]
set-environment:
    #!/bin/zsh

    ENVIRONMENT_FILE="$DEVCONTAINER/.zshenv"

    rm -rf $ENVIRONMENT_FILE
    touch $ENVIRONMENT_FILE

    echo "export LC_ALL=C" >> $ENVIRONMENT_FILE
    echo "export USER=$USER" >> $ENVIRONMENT_FILE

[private]
copy-git-config-from-outside-container:
    #!/bin/zsh

    cp -f ~/.gitconfig $DEVCONTAINER/.gitconfig

[private]
copy-to-container:
    #!/bin/zsh

    cp -f $DEVCONTAINER/.gitconfig ~/.gitconfig
