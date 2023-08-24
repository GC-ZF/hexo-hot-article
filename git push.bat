@echo off
echo 需要提交的文件
git status
set /p t2="提交信息："
git add .
git commit -m "%t2%"
git push
pause