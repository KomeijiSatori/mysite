# Satori's personal website
This is the source code of my site. If you have any questions or suggestions please let me know.
[View my site immediately!][1]
Thanks for your feedback~


## python version requirements
python >= 3.5


## Setup
### 1. Migrate and collect static files
1. execute the following command.
```
python3 manage.py migrate
python3 manage.py collectstatic
```

### 2. Make i18n works
1. Rename the standard avatar locale folder from 'zh-CN' to 'zh-Hans' to make i18n work.
Example command:
```
mv /usr/local/lib/python3.5/dist-packages/avatar/locale/zh-CN /usr/local/lib/python3.5/dist-packages/avatar/locale/zh-Hans
```
2. execute the following command.
```
cp custom_files/Markdown.Editor.js static/pagedown/Markdown.Editor.js
```

### 3. Add the background files
1. Create `media/background` folder and move all your background there, at least 6 pictures is required.
2. Create `media/background/H` folder and move all hidden images there, at least 1 picture is required.
### 4. Add the emoticon files
1. Create `media/emoticon` folder and move all your emoticon folders there.
In each emoticon folder, put all your emoticons in that folder.
The emoticons' name should never contain the following characters: `[`, `]`, ` `, while names with pure numbers are recommended.

  [1]: http://chongliu.me

