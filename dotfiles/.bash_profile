# How to use
# 1. Write `alias reload="source THIS_FILE"` to ~/.bash_profile
# 2. Do `reload`

ll_function(){
    ls -la $@
}
alias ll=ll_function
alias la="ls -a"
alias lla="ls -la"
alias qq='exit'
alias python="python3"
alias reload="source ~/.bash_profile"
alias catme="cat ~/.bash_profile"
alias editme="vim ~/.bash_profile"
#alias editgc='code ~/.gitconfig'

# entrypoint
export PS1="$ "
export GLOBAL_ALIAS="~/global_alias"
#export NODEBREW_NODE="$HOME/.nodebrew/current/bin"
#export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
#export PATH=$NODEBREW_NODE:$GLOBAL_ALIAS:$PATH
