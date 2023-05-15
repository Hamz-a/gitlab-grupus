# gitlab-grupus

Are you tired of cloning manually each repository one by one? This tool allows you to clone repositories from gitlab by group ID. This can also be done recursively.  

## Installation
```
git clone https://github.com/Hamz-a/gitlab-grupus
python3 setup.py install --user
```

## Usage

1. Login into gitlab and copy the gitlab session value from the cookies (I should probably also support access tokens...)
2. Copy group ID of target group you want to clone
3. Make sure you have configured git correctly with SSH
4. Commands are self-explanatory. Ask for help `ggrupus -h`.
5. Clone repositories by group ID: `ggrupus _gitlab_session group_id`
6. If you want to clone recursively: `ggrupus -r _gitlab_session group_id`






